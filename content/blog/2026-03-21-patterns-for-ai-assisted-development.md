---
title: "Patterns for AI-Assisted Development"
date: 2026-03-21
description: "A practical guide for matching the right level of AI assistance to the right task, from one-shot edits to multi-agent workflows."
tags: ["blog", "ai", "tooling", "engineering"]
categories: ["engineering"]
draft: true
---

The tooling for AI-assisted development is moving fast. Coding assistants ship new features every week, each with their own spin on agents, planning mode, and various levels of customization. It's a lot to keep up with, and most of the discourse focuses on the tools themselves.

I think that's the wrong level to optimize at. The tools will keep changing. What's more durable are the **patterns** and knowing which level of AI assistance to reach for based on the size and ambiguity of the task in front of you.

Over the past several months, I've been working with folks on my team to standardize how we think about this. What we've landed on isn't a framework in the formal sense. It's more of a shared vocabulary. Four patterns, ordered by investment of time and tokens, that help engineers pick the right approach without overthinking it.

This post isn't about any specific tool. When I say "coding assistant," I mean the whole category: GitHub Copilot, Claude Code, Cursor, OpenCode, whatever you're using. The patterns apply regardless.

## 1. One-Shot Editing (~1 minute)

The simplest pattern. You know exactly what you want, you tell the assistant, it does it.

This is the bread and butter of AI-assisted development: the one-shot prompt. Rename a variable across a file, add a missing null check, generate a boilerplate function signature, convert a block of code from one pattern to another. Tasks where the specification *is* the instruction.

I use this constantly for things I know how to do but don't feel like typing out. Reformatting a data structure, adding error handling I've written a hundred times, cleaning up imports. It's not that the task is hard. The AI just makes the mechanical parts free.

**When to reach for it:**
- You can describe the change in one or two sentences
- The scope is a single file or a small, well-defined edit
- You don't need the assistant to understand broader context

**When to move on:** If you catch yourself writing a multi-paragraph prompt to explain what you want, you've probably outgrown one-shot. Step up to plan mode.

## 2. Plan Mode (~2–3 minutes)

Most coding assistants now have some form of planning mode where they read files, explore the codebase, reason about the task, and propose a plan without making any changes. The mechanics differ, but the pattern is the same: the AI thinks before it acts.

What makes this different from one-shot isn't just the time investment. It's the **collaboration model**. The assistant presents its understanding of the problem and its intended approach, and you get to redirect before it commits to a path. That feedback loop matters. I've seen agents go completely sideways on medium-complexity tasks when they're not given the chance to show their work first.

Plan mode has gotten meaningfully better in the last year. Assistants now routinely spin up sub-agents to explore different parts of a codebase in parallel, read test files to understand expected behavior, and check for existing patterns before generating new code. It's not just "read the file and write a diff" anymore.

A concrete example: building a new API endpoint. Instead of asking the assistant to write the code, you ask it to survey the codebase and list out the steps it would take. It prints an ephemeral plan in the chat: update the schema, add a new route, create the controller, add tests. You read it, spot that it missed adding the authorization middleware, correct it in the chat, and *then* tell it to execute.

**When to reach for it:**
- The task touches multiple files or requires understanding existing patterns
- You want to review the approach before implementation starts
- The task is small to medium: a small feature or a bug that spans a few modules

**When to move on:** If the task is large enough that you'd want a second opinion on the plan, or if you need the plan to persist as a document rather than disappearing in the chat log, step up to spec-driven development.

## 3. Spec-Driven Development (~5–10 minutes)

This is where things get interesting. Coding assistants have made code generation fast and cheap. The bottleneck has shifted upstream. The quality of the output depends almost entirely on how well the task is specified. Spec-driven development makes the specification an explicit, tangible artifact.

The idea is straightforward: before you generate any code, have the AI produce a markdown spec file that describes what's being built, why, and how. Think of it as a lightweight design doc that drives implementation. Tools like [SpecKit](https://github.com/github/spec-kit) and [GSD](https://github.com/gsd-build/get-shit-done/) have built tooling around this pattern. We've been using our own internal tooling for SDD, but again, the important part is not the tool, it's the pattern.

Here's why this matters beyond the obvious "planning is good" truism: **the spec becomes a review artifact**. My team has started checking these specs into the repo and code reviewing them together before implementation. It sounds like an extra step, and it is. The cost is front-loaded. But it has more than paid for itself: fewer wrong turns, less rework, and clearer intent for reviewers.

