# Research 03 — Adobe Premiere automation surfaces: technical map

> Researched 2026-07-18 by a Sonnet-tier subagent (technical deep-dive). Raw evidence — no recommendations.
> Part of the [Premiere automation handoff](../HANDOFF.md).

Note on naming: Adobe rebranded "Premiere Pro" → **"Premiere"** at the v26.0 launch (Jan 20, 2026). Current shipping version referenced in Adobe's changelog is **26.3.0**.

## 1. UXP Scripting for Premiere

**Status: Supported, current/primary path (GA).**

- Public beta Dec 5, 2024; **GA in Premiere v25.6 (announced Dec 1, 2025)**. [Adobe Tech Blog](https://blog.developer.adobe.com/en/publish/2025/12/uxp-arrives-in-premiere-a-new-era-for-plugin-development)
- Only Premiere **v25.6+** supports UXP plugins.
- Toolchain: **UXP Developer Tool (UDT) v2.2.1+** via Creative Cloud Desktop — scaffolds, live-loads, debugs.
- Runtime: `const app = require('premierepro')`; static classes rather than ExtendScript's global `app` tree.
- Docs: https://developer.adobe.com/premiere-pro/uxp/ · API reference: https://developer.adobe.com/premiere-pro/uxp/ppro-reference/classes/ · Changelog: https://developer.adobe.com/premiere-pro/uxp/changelog/ · Samples: https://github.com/AdobeDocs/uxp-premiere-pro-samples · Types: https://github.com/adobe/premierepro-types, npm `@adobe/premierepro` (observed v26.3.0)

**API coverage** (confirmed classes, 26.3 `types.d.ts`): `Project`, `Sequence`, `SequenceEditor`, `SequenceSettings`, `SequenceUtils`, `VideoTrack`/`AudioTrack`/`CaptionTrack`, `VideoClipTrackItem`/`AudioClipTrackItem`, `TrackItemSelection`, `Marker`/`Markers`, `Metadata`, `Keyframe`, `VideoFilterComponent`/`AudioFilterComponent`/`*ComponentChain`/`*FilterFactory`, `VideoTransition`/`TransitionFactory`, `SourceMonitor`, `ProjectItem`/`ClipProjectItem`/`FolderItem`, `ProjectConverter` (incl. `exportAAF`, 26.3), `Exporter`, `EncoderManager`, `Transcript`, `EventManager`, `ProjectUtils`, `TickTime`/`FrameRate`, `Properties`, `Guid`, `Constants`.

- **Can do**: get/set active project & sequence; create sequences (incl. from media or preset); import media/AE comps; enumerate/edit track items; add markers with unique `guid` (26.3); read/set effect params via component chains; transitions; keyframes; Source Monitor control; transcript queries (`hasTranscript`, `querySupportedLanguages`, transcription functions in 26.3); push renders into AME (`EncoderManager.launchEncoder`, `startBatchEncode` — 26.3); export still frames (`Exporter.exportSequenceFrame` — image formats only, not video); export sequences via `EncoderManager.exportSequence()` (routes through AME); AAF export (26.3).
- **Cannot / limitations**: everything is **async (Promises)** — deliberate break from ExtendScript's synchronous model. 26.3 breaking changes: `create*Action` must run inside `project.lockedAccess(() => {...})`; `Sequence.setSelection` became synchronous. Adobe ships `@adobe/eslint-plugin-premierepro` to catch misuse. No frame-accurate video render API outside AME. Hyper Brew (Mar 2026): "most APIs are stable, some are still missing" vs full ExtendScript/QE parity. [Hyper Brew: UXP Plugins in Premiere 2026](https://hyperbrew.co/blog/uxp-plugins-in-premiere-2026/)
- UXP supports **C++ Hybrid plugins** (native compute) — impossible in CEP.
- First-class TypeScript support via `@adobe/premierepro` type defs.
- Entry barrier: moderate — Premiere 25.6+, UDT, JS/TS + npm.

## 2. ExtendScript (.jsx) + CEP Panels

**Status: Supported but sunsetting — timelines inconsistent across Adobe's own sources.**

- As of Premiere 25.6, CEP is officially "superseded by" UXP. Community-maintained scripting guide: *"ExtendScript-based integrations are still supported... through **September 2026**."* [ppro-scripting.docsforadobe.dev](https://ppro-scripting.docsforadobe.dev/)
- Adobe's stated CEP policy: support both for a calendar year from UXP GA (Dec 2025) → implying ~Dec 2026 removal.
- **However** Hyper Brew (Mar 31, 2026) reports Adobe saying CEP has "several years" left, declining a hard date, while urging migration now.
- **Verified**: CEP panels still load and ExtendScript still runs in Premiere as of mid-2026. **CEP 12 is the last major CEP version** — security patches only. Adobe: "if you are starting new development, start in UXP."
- **QE DOM** (`qe` object via `app.enableQE()`): internal, undocumented DOM built for Adobe's own automated testing. Officially unsupported. Fills real gaps: apply effect to clip by name (`QETrackItem.addVideoEffect()`), ripple deletes, advanced trims, razor/cut, clip `move()` by timecode. Introspectable via `qe.reflect.methods`. Dies when ExtendScript/CEP is removed; no announced 1:1 UXP replacement (though some capabilities — effects-by-name via component chains — now covered).
- Refs: [Adobe-CEP/Samples PProPanel](https://github.com/Adobe-CEP/Samples/blob/master/PProPanel/ReadMe.md) · [Premiere Pro Scripting Guide](https://ppro-scripting.docsforadobe.dev/) · [QE DOM community thread](https://community.adobe.com/questions-729/what-is-qe-dom-in-premiere-pro-1364808)
- Entry barrier: low — plain JS-like syntax, HTML/CSS/JS panel + manifest, well-trodden ZXP tooling.

## 3. pymiere (Python, qmasingarbe)

**Status: Unmaintained (explicit upstream warning); at risk from CEP sunset.**

- https://github.com/qmasingarbe/pymiere — 470 stars, GPLv3, created 2019.
- README verbatim: *"Pymiere is not maintained anymore. It should still work fine but some newer part of the Premiere pro api may not be wrapped."*
- Bridges via a CEP panel ("Pymiere Link" `.zxp`); Python mirrors the ExtendScript object model 1:1 including `pymiere.objects.qe.*` (QE DOM).
- Tested against Premiere 23.1 and older only; **no evidence of 24.x/25.x/26.x testing**.
- pymiere's own README recommends XML/OpenTimelineIO timeline generation + import for pure project-generation use cases.

## 4. File-Level Manipulation (.prproj, FCP XML, EDL, OTIO)

**Status: .prproj unofficial/reverse-engineered; FCP7-XML/EDL officially supported import/export; partial-fidelity round-trips.**

- **.prproj**: gzip-compressed XML with a **non-standard OS byte (`0x13`) at gzip header offset 9** — naive re-gzip may produce a file Premiere refuses unless the byte is preserved. Content: bins, sequences, clips, effect params, markers cross-referenced by `ObjectID`/`ObjectRef`. Undocumented; community-reverse-engineered. Refs: [PyPremiere format notes](https://github.com/ArnoXiang/PyPremiere_L10n_Tools/blob/main/Adobe_Premiere_Pro_Project_File_Format.md) · [PRPROJ-READER](https://github.com/sergeiventurinov/PRPROJ-READER) · [fileformats wiki](http://fileformats.archiveteam.org/wiki/Premiere_Pro)
- **Build a timeline outside Premiere and import it? Yes.**
  - Premiere's "Final Cut Pro XML" import/export uses the **legacy FCP7 `xmeml` schema** (not modern FCPXML). [Adobe help](https://helpx.adobe.com/premiere/desktop/render-and-export/export-files/export-a-project-as-a-final-cut-pro-xml-file.html)
  - **OpenTimelineIO's Premiere path is its `fcp_xml` adapter** (same xmeml generation).
  - **EDL (CMX3600)** via `otio-cmx3600-adapter` with an explicit `"premiere"` style; most limited: 1 video track + 2 stereo audio, no nesting, frame rate passed explicitly, 8-char reel names. [Adapter README](https://github.com/OpenTimelineIO/otio-cmx3600-adapter/blob/main/README.md)
  - **What survives**: cuts, clip placement, timecodes reliably; **markers** convert reasonably ([Marker Converter](https://editingtools.io/marker/) exists for OTIO↔Premiere). **Effects/transitions are lossy** (OTIO warns on import). **Audio levels/gain keyframes: unverified/likely partial.**
  - Practical: generating FCP7-XML and importing via File > Import is a documented, script-friendly way to construct a rough-cut timeline (clips + cuts + markers) with zero plugin install — but not for effects/transitions round-trips.

## 5. Premiere Transcript Access (Text-Based Editing)

- **Source of truth lives inside the `.prproj`** once transcription/editing has occurred — not a standalone sidecar. [Community thread](https://community.adobe.com/t5/premiere-pro-discussions/where-are-the-transcribed-transcription-files-stored/td-p/13964047)
- **`.prmi` sidecars** = Media Analysis *cache* only; transcript edits are NOT synced back — unreliable as a read path.
- **Export/interchange**:
  - **`.prtranscript`** — native container, round-trips word-level timing + speaker labels. [Docs](https://helpx.adobe.com/premiere/desktop/render-and-export/export-files/export-transcripts.html)
  - **Transcript JSON spec** — Adobe-published schema (Aug 2025 beta, "Import Your Own Transcript") with word-level timecodes, explicitly meant for third-party tools to generate transcripts for Text-Based Editing/captioning. Adobe suggests using an LLM to convert arbitrary formats into this JSON. [Announcement + spec](https://community.adobe.com/announcements-732/now-in-beta-import-your-own-transcript-311910)
- **Scripted access**: UXP `Transcript` class (`hasTranscript()`, `querySupportedLanguages()`, transcription functions in 26.3) is the documented programmatic path while a project is open.

## 6. Adobe Official APIs/SDKs (native, cloud, agentic)

- **Premiere Plugin SDK (C++)** — GPU effects/transitions, format import/export; unaffected by CEP→UXP. [ppro-plugins.docsforadobe.dev](https://ppro-plugins.docsforadobe.dev/)
- **Firefly Services Audio/Video APIs** — cloud REST, async job model. [Docs](https://developer.adobe.com/audio-video-firefly-services/). Confirmed endpoints: **Dynamic Graphics Render API** (render MOGRT variations, up to 500/call), **Reframe API**, **Translate & Lip-Sync (TLS) API**, **Text-to-Speech**, **Text-to-Avatar**.
- **Adobe MAX 2025 (Oct 2025)**: **Project Moonlight** — conversational/agentic Firefly interface operating across Adobe apps incl. Premiere; as of July 2026 a product-level preview, **not a third-party-callable API**. AI Assistants public beta in CC apps. **AI Object Mask** in Premiere (public beta) — scriptable via new UXP `ObjectMaskUtils` (26.3). Firefly Custom Models; multi-model marketplace.
- **No evidence** of a public API to drive Premiere through Moonlight/Firefly Assistant as of July 2026.

## 7. Media Encoder Automation

- **CLI**: `"Adobe Media Encoder.exe" --console es.executeScript "script.jsx"` — cannot pipe commands into a running instance; fire-and-relaunch only. [Thread](https://community.adobe.com/t5/adobe-media-encoder-discussions/current-media-encoder-automation-from-command-line-information/td-p/13110808)
- **Watch Folders**: native no-code automation (folder + preset → auto-encode); still supported in 2026; no subfolder recursion.
- **ExtendScript API**: [ame-scripting.docsforadobe.dev](https://ame-scripting.docsforadobe.dev/) — queue/encoder/preset/output objects; same sunset concerns as §2.
- **AME UXP API** (newer, thin): [developer.adobe.com/media-encoder/uxp/api/](https://developer.adobe.com/media-encoder/uxp/api/) — `stitchFiles()`, queue `start()`/`stop()`, `RenderOptions.setSequenceGUID()` + `getProjectItemGUIDs()` to **render a sequence from a `.prproj` by GUID without opening Premiere's UI**, progress polling.
- **Cross-app**: Premiere 26.3's UXP `EncoderManager` pushes jobs directly into AME's queue — the two UXP surfaces are designed to pair.
