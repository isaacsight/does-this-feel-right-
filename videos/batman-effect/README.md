# BATMAN MAKES PEOPLE NICER — APPARENTLY

kernel.chat behavioural-science film. **6:43 · 1920×1080 · 30fps.**
Built 2026-07-26.

```
deliver/                    ← everything for publishing lives here
  publish-manifest.json     file inventory, hashes, sources, known defects
  youtube/
    batman-effect.mp4       6:43 master
    batman-effect.srt       115 cues
    narration.mp3           isolated VO, level-flat
    thumbnail-a.png         the accordion commuter pile
    thumbnail-b.png         the limitations line-up
  shorts/                   3 verticals + matching SRTs
    01-batman-on-a-subway   43s · "They put Batman on a subway"
    02-nobody-saw-him       39s · "44% never saw him"
    03-or-a-giant-banana    40s · "Or a giant banana"

docs/
  SCRIPT.md                 locked script, source verification table
  STATUS.md                 full build log, bugs found, lessons
production/
  frames.mjs                76 frame definitions, each tagged to its line
  batch.mjs                 generation runner
  place.py                  content-lock placement
  narrate-chunked.mjs       per-scene narration (the level fix)
  narrate.mjs               single-call narration (superseded)
  segments.json edl.json batch-log.json shorts.json
frames-canonical/           76 final frames — the ONLY source for assembly
frames-v1-backup/           pre-CLEAN originals, kept for comparison
assets/ audio/ renders/     references, narration variants, cuts
```

One set of verticals serves TikTok, Reels and Shorts — the caption safe zones
are the union of all three platforms' UI.

## Source

**Unexpected events and prosocial behavior: the Batman effect.**
*npj Mental Health Research* vol. 4 (2025). DOI 10.1038/s44184-025-00171-5.

Verified: 37.66% control · 67.21% with Batman · OR 3.393, p<0.001 · ~44% of
helpers reported not noticing him.
**Unverified — check before publishing:** the 138-observation count and the
June 2026 correction. Nature blocks automated fetching; open it in a browser.

## Known defects, honestly

1. **9 holds exceed the 8.0s ceiling**, worst 13.8s. Thin coverage in the
   reflective stretches. ~8 more frames would clear it.
2. **The 76 frames have never been individually inspected at full resolution.**
   They were regenerated in one pass and cut straight in. The earlier slop was
   caught by Isaac, not by me — this gap is unclosed.
3. **The shorts have not been watched muted**, which is how most people will
   see them. Captions are verified to fit, not to read well.
4. **Publishing copy not written** — no titles, descriptions, tags.

## Do not publish without

- [ ] Checking the two unverified figures against the paper
- [ ] A full-resolution pass on all 76 frames
- [ ] Watching the master and all three shorts end to end
- [ ] Confirming no frame renders a recognisable franchise character. Two did
      early (b03 was DC's Batman, b16 was three Spider-Men) and were reshot —
      but only b03 and b16 were checked

## The four rules this film proved

Every one cost a failed batch to learn. All four are the same principle:
**a prohibition loses to a description.**

| Problem | What failed | What worked |
|---|---|---|
| Text in frames | "no letters, no labels" | delete the labelled *object* — an emergency handle summons its own sign |
| People in empty rooms | "nobody in frame" | remove the character clause from the style block |
| A calm frame in an action film | "this frame is quiet" | swap the whole register block (`CALM` not `PEAK`) |
| Cluttered, sloppy images | more art direction | **two events per frame**, most of the frame empty |

The last one was the big one. The brief asked for *one dominant gag plus one
smaller callback* — two things. Scene text routinely described five, and the
model rendered all five faithfully. Five focal points reads as slop however well
each is drawn.

## Two production notes

**Narration must be generated in chunks.** A single 891-word ElevenLabs call
drifts 11.3 dB from start to end (−25.3 dB → −36.6 dB), which sounds like a
filter closing rather than a volume change. Eight ~110-word chunks, each
two-pass loudnorm'd to −18 LUFS, holds within 0.9 dB.
Use `production/narrate-chunked.mjs`.

**Frames must be content-locked, never evenly spaced.** Even distribution put 44
of 54 frames on the wrong line while producing healthier-looking statistics —
it smears frames across gaps to keep the mean tidy. `place.py` matches each
frame independently against every segment, then sorts by time. A monotonic
cursor breaks as soon as frame ids stop following narration order, which they do
the moment a second authoring pass is appended.
