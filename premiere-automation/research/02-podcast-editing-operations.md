# Research 02 — Video-podcast post-production: what's automatable

> Researched 2026-07-18 by a Haiku-tier subagent (web sweep). Raw evidence — no recommendations.
> Part of the [Premiere automation handoff](../HANDOFF.md).

## 1. Standard Video-Podcast Post-Production Checklist

**Ingest & Media Management**
- Media ingestion and proxying: Premiere supports automated proxy workflow configuration and background ingest while editing continues
- Media linking: automatic relinking based on file location and naming consistency
- Dailies management: metadata-based organization using Camera Label/Camera Angle fields

**Multicam Setup**
- Audio sync methods: timecode, waveform, markers, or in-points
- Metadata-based track organization: camera angles automatically placed on matching tracks
- Create Single Multicam Source Sequence (automatic preset available)

**Rough Cut & Assembly**
- Silence/dead-air removal · filler-word removal · camera switching on active speaker · sequence assembly for narrative flow

**Audio Processing**
- Essential Sound panel: dialogue tagging, Reduce Noise, Reduce Rumble
- Enhance Speech: AI audio cleanup for imperfect acoustic conditions
- Multitrack balancing: host voice at −16 LUFS integrated, guest matching, music/SFX mixing

**Captions & Metadata**
- Speech-to-Text transcription (20+ languages, voice identification) → caption generation
- Chapter/timestamp generation from transcript; YouTube chapter format export

**Intro/Outro/Branding**
- Intro music, outro, sponsor reads, interstitial stings; lower-thirds templates (MOGRT or PNG); watermarks and end pages

**Social Distribution**
- Short-form clip extraction (1920×1080, 1080×1350, 1080×1920); Auto Reframe for multi-aspect delivery

**Export & Publishing**
- Export for primary platform; metadata (chapters, descriptions, keywords) export

## 2. Premiere Built-in AI/Automation Features (2025-2026)

| Feature | Status | Automation Level | Notes |
|---------|--------|------------------|-------|
| **Text-Based Editing** | Integrated | Partial | Select/cut/rearrange text from transcript; clips auto-trim/place; creative keep/cut decisions remain manual |
| **Speech-to-Text** | Integrated | Full | 20+ languages; speaker identification; 95–98% accuracy with clean audio |
| **Enhance Speech** | Integrated | Full | AI noise removal for dialogue; handles HVAC, wind, room echo |
| **Auto Reframe** | Integrated | Full | 16:9→9:16/1:1 etc.; subject-tracking; three motion presets |
| **Scene Edit Detection** | Integrated | Full | Automatically identify cuts within a video file |
| **Captions/Subtitles** | Integrated | Full | Auto-generate caption tracks from transcription |
| **Essential Sound** | Integrated | Partial | Audio categorization; Reduce Noise/Rumble sliders; single-pass analysis required |
| **Multicam Auto-Switching** | Third-party | Manual natively | e.g. Premiere Assistant / Cutback detects active speaker and generates angle switches |
| **Chapter Markers** | Third-party | Partial | AI topic-shift detection from transcript (CaptionX, PremiereCopilot, Phantom Editor) |
| **Lower Thirds** | Template-based | Manual | MOGRT templates; no automation of placement/timing logic natively |
| **Generative Extend** | 2025 addition | Full | AI-generated frames to extend clips |

**Transcript API access:** no public transcript API documented in official sources at the feature level; third-party tools use their own transcription. (See Research 03 §5 for the transcript JSON import spec and UXP `Transcript` class.)

## 3. Third-Party Auto-Editing Plugins

### AutoPod (podcast-specialized) — https://autopodcastai.com/
- Native CEP panel (Window → Extensions → AutoPod)
- **Multi-Camera Auto-Switching**: up to 10 cameras/10 mics, driven by audio cues (~85% correct; remaining 15% needs human judgment)
- **Jump Cut Editor**: detects and removes silence
- **Social Clip Creator**: auto-converts to social aspect ratios, watermarks, end pages
- Does NOT include captions, zooms, profanity filtering
- $29/month, 30-day free trial

### AutoCut — https://www.autocut.com/en/
- Premiere + DaVinci Resolve panel
- Basic ($6.6/mo): silence removal with configurable thresholds/presets
- AI ($14.9/mo): + filler words, AutoCaptions (80+ languages), AutoZoom, repetition/bad-take detection, profanity bleeping, chapters, B-roll suggestion, podcast multi-track handling, translation
- Performance degrades with mixed/non-separated audio tracks

### FireCut — https://firecut.ai/
- Premiere-only panel (2022+), Windows/macOS
- Silence removal, filler words ("um/uh"), bad-take detection, dynamic captions (50+ languages), zoom placement, YouTube chapters, B-roll search, AI voiceover (25k chars/mo)
- Starter $14/mo · Pro $29/mo · 14-day trial; 8 h/mo transcription included
- Philosophy: "rule-based manual control" rather than full automation

