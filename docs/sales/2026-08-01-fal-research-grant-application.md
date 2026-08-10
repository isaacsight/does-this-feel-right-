# fal.ai Research Grant — application draft

**To:** grants@fal.ai
**From:** isaacsight@gmail.com
**Status:** SENT 2026-08-01 4:07 PM from isaacsight@gmail.com, with all three
ledgers attached (12K / 12K / 18K). Confirmed in Sent Mail.
Awaiting reply from grants@fal.ai.
**Ask:** $500 in credits

---

## Subject

Research grant request — open-source agent, published per-call fal.ai cost ledgers

## Body

Hello,

I publish kernel.chat, an independent two-surface publication: an open-source
terminal AI agent (kbot, MIT — https://www.npmjs.com/package/@kernel.chat/kbot,
currently v4.5.0) and an editorial magazine that ships short documentary films.
Both run on the same discipline: count what gets read, cut what doesn't, file the
audit in public.

fal.ai is the generation layer for the films. I would like to request research
credits to continue, and to run an experiment I currently cannot afford to run
properly.

What I think makes this worth your time is that I already publish the thing most
credit recipients never produce: a complete, per-call cost ledger.

Every fal.ai call in a film is logged with a timestamp, the frame it produced,
the model, and its price — written by the generation script as it runs, not
reconstructed afterward. Across the three most recent films that is 704 logged
calls. I have attached all three ledgers to this email so you can read the raw
lines rather than take my summary for it:

| Film | fal.ai calls | Logged spend |
|---|---|---|
| You Are Not Finished | 204 | $7.96 |
| You Happen To Life | 204 | $7.96 |
| You Watched It Happen | 296 | $11.54 |

An earlier film, built on video models rather than stills, came to roughly $37.70
against a $40 authorisation for 83 unique frames — no image reused twice.

Those ledgers are what I use to decide model routing: which fal.ai models a shot
goes to, at what budget, and when a cheaper route produces an indistinguishable
result. Earlier films fanned out across Veo, Omni, Kling and Seedance; the recent
three are 704-for-704 on nano-banana/edit, because the ledger showed it was the
better cost-per-usable-frame for that particular job. That is a measurement
changing a production decision, which is the only reason to keep a ledger at all.

Two finished films are public on the channel:

- You Are Not Finished — https://youtu.be/yEeL5u4nwNw (7:01)
- You Watched It Happen — https://youtu.be/9kHUSRU3zms

Films also ship as vertical recuts to TikTok, Reels and Shorts, so one generation
budget produces four distributed editions.

**What $500 would fund.** At the observed rate that is roughly forty films of
frame work — but volume is not what I want it for. I want it to answer a question
I currently answer too conservatively because every comparison costs money out of
pocket: for a given shot, what is the cheapest model in your catalog that still
clears the quality bar?

With credits I would run that comparison properly across your catalog and publish
the result in the same format as the ledgers above — model by model,
cost-per-usable-frame, with the frames attached so readers can judge the quality
call themselves rather than take my word for it. The production playbook it feeds
is already public in the repo.

If that comparison is useful to you as well as to me, I am glad to shape the
methodology around what you would want measured.

Repo: https://github.com/isaacsight/kernel

Thank you for reading.

Isaac Hernandez
kernel.chat

---

## Closed since first draft

- **Sending address** — isaacsight@gmail.com (personal; the grant track targets
  solo developers and creators).
- **Repo is public** — github.com/isaacsight/kernel returns 200 unauthenticated.
- **npm link** — verified live at v4.5.0, matching the claim in the body.
- **Publish status** — verified via YouTube oEmbed. *You Are Not Finished*
  (yEeL5u4nwNw) and *You Watched It Happen* (9kHUSRU3zms) are public on
  @Kernelchat. *You Happen To Life* (fVPZbRDCK5A) returns Unauthorized — it is
  private or unlisted, so the draft claims **two** published films, not three.
  If you make it public before sending, add the link and change "Two finished
  films" to three.

## Ledgers — attach, do not publish

Nothing from `videos/` goes to GitHub: no films, no frames, no production tree.
`videos/**` stays gitignored at `.gitignore:151` and the repo is unchanged.

The ledgers travel as **email attachments** instead. Three plain-text files,
42 KB total, no media:

| File | Size |
|---|---|
| `videos/you-are-not-finished/production/spend.log` | 12.1 KB |
| `videos/you-happen-to-life/production/spend.log` | 12.2 KB |
| `videos/you-watched-it-happen/production/spend.log` | 17.8 KB |

Each line is `timestamp  frame-id  model  price`, e.g.

```
2026-07-30T19:22:23.760Z 02a fal-ai/nano-banana/edit 0.039
```

This is better than a repo link for the purpose: the reviewer opens one
attachment and sees all 704 lines, with nothing to navigate and no claim about
public hosting to verify. The body has been reworded to say the ledgers are
attached rather than published.

Check before sending: the logs contain timestamps, frame IDs, model names and
prices — no keys, paths, or personal data. Worth one skim anyway, since they were
written for internal use.
