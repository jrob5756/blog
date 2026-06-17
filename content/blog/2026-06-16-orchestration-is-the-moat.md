---
title: "Orchestration Is the Moat"
date: 2026-06-16
description: "As frontier models get cheaper and more interchangeable, the useful work moves into routing, review loops, and context control."
tags: ["blog", "ai", "tooling", "engineering"]
categories: ["engineering"]
draft: true
---

One benchmark detail from last week has been rattling around in my head.

OpenRouter shipped [Fusion](https://openrouter.ai/openrouter/fusion), a compound API that sends the same prompt to several models in parallel, then uses a judge model to combine their answers. The result beat a single frontier model, but that was not the part that stuck with me. According to OpenRouter's writeup, roughly **75% of the performance gain came from the synthesis and judge step**, not from having a more diverse panel of models. A budget panel of cheaper models came within 1% of a solo frontier model at about half the cost.

Most of the lift came from the orchestration, not the models.

That feels more useful than another round of model leaderboard news. It says something practical about where builders should spend their time.

## The models are commoditizing

The backdrop makes the Fusion result land harder. ChatGPT's market share [slipped below 50%](https://techcrunch.com/2026/06/16/chatgpts-market-share-slips-below-50-for-first-time/) for the first time. OpenAI is [considering price cuts](https://www.cnbc.com/2026/06/11/openai-mulls-slashing-prices-ahead-of-competition-from-anthropic-wsj.html) to stay competitive. Microsoft shipped [seven MAI models](https://microsoft.ai/news/building-a-hillclimbing-machine-launching-seven-new-mai-models/) built from scratch. Open-weight models keep closing the gap, and local models are now good enough that people run them for daily work.

When four or five vendors are all shipping near-frontier capability and racing each other down on price, the raw model stops looking like a moat. It starts looking like compute or bandwidth: important, expensive if you waste it, but not where your product becomes hard to copy.

The Fusion result gives one answer. Spend less time worshipping the model choice and more time on the structure around it: the routing, the review loops, and the control over what context each step sees. That is the part you can actually own.

## The compounding part isn't the model

I made a version of this argument in [Patterns for AI-Assisted Development](/blog/2026-03-21-patterns-for-ai-assisted-development/). For hard tasks, the best pattern I had seen was not one bigger prompt. It was a multi-agent workflow with real quality gates. Fusion is the same idea showing up at the API layer: a panel plus a judge, with the structure doing most of the work.

There's a second piece from last week that I keep coming back to. Someone did a [deep read of how six coding agents handle context compression](https://www.reddit.com/r/MachineLearning/comments/1u34hvc/what_should_context_compression_keep_i_looked_at/) (Claude Code, Codex, Cursor, and others) and argued that context management quality, not raw model intelligence, is now what separates the good agents from the bad ones. You still need a good model, but the engineering around it is where the differences start to show.

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
