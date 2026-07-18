# Research 00 — Original Gemini seed: "Premiere Pro Live Automation Blueprint"

> Provided by the user on 2026-07-18 (pasted; the share URL https://share.gemini.google/bVjSyOVI7WIe was unreachable from the research environment). Preserved verbatim below, with annotations.
>
> **Completeness note:** the pasted document is truncated — Section 3's Implementation Blueprint names three code files (`server.js`, `src/main/index.ts`, `send-command.js`) but their code bodies were not included, and Section 4 ("ExtendScript Guidelines for Claude Code") cuts off after "must strictly adhere to the following language standards:". Treat those as gaps to fill during implementation, not as lost requirements — the architecture and reference directory are complete.
>
> **How this relates to the main handoff:** the blueprint describes the DIY variant of the CEP-bridge pattern documented in [research/01](01-landscape-claude-premiere.md) §Common Patterns and [research/04](04-mcp-server-evaluation.md) §3 — the same architecture the existing open-source Premiere MCP servers already implement. See [HANDOFF.md](../HANDOFF.md) §5a for how the two options are reconciled.

---

## Verbatim seed content

**Claude Code Context: Live Premiere Pro Automation Bridge**

This document establishes the architecture, code execution specifications, and research references for building a live, bidirectional, real-time automation bridge between Claude Code (CLI) and Adobe Premiere Pro.

### 1. System Architecture

To bypass Premiere Pro's "launch-only" command-line restriction, we maintain a persistent WebSocket bridge. This allows real-time timeline manipulation from the terminal without restarting the application.

Components:

1. **Terminal Trigger**: A simple terminal script/command that sends stringified JavaScript payloads over an HTTP endpoint.
2. **Local Relay Server** (`localhost:3000` / `8080`): An Express and WebSocket relay broker. It routes automation strings down to the connected active Premiere extension panel and listens for responses.
3. **Active Premiere Panel** (`bolt-cep` / `bolt-uxp`): A headless CEP panel loaded in Premiere Pro that maintains an active WebSocket client. It evaluates received ExtendScript snippets via the native API (`csInterface.evalScript`) and returns output data (or runtime errors) to the server.
4. **ExtendScript Engine**: Premiere's internal environment that modifies timelines, tracks, bins, and sequences.

### 2. API & SDK Reference Directory

When writing code, scripts, or debugging native API objects, use these verified, official developer resources.

#### 2.1 Host & API Documentation

- **The Premiere Pro Scripting Guide (ExtendScript)**: ppro-scripting.docsforadobe.dev — use this to inspect properties and methods of the `Project`, `Sequence`, `TrackItem`, `Component`, and `QE` (Quality Engineering) objects.
- **Official Adobe Sample Panel (PProPanel)**: PProPanel on GitHub — the gold standard example maintained by Adobe. Reference this for exact syntax implementations of clip import, sequence creation, metadata adjustments, and media export.
- **Adobe CEP HTML Extension Cookbook**: CEP Cookbook on GitHub — crucial for understanding lifecycle hooks, window permissions, Node.js integration inside Adobe windows, and IPC configurations.
- **Adobe UXP Developer Tool & API Guide**: developer.adobe.com/uxp — crucial if migrating the pipeline from CEP panels to the modern Unified Extensibility Platform (UXP) backend.

#### 2.2 Frameworks & Typings

- **Hyper Brew Bolt CEP Boilerplate**: github.com/hyperbrew/bolt-cep — used to generate the build process. Features hot-reloading (HMR), TypeScript compiling, and automated development staging setup.
- **Types-For-Adobe (Premiere Pro)**: community-provided TypeScript definitions (`types-for-adobe` on npm/GitHub) — provide autocomplete and compiler checking inside VS Code, preventing spelling errors on internal structures like `app.project.activeSequence.videoTracks`.

### 3. Implementation Blueprint

- **A. Local Relay Server (`server.js`)** — use this implementation on your host machine to broker traffic. *(code body not included in the recovered seed)*
- **B. Headless CEP Client (`src/main/index.ts`)** — run this routine in your Bolt extension client framework inside Premiere to execute incoming commands. *(code body not included in the recovered seed)*
- **C. Script Dispatcher CLI (`send-command.js`)** — command trigger utilized by Claude Code or human terminal operators. *(code body not included in the recovered seed)*

### 4. ExtendScript Guidelines for Claude Code

When writing ExtendScript payloads (`jsxCode`) to pass down the websocket, Claude must strictly adhere to the following language standards: *(document truncated here)*

---

## Annotations (what the seed adds vs. the fresh research)

**New, useful references not surfaced by the fresh research:**
- [bolt-cep](https://github.com/hyperbrew/bolt-cep) — Hyper Brew's CEP boilerplate (TypeScript, HMR, build tooling). Hyper Brew also authored the UXP-status blog post cited in research/03; there is a sibling `bolt-uxp` for the migration path.
- [types-for-adobe](https://github.com/docsforadobe/Types-for-Adobe) — TypeScript definitions for the ExtendScript DOM (autocomplete + compile checking for `app.project.activeSequence...`).
- [Adobe CEP HTML Extension Cookbook](https://github.com/Adobe-CEP/CEP-Resources) — panel lifecycle, permissions, Node integration, IPC.

**Where the seed's architecture matches the fresh research:** identical to bridge pattern #1 (CEP + ExtendScript + WebSocket relay) used by antipaster, Nate-valerian, and (HTTP variant) MauricePutinas — see research/01 and research/04.

**Where the seed differs from the main handoff's recommendation:**
- The seed assumes a raw HTTP/CLI dispatcher (`send-command.js` called from the terminal). The handoff prefers exposing the bridge as an **MCP server** so Claude Code gets typed tools, discoverability, and the permission model instead of shelling out raw `jsxCode` strings — functionally equivalent transport, better agent ergonomics and safety.
- The seed proposes building the bridge from scratch; the handoff recommends adopting a maintained existing server first (same architecture, already debugged against current Premiere builds) and keeps the DIY build as Plan B.

**What the seed omits (covered by the handoff):** existing MCP-server ecosystem, podcast-specific workflow design, transcript-first pipeline, model tiering, caption-track limitation, CEP sunset timeline and UXP/OTIO fallbacks, safety/backup practices, verification plan.
