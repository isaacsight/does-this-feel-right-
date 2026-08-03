# Platform policy — what each one actually requires

Standing constraints for every GALLEY film and every social edition cut from one.
Checked against primary sources 2026-08-02. Four platforms, four different rules.

> **The one-line version.** Only YouTube penalises a channel for publishing a lot
> of similar things. Instagram and TikTok define "unoriginal" against copying
> **other people**, which we never do. X has no such rule at all. And **none of
> our shorts qualify for TikTok's programme, because every one is under 60s.**

Do not generalise one platform's policy to the others. The first version of this
document did, and the cadence guard throttled all four platforms to YouTube's
ceiling — buying nothing on three of them and costing reach.

---

## At a glance

| | YouTube | Instagram / Meta | TikTok | X |
|---|---|---|---|---|
| Penalises repetitive output of **your own** work | **Yes** | No | No | No |
| "Unoriginal" means | generic, templated, no arc | reposting **others'** work | copying **others'** work | n/a |
| Judged on | the **channel** | the account | account + per video | per post |
| AI disclosure | not needed (non-realistic exempt) | not specified | only if **realistic** | only for **armed conflict** |
| Our shorts eligible | yes | yes | **no — under 60s** | yes |

---

## YouTube — the only real constraint

YPP is assessed on the **channel**, not the video: *"we look at the channel as a
whole."* Three named buckets replaced the old catch-all "inauthentic content"
(the policy did not change; the language did).

1. **Generic and repetitive** — *"made with templates and there's not much
   variation from video to video"*, *"lots of videos really quickly that are very
   similar... don't really have a narrative arc."*
2. **Off-putting / distressing** — manufactured emotional manipulation. Not a
   risk for us; must not become one.
3. **AI personas on sensitive topics** — *"AI personas that are talking about
   finance or legal issues or health care, medical issues."*

**Explicitly NOT a problem: the tools.** *"If you make it with genAI great, if you
make it without genAI that's great too... our policies are independent of how the
content is made."* Nor viewer or competitor flags — *"the number of flags has
nothing to do with how an evaluation is done"*, stated with "100% conviction".
Nor altered-content disclosure: non-realistic animation is exempt, and
`containsSyntheticMedia` is not a Data API field (PLAYBOOK 10.26).

### Rules

- **At most two shorts per rolling 24h to YouTube**, across all films.
  `tools/publish/cadence.mjs`, on by default. Overriding is deliberate.
- **Never two from the same film on the same day.**
- **Every short carries its sources** — the clearest not-farmed signal.
- **The narrator is never a character.** No name, face, "hosted by", or
  first-person credentials — permanently. Our films land on medicine routinely;
  what exempts us from bucket 3 is that we have narration, not a presenter.
- **On any health, medical, legal or financial claim the authority is the
  citation.** "The research found X" is reporting. "You should do X" is a persona
  giving advice.

Appeal within 21 days; reapply after 90 with new content.

---

## Instagram / Meta — about other people's work, not your volume

Meta's originality policy (updated March 2026) deprioritises *"simply watching
along, reacting with facial expressions, stitching multiple clips together, or
narrating"* without adding value, plus duplicative posts and minor edits to
someone else's work — borders, captions, speed changes, re-uploading things the
account had no role in creating. Accounts posting mostly unoriginal content can
be *"deemed non-recommendable and demonetized."*

Original is *"content filmed or produced directly by a creator or owner."*

**Where we land: clean.** We produce every frame, every word and the narration.
Nothing in Meta's policy penalises the volume of your own original output — the
whole rule is about republishing others. No cadence limit applied.

---

## TikTok — we are outside the programme entirely

Creator Rewards requires an account to have **10,000 followers** and **100,000
views in 30 days**, and requires each video to *"be at least one minute long."*

**Every short we have ever cut is under 60 seconds** — the longest is 59.1s,
across all six films. So none of them can earn under the programme regardless of
anything else. Cadence is not the binding constraint on TikTok; length is.

Original content is *"designed, filmed, and produced by you."* The not-original
list is again about copying others — duets and stitches, others' watermarks,
*"reproduced from others with only slight modifications"*, *"different videos or
pictures originating from other people... without new and personal ideas."*

