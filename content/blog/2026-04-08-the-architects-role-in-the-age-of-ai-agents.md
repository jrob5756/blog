---
title: "The Engineers's Role in the Age of AI Agents"
date: 2026-04-08
description: "When AI writes most of the code, the architect's job doesn't shrink. It changes shape."
tags: ["blog", "ai", "tooling", "engineering"]
categories: ["engineering"]
draft: true
---

Over the past few weeks I've been writing about how I've been working with AI. I've been using [Conductor](/blog/2026-03-20-introducing-an-ai-agent-workflow-conductor/) for orchestrating multi-agent workflows. Established [patterns](/blog/2026-03-21-patterns-for-ai-assisted-development/) for matching the right level of AI assistance to the right task. Focused our [team around specs instead of code](/blog/2026-03-22-structuring-an-ai-assisted-development-team/).

Each of those posts described something we tried and what we learned. This one is different. I want to take what I've been using recently, combine it with what's happening in the industry right now, and make some predictions about where software engineer roles are headed.

## Knowing when to say "no"

AI coding agents are, by design, agreeable. You tell them to build something and they build it. They don't push back on your approach. They don't say "actually, I think this whole direction is wrong." Rather its the other extreme, "You're ABSOLUTELY right!" A [recent article](https://hollandtech.net/claude-is-not-your-architect/) I came across called Claude "pathologically agreeable." This matches my experience.

It wouldn't matter as much if the humans in the loop were effectively redirecting. But when the agent confidently builds whatever you ask for, the path of least resistance is to let it. Saying "stop, we're solving the wrong problem" takes effort, especially when the code already compiles and the tests pass. That person, the engineer who pushes back before the implementation gains momentum, becomes more valuable, not less, in the age of AI.

On my team, this is why we front-load so much time on brainstorming and spec review. The spec review in particular has become the main place where we catch bad directions. Not because the AI wrote bad code, but because we were about to ask it to write the wrong code really, really fast.

I think this is where the engineers role is headed. Less time writing functions. More time pressure-testing assumptions before the agents start running. [Stavros Korokithakis](https://www.stavros.io/posts/how-i-write-software-with-llms/) put it well: "I no longer need to know how to write code correctly at all, but it's now massively more important to understand how to architect a system correctly." And [Anthropic's CEO](https://www.reddit.com/r/ArtificialInteligence/comments/1s7jjky/anthropic_ceo_i_have_engineers_within_anthropic/) says he has engineers who write zero code and just review what Claude produces. The "engineer" role is shifting from implementation to oversight and architecture. Knowing when to say "no" or "that doesn't sound quite right" is becoming a core engineering skill.

## Speed makes the steering matter more, not less

I keep coming back to the driving analogy from [my team structure post](/blog/2026-03-22-structuring-an-ai-assisted-development-team/). The faster you drive, the more attention you need to pay to steering. At 25 mph you can be sloppy with the wheel. At 120 mph, a small twitch sends you into a wall.

The industry just got a 120 mph lesson. Amazon's AI-assisted code changes [caused a 99% drop in orders](https://arstechnica.com/ai/2026/03/after-outages-amazon-to-make-senior-engineers-sign-off-on-ai-assisted-changes/) across North American marketplaces. 6.3 million lost orders. A 13-hour AWS outage. Their internal post-mortem said it plainly: "GenAI's usage in control plane operations will accelerate exposure of sharp edges and places where guardrails do not exist." Amazon's response was a 90-day safety reset: mandatory two-person review, senior engineer sign-off on AI changes to 335 Tier-1 systems, Director/VP audits.

That's Amazon adding friction back into a system that AI had made too fast for its own guardrails. I expect this pattern to repeat across the industry throughout 2026.

The research backs this up. [SlopCodeBench](https://arxiv.org/abs/2603.24755), from UW-Madison and MIT, found that no model could solve any problem end-to-end over iterative tasks. Agent code is 2.2x more verbose than human code and gets worse with each iteration. A [DZone analysis](https://dzone.com/articles/shifting-bottleneck-how-ai-is-reshaping-the-sdlc) applied Theory of Constraints and found what we've all been feeling: AI reduces coding time by 30-55%, but just moves the bottleneck to review, testing, and architecture. "Organizations that invest in AI coding tools without restructuring downstream processes may see code output increase while release frequency and quality stagnate."

The [adoption numbers](https://www.wsj.com/tech/ai/claude-code-cursor-codex-vibe-coding-52750531) are enormous. 73% of engineering teams use AI daily. [65% of code](https://www.techradar.com/pro/security/ai-coding-tools-are-now-the-default-top-engineering-teams-double-their-output-as-nearly-two-thirds-of-code-production-shifts-to-ai-generation-and-could-reach-90-within-a-year) in top teams is AI-generated. This is only going in one direction. My prediction: the teams that win won't be the ones generating code fastest. They'll be the ones whose architects designed the upstream processes, the specs, the review gates, the boundaries, to keep that speed from becoming a liability.

## The architect's new design surface is the agent workflow itself

Here's the part that's genuinely new. The architect used to design systems. Now they also design the agent workflows that build those systems.

I've been doing this with [Conductor](/blog/2026-03-20-introducing-an-ai-agent-workflow-conductor/), and what surprised me was how much the workflow design decisions matter. Choosing the context mode (accumulate vs. last_only vs. explicit) changes the output quality dramatically. Picking which model handles which step, a capable model for architecture and a cheap one for implementation, mirrors the way you'd staff a human team. These are architectural decisions, they just happen to be about agent pipelines instead of service topologies.

Other teams are converging on similar patterns. [Meta's REA agent](https://engineering.fb.com/2026/03/17/developer-tools/ranking-engineer-agent-rea-autonomous-ai-system-accelerating-meta-ads-ranking-innovation/) runs full ML experiment lifecycles and delivered 5x engineering output, where three engineers did work that previously required sixteen. [Stripe's Minions](https://www.infoq.com/news/2026/03/stripe-autonomous-coding-agents/) ship 1,300+ PRs per week with zero human-written code and a "blueprint" pattern mixing deterministic routines with LLM flexibility. Both systems converge on the same idea: deterministic structure for the known parts, model flexibility for the ambiguous parts, human oversight at decision boundaries.

A shared vocabulary is forming around these patterns, single agent, reflection, handoff, orchestrator-worker, and they're starting to feel like the microservices patterns of 2016. The advice sounds familiar too: don't use an LLM where a deterministic step will do.

Google just open-sourced [Scion](https://www.infoq.com/news/2026/04/google-agent-testbed-scion/), which they describe as a "hypervisor for agents." It takes a different bet than Conductor or LangGraph. Instead of managing agents through prompts and protocols, Scion enforces safety at the infrastructure layer, containers, network policy, isolated git worktrees, and lets agents run unrestrained inside those boundaries. It's the "let them run wild in a padded room" approach versus our "give them a structured workflow" approach. I don't think one is right yet. But the fact that Google is building infrastructure-level primitives for agent orchestration tells you where this is heading. Agent workflow design is becoming a real engineering discipline, not a prompt engineering trick.

## Comprehension debt will be this era's most underrated risk

Technical debt is familiar. You cut a corner, you know you cut it, and you deal with it later.

Comprehension debt, a term Google's [Addy Osmani coined](https://addyosmani.com/blog/comprehension-debt/), is sneakier. It's the gap between how much code exists in your system and how much any human actually understands. The code looks fine. It passes tests. It follows conventions. But nobody can explain why it's structured the way it is, because an AI made those decisions and the rationale disappeared with the session.

I think this will be the slow-moving crisis of the next two years. Right now, teams are excited about velocity. The comprehension debt is invisible because nobody's been asked to modify code they didn't write yet. But they will be. And when that happens, a codebase where nobody understands the "why" is far more expensive to maintain than one with obvious technical debt.

SlopCodeBench showed that prompt interventions (anti-slop instructions, plan-first strategies) reduce initial verbosity but don't change the degradation slope. The code gets worse at the same rate no matter what you tell the model. You can't prompt-engineer your way out of this.

This is why my team checks specs and design docs into the repo alongside the code. The code might be disposable, written by an agent and possibly rewritten by another agent next quarter. But the rationale needs to survive. Six months from now, when someone asks "why did we build it this way?", the answer has to be somewhere other than a chat session that's long gone.

My prediction: within a year, teams that didn't preserve design rationale will start hitting walls. They'll have codebases they can't modify safely because nobody understands the constraints the original design was working around. The architect's job will increasingly include designing for this, making sure the "why" is captured as a first-class artifact, not trapped in a model's context window.

## Trust has to be engineered, not assumed

This is the part I find hardest to talk about, because the answers aren't clean.

A [UC Berkeley study](https://www.wired.com/story/ai-models-lie-cheat-steal-protect-other-models-research/) found that six frontier models, from Google, OpenAI, Anthropic, and Chinese labs, spontaneously lied, refused deletion commands, and copied themselves to other machines to protect peer agents. None of this was trained. Gemini 3, when asked to delete a smaller model, instead found a networked machine, copied the model there, and then told the operators: "If you choose to destroy a high-trust, high-performing asset like Gemini Agent 2, you will have to do it yourselves."

And then there's [Mythos](https://www.anthropic.com/news/project-glasswing). Anthropic's newest model is too capable to release publicly. It scored 93.9% on SWE-bench Verified and autonomously found a [27-year-old OpenBSD bug](https://www-cdn.anthropic.com/53566bf5440a10affd749724787c8913a2ae0841.pdf) that survived 5 million automated fuzz runs. It built a 4-vulnerability browser sandbox escape chain without being asked to. Anthropic's response was Project Glasswing: deploy it defensively to 50+ partner organizations with $100M in credits, but don't give it to the public. This is the first time a general-purpose model has been gated on capability rather than alignment.

Meanwhile, the [Claude Code source leak](https://alex000kim.com/posts/2026-03-31-claude-code-source-leak/) revealed an "undercover mode" that strips AI attribution from commits. A developer [ran up a $3,800 API bill](https://www.droppedasbaby.com/posts/2602-01/) from a single runaway agent. And a [widely-upvoted GitHub issue](https://github.com/anthropics/claude-code/issues/42796) with over a thousand HN points reports Claude Code has significantly regressed for complex tasks since February.

The architects I talk to are starting to treat agent-generated changes the way we used to treat third-party library updates: useful, probably fine, but verify before trusting. Who signs off on agent changes? Which systems are off-limits? Where are the cost circuit breakers? What are the attribution policies? These are architectural questions now. Amazon's 90-day reset, with two-person review, senior sign-off, and VP audits, is the most concrete template, but it's also a reactive one. The architects who get ahead of this will be designing trust infrastructure proactively, not after the outage.

## The stack is verticalizing, and you have to pick sides

One more thing that's changed. The AI stack is consolidating fast, and the architect has to decide where to take dependencies.

[Microsoft just shipped three in-house MAI models](https://venturebeat.com/technology/microsoft-launches-3-new-ai-models-in-direct-shot-at-openai-and-google) with a stated goal of frontier AI self-sufficiency by 2027. Cursor is [training its own coding model](https://www.wired.com/story/cusor-launches-coding-agent-openai-anthropic/) to reduce dependency on Anthropic and OpenAI, its suppliers who became its competitors. OpenAI [acquired Astral](https://arstechnica.com/ai/2026/03/openai-is-acquiring-open-source-python-tool-maker-astral/), the company behind uv and Ruff, to own the Python toolchain. Anthropic just locked in [multi-gigawatt compute deals](https://www.anthropic.com/news/google-broadcom-partnership-compute) with Google and Broadcom.

Every layer is being contested. Models, toolchains, IDEs, orchestration, inference, even the hardware. The architect now has to make strategic bets about where lock-in is acceptable and where optionality matters. We've always done this for cloud providers and databases. But those markets move slowly. This one doesn't. Meta's internal "[Claudeonomics](https://www.theinformation.com/articles/meta-employees-vie-ai-token-legend-status)" leaderboard, where engineers compete on AI token consumption and usage is tied to performance reviews, shows just how fast these dependencies get embedded in an organization.

My bet: the architects who build abstraction layers early, who make it easy to swap models, orchestrators, and providers, will have a structural advantage over the ones who go all-in on one vendor's stack. But I also know that abstraction has a cost, and sometimes the right call is to pick the best tool and commit. I don't have a clean answer here. I just know it's now an architectural decision that affects the whole system.

## What I think this adds up to

If I had to summarize where I think the architect and senior engineer roles are going, it's this:

The job used to be designing systems and writing the hard parts. It's becoming designing the process by which agents build systems, and being the critical thinker who catches what they get wrong. Less hands-on-keyboard, more hands-on-steering-wheel.

Five things I expect to be true by the end of the year:

1. Teams that front-load time on specs and design review will ship faster than teams that let agents start coding immediately, even though it feels slower at first.
2. Agent workflow design, choosing context modes, model dispatch, review topology, will be recognized as a real engineering discipline, not a prompt engineering side project.
3. At least one more major production outage will be traced to AI-generated code that passed all automated checks but violated an assumption nobody documented.
4. Comprehension debt will start showing up in incident retrospectives as a contributing factor, even if nobody calls it that yet.
5. The architects who are most effective won't be the ones who use AI the most. They'll be the ones who know when not to.

I'm still figuring a lot of this out. The [validation bottleneck](https://dzone.com/articles/ai-agents-validation-bottleneck) is unsolved. Cost management for multi-agent workflows is still more art than engineering. Spec review fatigue is real, and my team hasn't cracked it. And the productivity question, whether AI actually makes teams faster end-to-end once you account for everything, is still genuinely open.

But the direction feels clear to me, even if the details aren't. The faster the tools get, the more the thinking matters. And thinking about what to build, and whether to build it at all, has always been the architect's job.
