# Channel Studio

Channel Studio is the private, draft-first publishing folio at `/channel-studio`.
It creates platform-native editions for YouTube Shorts, TikTok, Instagram Reels,
and X, then hands approved editions to Buffer as private drafts. Reddit remains a
manual community edition by design.

## Art direction

- **Editorial sentence:** Distribution is a press run with accountable human
  control, so the page feels like a marked production ledger moving from a
  manuscript to signed platform proofs.
- **Material metaphor:** pressroom job ticket on ledger, cream, butter, and kraft
  stocks; tomato proof marks; pool-blue source slips.
- **Dominant gesture:** a strict five-edition register interrupted by one large
  active proof sheet.
- **Type:** EB Garamond for the editorial argument, Courier Prime for job state,
  receipts, channel bindings, and approvals.
- **Responsive transformation:** the job ticket becomes the mobile anchor; the
  edition register remains sequential; the proof columns become one reading flow.
- **Motion:** none beyond native control feedback. The page is a stationary
  instrument and print remains a complete ledger.
- **Anti-goals:** no equal SaaS cards, no gradient hero, no animated vanity
  metrics, and no decorative state that disappears in print.

## Safety contract

- The route is restricted to authenticated users with `app_metadata.is_admin`.
- The Buffer API key exists only as a Supabase Edge Function secret.
- The Edge Function can discover channels and create drafts. It cannot schedule,
  publish, comment, like, follow, or engage.
- Draft creation is fail-closed: the function reads the created post's status back
  from Buffer and reports success only when that status is exactly `draft`. Any
  other status (queued, pending, sent) or an unreadable status is surfaced as an
  error so the operator removes the post in Buffer.
- Every press run requires four explicit approvals in the browser and the Edge
  Function independently rejects a request unless all four named approvals are
  present and true.
- Request bodies are capped at 128KB; malformed JSON and oversized requests fail
  before any Buffer mutation is attempted.
- Buffer receives a stable public media URL. Common AWS, Google Cloud, Azure,
  generic signed, tokenized, and expiring URL parameters are rejected.
- Reddit copy is never sent through the broadcast boundary.

## Configuration

Create a Buffer API key as the owner of the Buffer organization, then configure:

```sh
npx supabase secrets set BUFFER_API_KEY=REDACTED
npx supabase secrets set BUFFER_ORGANIZATION_ID=OPTIONAL_ORGANIZATION_ID
npx supabase functions deploy channel-publisher --project-ref eoxxpyixdieprsxlpwcs
```

`BUFFER_ORGANIZATION_ID` is optional. When absent, the first organization returned
by the authenticated Buffer account is used.

Connect YouTube, TikTok, Instagram, and X inside Buffer itself. Channel Studio does
not receive or store social-account passwords.

## Operating sequence

1. Render a clean vertical MP4 and place it at a stable public HTTPS URL.
2. Open `/channel-studio` as the publisher.
3. Inspect Buffer and bind each edition to its connected channel.
4. Edit the platform-specific title and copy.
5. Complete the claim, rights, disclosure, and preview register.
6. Send the editions to Buffer drafts.
7. Review timing and final native options in Buffer before scheduling.

For the first canary, enable only one low-risk test channel. After Channel Studio
returns a verified `draft` receipt, open Buffer and confirm the post is in Drafts,
absent from the queue, and absent from the social platform before connecting the
remaining production channels.

Long-form YouTube remains a native YouTube Studio upload until a verified YouTube
API project is justified. Native-only music, stickers, and effects remain a
finish-in-app step.

## Local design proof

In Vite development mode, `/channel-studio?proof=folio` renders the folio without
an authenticated session for responsive and print QA. The production build removes
this bypass because it is guarded by `import.meta.env.DEV`.
