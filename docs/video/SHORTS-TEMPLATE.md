# The kernel.chat shorts template

> Researched and written 2026-07-24, after publishing three shorts by hand and
> finding two defects only on a phone. This is the house template for every
> vertical short: one geometry, one caption style, one beat structure.
>
> It supersedes the `centerY: 0.70` figure in [`CAPTION-SPEC.md`](CAPTION-SPEC.md)
> — see **The correction** below. Everything else in that document stands.

## The correction

The published shorts put captions at `centerY: 0.70`. On a 1920px canvas that
centres them at **1344px**. TikTok's bottom unsafe zone begins at **1436px**.
Bold 64px type centred at 1344 reaches roughly **1424px** at its lowest — twelve
pixels of clearance, and none at all the moment a caption wraps to two lines.

**House value is now `centerY: 0.64`** (1229px centre, ~1309px lowest), which
clears every platform with about 127px to spare.

This was not visible in the editor and not visible in the exported frame at
desktop scale. It is only visible on a phone with the platform chrome drawn
over it. Check there.

## Geometry — one export for all three platforms

All three platforms take **1080 × 1920** (9:16). They differ only in where
their own interface covers the frame. Design for the union and one file posts
everywhere.

Published figures disagree — one source puts TikTok's bottom margin at 320px,
another at 484px. **Where sources conflict, take the maximum.** Over-caution
costs nothing; under-caution costs the caption.

| Edge | Reserve | What lives there |
|---|---|---|
| Top | **130 px** (6.8%) | Profile chrome, "Following / For You" |
| Bottom | **484 px** (25.2%) | Description drawer, handle, audio ticker, platform captions |
| Right | **140 px** (13.0%) | Like / comment / share / avatar rail |
| Left | **60 px** (5.6%) | Device edge crop variance |

**Usable safe box: x 60 → 940, y 130 → 1436. That is 880 × 1306.**

Ads shrink it further — a TikTok CTA button adds ~50px to the bottom, an
Instagram "Sponsored" label plus button costs ~80px. If a short will ever be
promoted, treat the bottom reserve as **534px**.

### The page

Derived from the vertical layout the Editor arrived at on *The Price of a
Glance*, corrected to the safe box above.

```
  0.000  ┌─────────────────────┐
         │   platform chrome   │   ← keep empty
  0.068  ├─────────────────────┤
         │       KICKER        │   0.11  Courier Prime, 34px, tracked +0.18
  0.150  ├─────────────────────┤
         │                     │
         │      PICTURE        │   0.18 → 0.56, full width on the ivory matte
         │                     │
  0.560  ├─────────────────────┤
         │      CAPTIONS       │   0.64  ← the corrected value
  0.700  ├─────────────────────┤
         │                     │
         │   platform chrome   │   ← keep empty
  1.000  └─────────────────────┘
```

**Never centre-crop a 16:9 frame to fill 9:16.** It keeps ~31% of the picture
and destroys every two-object gag. Full-width picture band on the matte instead.

## Beat structure — 45 seconds, single idea

The retention research is consistent across sources: roughly **71% of viewers
decide in the first few seconds**, and a hook / promise / payoff structure laid
down in the first 3–5 seconds correlates with a **15–25% higher chance** of the
viewer reaching ten seconds.

| Beat | Time | Job |
|---|---|---|
| **Hook** | 0.0 – 3.0s | The claim that sounds wrong. No preamble, no logo, no "in this video". |
| **Promise** | 3.0 – 5.0s | Name the thing that will resolve it — the study, the number. |
| **Body** | 5.0 – 38s | The finding. One idea. Cite it on screen. |
| **Turn** | 38 – 43s | What it means for the viewer. This is where they decide to share. |
| **Sign-off** | 43 – 45s | The mark. Two seconds, no ask. |

**Education tolerates length.** The research notes explainer content sustains
+5–10s beyond entertainment's ceiling, and wants slower cuts — entertainment
runs 1–2s, we do not have to. What kills an explainer is a slack *opening*, not
a long middle.

**No call to action.** House rule, not a research finding: the channel's premise
is that it counts what gets read rather than asking to be followed. A short that
ends by begging contradicts the thesis it just spent forty seconds arguing.

## Cutting

Carried from [`PRODUCTION-PLAYBOOK.md`](PRODUCTION-PLAYBOOK.md), which earned
these the hard way.

- **Comic timing is uneven timing.** Uniform cutting fixes drag and kills every
  joke in the same pass.
- Target **~3.0s average** on a short (the long film ran 3.34s). Never exceed
  **8s** on a still — past that a static image dies.
- **Hard cuts only. No transitions.** The cut is the joke.
- Every image different. A repeat reads as a budget, not a motif.

| Hold | Range | Use |
|---|---|---|
| Snap | 1.0 – 2.0s | The punchline. |
| Quick | 1.5 – 2.5s | Escalating runs, lists. |
| Setup | 3.0 – 5.0s | Let the viewer read the situation. |
| Breath | 5.0 – 8.0s | After a big beat, and through the turn. |

## Captions

Full rationale in [`CAPTION-SPEC.md`](CAPTION-SPEC.md). The short version:

- Cards built with **`add_texts` from the locked script** — never `add_captions`.
  ASR mangles every researcher name, and `maxWords` cannot slow the cards down:
  Palmier chunks on speech pauses, giving 84 cards on a 52s track no matter what
  you pass.
- **AvenirNextCondensed-Heavy, 52pt, ink `#1F1E1D`, uppercase, tracking -1.**
- **One colour.** No highlight, no per-word animation — whole-card `popIn`.
  A tomato accent flicking on and off twice a second is a full-screen strobe.
- **`centerY: 0.63`**, explicit `transform` on every clip.
- **~2s per card, 2 lines maximum, ≤21 characters per line.**

`fontSize` is canvas **points**, not pixels — 52 renders at roughly 48px per
glyph on a 1080px canvas. Size by the character budget, not by eye.

One caption note the research adds: **all three platforms now generate their own
captions by default in 2026.** Ours are burned in, so the platform layer is
redundant and doubles the type on screen. Turn it off at upload where the
platform allows it.

## Checklist

- [ ] 1080 × 1920, everything inside x 60→940, y 130→1436
- [ ] Hook lands before 3.0s, no preamble
- [ ] One idea, cited on screen
- [ ] Average hold ~3s, nothing over 8s, no repeated image
- [ ] Hard cuts, no transitions
- [ ] Captions `highlightPop`, tomato, `centerY: 0.64`
- [ ] Caption text corrected against the locked script
- [ ] Platform auto-captions disabled at upload
- [ ] **Checked on a phone with the chrome drawn over it** — not in the editor

## Sources

- [Kreatli — Safe Zone Hub 2026](https://kreatli.com/guides/safe-zone-guide)
- [Zeely — TikTok safe zones 2026](https://zeely.ai/blog/tiktok-safe-zones/)
- [trustypost — TikTok video size 2026](https://trustypost.ai/blog/tiktok-video-size-2026-dimensions-ratio-safe-zones/)
- [Postplanify — Social media safe zones 2026](https://postplanify.com/blog/social-media-safe-zones-2026-complete-guide)
- [Teleprompter — Short-form video strategy 2026](https://www.teleprompter.com/blog/short-form-video-strategy)
- [Miraflow — YouTube Shorts best practices 2026](https://miraflow.ai/blog/youtube-shorts-best-practices-2026-complete-guide)
- [CapCut — First 3-second hook patterns](https://www.capcut.com/create/short-form-video-hooks-first-3-second-patterns)
