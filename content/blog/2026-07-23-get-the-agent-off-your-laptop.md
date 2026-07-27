---
title: "Get the Agent Off Your Laptop"
date: 2026-07-23
description: "Conductor's new experimental aca provider moves an agent's execution loop into a throwaway Azure container, so the orchestration you own stays on your machine and the model-driven shell doesn't."
tags: ["blog", "ai", "tooling", "open-source", "security"]
categories: ["engineering"]
draft: true
---

Every coding agent I run executes its shell commands on the machine I work from. That's the same machine holding my SSH keys, an `az login` session, a `gh` token, and about forty repos I've cloned and forgotten about. I've mostly handled this by trusting the agent to behave. That isn't a control, it's a hope.

So my team added an experimental provider to [Conductor](https://github.com/microsoft/conductor) called `aca`, and it does one thing: it takes the agent's execution loop off your machine and runs it in a container in Azure that you throw away when it's done.

## What it does

Normally Conductor runs each agent's loop in the same process as the orchestrator: model calls, tool calls, file edits, all local. The `aca` provider relocates that sub-loop into an [Azure Container Apps dynamic session](https://learn.microsoft.com/azure/container-apps/sessions), a Hyper-V isolated container allocated out of a warm pool. The model-driven shell, the built-in tools, and any MCP servers you've declared all run in there.

The workflow-level loop stays home. Routing, context, checkpoints, and the event bus still run on your machine, still with no LLM in the loop. Only the part where a model decides to run a command moves.

Turning it on is one block of YAML:

```yaml
runtime:
  provider:
    name: aca
    pool_endpoint: "https://my-agent-pool.<region>.azurecontainerapps.io"
    inner_provider: copilot
    identifier_scope: agent
    egress: enabled
```

The rest of the workflow is unchanged. The host-side provider owns no agentic logic at all: it derives a session identifier, grabs an Azure token, posts one streaming request to the pool, and relays each NDJSON event frame back to the event bus verbatim as the container emits it. So the dashboard, the console, and the JSONL log render a sandboxed agent exactly like a local one. Sandbox wall-clock time shows up as its own usage row so you can see what you're spending time on.

## Why we bothered

The reason has less to do with containers than with where the boundary between the agent and everything I own ends up sitting.

Pillar Security published a [writeup of seven sandbox escapes](https://www.bleepingcomputer.com/news/security/cursor-codex-gemini-cli-antigravity-hit-by-sandbox-escapes/) across Cursor, Codex CLI, Gemini CLI, and Antigravity a few days before we shipped this, and the mechanism is what got my attention. In several of them the agent never breaks the sandbox. It follows every rule and writes a file into your workspace, a `.vscode` task or a hook or a patched virtualenv interpreter, and a trusted tool outside the sandbox runs it for you later. Usually triggered by an instruction buried in a README or a diff.

That whole class of attack needs two things: a "later," and a trusted tool sitting on the same filesystem. A dynamic session has neither. There's no editor to run its tasks, no shell profile to poison, no other repos to wander into, and no filesystem after the session ends. You clone what the agent needs at the start and push results out before it's over.

The other reason is that I want to run a lot of these at once. Sessions are keyed by an identifier, and Conductor mixes a concurrency discriminator into that key, so parallel agents and for-each iterations always land in separate sessions. Fanning out ten workers gives you ten isolated containers instead of ten processes elbowing each other over one working directory. Sequential reuse is configurable per agent: the default keeps one workspace per agent so retries and loop-backs come back to the same clone, which is what makes the [coding-agent example](https://github.com/microsoft/conductor/blob/main/examples/aca-coding-agent.yaml) work (clone, implement, run tests, loop back on failure without re-cloning).

## What it doesn't do yet

It's early, and the gaps are real enough that `conductor validate` rejects workflows that depend on the things it can't support.

Stopping a run stops your host from waiting on the stream. It doesn't stop the container, which keeps computing until it finishes or times out, because the runner image doesn't expose an interrupt endpoint yet and ACA's session-delete operation isn't supported for custom container pools. A single streaming turn also gets cut off around the 30 minute mark on default ACA ingress. `conductor resume` re-runs the agent instead of restoring the session, since there's nothing persistent to restore. The per-agent `tools:` allowlist isn't honored inside the container, so validation rejects it outright rather than quietly ignoring it. And you bring your own pool. Conductor doesn't provision Azure infrastructure for you, though there's a [provisioning script](https://github.com/microsoft/conductor/blob/main/scripts/aca/provision-pool.sh) in the repo that shows the whole two-step deploy.

## The credential problem

The container has to talk to a model backend, which means it needs a credential, which means a model-driven shell inside that container can read it. We decided not to pretend otherwise. The design accepts that the credential enters the sandbox and defends it with scope and lifetime instead.

The recommended path is a fine-grained GitHub token with only the Copilot Requests permission. The worst it can spend is your Copilot quota, it expires, and you can revoke it centrally. With zero setup you get whatever `gh auth token` returns, which is your full `gh` identity: fine on a machine you control for work you trust, not fine anywhere else. The one rule I'd tape to the wall is to never bake a long-lived token into the pool or the image, where it sits there exposed indefinitely.

That's why this is trusted-use only right now. ACA gives you no per-session secret store and no per-destination egress allowlist, so there's nothing to lean on for untrusted or multi-tenant work. Keeping the credential off the sandbox entirely, behind a host-side broker, is designed and not built.

## Where this lands

This is the same bet as the rest of Conductor. I already decided the [orchestrator shouldn't be an LLM](/blog/2026-03-20-introducing-an-ai-agent-workflow-conductor/) and that the structure worth owning is the routing and the gates around the model. Moving the agent loop into a disposable container extends that line to where the model's shell actually runs: deterministic parts on my machine, model-driven parts somewhere I can delete.

I don't want to oversell it. Isolation is a boundary, and boundaries fail. The way to use this is to assume the sandbox gets compromised and set things up so that's survivable, which mostly means scoping the token, turning egress on deliberately, and treating the container filesystem as hostile. None of it makes the agent trustworthy. It just means the day it does something stupid costs me a container I can delete rather than the machine I work from.

If you want to look at it, it's [issue #284](https://github.com/microsoft/conductor/issues/284) and the [provider docs](https://github.com/microsoft/conductor/blob/main/docs/providers/aca.md) cover the setup and every caveat above in more detail than a blog post should.
