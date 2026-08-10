# You Are Not Finished — style block

Locked 2026-07-30. The approved reference is
[`public/images/REFERENCE.png`](public/images/REFERENCE.png) (2752x1536 native).
Paste it into every Gemini session before generating any batch.

## The style block

Copy this verbatim into the tail of every image prompt:

> Flat mid-century comic line art. Clean black outlines of even weight. Flat
> solid colour fills only — no halftone dots, no stipple, no gradients, no
> texture. Cream paper background. Muted olive green for foliage. No text, no
> labels, no lettering of any kind. Fill the entire canvas edge to edge with
> the background colour — no border, no frame, no white margin.

## Palette

| Role | Hex |
|---|---|
| Paper | `#F4E8C8` |
| Ink | `#1F1E1D` |
| Jacket | red, as reference |
| Companion | cyan, as reference |
| Foliage | muted olive green |
| Accent (assembly only) | tomato `#E24E1B` |

## Geometry

**1920x1080, full bleed.** One geometry for the whole film. Sources arrive
around 2752x1536 and are downscaled — nothing is ever upscaled.

## Construction notes that matter

**THE COMPANION** — a cyan cube head sitting **directly on two thin straight
legs**, with two thin straight arms coming **straight out of the cube itself**.
It has no torso. It has no joints, no antenna, no rivets, no panel lines and no
mouth. Two round black dot eyes only.

This one took three failed attempts. The cause was not prompt wording: the
references supplied showed the robot cropped at chest height, so the generator
had never seen that it has no body and filled the gap from generic robot
priors. **Always include a full-body reference of every character.** Reference
conditioning beats instruction.

**THE PERSON** — bald with two hair tufts, red jacket over a cream shirt, black
trousers, cream shoes, a cream satchel on a shoulder strap.

**THE FUTURE SELF** — the person's exact silhouette filled flat cream, thin ink
outline, no face and no clothing detail.

## Two things Gemini reliably ignores

Both appeared on the approved reference sheet despite explicit instruction.
Audit for both on every batch; do not trust the prompt.

1. **Lettering.** It labels things anyway. Any frame with text in it must be
   regenerated — all type in this film is added at assembly.
2. **Full bleed.** The reference sheet trims to `2602x1440+70+84`, i.e. a ~70px
   left and ~84px top margin. Run the frame-edge audit after every batch:

```bash
./production/frame-audit.sh
```

## Why flat fills, not halftone

The last film used halftone shading. This one does not, and that is a style
choice rather than a technical necessity — an earlier analysis claimed halftone
would degrade under upscaling, but that was measured against Gemini's 1024px
page preview rather than the 2752px download, and there is no upscaling.

Flat fills give this film its own surface against *Why Humans Need Rituals*.
Restoring halftone would be a legitimate style decision, not a bug fix.
