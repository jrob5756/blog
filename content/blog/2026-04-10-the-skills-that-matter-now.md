---
title: "The Skills That Matter Now"
date: 2026-04-10
description: "AI changed what engineers spend their time on. The skills that separate engineers who thrive from those still catching up."
tags: ["blog", "ai", "tooling", "engineering"]
categories: ["engineering"]
draft: false
---

AI has made engineers more productive. There's no doubt about that. What's changed is where the time goes. The hands-on coding that used to dominate our day is shrinking, and everything around it, such as planning, design, and review, is expanding to fill the gap. The role is completely shifting.

I've been thinking about what specifically separates the engineers who are thriving from the ones still finding their footing in this new era of software development. It's not the tools they use. It's the skills they develop. Here are five that I believe matter most right now.

## Staying curious

In the past, an engineer who wasn't keeping up with the latest trends could still be productive for years on what they knew. The work didn't change that fast. That's no longer true.

The tools are changing monthly. The patterns for how to use them are changing just as quickly. Six months ago, I hadn't even considered multi-agent review workflows. Now those are default parts of how I work. 

The good news is that curiosity compounds. Each new thing you learn makes the next thing easier to adopt, because you've built intuition for how these tools behave and where they break down. On the other hand, standing still is more expensive than it used to be. I wouldn't recommend waiting for the dust to settle. It's not settling.

## Bias toward action

Curiosity alone isn't enough if it stays theoretical. The engineers pulling ahead are the ones who actually try things. And AI has made trying things very easy. Spinning up a prototype that would have taken a couple of days now takes a couple of hours. Writing a proof of concept for an API design, making a web app, exploring whether an approach is even viable. All of that got faster.

This should change how engineers approach uncertainty. The old instinct was to think carefully before writing any code, because the cost of going down the wrong path was high. That instinct is still correct at the design level (see next section), but at the implementation level, the math has shifted. Building a quick prototype to validate an idea is now cheaper than spending the same time debating it in a meeting.

Be honest with yourself about what's working, though. A [METR study](https://metr.org/blog/2025-07-10-early-2025-ai-developer-study/) found that developers believed AI made them 20% faster while objectively being 19% slower. Experimentation is cheap, but self-deception isn't. Try things, measure whether they actually helped, and adjust. The goal is experimentation with feedback loops, not just vibe coding.

## Systems design mindset

Coding is no longer the hard part. For most tasks, a good coding assistant can produce a working implementation faster than you can type it. Where engineers still provide the most value is in the architectural decisions, e.g, whether the code is maintainable, scalable, and correct at the system level.

Systems design is more important than ever. Prototyping an implementation is cheap and reversible. But committing to the wrong abstraction, the wrong service boundary, or the wrong data model cascades through everything that gets built on top of it. That's where getting it right upfront matters more than ever, and AI will overlook these decisions (or make assumptions) if you don't guide it carefully.

I'd encourage every engineer to get comfortable spending what feels like "too much" time on the design step. Sketch the components, define the interfaces, talk through the failure modes, review it with a peer. Then hand the spec to your coding assistant. The code will be better, the rework will be less, and the system will hold together under pressure.

## Reviewing with intent

Every time you accept a suggestion, approve a plan, or commit AI-generated code, you're doing a code review. It's no longer just a PR gate, it's part of your inner loop. This constant oversight matters more than ever because the volume of code is increasing exponentially. A [SlopCodeBench study](https://arxiv.org/abs/2603.24755) found that agent-generated code is 2.2x more verbose than human-written code, and quality degrades with each iteration. Let your agents loose untethered and you'll build up what Addy Osmani from Google calls [comprehension debt](https://addyosmani.com/blog/comprehension-debt/): the gap between how much code exists and how much any human genuinely understands.

So how can we review all this code without drowning in it? Review at the right level. Nits are fine, but they're not where the value is... maybe they never were. The important questions are structural: does this follow the patterns we've established? Is the abstraction right? Are there hidden coupling points? Does this fit into the system, or does it just solve the immediate problem in a vacuum? When I wrote about [structuring a team around AI-assisted development](/blog/2026-03-22-structuring-an-ai-assisted-development-team/), we found that shifting review time from implementation details to design and architecture was one of the highest-leverage changes we made.

## Pattern matching

In [a previous post](/blog/2026-03-21-patterns-for-ai-assisted-development/), I wrote about four patterns for AI-assisted development: one-shot, plan mode, spec-driven, and multi-agent workflows. Each is appropriate for a different level of task complexity.

Over time, this should become second nature. A simple function rename gets a one-shot prompt. A new API endpoint gets plan mode. A cross-cutting feature gets a spec that's reviewed before implementation starts. A large feature in a complex codebase gets a multi-agent workflow with quality gates.

The most common failure mode is defaulting to one-shot for everything. It works great for small tasks, but for anything with real design decisions, skipping the planning step means the AI is making architectural choices on your behalf without you even noticing. The second most common failure mode is over-engineering: running a full multi-agent pipeline for a task that needed a two-line edit.

The skill is pattern matching. Knowing when a task deserves more investment upfront and when it doesn't. That judgment comes from experience, and the only way to build it is practice.

## The common thread

All of these skills point in the same direction. The value an engineer provides is shifting from the mechanical to the architectural. From writing code to deciding what code should be written.

None of this means the fundamentals stop mattering. You still need to understand data structures, concurrency, system design, and debugging. In many ways, you need to understand them more deeply, because you're now reviewing and steering code rather than writing it line by line. 

The tools will keep changing. The models will keep getting better. But the essence of the job is still engineering. Contrary to what you may be hearing, that's not going anywhere. There's just a lot less typing, and a lot more thinking

... Happy coding!
