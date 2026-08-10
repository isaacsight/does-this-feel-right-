# You Happen to Life — YouTube delivery kit

Master: `deliver/you-happen-to-life-1080p.mp4` · **6:43** · 1920x1080 30fps
Opens with the 14.6s channel intro (`videos/kernel-chat-intro/renders/channel-intro-v14.mp4`),
so every timecode below is offset by 14.6s and the SRT was built with `--offset 14.6`.
Captions: `deliver/you-happen-to-life.srt` — **upload this**; do not let the
platform auto-caption. Act 4 is nothing but numbers and ASR mangles numbers.

## Title

> You Happen to Life

Alternates, if the plain one tests badly:
- The Most Comforting Idea in Self-Improvement Is Partly a Report
- Practice Explains 26% of Chess and Under 1% of Your Job

## Description

```
"I happen to life. Life doesn't happen to me."

You have heard some version of that line. It sounds brave, and the belief
underneath it is real: psychologists have measured it since 1966 and it has a
name. People who hold it do better on a lot of things.

This film is about what the research says next, and why the advice built on it
can turn cruel in the wrong room.

Sources, in order of appearance:

Rotter, J. B. (1966). "Generalized expectancies for internal versus external
control of reinforcement." Psychological Monographs, 80(1), 1-28. The
Internal-External Locus of Control Scale. Note that it measures how much
control you FEEL, not how much you have.

Macnamara, B. N., Hambrick, D. Z., & Oswald, F. L. (2014). "Deliberate practice
and performance in music, games, sports, education, and professions: a
meta-analysis." Psychological Science, 25(8), 1608-1618. Variance in
performance explained by practice: games 26%, music 21%, sports 18%,
education 4%, professions under 1%.

These are variance-explained figures from a meta-analysis. They are not a claim
that practice is useless - nobody gets good at anything without it. They are a
claim about what separates one person from the next.

The film does not cite the podcast the opening line comes from, and does not
name the person who said it. The argument being examined is held by millions;
it is not one guest's mistake.

kernel.chat
```

## Chapters

Paste into the description below the sources. YouTube needs the first at 0:00.

```
0:00 Intro
0:14 The claim
1:09 It is a real thing
2:06 And the practice claim
2:23 The numbers
3:29 Which way does it point
4:35 Where it turns cruel
5:48 What survives
```

## Settings

- **Visibility:** public, listed
- **Category:** Education
- **Captions:** upload `you-happen-to-life.srt`, then **turn off automatic
  captions** so the uploaded track is the one that serves
- **Thumbnail:** frame `030a` (the five collapsing bars) or `047c` (the person
  and the stranger). 030a is the stronger hook; 047c is the truer subject.
- **End screen:** link *You Are Not Finished* — the two films argue opposite
  halves of the same question about how much of you is authored.

## Tags

locus of control, rotter, deliberate practice, macnamara, self improvement,
psychology, agency, meta analysis, behavioural science, kernel.chat

---

## Shorts

Three verticals, 1080x1920, cut from the film master (no channel intro — at
under a minute the intro would eat a sixth of the runtime).

**55-59s by design.** The last set ran 40-51s; the School of Life study found
that is short enough to cut a thought off before it lands.

| File | Runtime | Kicker | The passage |
|---|---|---|---|
| `01-under-one-percent.mp4` | 57.0s | UNDER ONE PERCENT | the meta-analysis, 26% at games down to under 1% at your job |
| `02-cause-or-report.mp4` | 56.6s | CAUSE, OR REPORT? | feeling in control tracks with being in control |
| `03-said-kindly.mp4` | 57.6s | SAID KINDLY | one dial, and what it does when pointed at a stranger |

Each ships with an `.srt` sidecar cut from the locked script.

**On every platform: upload the SRT and turn OFF automatic captions.** The
captions are already burned in, so platform auto-captions double them up on
screen and get the numbers wrong on top of it.

Caption cards are rendered with ImageMagick and composited, not drawn by
ffmpeg: this machine's ffmpeg has neither libass nor libfreetype, so
`subtitles=`, `ass=` and `drawtext=` are all unavailable.
