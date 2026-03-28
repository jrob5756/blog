---
title: "Brainstorm-Driven Development"
date: 2026-03-27
description: "Why using AI as a brainstorming partner before writing specs or code is just as valuable as using it for implementation."
tags: ["blog", "ai", "tooling", "engineering"]
categories: ["engineering"]
draft: true
---

Most of the attention around AI-assisted development focuses on execution. Code generation, refactoring, test writing, debugging. All valuable. But the use case that's changed my workflow the most is much simpler: using AI as a brainstorming partner before I write anything.

Not brainstorming in the loose, "give me ideas" sense. I mean structured conversations where I describe a problem, explore the solution space with the model, pressure-test my assumptions, and walk away with a clearer picture of what to build. It happens before the spec, before the code, sometimes before I've even decided if the thing is worth building at all.

I've come to think this is at least as important as AI-assisted execution. Maybe more so.

## The bottleneck isn't typing

In [a previous post](/blog/2026-03-21-patterns-for-ai-assisted-development/), I wrote about matching the right level of AI assistance to the right task. One-shot edits, plan mode, spec-driven development, multi-agent workflows. All of those patterns assume you already know *what* you're building. The brainstorming step is what gets you there.

The hardest part of most engineering work isn't the implementation. It's figuring out the right approach. Which abstraction to use, how to decompose the problem, what edge cases matter, where the existing system will push back. These are the decisions that, if you get them wrong, cost you days of rework later. And they're exactly the kind of decisions that benefit from talking them through with something that can push back.

Before AI, this was the hallway conversation. Grab a colleague, explain the problem, see if their reaction matches your thinking. That worked, but it required someone else to be available, interested, and up to speed on the context. AI doesn't replace that conversation, but it's always available, infinitely patient, and it brings broad pattern-matching that surfaces angles you might not have considered.

## What this looks like in practice

My typical brainstorming session starts with a problem statement. Not a polished one. Just enough context for the model to understand what I'm working with. Something like:

> "I need to add authorization middleware to our API gateway. The current system uses role-based access control, but we're adding resource-level permissions. I'm trying to figure out the right way to layer this in without rewriting the existing auth flow."

From there, the conversation branches. I'll ask for different approaches and their tradeoffs. The model might suggest three or four patterns, some of which I was already considering and some I wasn't. That's useful on its own, but the real value comes from the follow-up: "What are the failure modes of approach #2?" or "How does approach #3 interact with our existing caching layer?" or "Which of these is easiest to roll back if it doesn't work?"

A few specific techniques I keep coming back to:

**Exploring the solution space.** I'll ask for multiple approaches to the same problem, explicitly requesting tradeoff analysis for each. This prevents me from anchoring on the first solution that comes to mind.

**Playing devil's advocate.** Once I'm leaning toward an approach, I ask the model to argue against it. "What could go wrong with this? What am I not thinking about?" This is the most consistently valuable prompt I use. It surfaces blind spots that would otherwise show up during code review or, worse, in production.

**Pre-flight edge case analysis.** Before I've written a line of code, I describe my intended data model or API surface and ask for edge cases. Concurrent access patterns, partial failure scenarios, backward compatibility issues. It's like getting a code review before the code exists, when changes are cheapest to make.

**Comparing technology choices.** When I'm evaluating between libraries, patterns, or architectures, I'll provide my constraints and ask for a structured comparison. Not to outsource the decision, but to make sure I'm considering the right dimensions.

## Why this isn't vibe coding

There's an important distinction here. Andrej Karpathy coined "vibe coding" to describe a workflow where you let the AI handle everything and just go with the vibes. That's a fine approach for prototypes and throwaway experiments. But brainstorm-driven development is the opposite. You're using AI to think *more carefully*, not to think less.

The developer stays in the driver's seat the whole time. You're interrogating approaches, challenging assumptions, and building a mental model of the solution before any code gets written. The AI is a sparring partner, not an autopilot.

In my experience, the engineers who get the most out of AI tools are the ones who use them for thinking first and coding second. They come to the implementation phase with a clear picture of what they're building and why, which means the code generation step (whether AI-assisted or manual) goes smoother and produces fewer wrong turns.

## Saving the conversation

One thing I've started doing consistently is saving brainstorming output as a markdown file. Not the raw chat transcript, but a cleaned-up version that captures the key decisions, the approaches considered, and the rationale for the chosen direction.

This matters for a few reasons:

**It feeds into downstream processes.** If you're doing [spec-driven development](/blog/2026-03-21-patterns-for-ai-assisted-development/#3-spec-driven-development), the brainstorming output becomes the raw material for the spec. You've already explored the solution space and identified the tradeoffs. Turning that into a structured spec is a much smaller step than starting from scratch.

**It creates a decision record.** Six months from now, when someone asks "why did we build it this way?", the brainstorming doc has the answer. It captures not just what you decided but what you considered and rejected, which is often more valuable.

**It becomes reusable context.** When you hand a brainstorming doc to a coding assistant alongside your spec, the assistant has the full picture: the problem, the options you considered, the constraints that shaped the decision, and the chosen approach. That context makes the implementation dramatically better than a cold start.

Our workflow has evolved to look something like this:

1. **Brainstorm** with AI to explore the problem and solution space. Save as `brainstorm.md`.
2. **Spec** the solution, using the brainstorming output as context. Save as `spec.md`.
3. **Implement** against the spec, with the brainstorming doc and spec both in context.
4. **Review** the spec and code with the team, with the brainstorming doc available for "why did you pick this approach?" questions.

Each step builds on the previous one. The brainstorming doc makes the spec better. The spec makes the implementation better. It's a pipeline, and the first stage is where you set the trajectory.

## The team-level case

This pattern scales beyond individual work. On my team, we've started doing brainstorming sessions with AI before our design discussions. An engineer will brainstorm with AI, save the output, and share it with the team before the meeting. The meeting then starts from a higher baseline: instead of spending the first 20 minutes explaining the problem and the first approach that came to mind, we're comparing approaches that have already been pressure-tested.

It's also been useful for onboarding. When a new engineer picks up an unfamiliar part of the codebase, a brainstorming session with AI can map out the territory faster than reading through the code cold. "Here's the module I need to modify. Walk me through the key abstractions, the data flow, and the common extension points." It's not a replacement for reading the code, but it gives you a mental framework to hang the details on.

## The underappreciated half

There's a gap in how people talk about AI-assisted development. The conversation is heavily weighted toward execution: how fast can you ship, how many lines of code did the AI write, how much time did you save on boilerplate. Those things matter. But the quality of what you ship depends more on the thinking that happens before the first line of code than on how efficiently the code gets written.

Using AI for brainstorming doesn't show up in productivity metrics. You can't measure "wrong approaches avoided" or "edge cases caught before implementation." But in my experience, the time spent brainstorming with AI pays for itself many times over in reduced rework, cleaner architectures, and fewer surprises during review.

The tools keep getting better at execution. Code generation is fast and getting faster. But the thinking phase is where you set the direction, and a wrong direction executed quickly is worse than a right direction executed slowly. If you're using AI to write code but not to think about what to write, you're leaving the most valuable half on the table.
