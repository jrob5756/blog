---
title: "Skill Rot Is Real"
date: 2026-06-18
description: "When the agent does the typing, your fundamentals quietly atrophy. Why it happens now, and the habits I'm using to stay sharp."
tags: ["blog", "ai", "engineering", "mentorship"]
categories: ["engineering"]
draft: false
---

Two things crossed my feed recently, which caught my attention and were related to a few of my recent posts.

The first was [Fata](https://fata.dev), a spaced-repetition app with a blunt pitch: fight "skill rot from AI coding." I'm not promoting Fata (or similar tools) necessarily but I found the concept interesting. The second was a [Hacker News thread with more than 1,000 points](https://news.ycombinator.com/item?id=44302598) where developers were asking, half-seriously, whether they should go back to a local model for daily coding because the friction might keep them sharper. The underpinning of both is the same. We can all feel certain skills quietly atrophying...

... myself included

## Why it's happening now specifically

In [Growing Engineers in the Age of AI](/blog/2026-04-17-growing-engineers-in-the-age-of-ai/) I wrote about how AI short-circuits the feedback loop that used to build judgment. That doesn't stop being true after you become a senior engineer either. The hard parts used to force you to learn, such as chasing the wrong branch in the debugger, remembering various edge cases, rebuilding your mental model after tests fail. When the agent does that work, the code can get better while your own instincts get less exercise.

Here's a good example. Simon Willison wrote about giving Claude Fable 5 a one-line prompt to fix a CSS bug and then [walking away from his computer](https://simonwillison.net/2026/Jun/11/fable-is-relentlessly-proactive/). The agent ran a 15-step autonomous investigation. It spun up headless browsers, cross-tested across engines, built a custom proxy to capture diagnostics, and fixed the bug. I'm not going to pretend that isn't amazing. It is. But if you weren't watching, you saw only the result. The debugging practice happened somewhere else.

Do that across enough tasks and skill rot stops sounding mysterious, and feels very real. You stopped practicing the parts that used to keep you sharp.

## The gap is measurable, not just "vibes"

I don't think this is just nostalgia either. There are a few data points that make the concern harder to hand-wave.

There's the [METR study](https://metr.org/blog/2025-07-10-early-2025-ai-developer-study/) from last year that I mention often, where developers believed AI made them 20% faster while they were actually 19% slower. That gap matters because we're terrible at sensing the drift from inside our own workflow. [SlopCodeBench](https://arxiv.org/abs/2603.24755) reports that agent-generated code is about 2.2x as verbose as human-written code, with quality degrading on each iteration. That's code we ultimately have to read and maintain. Addy Osmani's [comprehension debt](https://addyosmani.com/blog/comprehension-debt/) names the downstream problem... code piles up faster than understanding does.

So yes, the tools help. They also make it easier to ship more code than anyone on the team can explain. That's a rough place to discover your fundamentals have gotten soft.

## This isn't a "type everything yourself" post

I'm not trying to make hand-rolling boilerplate code sound virtuous. Coding assistants have revolutionized how we work. I use them constantly and would likely need to find a new career if they disappeared tomorrow. In [The Skills That Matter Now](/blog/2026-04-10-the-skills-that-matter-now/) I argued that the job is shifting from the mechanical to the architectural, and I still think that's accurate.

The risk is coasting without noticing. Software fundamentals used to get exercise for free because the work forced you into reps. Now you can skip more of them than ever. If you want to stay sharp, you have to choose a few reps on purpose. 

> Side note: I hope you're following the exercise parallels, because it's actually a great analogy.

For me, there are a few things I'm trying to do to stay strong ;). It starts with carefully reading the diff. AI-generated code review is part of the inner loop. If I can't explain a block, I didn't review it and I approved a stranger's code... sorry to my future AI overlords.

I also stay stricter about design. That's why I keep leaning on [spec-driven](/blog/2026-03-21-patterns-for-ai-assisted-development/) workflows and spending more time on the planning and design cycles. The system shape, failure modes, boundaries, names... those are the decisions that train judgment and set the agent's rails. Let the agent fill in the boring parts, but don't let it quietly decide the architecture while you watch a progress spinner.

I'm also picking a few fundamentals to exercise deliberately. Fata's spaced-repetition angle is interesting. My list (or workout program if you will) is systems design, architecture, distributed systems, and the data structures hiding under nice abstractions. I keep them strong by being intentional, reading unfamiliar code, solving a small problem the hard way now and then. The reps are optional, which makes them easier to skip (e.g. legs day) and more important to schedule.

## The part that doesn't rot

I keep coming back to fundamentals because these AI-tools have a short half-life and change rapidly. Software fundamentals will be important for far longer. As the agents get better, you're doing less of the typing and more of the steering, which means your judgment matters more, not less. You can't catch a subtle concurrency bug in generated code if you never built the intuition for concurrency yourself.

There's a new kind of job forming, and it's the one who lets the tools accelerate the work but keeps ownership of the thinking who will thrive. They're the ones who use AI to move faster without letting their own understanding go stale. They know the coding can be delegated, but the architectural skill still has to live with them... at least for now.

Until next time... Thanks for reading...
