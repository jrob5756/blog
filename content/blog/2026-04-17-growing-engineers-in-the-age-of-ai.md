---
title: "Growing Engineers in the Age of AI"
date: 2026-04-17
description: "AI changed how we write code, but it didn't change what makes a great engineer. Early-in-career developers need mentorship more than ever, and spec-driven development is one of the best ways to provide it."
tags: ["blog", "ai", "engineering", "mentorship"]
categories: ["engineering"]
draft: true
---

Mark Russinovich and Scott Hanselman recently published a piece in Communications of the ACM called ["Redefining the Software Engineering Profession for AI"](https://cacm.acm.org/opinion/redefining-the-software-engineering-profession-for-ai/) that focuseson what happens to early-in-career (EiC) engineers when AI changes the shape of the job?

Their thesis is straightforward. AI is acting as what they call "seniority-biased technological change." It disproportionately amplifies engineers who already have systems judgment, architectural taste, debugging intuition, and operational awareness. Senior engineers get an enormous productivity boost. EiC developers who lack that hard-won knowledge struggle to contribute meaningfully, because they can't steer, verify, or integrate AI output the way experienced engineers can.

I think they're right. And one meaningful way we can help starts with how we structure the work.

## The experience gap

When I think about what separates a senior engineer from a junior one, it's rarely syntax or language knowledge. It's the accumulated intuition from years of building, breaking, and fixing systems. Things like:

- **Systems design.** How to decompose a problem into components with clear boundaries. Where to draw service lines. What belongs in a shared library versus what stays local.
- **Distributed systems.** Understanding consistency tradeoffs, failure modes, retry semantics, idempotency. Knowing that "it works on my machine" means almost nothing when the system spans a dozen services.
- **Data modeling.** Choosing the right storage abstractions, understanding access patterns, knowing when denormalization is a pragmatic choice versus a future landmine.
- **Operational thinking.** How will this behave under load? What happens when a downstream dependency goes down? How do we observe this in production?

None of this is taught effectively by reading docs or watching tutorials. It's learned by doing, by making mistakes, and by working alongside people who've made those mistakes before. The problem is that AI tools can now generate plausible-looking code that sidesteps all of these considerations. An early-in-career engineer can ship a feature that works in dev and collapses under real-world conditions, and the feedback loop that would have taught them something gets short-circuited.

This is the core of the problem. The agents aren't bad. They're just not a substitute for the judgment that comes from experience. And if we don't create structures that help EiC developers build that judgment, we end up with a generation of engineers who can produce code but can't evaluate whether it's the right code.

## Moving fast in the wrong direction

There's a version of this that looks like productivity on the surface. An early-in-career engineer picks up a task, fires up their coding assistant, gets a working implementation quickly, opens a PR. The code runs, the tests pass. But the data model doesn't account for the access patterns that will hit it at scale. The service boundary is drawn in the wrong place. The error handling swallows failures silently. The API contract is inconsistent with the rest of the system.

In [a previous post](/blog/2026-04-10-the-skills-that-matter-now/), I wrote about how the value an engineer provides is shifting from the mechanical to the architectural. That shift is hardest on the people who haven't had time to develop architectural judgment yet. They're being asked to steer at high speed before they've learned how to drive.

This isn't a criticism of early-in-career engineers. They're doing exactly what the tools encourage: moving fast and shipping. The problem is that without the right support structure, moving fast can mean moving fast in the wrong direction. And fixing architectural mistakes after the fact is expensive, regardless of how quickly the code was written.

## Spec-driven development as a mentorship tool

I've written before about [spec-driven development](/blog/2026-03-21-patterns-for-ai-assisted-development/#3-spec-driven-development) as a way to improve code quality by making the specification an explicit artifact. What I didn't emphasize enough is that it's also one of the best mentorship tools I've found.

Here's how we've been using it with early-in-career engineers on my team:

1. **The engineer writes the spec, not the code.** Before touching any implementation, they produce a markdown document that describes what they're building, how it fits into the system, what the interfaces look like, and what failure modes they've considered.
2. **The spec becomes a PR.** They check it into the repo and open a pull request, just like they would for code.
3. **We review it together.** Not asynchronously with comments, but in a live conversation. We walk through the design decisions, I ask questions about tradeoffs they may not have considered, and we talk through alternatives.

The magic is in step three. When you review a spec together, you're having the kind of conversation that used to happen organically over years of working alongside senior engineers. "Why did you put this boundary here?" "What happens if this service is unavailable?" "Have you thought about how this data model handles the query patterns from the dashboard?" These are the questions that build architectural intuition, and they're much easier to have over a one-page spec than over a 500-line diff.

The feedback is also cheaper to act on. Changing a paragraph in a spec is trivial. Refactoring three services because the boundary was wrong is not. By front-loading the design conversation, you catch the expensive mistakes before any code exists.

## Why this works better than code review alone

Traditional code review is still valuable, but it has limitations as a teaching tool for early-in-career engineers. By the time code exists, the big decisions have already been made. Reviewing a PR and saying "the service boundary should be different" is demoralizing when someone just spent two days building it. The sunk cost makes it harder to change direction, and the feedback arrives too late to shape the thinking.

Spec review flips the timing. The investment is small (a document, not an implementation), so changing direction is painless. The conversation happens at the design level, where the most important learning occurs. And because there's no code to defend, the engineer is more open to exploring alternatives.

I've also found that writing specs forces a kind of clarity that coding doesn't. When you're writing code, it's easy to let the implementation details carry you forward without articulating why you made a particular choice. A spec requires you to explain your reasoning in plain language. That act of explanation surfaces gaps in understanding that would otherwise stay hidden until production.

When I wrote about [structuring a team around AI-assisted development](/blog/2026-03-22-structuring-an-ai-assisted-development-team/), I talked about how we shifted time from code review to design review. For early-in-career engineers, that shift is even more impactful. The design conversation is where the mentorship actually happens.

## Making it practical

A few things we've learned about running this effectively:

**Keep the spec lightweight.** The goal isn't a formal design document. It's a page or two that covers the what, the why, and the how. If the spec takes longer to write than the implementation would, you've over-invested. For most tasks, 30 minutes of spec writing and 30 minutes of review is the right balance.

**Review live, not async.** Written PR comments work for code review, but spec review benefits from conversation. Questions lead to follow-up questions. Tradeoffs need to be discussed, not just flagged. A 30-minute call where you walk through the spec together teaches more than a dozen inline comments.

**Ask questions, don't prescribe.** The temptation as a senior engineer is to just tell them the right answer. Resist it. "What happens if this service is down?" is a better prompt than "You need to add a circuit breaker here." The first builds judgment. The second just solves today's problem.

**Use AI to draft, humans to review.** Early-in-career engineers can use their coding assistant to help generate the initial spec. That's fine. The value isn't in writing the spec from scratch. It's in the review conversation that follows. Whether the first draft came from the engineer's keyboard or their AI assistant matters a lot less than whether they can defend and refine the design in review.

**Make it a habit, not a gate.** If spec review feels like bureaucracy, you'll lose buy-in fast. Frame it as a collaboration tool, not a compliance step. The engineer should walk away from the review feeling like they learned something, not like they were graded.

## The bigger picture

The paper makes a strong case for formal mentorship programs at scale. I 100% agree. But you don't need a formal program to start today! You just need to be intentional about helping EiC developers build the judgment that experience used to provide on its own.

Spec-driven development with active review is one practical way to do that. It doesn't require a new org structure. It just requires senior engineers to invest time in reviewing design decisions with their junior teammates before implementation starts. I've been practicing this on my current projects and it's not perfect. The specs aren't always the right level of detail, and I'm still figuring out the right cadence. But EiC engineers are asking better questions, catching more of their own design gaps, and building intuition faster than they would from code review alone.

As I've said before, the tools will keep changing. The need to grow engineers who understand *why* a system should be built a certain way (or not at all), not just *how* to build it, isn't going anywhere. That's on us. More to come as I learn what works.
