---
title: "Structuring a Team Around AI-Assisted Development"
date: 2026-03-22
description: "What changes about team structure and project planning when coding is no longer the bottleneck."
tags: ["blog", "ai", "tooling", "engineering"]
categories: ["engineering"]
draft: true
---

Most of the conversation around AI-assisted development focuses on individual productivity. How can one engineer ship faster, write fewer bugs, automate more of the tedious stuff. But I've been thinking more about the team-level question: when coding speed stops being the constraint, what do you actually change about how a project is structured?

My team has been running a project this way recently, and we've learned some things. Not all of them obvious.

## Coding speed changed the bottleneck

Here's the thing that took a while to internalize: when AI makes implementation fast, the bottleneck shifts to coordination. The actual writing of code is no longer the slow part. Figuring out what to build, making sure it's the right thing, and keeping multiple people from stepping on each other's work is where the time goes.

The best analogy I've found is driving. The faster you drive, the more attention you need to pay to steering. At 25 mph you can be a little sloppy with the wheel and it's fine. At 120 mph, a small twitch sends you into a wall. AI-assisted development is the same. When your team can go from spec to working code in a day instead of a week, every wrong decision, every misaligned interface, every ambiguous requirement hits you faster and harder in terms of productivity loss. The steering (your coordination, your specs, your design reviews) has to get proportionally better.

This sounds like it should be obvious. This is not always the case, at least not operationally. People tend to plan projects the same way they've always had, with the same sprint structures. What we've found is engineers can start finishing tasks faster than you can plan the next ones. The planning and coordination process became the bottleneck, not the coding.

## Parallel workstreams with clear boundaries

The biggest structural change we made on our project was breaking the project into parallel workstreams with well-defined boundaries between them. Each workstream owns a vertical slice: its own set of components, its own interfaces, its own tests. The boundaries are defined at the API or contract level so workstreams can move independently.

This isn't a new idea. Teams have been doing vertical slicing for years. What's different is how aggressively you can lean into it when implementation is fast. A single engineer with a good spec and a coding assistant can move through a workstream at a pace that would have required two or three people before. That changes the math on how you decompose work.

We've been assigning one person per workstream. That sounds risky, and it would be if the work were poorly specified. But when the spec is solid and the boundaries are clear, a single engineer with AI assistance can maintain the full context of their workstream without the coordination overhead of splitting it across people. Fewer handoffs, fewer sync meetings, fewer merge conflicts.

The tradeoff is obvious: bus factor. If someone is out, their workstream stalls. We've mitigated that by making specs and design decisions reviewable artifacts (more on that below), so anyone can pick up where someone left off. It's not perfect, but the productivity gain has been worth the risk so far.

## Specs as the coordination layer

In [my last post](/blog/2026-03-21-patterns-for-ai-assisted-development/), I wrote about spec-driven development as a pattern for individual work. At the team level, it becomes something more: the primary coordination mechanism.

Here's what that looks like in practice. Before anyone starts coding a workstream, they produce a spec. The spec describes what's being built, how it connects to other workstreams, what the interfaces look like, and what assumptions it makes. These specs get checked into the repo and reviewed by the team, just like code.

The review process is where the real value shows up. When you review a spec, you're reviewing the *intent* and the *design* before any code exists. You catch interface mismatches between workstreams early. You surface assumptions that don't hold. You find gaps that would have taken days to discover during implementation. It's cheaper to fix a paragraph in a markdown file than to refactor three services.

We've been doing cross-workstream spec reviews, where engineers review specs outside their own workstream specifically to check integration points. This has caught issues that the workstream owner wouldn't have seen because they were too close to the work.

## Investing more in design reviews

This is the part that feels counterintuitive: we're spending *more* time in reviews now, not less. When implementation is fast, the cost of building the wrong thing goes up relative to the cost of building it. A bad spec turns into a bad implementation in an hour instead of a week. The feedback loop is shorter, but the blast radius per bad decision is the same.

So we've shifted time from code review to design review. Not that we skip code review, but the ratio has changed. More time arguing about specs, less time arguing about implementation details.

This has been a cultural adjustment. Engineers are used to code review as the quality gate. Spec review feels different. It's less concrete, harder to point at a specific line and say "this is wrong." The team is still building that muscle. But the early signal is that the time spent here pays off downstream.

## What we use

For specs, we're using [spec-driven development](/blog/2026-03-21-patterns-for-ai-assisted-development/#3-spec-driven-development) with AI-generated drafts that get human-reviewed. For complex specs, we run them through multi-agent review workflows using [Conductor](/blog/2026-03-20-introducing-an-ai-agent-workflow-conductor/) to catch gaps before the team even sees them. The AI reviewer catches the mechanical stuff (missing edge cases, inconsistencies, vague steps), so the human review can focus on the design decisions.

## What I'd do differently

A few things I've learned that I'd apply from day one next time:

- **Define workstream boundaries before you define workstream content.** We did it the other way around on the first iteration and ended up with overlapping responsibilities that caused friction.
- **Budget more time for spec review than you think you need.** It feels slow early on. It saves time later.
- **Don't let "it's fast to build" become an excuse to skip design.** Speed makes it tempting to just try things. That works for small experiments. For a multi-workstream project, the coordination cost of undoing a bad decision doesn't go down just because coding is faster.

## Still early

This is one project, one team, a few months of data. I'm not claiming this is the right structure for every team. But the underlying observation feels durable: when AI shifts the bottleneck from implementation to specification, the team structure should shift with it. More investment in design, more parallelism in execution, and specs as the connective tissue between workstreams.

I'll keep sharing what we learn as the project progresses.
