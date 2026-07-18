# Research 01 — Landscape: Claude ↔ Premiere Pro demos, projects & products

> Researched 2026-07-18 by a Haiku-tier subagent (web sweep). Raw evidence — no recommendations.
> Part of the [Premiere automation handoff](../HANDOFF.md).

## YouTube Videos/Demos (2025-2026)

| Title | Channel | Date | URL | Approach Summary |
|-------|---------|------|-----|------------------|
| I Tested Premiere Pro's MCP In Claude | AI Aidan | May 22, 2026 | https://www.youtube.com/watch?v=QSXyT2fJi2E | Live demo: Claude Code + 269-tool MCP server removes silence from 17-min video; reusable /auto-cut skill; shows full CEP bridge setup |
| I taught Claude how to use Premiere Pro and it's INSANE | Soroosh Hedayati | Apr 22, 2026 | https://www.youtube.com/watch?v=CK5per-3T5s | Live editing demo where Claude reads transcript only (no video), performs cuts, ripple deletes, silence removal, and gap closure automatically via Premiere DOM access |
| this Claude AI Premiere Pro Plugin changes EVERYTHING | ELEVEN PERCENT | May 20, 2026 | https://www.youtube.com/watch?v=2GFiPKRPQkU | AutoEdit plugin demo: Claude removes bad takes, repeats, silences; uses three-layer audio pipeline (RMS + Whisper + LLM); review before commit |
| How to use Claude AI to Edit your Content 10X Faster | ELEVEN PERCENT | Apr 10, 2026 | https://www.youtube.com/watch?v=ShDALXMWTqk | AutoEdit Creator Mode: three edit modes (Standard/Brain/Beast); detects filler, bad takes; applies cuts natively in Premiere |
| Claude AI Now Edits My Videos in Premiere Pro (Full Tutorial) | ELEVEN PERCENT | May 27, 2026 | https://www.youtube.com/watch?v=kvK8y3rI028 | AutoEdit + Claude: talking-head workflow, transcript analysis, auto-captions, rough cuts in seconds |
| Claude + Premiere Pro make pro plugins in seconds | AKV Studios | Jun 8, 2026 | https://www.youtube.com/watch?v=plVstfuasbM | Claude itself builds a Premiere Pro plugin (PR Flow); no developer needed; builds professional UXP/CEP panels |
| How to Edit 10X Faster With Claude AI in Premiere Pro | ELEVEN PERCENT | May 22, 2026 | https://www.youtube.com/watch?v=kk8MKhPJxQE | AutoEdit: contextual AI editing, repeat detection, silence trimming, automated captions |
| This Free Claude AI Plugin can edit YouTube Videos NOW | ELEVEN PERCENT | Apr 17, 2026 | https://www.youtube.com/watch?v=WJp07ZtVUlo | AutoEdit free trial: removes bad takes, repeats, filler; prompt-guided editing; marker + topic detection |
| How to Setup Claude AI in Premiere Pro | George Pags | Apr 18, 2026 | https://www.youtube.com/watch?v=UMNvF8vQ4_c | Step-by-step Windows setup: clone MCP repo, registry edits, CEP extension install, Claude Desktop config, direct live demo |

## Open-Source MCP Servers & Projects (2025-2026)

