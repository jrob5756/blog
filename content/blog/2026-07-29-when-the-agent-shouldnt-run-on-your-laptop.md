---
title: "When the Agent Shouldn't Run on Your Laptop"
date: 2026-07-29
description: "Conductor's new experimental aca provider moves an agent's execution loop into a throwaway Azure container, so the orchestration you own stays on your machine and the model-driven shell doesn't."
tags: ["blog", "ai", "tooling", "open-source", "security"]
categories: ["engineering"]
draft: true
---

Every coding agent I run executes its shell commands on the machine I work from. That's the same machine holding my SSH keys, an `az login` session, a `gh` token, and about forty repos I've cloned and forgotten about. In fairness, the agent usually asks before it runs anything. I've also been known to start it with `--dangerously-skip-permissions` so it stops asking, because approving the fortieth `ls` in a row wears you down and I wanted to go get coffee. So the real control here is that I trust the agent to behave, which is less a control than a hope.

So we added a new provider to [Conductor](https://github.com/microsoft/conductor) called `aca`, and it does one thing: it takes the agent's execution loop off your machine and runs it in a container in Azure that you throw away when it's done.

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

To the rest of Conductor, nothing changes. Events stream back to the console and dashboard just as they do for a local agent, and sandbox time appears as its own usage row.

## Why we bothered

The point is where the boundary between the agent and everything I own ends up sitting.

A few days before we shipped this, I saw an article about [seven sandbox escapes](https://www.bleepingcomputer.com/news/security/cursor-codex-gemini-cli-antigravity-hit-by-sandbox-escapes/) across Cursor, Codex CLI, Gemini CLI, and Antigravity. In several cases the agent never broke the sandbox. It wrote a `.vscode` task, a hook, or a patched interpreter into the workspace, then a trusted tool on the host ran it later.

That attack needs a filesystem shared with the host and something trusted to execute the file later. An ACA session shares neither with your laptop. Its workspace is ephemeral and disappears when the session ends.

It also scales cleanly. Parallel agents and for-each items automatically get separate sessions, while retries and loop-backs can return to the same workspace. Ten workers become ten isolated containers instead of ten processes sharing one directory. The [coding-agent example](https://github.com/microsoft/conductor/blob/main/examples/aca-coding-agent.yaml) uses this to clone once, implement, test, and loop back on failure.

## What it doesn't do yet

It's still experimental, and there are some gaps to address. You need to provision your own ACA pool, sessions are ephemeral, and `conductor resume` reruns the agent rather than restoring its workspace. Individual turns should stay under about 30 minutes. Stopping a workflow currently stops the host from waiting, but the remote agent may continue until it finishes or times out. Tool allowlists aren't supported yet, so `conductor validate` rejects them rather than silently ignoring them.

The repo includes a [provisioning script](https://github.com/microsoft/conductor/blob/main/scripts/aca/provision-pool.sh), and the [provider docs](https://github.com/microsoft/conductor/blob/main/docs/providers/aca.md) cover these limitations in detail. These are gaps we hope to close as we do more experimentation and get feedback.

## Extra isolation when you need it

I don't expect every Conductor workflow to run in ACA. Local execution is simpler, faster, and the right choice for plenty of work.

What I wanted was another option for workflows where the agentic loop shouldn't share my machine, whether because of the inputs, the tools it can access, or the number of agents running in parallel. For those workflows, ACA provides an isolated workspace that can disappear when the run is over.

Most of my workflows will still run locally. The ones I don't want running beside my SSH keys now have somewhere else to go.
