# Handoff — Claude Code ↔ Adobe Premiere: Automated Video-Podcast Editing

> **Status:** Research complete, ready for implementation. Written 2026-07-18.
> **For:** the next Claude Code session. Pick this up with:
> *"Read `premiere-automation/HANDOFF.md` and guide me through the implementation, starting at Phase 0."*
> **Research appendices:** [`research/00`](research/00-gemini-seed.md) (original Gemini seed, annotated) · [`research/01`](research/01-landscape-claude-premiere.md) (landscape) · [`research/02`](research/02-podcast-editing-operations.md) (podcast ops) · [`research/03`](research/03-premiere-scripting-surfaces.md) (scripting surfaces) · [`research/04`](research/04-mcp-server-evaluation.md) (MCP evaluation)

---

## 1. Context & mission

The user produces a **video podcast** and has little time to edit. The goal is a **live, conversational automation loop between Claude Code and Adobe Premiere** — like the 2025-26 YouTube demos where Claude removes silence, makes cuts, and assembles timelines directly in a running Premiere instance — tuned specifically for the recurring, mechanical parts of podcast post-production. Seamlessness is the top priority: after one-time setup, editing an episode should be a single skill invocation plus a human review pass.

The original seed was a Gemini handoff titled **"Premiere Pro Live Automation Blueprint"**, later recovered from the user and preserved (annotated, partially truncated) at [`research/00-gemini-seed.md`](research/00-gemini-seed.md). It independently proposes the same core architecture this handoff recommends — a persistent WebSocket bridge into a headless CEP panel executing ExtendScript — which is exactly the pattern the existing open-source MCP servers implement. Its unique contributions (the **bolt-cep** boilerplate, **types-for-adobe** typings, and the CEP Cookbook, for a build-your-own bridge) are folded into §5a below.

**Guiding principle from the research:** automate the mechanical 80% (silence, filler, sync, captions, chapters, reframing, export), keep the human on the creative 20% (pacing, what to keep, final QC). Full automation of narrative judgment is not the goal and not currently achievable well.

## 2. TL;DR recommendation

1. **Bridge:** install a community **Premiere MCP server using the CEP/ExtendScript bridge pattern** — it's what all the convincing live demos use, and it's the only pattern that reaches the QE DOM (ripple delete, razor, effects-by-name) needed for real editing. Pick the server by OS at Phase 0 (see §4 decision gates): macOS → `hetpatel-11/Adobe_Premiere_Pro_MCP` (278 tools, most verified, ships its own agent skill); Windows → `antipaster/Adobe-Premiere-Pro-MCP` (170+ tools, Windows installer) with `leancoderkavy/premiere-pro-mcp` (+ community windows-fix) as runner-up. If none fit, build the bridge yourself per the Gemini blueprint (§5a — bolt-cep + WebSocket relay, wrapped as MCP).
2. **Workflow:** build a **transcript-first editing pipeline** as a project skill (`/edit-podcast`): transcribe → Claude computes a cut list from the transcript + audio analysis → MCP bridge executes cuts on the live timeline → human reviews in Premiere → export via Media Encoder.
3. **Fallback / zero-install path:** generate a rough-cut timeline as **FCP7 XML (via OpenTimelineIO)** and import it into Premiere — works with no plugin at all, survives cuts/placement/markers, and is the escape hatch whenever the bridge breaks on a Premiere point release.
4. **Model tiering:** mechanical stages run on **Haiku/Sonnet subagents**; only creative judgment (what to cut, pacing, chapter titles, shorts selection) runs at the top tier. Encoded in §7.
5. **Do NOT rely on** Adobe's official "Adobe for Creativity" MCP connector for this (independently tested at Express-tier depth only, not real timeline control), and don't build anything new on pymiere (unmaintained, CEP-dependent).

## 3. Architecture

```
┌────────────────────────── user's machine ──────────────────────────┐
│                                                                    │
│  Claude Code (this repo)                                           │
│   ├─ /edit-podcast skill  ← orchestrator, model-tiered             │
│   ├─ MCP client ──stdio──► Premiere MCP server (Node)              │
│   │                          │ file-poll or WebSocket bridge       │
│   │                          ▼                                     │
│   │                       CEP panel (inside Premiere)              │
│   │                          │ CSInterface.evalScript()            │
│   │                          ▼                                     │
│   │                       Premiere DOM + QE DOM  ──► live timeline │
│   │                                                                │
│   ├─ local analysis (no bridge needed):                            │
│   │    ffmpeg + faster-whisper → transcript w/ word timings        │
│   │    (reuse this repo's youtube-transcript venv pattern)         │
│   │    silence/energy detection → candidate cut list               │
│   │                                                                │
│   └─ fallback lane: OTIO → FCP7 XML → File > Import in Premiere    │
│                                                                    │
│  Adobe Media Encoder ◄─ EncoderManager / watch folder ─ export     │
└────────────────────────────────────────────────────────────────────┘
```

