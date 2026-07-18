# Research 04 — MCP servers & agent bridges for Premiere: evaluation

> Researched 2026-07-18 by a Sonnet-tier subagent (GitHub/web deep-dive). Raw evidence with maintenance signals; star/issue counts are a snapshot of 2026-07-18 in a fast-moving space.
> Part of the [Premiere automation handoff](../HANDOFF.md).

## 1. Official Adobe Effort

### Adobe for Creativity (official remote MCP connector)
- Endpoint: `https://adobe-creativity.adobe.io/mcp` · https://developer.adobe.com/adobe-for-creativity/
- Hosted **remote** MCP server, Streamable HTTP, OAuth against an Adobe account. Register: `claude mcp add adobe-creativity --transport http https://adobe-creativity.adobe.io/mcp`
- Marketed as covering Photoshop, Lightroom, Illustrator, Firefly, Premiere, Express, InDesign, Stock — "50+ tools."
- **Caveat (independent test, MindStudio May 2026):** actually operates at the **Adobe Express level**, not the professional Premiere API layer — a 9:16 reframe took 3m14s and mis-centered; white balance underperformed a 13-second manual slider. Not a scripting-level Premiere bridge today. https://www.mindstudio.ai/blog/claude-mcp-adobe-vs-photoshop-premiere-what-it-does
- Adobe Express Developer MCP (`@adobe/express-developer-mcp`) is dev-tooling for Express add-ons — unrelated to Premiere control. Firefly Services MCP exposes generative APIs — tangential.

## 2. Community/Open-Source Servers — ranked by maintenance signal