One clause to watch as we grow: *"content that contains looping videos, single or
multiple photos, or only text overlays"* is not original. Our films are largely
held illustration with slow moves and burned-in captions. We are on the right
side of it — original artwork, original narration, motion, an argument — but it
is the one place our format sits adjacent to a prohibition, and it is a reason to
keep motion, cards and pacing varied rather than shipping slideshows.

**AI disclosure:** required when content is entirely AI-generated or
significantly edited **and shows realistic-looking scenes or people**. Our flat
line art is not realistic, so it is not required. But TikTok states the label
*"won't affect the distribution of your video"* — it costs nothing and removes
the ambiguity. **Use the toggle.**

---

## X — no originality or repetition rule at all

The Creator Monetization Standards cover eligibility (Premium subscription, 5M
organic impressions in 3 months, 2,000 Premium followers), conduct (no
solicitation, fraud, platform manipulation or spam), and prohibited content
categories (illegal, adult, graphic, hate, sensitive). There is no clause about
repetitive, templated or generic output.

The only originality line is rights-based: *"You must only monetize content that
is original and authentic, or otherwise content that you have the rights to
monetize."* We own everything we post.

**AI disclosure on X is narrowly scoped to armed conflict** — irrelevant to us.

No cadence limit applied.

---

## Substack — no rule that touches us

No AI policy, no duplicate-content rule, no originality bar beyond plagiarism:
do not *"publish any material that was written or created by someone else and
claim it as your own."* Monetization is direct subscription via Stripe, so there
is no platform eligibility gate to fail.

The real constraints are list hygiene — no purchased, scraped or harvested email
lists, no adding people without consent — and that a publication must not exist
primarily to advertise external products or services.

---

## What this changes upstream

| Chair | Constraint |
|---|---|
| Director | Sensitive-topic films carry primary citations; no advice register; the narrator never becomes a character. |
| Art Director | Name each film's world AGAINST the catalogue: the last three films' worlds must be legibly different from this one. House tokens stay the spine; the world around them moves. A run of matching films is the "template" bucket arriving through the art department. |
| Editor | Sources on every social edition. Keep motion and cards varied — never a slideshow. Karaoke captions by default (word timings exist for every film). |
| Publisher | Cadence throttles **YouTube only**, two per 24h across all films, enforced by `cadence.mjs` per platform. Instagram, TikTok, X and Substack are unthrottled — their policies do not penalise the volume of your own original output. `drip.mjs` drains the queue daily and `verify.mjs` audits owner-side after every publish run. |
| Analytics | `tools/analytics/shorts-report.py` weekly; the next batch's passages are chosen from what already earned views, not from what reads well on paper. |

## Resolved decisions

- **Shorts are cut at 61–74s** (decided 2026-08-02). The old 52–59s window made
  every short TikTok-ineligible by seconds; `pick-spans.py` now targets the new
  window. YouTube Shorts and Reels take up to 3 minutes, so it costs nothing
  elsewhere.
- **The TikTok AI label is set on every upload** — not required for
  non-realistic art, but TikTok states it does not affect distribution, so it
  costs nothing and removes the ambiguity. The adapter does it.
- **Each film gets its own visual world** (decided 2026-08-02). The channel-level
  "generic and repetitive" bucket is not only a cadence problem — a catalogue of
  visually identical films is the template pattern however good each one is.
  The Art Director names each world against the last three films'.

## Sources

- [YouTube Creator Insider — inauthentic content clarified](https://www.youtube.com/watch?v=7JXOgUJGCRY) (Matt Koval, 2026-08)
- [TikTok Creator Rewards Program](https://www.tiktok.com/support/faq_detail?id=7581821550694013452)
- [TikTok — new labels for disclosing AI-generated content](https://newsroom.tiktok.com/new-labels-for-disclosing-ai-generated-content)
- [Meta — Rewarding original creators on Facebook](https://about.fb.com/news/2026/03/rewarding-original-creators-on-facebook/)
- [Instagram Content Monetization Policies](https://help.instagram.com/2635536099905516)
- [X's Creator Monetization Standards](https://help.x.com/en/rules-and-policies/content-monetization-standards)
- [Substack Content Guidelines](https://substack.com/content)
