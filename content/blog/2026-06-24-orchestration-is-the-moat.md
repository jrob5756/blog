---
title: "Orchestration Is the Moat"
date: 2026-06-24
description: "As frontier models get cheaper and more interchangeable, the useful work moves into routing, review loops, and context control."
tags: ["blog", "ai", "tooling", "engineering"]
categories: ["engineering"]
draft: true
---

OpenRouter ran an experiment that provides an interesting perspective as the focus has been squarely on Fable, GLM, etc. these past few weeks

They shipped [Fusion](https://openrouter.ai/openrouter/fusion), a compound API that fans the same prompt out to several models in parallel, then uses a judge model to merge the answers. This strategy beat a single frontier model, but the interesting part is *why*. According to OpenRouter's writeup, roughly **75% of the performance gain came from the synthesis and judge step**, not from having a more diverse panel of models. A panel of cheaper models came within 1% of a solo frontier model at about half the cost.

Most of the lift came from the orchestration, not the models themselves... which is interesting

## The models are commoditizing

The backdrop makes the Fusion result land harder. The clearest signal is the open-weight side. Z.ai's [GLM-5.2](https://www.interconnects.ai/p/glm-52-is-the-step-change-for-open) shipped with MIT-licensed weights and benchmark scores strong enough that some are calling a step change for open weight models. It is good enough that people are now making the case that there's [minimal downside to switching to open models](https://www.marble.onl/posts/cancel_claude.html), drawing the analogy to the move from Windows to Linux. It's not an isolated result either: [VibeThinker](https://arxiv.org/abs/2606.16140), a 3-billion-parameter model, reportedly beats Opus 4.5 on reasoning benchmarks. When a model you can download and run yourself is topping leaderboards, the "frontier" stops being a place only a couple of labs can reach.

The caveat is that the absolute top is still proprietary. Anthropic's Fable and Mythos remain the bar everyone else is measured against, and GLM-5.2 is closing the gap with some of the less capabile frontier models. But "closing the gap" is exactly the point. When four or five vendors are all shipping near-frontier capability and racing each other down on price, the raw model stops looking like a moat. It starts looking like compute or bandwidth: important, expensive if you waste it, but not where your product becomes hard to copy.

Fusion isn't the only signal here. Sakana AI just shipped [Fugu](https://venturebeat.com/orchestration/no-claude-fable-5-no-problem-sakana-achieves-frontier-performance-with-new-fugu-multi-model-auto-synthesis-system), a multi-agent orchestration system that exposes a single OpenAI-compatible API while internally routing each query across a swappable pool of models. Sakana claims its top tier matches Anthropic's Fable and Mythos on benchmarks. In Fugu's case, the orchestration layer is itself a *trained* model that learns how to assemble the scaffold per query, rather than hand-coded routing. Different mechanism than Fusion's panel-plus-judge, but the same conclusion. The structure and orchestration are the impactful parts, and the underlying models underneath become interchangeable.

The Fusion result gives one answer. Spend less time worshipping the model choice and more time on the structure around it: the routing, the review loops, and the control over what context each step sees. That is the part you can actually own.

## The compounding part isn't the model

I made a version of this argument in [Patterns for AI-Assisted Development](/blog/2026-03-21-patterns-for-ai-assisted-development/). For hard tasks, the best pattern I had seen was not one bigger prompt. It was a multi-agent workflow with real quality gates. Fusion is the same idea showing up at the API layer: a panel plus a judge, with the structure doing most of the work.

There's a second piece I keep coming back to. Someone did a [deep read of how six coding agents handle context compression](https://www.reddit.com/r/MachineLearning/comments/1u34hvc/what_should_context_compression_keep_i_looked_at/) (Claude Code, Codex, Cursor, and others) and argued that context management quality, not raw model intelligence, is now what separates the good agents from the bad ones. You still need a good model, but the engineering around it is where the differences start to show.

## What owning the structure looks like

If the model is the commodity, the structure around it is the asset. In practice, that means a few unglamorous choices that are easy to skip until the bill is too high or the output gets sloppy.

The orchestrator does not have to be an LLM. For a workflow with a known shape, the logic that decides what runs next can be plain deterministic routing: explicit conditions, first match wins. With no model choosing the next step, a workflow can iterate dozens of times without spending a token on orchestration. That's the opposite of the "let the agent figure out its own plan" approach, and for repeatable work it is usually the right call. If the structure is the asset, make it explicit, version controlled, and cheap to run.

The review loop needs to be part of the design. This maps directly onto the Fusion finding. One agent produces, another scores the output against explicit criteria, and anything below the bar routes *back* with the feedback attached until it passes. That is the judge step from Fusion, made durable and inspectable. The reviewer is where a lot of the quality comes from. A first draft is rarely terrible, but it is rarely thorough enough either.

That separation matters. The *structure* stays fixed and owned, while the *model* at each step becomes a casting decision. Run the draft on one model and the review on another. Swap either one when something cheaper or stronger ships. The workflow logic does not have to care.

Context is a budget you control. Decide how much prior context flows into each step: everything, just the previous step, or only the dependencies that step needs. On a large workflow, that one choice can be the difference between a sane token bill and a runaway one. If context management is becoming the differentiator between coding agents, it should be an explicit knob, not an accident of whatever happens to be in the chat.

None of this is theoretical for me. [Conductor](/blog/2026-03-20-introducing-an-ai-agent-workflow-conductor/), the multi-agent workflow tool I maintain, is built on these bets. But the principle outlasts any one tool. I want the durable work to live in the orchestration around the model, not in the model itself.

## Why I'd bet on the structure

This is why I'd rather bet on the structure. If you pour your effort into picking the perfect model, you've built on something that will get matched, undercut on price, or yanked offline by a regulator. If you pour the effort into orchestration, you build something that gets *better* as models get cheaper and more interchangeable. You can drop a stronger or cheaper model into any step without touching the logic that makes the system good.

The model is the easiest part for a competitor to buy, rent, or match. The routing, review gates, context discipline, and accumulated judgment about which step needs which model at which effort level are harder to clone. You do not get those by signing the same API contract.

## The caveats, as always

Orchestration is a multiplier on a capable model, not a replacement for one. A clever review loop wrapped around a weak model still produces weak output, just more expensively. The Fusion budget panel got within 1% of a frontier model, not within 1% of nothing.

Deterministic structure is also the right tool only when the task *has* a known structure. For genuinely exploratory work, where the plan should change based on what the agent discovers, letting the model drive is still the better fit. I covered that trade-off when I [introduced Conductor](/blog/2026-03-20-introducing-an-ai-agent-workflow-conductor/) and I'd make the same caveat now. The moat is only as deep as the structure is non-trivial. Wrapping one prompt in YAML does not buy you much.

For the large, repeatable workflows that are taking up more of my work, though, I keep landing in the same place. The models are converging on each other. I'd rather spend my effort on the orchestration around them.
