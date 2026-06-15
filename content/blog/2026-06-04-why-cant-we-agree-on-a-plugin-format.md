---
title: "Why Can't We Agree on a Plugin Format?"
date: 2026-06-04
description: "A small template repo for authoring AI coding plugins in a tool-agnostic format and transpiling them into Claude Code, Copilot CLI, OpenCode, and Codex bundles."
tags: ["blog", "ai", "tooling", "open-source"]
categories: ["engineering"]
draft: false
---

I switch between coding assistants from time to time. Sometimes it's Claude Code, sometimes it's GitHub Copilot CLI, or occasionally I'm playing with OpenCode on a side project. Each one is good at different things, and I like having the option to switch between them.

What I don't like is the tax I pay every time I move my own plugins between them.

## The annoying part

My plugins aren't anything fancy. A handful of skills and agents, plus a few MCP servers here and there. Stuff I've built up over time and want available wherever I happen to be typing that day.

The problem is that every tool has its own packaging format:

- **Claude Code** wants a `.claude-plugin/` directory, a `marketplace.json` registry, and skill/agent markdown files with very specific frontmatter.
- **Copilot CLI** wants a `plugin.json` manifest with its own schema, plus a `.github/plugin/marketplace.json` registry to be discoverable.
- **Codex CLI** uses yet another layout under `~/.codex/`.
- **OpenCode** has no marketplace concept at all. Each plugin is just files you drop into a project's `.opencode/` folder.

The differences are small on their own (a field gets renamed in one tool, a directory moves in another, frontmatter keys swap around), but copy-pasting one plugin into the layout another tool expects still takes about fifteen minutes of fiddly editing every time. And I have to do it again on each of my dev machines. Multiply by a few plugins and the friction adds up fast... and then when I want to switch back... well, you get the idea.

## What other people are doing

Before I built anything, I poked around to see how other people were solving this. There's a fair bit going on, but most of it didn't directly address my problem.

The biggest projects in this space are large skills libraries that handle the cross-tool install for you. [`alirezarezvani/claude-skills`](https://github.com/alirezarezvani/claude-skills) and [`borghei/Claude-Skills`](https://github.com/borghei/Claude-Skills) both ship hundreds of `SKILL.md` files plus install scripts (`./scripts/convert.sh --tool all`, `npx @borghei/claude-skills add ...`) that drop the right thing into each tool's expected directory. They cover 9–11 assistants between them and they clearly work, which is why they have thousands of stars. The catch is they're skills-only. A skill is one thing in a plugin. Agents, MCP server configs, hooks, slash commands, and the marketplace registry that tells `/plugin install` what's available are different things, and those libraries don't handle them. They also assume Claude's `SKILL.md` schema as the canonical source and convert outward, which is fine until you want to author in a tool-neutral format.

[**Happier**](https://guides.happier.dev/how-to-keep-prompts-and-skills-in-sync-across-claude-code-codex-and-opencode) is a companion app that treats your prompt/skill library as the source of truth and exports it to provider-native locations on each machine. It's a thoughtful approach if you want a long-lived app managing your library, but again the surface is prompts and skills, not full plugin bundles.

A few people are reaching for [**symlinks**](https://understandingdata.com/posts/symlinked-agent-configs/), keeping one master file and linking it into each tool's expected path. That only solves the case where the files are *identical* across tools. But a lot of the providers have different frontmatter requirements, and some have fields the others don't support.

These are all really cool projects. They just don't solve the specific thing I was hitting: I wanted to author a complete plugin (skills, agents, hooks, MCP, plus the marketplace metadata) once, and let each tool's native `/plugin install` flow consume it without me hand-editing four versions every time something changed.

## The template repo

[`plugin-marketplace-template`](https://github.com/jrob5756/plugin-marketplace-template) is a GitHub template repository I created to help eliminate some of this toil. You click "Use this template," get your own copy, and that copy is a working plugin marketplace from day one. It's a template because it doesn't actually contain any plugins, just the scaffolding to make it easy to add your own and keep them in sync across tools.

You author each plugin once:

```
plugins/<name>/
  plugin.yaml             # declarative manifest, with per-target overrides
  agents/<agent>.md       # body only, no frontmatter
  skills/<skill>/SKILL.md # body only
  .mcp.json               # optional
  hooks/hooks.json        # optional
```

Then `npm run build` runs a small Node transpiler that produces:

```
dist/claude/<name>/      → Claude Code plugin
dist/copilot/<name>/     → Copilot CLI plugin
dist/codex/<name>/       → Codex CLI plugin
dist/opencode/<name>/    → OpenCode bundle
```

…and regenerates the per-tool marketplace registries (`.claude-plugin/marketplace.json`, `.github/plugin/marketplace.json`) so each assistant's `/plugin install` flow just works.

The `dist/` directory is committed on purpose. The generated marketplace files point at `./dist/<target>/<plugin>` as the plugin source, and the tools resolve those paths over the remote git tree. So the downstream loop is: edit `plugins/`, run `npm run build`, commit both, push. That's the whole workflow.

Adding a fifth target later (Gemini CLI, Cursor, whatever) is a drop-in transpiler. There's a section in the `AGENTS.md` walking through what to implement and where the tests live.

## Using it

Once you've created your marketplace from the template, point each tool at it:

**Claude Code**
```text
/plugin marketplace add <you>/my-plugins
/plugin install my-skill@my-plugins
```

**Copilot CLI** and **Codex CLI** follow the same flow. Register the marketplace, then install.

**OpenCode** has no marketplace concept, but each `dist/opencode/<plugin>/` folder ships with a README explaining how to drop it into a project's `.opencode/` directory.

On every new dev machine, the only setup is configuring the tool to know about your marketplace. The plugins themselves come along for the ride.

## Keeping forks in sync

One thing I wanted to get right was upstream syncing. GitHub doesn't give template-derived repos a "Sync fork" button (that's a fork-only feature), so the template ships with a `.gitattributes` that marks downstream-owned paths (`plugins/**`, `marketplace.yaml`, `dist/**`) as `merge=ours`. After a one-time `git remote add template ...`, pulling in upstream tooling improvements is `git fetch template && git merge template/main`, and your own plugins stay untouched while the build tooling, schemas, and docs flow through cleanly.

## If something better comes along

Honestly, I'd love for this template to become unnecessary. The long-term answer is for the tools to converge on a shared plugin format. If that happens, I'll archive the repo and move on happily :).

Until then, this is what I'm using to keep my own plugins portable, and I figured I'd put it out there in case it's useful to anyone else. If you've built something similar, or you have a better idea, I'd like to hear about it. The repo is on [GitHub](https://github.com/jrob5756/plugin-marketplace-template). Issues and PRs welcome.