### mikechambers/adb-mcp — most established
- https://github.com/mikechambers/adb-mcp — 660★, 93 forks, last push 2026-07-08, v0.85.4. "Not endorsed by nor supported by Adobe — proof of concept."
- Architecture: `AI ⇄ MCP Server (Python) ⇄ Node command-proxy (WebSocket) ⇄ UXP plugin ⇄ app` (proxy needed because UXP plugins can only dial out).
- Premiere agent explicitly "more limited than the Photoshop agent, due to current limitations of the Premiere plugin API." Capabilities: create projects, populate with clips/transitions/effects/audio.
- Requires UXP Developer Tool, Node, Python 3, Premiere Beta 25.3+. macOS + Windows.
- Sampled open issues: Illustrator not loading on Windows (#31), UI crash (#8), `spawn uv ENOENT` (#5), `get_project_info` broken (#21).

### hetpatel-11/Adobe_Premiere_Pro_MCP — largest verified tool catalog, very active
- https://github.com/hetpatel-11/Adobe_Premiere_Pro_MCP — ~353–367★ (growing during research), 67 forks, last push 2026-07-07, MIT, 6 contributors.
- Architecture: CEP bridge panel ↔ MCP server over shared temp dir (`/tmp/premiere-mcp-bridge`) with polling.
- **278 tools**; author states 197 live-executed against a real Premiere 2026 session, 57 schema-validated, 3 destructive no-arg tools intentionally skipped in verification.
- Categories: project setup, ingest, bins, sequences, timeline editing, transitions, effects, keyframes, captions, markers, metadata, proxies, multicam, color, audio, exports, plus high-level assembly tools (`assemble_product_spot`, `build_brand_spot_from_mogrt_and_assets` with LLM-directed `clipPlan`).
- Ships an installable Agent Skill: `npx skills add hetpatel-11/Adobe_Premiere_Pro_MCP --skill premiere-pro-mcp` — teaches the agent to install/verify/operate the bridge itself.
- **Validated on macOS only**; Premiere 2020+ (tested 26.0); Node 18+.
- Flags: issue-tracker metadata inconsistency (5 open issues reported, list not publicly visible); author pivoting to **Monet** (https://github.com/Monet-AI-Editor/Monet), "an AI-first video editor designed for full coding-agent control" — signal that the author sees CEP bridging as a workaround, not a long-term solution. Most-copied template in the space (many 0-star clones).

### leancoderkavy/premiere-pro-mcp — well-documented, npm-published, QE DOM
- https://github.com/leancoderkavy/premiere-pro-mcp (npm `premiere-pro-mcp`) — 86–123★, last push 2026-07-18, MIT.
- Architecture: `LLM → MCP server (Node, stdio) → .jsx command file in shared temp dir → CEP plugin polls, CSInterface.evalScript() → response file`.
- **269 tools / 28 modules**; uses the **undocumented QE DOM** (`app.enableQE()`) for ripple delete, roll/slide/slip, move-clip-to-track, speed/reverse, effects by exact name. States plainly: "UXP in Premiere Pro is still maturing and lacks equivalent API coverage" — why they chose CEP.
- Premiere 2020–2025+; install via `npm install -g premiere-pro-mcp` + CEP plugin symlink + debug-mode registry/plist edits (CSXS 9–14).
- Known issue #9 (Jul 4, 2026): `capture_frame`/`export_frame` broken on Premiere 2025 & 2026 (wrong QE object + silent false success).
- Windows rough edges: community patch repo `takeyama88/premiere-pro-mcp-windows-fix` (self-signing script for CEP 12).

### antipaster/Adobe-Premiere-Pro-MCP — Windows-focused
- https://github.com/antipaster/Adobe-Premiere-Pro-MCP — 26★, last push 2026-07-15, 170+ tools.
- `LLM ←→ Node MCP ←→ WebSocket ←→ CEP Panel ←→ ExtendScript`. **Windows only**, Premiere 2023+, tested 2026. `install.bat` enables unsigned CEP, symlinks panel, builds.
- Issue #4 (Jul 16, 2026, "with fix"): all `evalScript` calls fail on **Premiere 26.3.0** (ScriptPath wedges the engine) — active triage, but confirms fragility against point releases.

### nguyenph88 Premiere-Pro-MCP / Media-Editor-MCP — dual-server, podcast/reel-relevant analysis tools
- https://github.com/nguyenph88/Media-Editor-MCP (monorepo; also standalone `nguyenph88/Premiere-Pro-MCP`).
- **Two cooperating MCP servers**: `premiere-pro` (Node → UXP plugin via WebSocket :3001) + `media-analysis` (Python/uv: `beat_this` beat detection, `faster-whisper` transcription, SRT generation, `find_best_moments` ranking by motion/sharpness/faces/exposure). Claude orchestrates: analysis returns data, Claude decides, editing primitives execute.
- Windows verified / macOS; Node ≥20; **Premiere 25.6+** (verified to 26.2.2); requires UXP Developer Tools.
- Claude Code registration: `claude mcp add premiere-pro -- node "<repo>\packages\server\dist\index.js"` (+ second server via `uv run`).
- Ships `.claude/skills/` slash commands: `/pp-create-reel`, `/pp-lyric-reel`, `/pp-mark-beats`, `/pp-add-cross-dissolve` — encode editorial heuristics.
- **Explicit limitation:** "the one manual step — Premiere's plugin API can't create caption tracks" — transcripts must be exported `.srt` and manually dragged in.

### nepfaff/premiere-pro-mcp — minimalist raw-JS execution
- https://github.com/nepfaff/premiere-pro-mcp — 3★, dormant since 2026-02-10.
- **One tool** (`execute-script`): LLM generates arbitrary JS against the full UXP API. Bridge: JSON command files in `~/Documents/ppro-mcp-bridge/`, UXP plugin polls and `eval()`s (`allowCodeGenerationFromStrings: true` — real security consideration).
- macOS confirmed, Windows untested; Premiere 25.3+; UXP Developer Tool must stay open (plugin unloads when UDT closes; reload every Premiere restart).

### mhadifilms/prpr — CLI-first, headless UXP bridge, cleanest architecture
- https://github.com/mhadifilms/prpr · docs https://mhadifilms.github.io/prpr/ — brand new (created 2026-07-10), 4 releases, MIT. Sibling of `mhadifilms/dvr` (DaVinci Resolve).
- **CLI + typed Python library + MCP server** on the same operations. Inverted bridge: prpr **hosts** `ws://127.0.0.1:8855`; a **headless** UXP plugin (no panel, auto-starts with Premiere) dials in — no visible panel, no file-polling latency.
- Install: `pip install prpr` → `prpr plugin install` (Adobe's official installer) → restart Premiere → `prpr doctor --probe`.
- `prpr timeline inspect` returns structured JSON (fps, duration, frame size, per-track clips, markers). No community track record yet — worth tracking.

### Others (lower signal)
- **ayushozha/AdobePremiereProMCP** — 1,027 *claimed* tools, single contributor, dormant since 2026-03-19; community issue literally asks whether it's been tested against real Premiere. Treat with skepticism.
- **morim3/mcp_adobe_premiere** — Python FastMCP + UXP (TS); Premiere Beta 25.3+; maintenance unverified.
- **stewberticus/adobe-mcp** (stale) → superseded by author's Rust rewrite **David-Martel/adobe-controller** (not deep-dived).
- **CodeBuffalo0225/claude-ai-mcp-bridge** — dual Premiere (40+ tools) + After Effects (30+); CEP; small.
- **MauricePutinas/premiere-pro-mcp-claude-code** — 59 tools, only **`.mcpb` one-click desktop-extension** packaging found; CEP HTTP bridge (:3030, pymiere-style); Windows + Premiere 25.5.0 pin; Remotion-based brand intros, beat-cut via ffmpeg+numpy; ships `safety.ts` (allowlist, dry-run, automatic backups before destructive ops). `claude mcp add premiere -- node "C:\path\to\Premiere-MCP\dist\index.js"`.
- Recently created, unproven (metadata only): BEMBOOMER/premiere-mcp-bridge (2026-07-17), Siddhant704/premiere-pro-mcp, CaYatur/PremiereProMCP (UXP-first, CEP only for titles), shipshitshow/premiere ("frame-accurate transcript editing... every cut verified for A/V sync"), koptsev63/premiere-claude-bridge (Walter Murch heuristics; 7 open issues), saichandan112/FORGE, sylphiette269/premiere-mcp-editor-cn, ygtec/cut.skill (CapCut+Premiere), matrayu/adobe-mcp.

## 3. Cross-Cutting Architecture Patterns

Premiere has **no first-party REST API, CLI, or scripting socket**, so every bridge is one of:

1. **CEP + ExtendScript** — older, more capable; only way to reach the **QE DOM** (ripple deletes, roll/slip/slide, effects by name). Used by leancoderkavy, hetpatel-11, antipaster, MauricePutinas, and most others. Multiple READMEs: UXP "still maturing and lacks equivalent API coverage" in Premiere specifically.
2. **UXP** — Adobe's future; UXP plugins can only make *outbound* connections, so bridges need (a) a proxy/relay (adb-mcp), (b) file-polling (nepfaff, morim3), or (c) an inverted socket where the server hosts and the plugin dials in (prpr — cleanest).

**Universal limitation:** caption/subtitle **track creation is impossible via either scripting API** — transcripts must be exported `.srt` and manually dragged into Premiere.

**Common installation friction:** unsigned/debug-mode CEP enabling (registry / `defaults write com.adobe.CSXS.*`), CSXS version mismatches, and breakage on new Premiere point releases (leancoderkavy #9; antipaster #4 on 26.3.0). These bridges are fragile against Adobe's update cadence — pin versions, re-verify after updates.

## 4. Registering an MCP server with Claude Code

(Source: https://code.claude.com/docs/en/mcp, cross-checked against project READMEs)

- **Local** (default, private): `claude mcp add <name> -- <command> [args...]` → `~/.claude.json`
- **Project** (shared via source control): `claude mcp add <name> --scope project -- <command> [args...]` → `.mcp.json` at project root (approval prompt on first use)
- **User/Global**: available across projects.
- **Remote HTTP**: `claude mcp add adobe-creativity --transport http https://adobe-creativity.adobe.io/mcp`
- **Stdio** (every community Premiere bridge): `claude mcp add premiere -- node "/path/to/dist/index.js"`, env via `-e KEY=value`; or `claude mcp add-json` with a full config block.

Typical `.mcp.json` shape:

```json
{
  "mcpServers": {
    "premiere-pro": {
      "command": "node",
      "args": ["/absolute/path/to/premiere-pro-mcp/dist/index.js"],
      "env": { "PREMIERE_TEMP_DIR": "/tmp/premiere-mcp-bridge" }
    }
  }
}
```

## 5. Summary Table

| Project | Stars | Last Push | Bridge | Tools | Platform | Key Limitation |
|---|---|---|---|---|---|---|
| Adobe for Creativity (official) | N/A | live | Remote HTTP OAuth | ~50 cross-app | any | Express-tier depth, not pro Premiere control |
| mikechambers/adb-mcp | 660 | 2026-07-08 | UXP + Node proxy | unspecified | macOS/Win | Premiere agent limited vs Photoshop |
| hetpatel-11/Adobe_Premiere_Pro_MCP | ~360 | 2026-07-07 | CEP/ExtendScript | 278 | macOS only | author pivoting to Monet |
| leancoderkavy/premiere-pro-mcp | ~100 | 2026-07-18 | CEP + QE DOM | 269 | macOS/Win* | frame capture broken; Win needs patch |
| ayushozha/AdobePremiereProMCP | ~50 | dormant | CEP | 1,027 claimed | 2020–2026 | real-world testing unconfirmed |
| antipaster/Adobe-Premiere-Pro-MCP | 26 | 2026-07-15 | CEP/WS | 170+ | Windows only | evalScript broken on 26.3.0 (fix identified) |
| nguyenph88/Premiere-Pro-MCP | low | 2026-06-07 | UXP + WS dual server | 21 + 9 | Win verified/macOS | no caption-track creation |
| nepfaff/premiere-pro-mcp | 3 | dormant | UXP file-polling | 1 (unbounded) | macOS | eval() of AI code; UDT must stay open |
| mhadifilms/prpr | 0 (new) | 2026-07-11 | UXP headless inverted socket | CLI+lib+MCP | unspecified | no track record |
| MauricePutinas/premiere-pro-mcp-claude-code | 0 | 2026-06-21 | CEP HTTP + Remotion | 59 | Win, PPro 25.5 pin | narrow version pin |

**Unresolved/flagged:** Adobe's official connector depth for Premiere is disputed; star/issue counts moved during research (fast-moving space); hetpatel-11 issue-tracker inconsistency unresolved; several new repos unverified beyond metadata.