| Project | Date | Stars | Tools | Bridge Tech | Summary |
|---------|------|-------|-------|-------------|---------|
| [MauricePutinas/premiere-pro-mcp-claude-code](https://github.com/MauricePutinas/premiere-pro-mcp-claude-code) | Jun 21, 2026 | — | 59 | CEP HTTP bridge + Remotion | One-click `.mcpb` desktop extension; cinematic intros (4 styles), beat-cut editing, keyframes; includes synthesized SFX; Windows + Premiere 2025 |
| [nepfaff/premiere-pro-mcp](https://github.com/nepfaff/premiere-pro-mcp) | Feb 9, 2026 | 3 | 1 (`execute-script`) | UXP API + file polling | Minimalist: single tool generates arbitrary JS on-the-fly against UXP API; command/result JSON files bridge; macOS Premiere 2025+ |
| [Maciejdziuba/premiere-pro-mcp](https://github.com/Maciejdziuba/premiere-pro-mcp) | Jun 27, 2026 | — | 319 | CEP/ExtendScript + QE DOM | Comprehensive fork; undocumented QE DOM access; Whisper transcription, waveform silence mapping, retake grouping; two LLM context resources (config + ExtendScript reference) |
| [leancoderkavy/premiere-pro-mcp](https://github.com/leancoderkavy/premiere-pro-mcp) | — | — | 269 | CEP 12 + ExtendScript | Flagship open-source; covers Premiere 2020–2025+; ripple deletes, effects by name, keystoning; atomic command execution via UUID temp directory |
| [nguyenph88/Media-Editor-MCP](https://github.com/nguyenph88/Media-Editor-MCP) | Jun 9, 2026 | — | 21 (Premiere) + 8 (analysis) | Node MCP + UXP plugin + WebSocket | Two-server monorepo: Premiere Pro + media-analysis (beat detection, Whisper, SRT, best-moments ranking); orchestrated via Claude conversation; includes CapCut server |
| [kemerd/premiere-agent](https://github.com/kemerd/premiere-agent) | Apr 26, 2026 | 13 | — | XML export only | Claude Code / Codex only (no MCP); 100% offline; exports `.fcpxml` + `.xml` + `.srt` back to NLE; three perception lanes (Parakeet ONNX speech, Florence-2 vision, CLAP audio events); no cloud, no frame-dumping |
| [koptsev63/premiere-claude-bridge](https://github.com/koptsev63/premiere-claude-bridge) | May 4, 2026 | — | 15+ (with `/watch` skill) | CEP ExtendScript + Python analysis | Built by film director; Walter Murch's "Blink of an Eye" editing heuristics baked in; local Whisper/Groq/OpenAI backends for transcription; Resolve support roadmap |
| [antipaster/Adobe-Premiere-Pro-MCP](https://github.com/antipaster/Adobe-Premiere-Pro-MCP) | Mar 5, 2026 | — | 170+ | Node.js MCP + WebSocket + CEP | Oldest widely-adopted fork; includes ElevenLabs TTS voiceover; configurable; auto-installer for Windows |
| [jordanl61/premiere-pro-mcp-server](https://github.com/jordanl61/premiere-pro-mcp-server) | — | — | 20+ | CEP bridge | Focuses on read/write primitives: trim clips, get/set clip params, sequence details, markers |
| [matrayu/adobe-mcp](https://github.com/matrayu/adobe-mcp) | Jan 17, 2026 | — | Multi-app | UXP + WebSocket proxy | Unified server: Photoshop, Premiere Pro, Illustrator, InDesign; Python MCP + Node proxy; cross-platform |
| [Nate-valerian/claude-ai-mcp-bridge](https://github.com/Nate-valerian/claude-ai-mcp-bridge) | May 18, 2026 | — | 40 (Premiere) + 30 (AE) | CEP WebSocket bridge | Dual Adobe: Premiere Pro + After Effects; includes AI auto-edit, highlight detection, color grading, beat sync, face-tracking zoom |
| [Robelob/Ambar-AI-Video-Editor-Plugin-For-Premiere-Pro](https://github.com/Robelob/Ambar-AI-Video-Editor-Plugin-For-Premiere-Pro) | May 12, 2026 | 3 | 4 panels | UXP + CEP hybrid | Ambar vlog editor: silence detection, B-roll auto-placement, caption generation, bin organization; RMS + Whisper + LLM pipeline; no cloud uploads |
| [morim3/mcp_adobe_premiere](https://github.com/morim3/mcp_adobe_premiere) | — | — | — | Python FastMCP + UXP | Minimal Python-based MCP; uses Premiere Beta 25.3+; UXP Developer Tool required to load plugin |
| [ayushozha/AdobePremiereProMCP](https://github.com/ayushozha/AdobePremiereProMCP) | — | — | 1,027 claimed | CEP/ExtendScript | Claims most comprehensive: timeline editing, color grading, audio mixing, effects, export, graphics |
| [hetpatel-11/Adobe_Premiere_Pro_MCP](https://github.com/hetpatel-11/Adobe_Premiere_Pro_MCP) | — | — | 278 | CEP bridge | Active repository; widely recommended |

## Commercial/Hosted Products

| Product | URL | Type | Launch | Bridge | Note |
|---------|-----|------|--------|--------|------|
| **AutoEdit** | https://www.autoeditai.net | Premiere Pro plugin | 2026 (Product Hunt May 29) | Native UXP + Claude API | One-click inside Premiere; removes bad takes, repeats, silences, filler words; auto-captions; three modes (Standard/Brain/Beast); 15,000+ editors |
| **PremiereCopilot** | https://www.premierecopilot.com/en/claude-cut | Native Premiere plugin | 2026 | Direct Premiere API | Pick Claude (Anthropic) in model selector; native timeline operations; review before apply; 2-minute setup |
| **Jumper** | https://getjumper.io/ai-agents | Multi-NLE MCP server | Mar 9, 2026 | MCP local server | Works with Premiere, Resolve, Final Cut Pro, Avid; visual search, transcript search, face search; media stays local; one-click Claude Desktop/Claude Code/Codex integration |
| **viaSocket MCP** | https://viasocket.com/mcp/adobe-premiere-pro | MCP bridge (hosted) | 2026 | HTTP MCP endpoint | Connects Premiere to ChatGPT, Claude, Cursor; cloud-hosted endpoint; handles auth + API limits |

## Blog Posts & Tutorials (2025-2026)

| Title | Source | Date | URL | Key Takeaway |
|-------|--------|------|-----|--------------|
| How to Use Claude AI in Premiere Pro (2026): The Complete Guide | PremiereCopilot Blog | Jun 8, 2026 | https://www.premierecopilot.com/en/blog/how-to-use-claude-ai-in-premiere-pro | Three connection methods compared: native plugin (easiest), MCP/UXP (developer route), copy-paste (manual); 5-min setup for plugin; plain-English prompts |
| Claude MCP for Adobe vs Photoshop/Premiere | MindStudio | 2026 | https://www.mindstudio.ai/blog/claude-mcp-adobe-vs-photoshop-premiere-what-it-does | MCP = backend computer-to-computer; Claude talks to app API layer directly (not screen automation); native undoable edits |
| Can Claude + Premiere Pro MCP Search Your Footage? | Heimdex | 2026 | https://blog.heimdex.co/can-claude-premiere-pro-mcp-search-your-footage-what-it-actually-does-at-scale/ | Newer MCPs add search: Whisper transcription + Claude Vision on sampled frames; jump to matching moments; at-scale testing |
| How to Use Claude AI with Premiere Pro and CapCut | ToolAIPilot | 2026 | https://toolaipilot.com/blog/how-to-use-claude-ai-with-premiere-pro-and-capcut | Multi-editor perspective: Premiere MCP + CapCut offline editing |

## Common Patterns: Bridge Technologies

1. **CEP + ExtendScript + WebSocket** (most mature, 2025-2026 dominant)
   - MCP server (Node/Python) → WebSocket → CEP panel → `CSInterface.evalScript()` → Premiere DOM + QE DOM
   - Examples: antipaster, Maciejdziuba, leancoderkavy, Robelob (hybrid)
   - Advantage: deepest API access, undocumented QE DOM for effects/ripple-delete
   - Limitation: CEP is Adobe's legacy; QE DOM officially unsupported

2. **UXP + Direct API + File Polling** (newer, emerging 2026)
   - MCP server writes command JSON → UXP plugin polls → `eval()` in UXP context → Premiere UXP API
   - Examples: nepfaff, morim3
   - Advantage: modern Adobe direction; no CEP debug-mode hassle
   - Limitation: UXP API smaller than ExtendScript; can't access QE DOM

3. **Hybrid UXP + CEP** (best-of-both, May 2026+)
   - UXP panel for timeline operations + CEP panel for ExtendScript/QE work
   - Examples: Robelob (Ambar), Maciejdziuba (dual panels)

4. **XML-Only Export** (offline-first)
   - 100% local, no bridge: Claude outputs `.fcpxml` / `.xml` → user imports to NLE
   - Examples: kemerd/premiere-agent
   - Advantage: zero Premiere API coupling; works with any NLE
   - Limitation: one-way flow; no live timeline feedback

5. **HTTP Local Server Inside Premiere** (CEP bridge variant, emerging 2026)
   - CEP panel spins up HTTP server on `127.0.0.1:3030` → MCP server talks HTTP
   - Examples: MauricePutinas (with Remotion + sound design)

## Trend Summary

- **2025:** MCP servers proliferate on GitHub (CEP-based, open-source); first commercial plugin (AutoEdit) beta testing.
- **2026 (so far):** Native plugins ship (AutoEdit, PremiereCopilot); UXP pilots launch; hybrid UXP+CEP approach stabilizes; beat-synced auto-edit + cinematic intro generators enter mainstream.
- **No official Adobe Claude connector for desktop Premiere:** Adobe's "Creative Cloud connector" and "AI marketing agent" work only with Adobe Express (web), not desktop Premiere. All working solutions are community-built or third-party plugins.
