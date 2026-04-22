---
title: "Growing Engineers in the Age of AI"
date: 2026-04-17
description: "AI changed how we write code, but it didn't change what makes a great engineer. Early-in-career developers need mentorship more than ever, and spec-driven development is one of the best ways to provide it."
tags: ["blog", "ai", "engineering", "mentorship"]
categories: ["engineering"]
draft: true
---

Mark Russinovich and Scott Hanselman recently published a piece in Communications of the ACM called ["Redefining the Software Engineering Profession for AI."](https://cacm.acm.org/opinion/redefining-the-software-engineering-profession-for-ai/) Their central question is what happens to early-in-career engineers when AI changes the shape of the job?

Their thesis is straightforward. AI is acting as what they call "seniority-biased technological change." It disproportionately amplifies engineers who already have systems judgment, architectural taste, debugging intuition, and operational awareness. Senior engineers get an enormous productivity boost. Early-in-career developers who lack that hard-won knowledge struggle to contribute meaningfully, because they can't steer, verify, or integrate AI output the way experienced engineers can.

I think they're right, and one meaningful way we can help starts with how we structure the work.

## The problem

What separates a senior engineer from a junior one isn't code or language knowledge. It's the accumulated intuition from years of building, breaking, and fixing systems. Where to draw service boundaries, how to model data for real access patterns, what happens when a dependency goes down, why "it works on my machine" means almost nothing. That knowledge was always learned by doing, by making mistakes alongside people who'd made those mistakes before. AI short-circuits the feedback loop. An early-in-career engineer can now ship a feature that passes tests but collapses under real-world conditions, and the experience that would have come from struggling through the implementation never happens.

In [a previous post](/blog/2026-04-10-the-skills-that-matter-now/), I wrote about how the value an engineer provides is shifting from the mechanical to the architectural. That shift is hardest on the people who haven't had time to develop architectural judgment yet. They're being asked to steer at high speed before they've learned how to drive. This isn't a criticism of them. They're doing exactly what the tools encourage by moving fast and shipping. The problem is that without the right support structure, moving fast can mean moving fast in the wrong direction.

## Spec-driven development as a mentorship tool

I've written before about [spec-driven development](/blog/2026-03-21-patterns-for-ai-assisted-development/#3-spec-driven-development) as a way to improve code quality by making the specification an explicit artifact. What I didn't emphasize enough is that it's also one of the best mentorship tools I've found.

Here's how we've been using it with early-in-career engineers on my team:

1. **The engineer writes the spec, not the code.** Before touching any implementation, they produce a markdown document that describes what they're building, how it fits into the system, what the interfaces look like, and what failure modes they've considered.
2. **The spec becomes a PR.** They check it into the repo and open a pull request, just like they would for code.
3. **We review it together.** Not just asynchronously with comments, but also in a live conversation. We walk through the design decisions, I ask questions about tradeoffs they may not have considered, and we talk through alternatives.

The magic is in step three. When you review a spec together, you're having the kind of conversation that used to happen organically over years of working alongside senior engineers. "Why did you put this boundary here?" "What happens if this service is unavailable?" "Have you thought about how this data model handles the query patterns from the dashboard?" These are the questions that build architectural intuition, and they're much easier to have over a one-page spec than once the code is already written.

The feedback is also cheaper to act on. Changing a paragraph in a spec is trivial. Refactoring three services because the boundary was wrong is not. By front-loading the design conversation, you catch the expensive mistakes before any code exists.

## Why this works better than code review alone

Traditional code review is still valuable, but it has limitations as a teaching tool. By the time code exists, the big decisions have already been made. Reviewing a PR and saying "the service boundary should be different" is demoralizing when someone just spent two days building it. The sunk cost makes it harder to change direction, and the feedback arrives too late to shape the thinking.

Spec review flips the timing. The investment is small (a document, not an implementation), so changing direction is painless. The conversation happens at the design level, where the most important learning occurs. Because there's no code to defend, the engineer is more open to exploring alternatives.

I've also found that writing specs forces a kind of clarity that coding doesn't. When you're writing code, it's easy to let the implementation details carry you forward without articulating why you made a particular choice. A spec requires you to explain your reasoning in plain language. That act of explanation surfaces gaps in understanding that would otherwise stay hidden until production.

When I wrote about [structuring a team around AI-assisted development](/blog/2026-03-22-structuring-an-ai-assisted-development-team/), I talked about how we shifted time from code review to design review. For early-in-career engineers, that shift is even more impactful. The design conversation is where the mentorship actually happens.

## Making it practical

A few things we've learned about running this effectively:

**Keep the spec lightweight.** The goal isn't a formal design document. It's a page or two that covers the what, the why, and the how. If the spec takes longer to write than the implementation would, you've over-invested. For most tasks, 30 minutes of spec writing and 30 minutes of review is the right balance.

**Review live, not async.** Written PR comments work for code review, but spec review benefits from conversation. Questions lead to follow-up questions. Tradeoffs need to be discussed, not just flagged. A 30-minute call where you walk through the spec together teaches more than a dozen inline comments.

**Ask questions, don't prescribe.** The temptation as a senior engineer is to just tell them the right answer. Resist it. "What happens if this service is down?" is a better prompt than "You need to add a circuit breaker here." The first builds judgment. The second just solves today's problem.

**Make it a habit, not a gate.** If spec review feels like bureaucracy, you'll lose buy-in fast. Frame it as a collaboration tool, not a compliance step. The engineer should walk away from the review feeling like they learned something, not like they were graded.

## The bigger picture

The paper makes a strong case for formal preceptorship programs at scale. I 100% agree. But you don't need a formal program to start today! You just need to be intentional about creating the conditions where early-in-career engineers build judgment, not just ship code.

Spec-driven development with active review is one practical way to do that. It doesn't require a new org structure or a training budget. It requires senior engineers to invest time in reviewing design decisions with their early-in-career teammates before implementation starts. That investment scales one relationship at a time, which is both its strength and its limitation. You can't mentor a hundred people this way. But you can make sure the five or ten engineers closest to you are building real intuition, not just fluency with a coding assistant.

I've been practicing this on my current projects and it's not perfect. The specs aren't always the right level of detail, and I'm still figuring out the right cadence. But the engineers I work with are asking better questions, catching more of their own design gaps, and building intuition faster than they would from code review alone. As I mentioned in previous posts, the tools will keep changing. The need to grow engineers who understand *why* a system should be built a certain way, not just *how* to build it (or if it should even be built at all), isn't going anywhere.

Thanks for reading...