Two lanes, by design:

- **Live lane (primary):** MCP bridge edits the open project. Interactive, reviewable, undoable in Premiere's history. This is the "seamless" experience.
- **File lane (fallback):** Claude builds the edit outside Premiere (OTIO/FCP7 XML cut list from the source media) and the user imports it. One manual step, but immune to CEP/plugin/version breakage. Also the right lane if the user ever switches NLEs.

Analysis (transcription, silence detection) always runs **locally via ffmpeg/whisper**, not through the bridge — it's faster, testable, and identical in both lanes. This repo already has the `youtube-transcript` skill with a `faster-whisper` venv; reuse that pattern (uv venv per skill, `${CLAUDE_PROJECT_DIR}` paths).

## 4. Phase 0 — decision gates (ask the user first)

Ask these before installing anything; they pick the concrete components:

1. **OS?** macOS → `hetpatel-11/Adobe_Premiere_Pro_MCP`. Windows → `antipaster/Adobe-Premiere-Pro-MCP` (check issue #4 fix landed for 26.3.0) or `leancoderkavy/premiere-pro-mcp` + `takeyama88/premiere-pro-mcp-windows-fix`.
2. **Premiere version?** (`Premiere > About`) — bridges are fragile against point releases (documented breakage on 26.3.0). Whatever works, **pin it**: turn off CC auto-update for Premiere and re-verify the bridge after any update.
3. **Recording setup?** Number of cameras and whether audio is one mic per speaker on separate tracks (dramatically improves silence/filler detection and enables speaker-based camera switching) vs a single mixed track.
4. **Comfort with debug-mode CEP?** All CEP bridges require enabling unsigned extensions (macOS: `defaults write com.adobe.CSXS.12 PlayerDebugMode 1`; Windows: registry `HKCU\Software\Adobe\CSXS.12\PlayerDebugMode=1`). Low risk, reversible, but say it out loud before doing it.
5. **Buy-vs-build appetite?** If the user wants results *this week* with zero setup risk: **AutoPod ($29/mo, 30-day trial)** already does multicam auto-switching + jump-cut silence removal inside Premiere, and the Claude pipeline can be layered around it (chapters, shorts, show notes). Building the MCP route is more capable and free, but budget a real afternoon for setup + pilot. These are not mutually exclusive.

## 5. Implementation plan

### Phase 1 — install & smoke-test the bridge (~1 hour, one-time)

1. Clone the chosen MCP server; install per its README (Node 18+; CEP panel copy/symlink into the Premiere extensions folder; enable PlayerDebugMode; restart Premiere; confirm the panel shows "Connected" under `Window > Extensions`).
2. Register with Claude Code at **project scope** so it travels with this repo:
   `claude mcp add premiere --scope project -- node "/absolute/path/to/<server>/dist/index.js"`
   (writes `.mcp.json`; commit it with a placeholder path documented in the README).
3. Smoke test in a **scratch project** (never the real episode): list project items → create a sequence → import a clip → razor at 10 s → ripple delete → add a marker → undo everything. Verify each step visually.
4. Record working versions (Premiere build, server commit hash, CEP version) in `premiere-automation/VERSIONS.md`.

### Phase 1-alt (§5a) — DIY bridge lane (the Gemini blueprint)

Only take this lane if Phase 0 reveals the existing servers don't fit (unsupported Premiere build, both broken on the user's point release, or the user wants full ownership of the bridge). The [Gemini seed](research/00-gemini-seed.md) specifies it:

- **Stack:** [bolt-cep](https://github.com/hyperbrew/bolt-cep) boilerplate (TypeScript, hot reload) → headless CEP panel holding a WebSocket client → local Express/WebSocket relay (`localhost:3000`/`8080`) → payloads executed via `csInterface.evalScript()`.
- **Key references:** [Premiere Scripting Guide](https://ppro-scripting.docsforadobe.dev/) (Project/Sequence/TrackItem/QE objects) · [PProPanel sample](https://github.com/Adobe-CEP/Samples/tree/master/PProPanel) (canonical syntax for import/sequence/export) · [CEP Cookbook](https://github.com/Adobe-CEP/CEP-Resources) (lifecycle, permissions, Node integration) · [types-for-adobe](https://github.com/docsforadobe/Types-for-Adobe) (TypeScript defs for the ExtendScript DOM) · [bolt-uxp](https://github.com/hyperbrew/bolt-uxp) (future migration).
- **One deliberate change from the seed:** wrap the relay as a small **MCP server** (stdio) instead of a raw `send-command.js` CLI dispatcher. Same transport underneath, but Claude Code then gets typed tools, discoverability, and its permission model, rather than shelling out raw `jsxCode` strings through Bash. Cherry-pick tool schemas/ExtendScript snippets from `leancoderkavy` or `antipaster` (MIT) rather than writing 200 tools from scratch.
- The seed's code sections (`server.js`, panel client, dispatcher) and its "ExtendScript language standards" section were truncated in recovery — reconstruct from bolt-cep's examples and PProPanel; nothing essential is lost.

Either lane ends at the same place: a Premiere MCP server registered at project scope, smoke-tested per Phase 1 step 3.

### Phase 2 — local analysis toolkit (~1 hour, one-time)

1. New skill dir `.claude/skills/podcast-audio-analysis/` mirroring the `youtube-transcript` skill's venv pattern: `ffmpeg` + `faster-whisper` (word-level timestamps) + a silence/energy detector (e.g. `ffmpeg silencedetect` or librosa RMS).
2. Output contract (JSON): word-timed transcript per speaker track + candidate dead-air spans + filler-word spans. This file is the *interface* between mechanical analysis and creative judgment — everything downstream consumes it.
3. Optional: also emit Adobe's **transcript JSON spec** (word-level timecodes; see research/03 §5) so Premiere's own Text-Based Editing and captioning can ingest the same transcript.

### Phase 3 — the `/edit-podcast` skill (the deliverable, ~half a day incl. pilot)

Orchestrated stages, each resumable/idempotent (same pattern as `youtube-research-pipeline`):

1. **Ingest** — import episode media into a dated bin; create/verify the sequence (multicam source sequence if multiple cameras, synced by audio waveform).
2. **Analyze** *(local, Haiku-tier)* — run podcast-audio-analysis; produce the cut-list candidate JSON.
3. **Propose** *(top-tier, the creative step)* — Claude reads the transcript and candidates and produces an **edit decision document**: cuts to make (with reasons), segments flagged "keep despite silence" (laughs, beats), chapter points with titles, 3-5 shorts candidates with in/out points. **Show this to the user for approval before touching the timeline.** This is the seamlessness/safety tradeoff that the demos get wrong — cuts are cheap to propose, expensive to un-tangle.
4. **Execute** *(Sonnet-tier)* — apply the approved cut list via MCP tools (razor + ripple delete per span, close gaps), add chapter markers, save. Save a project copy first (`save_project_as` or file copy) — treat the bridge as capable of corrupting a project.
5. **Polish** *(mixed)* — apply Essential Sound/Enhance Speech preset to dialogue tracks via the bridge if the chosen server supports it; otherwise leave as a listed manual step. Insert intro/outro from a template project/MOGRT.
6. **Captions** — generate `.srt` from the transcript. **Known hard limit: no scripting API can create caption tracks** — the skill ends this stage with "drag `episode.srt` onto the timeline," the pipeline's one unavoidable manual step (besides review).
7. **Review gate** — user watches the cut in Premiere. Anything wrong → fix by hand or tell Claude ("restore the segment about X").
8. **Export** *(Haiku-tier)* — queue the YouTube master via `EncoderManager`/AME (or a watch folder); Auto Reframe sequences for approved shorts; export chapter list + show-notes draft as text.

### Phase 4 — hardening & iteration (ongoing)

- After each episode, append lessons to the skill (words the user always keeps, pacing preferences, intro timing) — same self-improving-loop pattern as the rest of this repo.
- Build the **OTIO fallback lane** the first time the bridge breaks (small Python script: cut-list JSON → `fcp_xml` via OpenTimelineIO; see research/03 §4 — cuts/placement/markers survive the import, effects don't).
- Watch **`mhadifilms/prpr`** (headless UXP bridge, CLI-first, created 2026-07) as the migration target when CEP finally sunsets (announced windows range Sept 2026–"several years"; see research/03 §2). The skill's stage structure survives a bridge swap — only stage 4's tool calls change.
- **Remotion lane (brand assets + shorts factory).** Once the core pipeline is stable, add [Remotion](https://www.remotion.dev/) (React-based programmatic video) for the template-shaped, data-driven graphics — *not* for editing the conversation itself, which stays in Premiere:
  - **Episode intros/title cards**: one React comp parameterized by episode number/guest/topic; Claude fills props from the transcript, renders MP4, imports via the bridge (pattern proven by MauricePutinas's brand-intro MCP tool, research/04).
  - **Lower thirds**: transparent overlays (ProRes 4444 / WebM alpha) dropped above the multicam track; restyled by editing code, versioned in git.
  - **Shorts renderer (the sleeper win)**: render approved vertical shorts *entirely outside Premiere* — crop/reframe the source clip and burn word-level animated captions with [`@remotion/captions`](https://www.remotion.dev/docs/captions), consuming the same word-timed transcript the pipeline already produces. Bypasses the Auto Reframe → caption → export loop; shorts become fully unattended.
  - Resources: [Remotion docs](https://www.remotion.dev/docs) · [templates gallery](https://www.remotion.dev/templates) (starting points for intro/lower-third comps) · license check: free for individuals and very small companies, paid company license beyond that ([terms](https://www.remotion.dev/license)).
  - Adobe-native alternative if branding is static: MOGRTs via Essential Graphics, or bulk variations via the Firefly **Dynamic Graphics Render API** (research/03 §6).

## 6. Skills to build (summary)

| Skill | Tier | Purpose |
|---|---|---|
| `podcast-audio-analysis` | Haiku (mechanical) | transcript + silence/filler candidates → JSON |
| `edit-podcast` | orchestrator | Phases: ingest → analyze → propose → execute → polish → captions → review → export |
| `podcast-shorts` (later) | mixed | from an edited episode: pick moments (top tier), then either Auto Reframe in Premiere or the Remotion shorts renderer (Haiku) — see Phase 4 Remotion lane |
| `podcast-shownotes` (later) | Sonnet | transcript → description, chapters, titles, social copy |
| `podcast-brand-assets` (later) | Sonnet | Remotion comps for intros/title cards/lower thirds, parameterized per episode; renders imported via the bridge |

## 7. Model-tiering policy (bake into every skill)

| Work | Tier |
|---|---|
| Transcription, silence detection, file wrangling, MCP tool execution, export queuing | **Haiku** subagents |
| Cut-list assembly, MCP execute stage, shownotes drafting | **Sonnet** subagents |
| Edit-decision judgment (what to keep), pacing, chapter/short selection, anything user-facing that requires taste | **top tier (Fable/Opus)** — main loop only |

Skills should spawn subagents with explicit model overrides for stages 1-2, 4, 8; only stage 3 (Propose) and user interaction stay at the top tier. This mirrors how this handoff itself was produced.

## 8. Risks & known limits (be upfront with the user)

1. **Caption tracks cannot be created by any scripting API** — `.srt` drag-in is permanent (until Adobe fixes it; UXP `CaptionTrack` class exists read-side, watch the changelog).
2. **CEP sunset** — the primary bridge is legacy tech with an uncertain removal date (Sept 2026 per one Adobe-adjacent doc, "several years" per Adobe's verbal guidance in Mar 2026). Mitigations: version pinning (§4.2), OTIO fallback lane, prpr migration path.
3. **Point-release fragility** — two of the top three servers had confirmed breakage on Premiere 26.3.0 in July 2026. Never auto-update Premiere mid-season; smoke-test after any update.
4. **Destructive operations** — bridges execute arbitrary script in the app. Always: save-as backup before Execute, small verified steps, Premiere's undo history as last resort. Prefer servers with dry-run/backup safety rails.
5. **eval-based bridges** run model-generated code inside Premiere — keep the MCP server local-only, review any server code before install (they're small Node projects).
6. **Ecosystem churn** — the recommended repos are snapshots of 2026-07-18. At Phase 0, spend 10 minutes re-checking stars/issues/last-push before committing to one.

## 9. Verification checklist (definition of done)

- [ ] Scratch-project smoke test passes: import, razor, ripple delete, marker, undo — all visually confirmed.
- [ ] `/edit-podcast` runs end-to-end on a **10-minute excerpt** of a real episode; user approves the proposed cut list; execute matches the approved list exactly (spot-check 5 cuts).
- [ ] Full episode pilot: wall-clock editing time measured vs the user's current baseline (target: mechanical pass < 30 min hands-on).
- [ ] Export lands a YouTube-ready master + `.srt` + chapter text file.
- [ ] `VERSIONS.md` records the pinned working combination.
- [ ] Kill-switch tested: bridge disconnected mid-run leaves the project openable and the pipeline resumable.

## 10. What NOT to do

- Don't build on **pymiere** (unmaintained since ~2023, CEP-dependent, untested on modern Premiere).
- Don't route through **Adobe's hosted "Adobe for Creativity" MCP** for editing (Express-tier depth; fine to keep for Firefly/stock tasks).
- Don't hand-edit **.prproj** files (undocumented gzip+XML with a non-standard header byte; corruption risk) — use FCP7 XML import instead.
- Don't chase the 1,000-tool repos by tool count — verified execution beats catalog size (see research/04 on ayushozha).
- Don't automate the Propose stage away. The human approval gate is the product, not a limitation.
