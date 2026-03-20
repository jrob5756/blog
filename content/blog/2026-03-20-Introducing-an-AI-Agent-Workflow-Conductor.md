---
title: "Conductor: Deterministic Routing for Multi-Agent Workflows"
date: 2026-03-20
description: "An open-source CLI for orchestrating multi-agent AI workflows with YAML — where the orchestrator isn't an LLM."
tags: ["blog", "ai", "tooling", "open-source"]
categories: ["engineering"]
draft: false
---

[Conductor](https://github.com/microsoft/conductor) is a CLI my team built for orchestrating multi-agent AI workflows. We've been using it on a recent project and building it in the open from the start. I kept putting off this post because I wanted to get the framing right, but at this point I'd rather just get it out there and iterate.

## What it is

Conductor is a CLI for running multi-agent AI workflows defined in YAML. You describe your agents, how they connect, and what conditions determine the next step... then you run it.

The key decision we made early on was that the orchestrator itself should not be an LLM. There are a lot of frameworks where the agent dynamically plans and adapts, and that's genuinely useful when the task is exploratory. But the workflows we kept reaching for (code review pipelines, research-then-synthesize, plan-then-implement) have a known structure. We don't need the model to rediscover the plan each time. We just need it to execute.

So routing between agents uses Jinja2 templates and expression evaluation. First matching condition wins. A workflow can loop hundreds of times without the routing layer consuming any tokens. The structure is fixed at definition time, and that's the point.

If you're currently stitching together multi-step LLM pipelines with Python scripts, prompt chains, and ad-hoc retry logic — that's the problem space we built this for.

## What we found interesting building it

**Agent isolation ended up mattering a lot.** Each agent gets its own session, its own system prompt, model, provider, and temperature. No shared conversation bleeding between steps. This means you can put a cheap model on a triage step and a capable one on reasoning, or mix Copilot and Claude in the same workflow. Context flow between agents is explicit, not implicit.

We built three context modes: `accumulate` (every agent sees all prior output), `last_only` (just the previous step), and `explicit` (only named dependencies). The default is `accumulate` because it's convenient, but for bigger workflows it eats your token budget fast. Being intentional about what each agent can see turned out to be one of the most impactful decisions we made.

**A web dashboard for watching workflows run.** The engine emits structured events, and the dashboard subscribes to them in real time — you can see each agent step execute, inspect context flowing between steps, and watch routing decisions happen. There's also a human gate step type that pauses execution, presents options, and routes based on the response. Works in both the terminal and the dashboard.

**Shell commands as first-class steps.** Not everything needs an LLM. Running tests, linting, fetching data. These just execute directly, with stdout, stderr, and exit codes captured into context. A code review workflow can run `pytest` between the "implement" and "review" steps without paying for a model to do it.

**Events over logs.** Under the hood, the engine uses a pub/sub system for all output. The terminal renderer, web dashboard, and any future consumers all subscribe independently. More work upfront than printing to stdout, but it decoupled things in a way that keeps paying off.

## The tradeoff

A question I keep getting is how this compares to frameworks where the agent manages its own plan. It's a fair one. If your task needs to dynamically restructure itself based on what it discovers, letting the LLM decide what comes next will feel more natural. Conductor's branching and loops cover a lot of ground, but the topology is fixed at definition time.

For us, that's usually what we want. The structure is known, and we'd rather have predictability and cost control than re-planning flexibility. But it's a real tradeoff, not a universal win.

## Links

It's on [GitHub](https://github.com/microsoft/conductor). The README covers the schema, examples, and how to get started.

The repo also includes a [Claude skill](https://github.com/microsoft/conductor/blob/main/.claude/skills/conductor/SKILL.md) that teaches agents how to author and execute workflows. Point your coding agent at it and it can build Conductor workflows for you.

I'll be writing more about specific patterns and workflows as we go.