### TimeBolt — https://www.timebolt.io/
- Standalone app; exports to Premiere/FCP/Resolve/Camtasia
- Waveform-based silence removal (local, no AI transcription), filler-word removal, section speed-up, keyboard-driven review
- $247 one-time; unlimited watermarked trial

### Recut — https://getrecut.com/
- Standalone; silence removal only; very fast (20-min file ≈ 1.2 s)
- $129 one-time, Windows/macOS

### Phantom Editor — https://phantomeditor.video/
- Premiere panel; 13+ tools: free Silence Remover, Banshee Captioner, AI long-form clipping, Wraith multi-cam editor, repeat removal, AI chapter markers, summaries
- One-time $35–$118 or $15–24/mo

### Comparison

| Plugin | Panel/Standalone | Silence | Filler | Captions | Zooms | Multicam | Pricing |
|--------|------------------|---------|--------|----------|-------|----------|---------|
| AutoPod | Panel | ✓ (jump cuts) | ✗ | ✗ | ✗ | ✓ primary | $29/mo |
| AutoCut | Panel | ✓ | ✓ | ✓ | ✓ | ✓ | $6.6–14.9/mo |
| FireCut | Panel | ✓ | ✓ | ✓ | ✓ | ✗ | $11–29/mo |
| TimeBolt | Standalone | ✓ waveform | ✓ | ✗ | ✗ | ✗ | $247 once |
| Recut | Standalone | ✓ waveform | ✗ | ✗ | ✗ | ✗ | $129 once |
| Phantom | Panel | ✓ | ✗ | ✓ | ✗ | ✓ | $15–24/mo or once |

## 4. Manual vs. Automatable

**Fully automatable (80–100%)**: silence removal · filler-word removal · noise cleanup (Enhance Speech) · transcription · auto captions · chapter detection from transcript · auto reframe · scene detection · proxy creation

**Mostly automatable with refinement (60–80%)**: multicam auto-switching (~85% accuracy) · zoom placement · auto color match · B-roll placement (AI suggests, human selects)

**Partially automatable (30–60%)**: audio mixing/balance (LUFS normalization automatable; voice-to-music balance needs ears) · rough-cut assembly (mechanical cuts automatable; narrative pacing manual) · intro/outro stings (template insertion automatable; timing creative) · lower thirds (templates automatable; speaker ID/timing manual)

**Manual/creative (0–20%)**: narrative pacing (when to keep a laugh, when a messy moment builds trust) · creative angle selection · emotional/contextual editing · branding consistency & sponsor reads · dialogue-continuity judgment · final QC listening pass · metadata/SEO strategy

**Key 2026 finding:** "The clearest shift is that editing is becoming more selective, not more automated." Best results combine AI efficiency with human judgment rather than full automation.

## Sources

- https://www.postmagazine.com/documents/AdobePremiereProBestPracticesGuide.pdf
- https://cutback.video/blog/the-complete-guide-to-podcast-interview-editing-in-2025-(manual-premiere-pro-ai-workflows)
- https://nextmedia.london/podcast-editing-workflow-2026/
- https://cutback.video/blog/best-multi-cam-editing-plugins-for-premiere-pro-users
- https://helpx.adobe.com/premiere/desktop/edit-projects/edit-video-using-text-based-editing/overview-of-text-based-editing.html
- https://helpx.adobe.com/premiere/desktop/add-text-images/insert-captions/auto-transcribe-video-using-speech-to-text.html
- https://helpx.adobe.com/premiere-pro/using/scene-edit-detection.html
- https://helpx.adobe.com/premiere/desktop/add-video-effects/commonly-used-effects/auto-reframe-overview.html
- https://blog.adobe.com/en/publish/2025/04/02/introducing-new-ai-powered-features-workflow-enhancements-premiere-pro-after-effects
- https://autopodcastai.com/ · https://autopodcastai.com/autopod-multi-camera-editing/ · https://autopodcastai.com/autopod-vs-autocut/
- https://www.autocut.com/en/pricing/ · https://www.autocut.com/en/blogs/autocut-vs-autopod/
- https://firecut.ai/pricing/all/ · https://www.editingcorp.com/firecut-best-ai-editing-plugin-premiere-pro/
- https://www.timebolt.io/ · https://getrecut.com/ · https://phantomeditor.video/
- https://cutback.video/blog/4-best-ai-podcast-editors-compared-selects-descript-autopod-and-more
- https://www.podcasteditingservices.com/podcast-editing-trends-2026/
- https://helpx.adobe.com/premiere/desktop/edit-projects/set-up-multi-camera-sequences-for-editing/create-a-multi-camera-source-sequence.html
