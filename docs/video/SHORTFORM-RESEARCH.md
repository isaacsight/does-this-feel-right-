# Short-form craft — what Opus Clip and its rivals actually do

> Researched 2026-07-24. Relevant to GALLEY because our shorts solve the same
> problem: turning a long narrated film into vertical clips that hold attention.

## What Opus Clip actually is

A pipeline, not a feature. It ingests long-form video and does four things:
**selects** the segment, **reframes** it vertical, **captions** it, and
**scores** it — then ranks the outputs so you know which to post.

The insight worth stealing is that they treat *selection* and *scoring* as the
product. Anyone can crop and caption; the hard part is knowing which forty
seconds of a fifty-minute podcast is worth posting.

### 1. Virality score (0–100)
Ranks clips on **hook strength, pacing, and topic relevance**. Reported effect:
clips scoring above 75 average roughly **2.3× the views** of clips below 50.

The lesson isn't the number, it's that they made *hook strength* a measurable,
rankable property rather than a matter of taste.

### 2. Active speaker detection
Speaker diarization identifies distinct voices and faces, then the crop
**tracks the active speaker dynamically** rather than centre-cropping. Offers
"Active Speaker" (cut to whoever talks) and "Split Screen" layouts.

Not directly applicable to us — we have no talking heads — but the principle
is: **never centre-crop blindly; crop to the subject that matters this second.**
Our Editor reached the same conclusion independently and solved it by refusing
the crop and designing a vertical page instead.

### 3. Captions — the part most worth copying
- **Word-by-word highlighting**, each word lighting as spoken. Roughly **70% of
  top-performing educational creators** use some variation of it.
- **Keyword highlighting** — important terms auto-emphasised by colour, size or
  weight while the rest stays plain.
- **Timing lead:** each word should highlight **50–100 ms BEFORE it is spoken**,
  because reading is faster than listening. Sync-on-the-word feels late.
- **Colour shift beats boxes and underlines** — white → yellow or a brand accent
  reads as natural emphasis; boxes and underlines distract.
- Claimed accuracy ~94% on clear English, dropping to ~88% with music or
  overlapping speakers.

> **This is the single biggest gap in our shorts.** Ours use static block
> captions — legible, correctly spelled, safe-zoned, but not word-by-word and
> not keyword-highlighted. The mechanism cited for why it works is that
> word-by-word converts passive watching into active reading, which raises
> retention and watch time.

## The competitive field

| Tool | What it is best at |
|---|---|
| **Opus Clip** | The default. Selection + scoring + captions in one pass. |
| **Submagic** | **The most visually striking captions** — animated text, emoji overlays, stock B-roll. The one to study for caption craft specifically. |
| **Vizard** | Text-based clip editing, 4K export, **native scheduling to 6 platforms**, subtitle translation into 100+ languages, team workspace. |
| **Klap** | Simplest possible flow — paste a URL, get clips. |
| **Crayo / Choppity / Ssemble** | Same category, varying price and polish. |

Paid tiers cluster at **$19–29/month** (Submagic $19, Choppity $20, Descript
$24, Vizard/Klap $29).

**Vizard is the interesting one for us** — it has native scheduling to six
platforms, which is exactly the TikTok/Instagram posting problem we hit. A
$29/month tool may be cheaper than maintaining a Playwright script against two
hostile DOMs.

## What to adopt

1. **Word-by-word captions with a 50–100 ms lead.** Highest-value change. We
   already have word-level timings from whisper, so the data exists — it is
   purely a rendering change in Palmier.
2. **Keyword highlighting in the accent colour.** Our house tomato red is
   already the film's focal discipline; using it on the load-bearing word of
   each line extends that grammar into type. Colour shift, never boxes.
3. **Score our own hooks before posting.** We chose the three beats by
   judgement. Naming hook strength, pacing and relevance explicitly — even
   informally — makes the choice reviewable instead of instinctive.
4. **Do not adopt** dynamic speaker-tracking crops or emoji overlays. We have
   no speakers, and emoji violate the house rule.

## What we already do better

- **Correct proper nouns.** Their ASR runs 88–94%; ours is whisper timings with
  the locked script's text, so researcher names are exactly right. On a cited
  film that matters more than animation.
- **Designed vertical page** rather than a crop, which preserves two-object
  gags a centre crop would destroy.
- **Deliberate uneven cut rhythm** tuned to comedy, rather than a uniform pace.

## Sources
- [OpusClip caption best practices](https://www.opus.pro/blog/best-caption-presets-styles-boost-retention)
- [TikTok caption/subtitle best practices](https://www.opus.pro/blog/tiktok-caption-subtitle-best-practices)
- [Opus Clip guide](https://aitoolradar.io/guides/opus-clip)
- [Alternatives, tested](https://www.choppity.com/blog/best-opus-clip-alternatives/)
- [AI clipping tools compared](https://www.ssemble.com/blog/best-ai-clipping-tools-2026)