The spec also acts as a checkpoint for the AI. When you hand a well-written spec to a coding assistant, the implementation tends to be dramatically better than when you describe the same task conversationally. The structure helps the model as much as it helps the humans.

**When to reach for it:**
- The task is medium to large and has real design decisions to make
- Multiple people need to understand or agree on the approach
- You want a reviewable artifact before implementation starts

**When to move on:** If the spec itself is complex enough to benefit from structured review (accuracy scoring, completeness checks, iterative refinement), it's time for a multi-agent workflow.

## 4. Multi-Agent Workflows (~10–30+ minutes)

For larger features in complex codebases, a single agent session starts to hit its limits. Context windows fill up, earlier decisions fall out of context, and the quality of output degrades over long sessions. Multi-agent workflows address this by giving each agent a focused, scoped context rather than an ever-growing conversation history, with built-in review cycles.

This isn't hypothetical for us. My team has been using [Conductor](https://github.com/microsoft/conductor), an open-source CLI we built for exactly this pattern (I wrote about it in [my previous post](/blog/2026-03-20-introducing-an-ai-agent-workflow-conductor/)). The key design decision was that routing between agents should be deterministic, not managed by another LLM. The structure is defined in YAML, and agents pass context explicitly.

Here's what our planning workflow looks like in practice:

1. **Architect agent** produces a solution design and implementation plan using a capable model with full codebase context.
2. **Content reviewer agent** evaluates the plan against a scoring matrix: accuracy, completeness, consistency, and feasibility. It produces a score from 0 to 100.
3. If the score is **below 90**, the plan goes back to the architect with the reviewer's feedback. This cycle repeats until it passes.
4. Once it scores above 90, a **readability reviewer** does a final pass. After multiple revision cycles, the logical flow of the document can suffer. This step catches that.
5. The result is a spec that's accurate, complete, and readable. At that point, it's ready for our implementation workflow.

The review loop is what makes this work. The first draft from the architect is rarely bad, but it's also rarely *thorough enough*. The reviewer catches gaps: missing edge cases, inconsistencies with existing patterns, vague implementation steps. Two or three cycles usually get it to a strong spec, but I've seen cases where it took five or six iterations to get a complex design fully fleshed out.

If you have the tokens to spare and the codebase complexity to justify it, multi-agent workflows are the highest-leverage pattern I've seen for large tasks. The upfront investment is real, but the output quality is in a different class.

**When to reach for it:**
- The task is large enough that a single session would lose coherence
- You need structured quality gates (accuracy, completeness, readability)
- The codebase is complex enough that context control matters

**When to move on:** This is the most involved pattern in the toolkit. If multi-agent workflows aren't producing good results, the issue is likely scoping or requirements, not tooling.

## Picking the right pattern

The goal isn't to always use the most sophisticated pattern. It's to match the level of investment to the task.

| Pattern | Time | When to use |
|---|---|---|
| **One-shot** | ~1 min | You know exactly what you want. Small, well-defined edits. |
| **Plan mode** | ~2–3 min | Multi-file changes. You want to review the approach first. |
| **Spec-driven** | ~5–10 min | Medium-to-large tasks. The team needs a reviewable plan. |
| **Multi-agent** | ~10–30 min | Large features. Complex codebases. Quality gates matter. |

The most common mistake I see is engineers either defaulting to one-shot for everything (resulting in a lot of rework on complex tasks) or overinvesting in elaborate workflows for simple changes. The skill is in the calibration.

## Navigating the trade-offs

This is an honest snapshot, not a finished framework. As we use these higher-investment workflows more, a few things I'm still working through:

- **How much to standardize.** These patterns help, but every engineer's workflow is a little different. Push too hard on standardization and you lose the flexibility that makes these tools useful. Too little and everyone's reinventing their own approach from scratch.
- **Spec review fatigue.** Reviewing AI-generated specs is a different skill than reviewing code. The team is still building that muscle, and determining how much review is "enough" without slowing down development.
- **Cost management.** Multi-agent workflows can burn through tokens fast. We're getting better at choosing context modes in Conductor (accumulate, last-only, or explicit) depending on the task, but balancing thoroughness with token spend is still a bit of an art.

If you're working on similar patterns, I'd be interested to hear what's working for your team. I'm sharing as I go, rough edges and all.
