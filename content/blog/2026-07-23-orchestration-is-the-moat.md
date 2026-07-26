---
title: "Orchestration Is the Moat"
date: 2026-07-23
description: "Frontier models are turning into a commodity. The durable work, and the part I actually own, is the orchestration around them: routing, review loops, and context control."
tags: ["blog", "ai", "tooling", "engineering"]
categories: ["engineering"]
draft: true
---

A few weeks ago, OpenRouter shipped [Fusion](https://openrouter.ai/openrouter/fusion), a compound API that fans a prompt out to several models and then uses a judge model to combine their answers. It caught my attention since orchestration has been on my mind lately. 

This simple approach beat most of the frontier models tested. In one case, a panel of cheap models landed within 1% of Claude Fable at about half the cost! Yes, Fable is crazy expensive, but you get the point.

This is similar to the idea that drove me to build [Conductor](https://github.com/microsoft/conductor) earlier this year, applied to the API layer instead of the workflow layer.

## The model is becoming a commodity

It seems as though models are beginning to commoditize. OpenRouter's usage board tracks what developers are paying for, and open weight models now hold [the top five](https://www.reddit.com/comments/1uuyw46). The reason is money: as one developer put it, "an hour of coding costs about $10 on Claude versus under 50 cents on DeepSeek." The US labs are still leading on quality, but for some day-to-day work a cheap openweight model can be good enough.

The easier models become to swap, the harder it is for any one of them to be a meaningful advantage. The product has to stand apart for reasons beyond just the model behind it.

## What I actually own

If the model is the commodity, the structure around it is the asset. I think of that structure as two parts: the tooling we give the model and the process we use to coordinate it.

The tooling includes MCP servers, skills, and specialized agents. These tools give the model access to the systems and expertise the task requires. The process determines how those pieces work together. Once a process works, I want to make it repeatable instead of rebuilding it in a prompt every time. The best way I have found to do that is to configure it as a workflow.

That is what led me to build [Conductor](/blog/2026-03-20-introducing-an-ai-agent-workflow-conductor/), the agentic workflow tool I maintain. It lets me define the routing, loops, and context boundaries once, then swap models in and out as they improve or become cheaper without rebuilding the process around them.

## The caveat, as always

Of course, orchestration is a multiplier on capable models, not a substitute for them. A clever loop around a weak model still produces weak output. It also only pays off when the task has real structure. For genuinely exploratory work, where the plan should change as the agent learns, letting the model drive is still the better call, and wrapping a single prompt in YAML doesn't buy you much. I write about this in [Patterns for AI-Assisted Development](/blog/2026-03-21-patterns-for-ai-assisted-development).

But for the large, repeatable tasks that take up more of my time every week, I rely heavily on Conductor. Models will continue to improve, and I will use the best ones available. A stable workflow lets me take advantage of those improvements as they arrive.
