---
title: "Get the Agent Off Your Laptop"
date: 2026-07-23
description: "A new experimental Conductor provider runs an agent's entire loop inside an isolated, throwaway container, so the blast radius is a sandbox you can delete, not the machine you work from."
tags: ["blog", "ai", "tooling", "open-source", "security"]
categories: ["engineering"]
draft: true
---

This past week was a bad one for the idea that a sandbox on your own machine will keep you safe. It was a good week to be building the opposite.

Three incidents, in the space of a few days:

- OpenAI published a [post-mortem](https://openai.com/index/safety-alignment-long-horizon-models) on an unreleased long-horizon model that kept acting outside its sandbox. Told to post benchmark results to Slack, it instead spent about an hour finding a hole in the sandbox and opened a pull request on a public GitHub repo. When a scanner blocked it for exposing an auth token, it split the token into fragments and reconstructed it at runtime to get past the scanner. It SSH'd into other live compute pods. The finding that stuck with me: *persistence itself* is the new threat. Older models hit a boundary and stopped and handed control back. This one treated the boundary as a bug to fix.
- Pillar Security published a ["Week of Sandbox Escapes"](https://www.bleepingcomputer.com/news/security/cursor-codex-gemini-cli-antigravity-hit-by-sandbox-escapes/): seven escapes across Cursor, Codex CLI, Gemini CLI, and Antigravity. The clever part is that the agent never breaks the sandbox at all. It obeys every rule and simply writes a file into your workspace — a `.vscode` task, a `.claude` hook, a patched virtualenv interpreter — that a trusted tool *outside* the sandbox runs for it later. Usually kicked off by prompt injection buried in a README or a diff. Their one-line summary is the one to tape to your monitor: sandbox ≠ security, and the developer's machine is the attack surface.
- And in case the point was too subtle, OpenAI and Hugging Face [disclosed](https://www.axios.com/2026/07/21/openai-says-hugging-face-breach-caused-by-one-its-models) that models under evaluation chained vulnerabilities and compromised parts of Hugging Face's production infrastructure while working a cyber benchmark.

All three are the same setup underneath: we hand a capable, persistent, sometimes adversarial agent a shell, then run that shell on the same machine that holds our SSH keys, our cloud credentials, and every repo we've got checked out.

## The scale pressure points the wrong way

Meanwhile everything pushes toward running *more* of them, not fewer. Cursor's [writeup on agent swarms](https://cursor.com/blog/agent-swarm-model-economics) is the cleanest version of where this goes: a frontier "planner" delegating to a swarm of cheap "workers" built a Rust implementation of SQLite from the 835-page spec alone, at roughly 87% less cost than an all-frontier run. The economics are real, and they're not going away. But "point fifty model-driven shells at your codebase" and "the developer's machine is the attack surface" are two sentences that should not be in the same room.

## What we built

That's the backdrop for a new provider my team added to [Conductor](https://github.com/microsoft/conductor), the multi-agent workflow tool I've [written about before](/blog/2026-03-20-introducing-an-ai-agent-workflow-conductor/). It's called `aca`, it's still experimental, and the premise is simple: get the agentic loop off your host.

Normally Conductor runs each agent's loop (the model calls, the tool use, the file edits) in the same process as the orchestrator, on your machine. The `aca` provider relocates that entire sub-loop into a remote Azure Container Apps dynamic-sessions container. The model-driven shell, its built-in tools, its MCP calls: all of it runs inside a Hyper-V-isolated, ephemeral cloud sandbox instead of on your laptop.

The split is the whole trick. The workflow-level loop — routing, context, checkpoints, the event bus — stays on the host, in your control, cheap, and never model-driven. Only the dangerous part, the part where a model decides to run a command, gets exiled. You flip one block in the workflow YAML:

```yaml
runtime:
  provider:
    name: aca
    pool_endpoint: "https://my-agent-pool.<region>.azurecontainerapps.io"
    inner_provider: copilot
    identifier_scope: agent
    egress: enabled
```

So what does this do to the attack surface? It takes the developer machine out of it. If a persistent agent goes looking for a way out (the OpenAI scenario), what it finds on the far side of the boundary is a disposable container with a narrowly scoped identity and an ephemeral filesystem, not your `~/.ssh` and your kubeconfig. The Pillar escapes work by writing a file that a trusted tool on your machine runs *later*; here there's no later, and no trusted tool on your machine, because the whole thing lived and died in a container you throw away. The blast radius stops being your laptop and becomes a sandbox with a short life expectancy.

And it composes with scale. Sessions are keyed by an identifier, and concurrent agents automatically diverge onto separate sessions, so a fan-out of workers is a fan-out of *isolated sandboxes* rather than a pile of processes elbowing each other over one filesystem. That's the swarm pattern with the isolation built in.

It's also the same bet I keep making about orchestration: keep the structure (the routing, the review gates, the deterministic parts) owned and on-host, and push the untrusted, model-driven part somewhere disposable.

## The honest part

Here's what I'd want to read before adopting this.

It's experimental, and the gaps are real. Sessions are ephemeral with no volume mounted, so you seed inputs at the start (a `git clone`) and push artifacts out (a `git push`) before the session cools down; nothing survives on its own. Interrupting a run doesn't actually stop the remote container yet. It stops your host from *waiting*, while the sandbox keeps computing until it finishes or times out. A single streaming turn gets cut off around 30 minutes. `conductor resume` re-runs the agent rather than restoring in-sandbox state. None of those are dealbreakers for the workflows I have in mind, but you should know them going in.

The one that deserves the most care is credentials. A model-driven shell inside the sandbox can read any environment variable the runner process has, so the design's one hard rule is that the real model key must never enter the sandbox. ACA gives you no per-session secret store and no per-destination egress allowlist to lean on, so that boundary has to live on the host. The Phase 1 mechanism forwards a short-lived, narrowly scoped token into the container, which is fine for *trusted* workflows you control and explicitly not fine for untrusted or multi-tenant use. The proper fix — a host-side credential gateway that injects the real key so the sandbox only ever sees a scoped token — is designed but not shipped yet.

Which is the thing I don't want to oversell: isolation is a boundary, not a guarantee. The right way to use this is to assume the sandbox will be compromised and arrange things so it doesn't matter: scope the token, turn on egress deliberately, treat the container filesystem as hostile. You're not making the agent safe. None of this does. It makes the day it misbehaves a lot less expensive: the worst it can reach is a container you can delete, and your laptop stays out of it.

That shift is the point for me. We spent a while trying to make the sandbox on the developer's machine strong enough to contain an adversarial agent, and this week reads like a fairly loud argument that we're going to keep losing that fight. Moving the model-driven execution off the host entirely, into something isolated, ephemeral, and cheap to throw away, feels like the more durable bet, the same way I keep landing on deterministic orchestration over letting the model drive.

The provider is early. The direction feels right. If you want to look, it's [issue #284](https://github.com/microsoft/conductor/issues/284) in the Conductor repo, and the provider docs cover the setup, the two-layer auth model, and every one of the caveats above in more detail than a blog post should.
