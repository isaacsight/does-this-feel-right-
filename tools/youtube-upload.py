#!/usr/bin/env python3
"""Upload a video to the kernel.chat YouTube channel via the Data API v3.

Resumable upload, so file size is irrelevant — this exists because the browser
file-upload path caps at 10 MB and the masters are ~85 MB.

One-time setup (only Isaac can do this — it is his Google account):

  1. https://console.cloud.google.com/ → create or pick a project
  2. APIs & Services → Library → enable "YouTube Data API v3"
  3. APIs & Services → OAuth consent screen → External → add
     kernel.chat@gmail.com as a Test user
  4. APIs & Services → Credentials → Create credentials →
     OAuth client ID → Desktop app → Download JSON
  5. Save it as ~/.config/kernel/youtube-client-secret.json

First run opens a browser for consent and caches a refresh token at
~/.config/kernel/youtube-token.json. Every run after that is non-interactive.

Usage:
  python3 tools/youtube-upload.py --meta output/publish/youtube-meta.json
  python3 tools/youtube-upload.py --meta ... --privacy public     # go live
  python3 tools/youtube-upload.py --publish VIDEO_ID              # flip later

Defaults to UNLISTED. Publishing is a one-way door; watch it on the platform
first, then flip.
"""

import argparse
import json
import os
import time
import sys
from pathlib import Path

CONFIG = Path.home() / ".config" / "kernel"
CLIENT_SECRET = CONFIG / "youtube-client-secret.json"
TOKEN = CONFIG / "youtube-token.json"
SCOPES = ["https://www.googleapis.com/auth/youtube.upload",
          "https://www.googleapis.com/auth/youtube",
          # force-ssl is required for captions().insert — without it the
          # caption upload fails with 403 insufficientPermissions.
          "https://www.googleapis.com/auth/youtube.force-ssl"]

try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    from googleapiclient.http import MediaFileUpload
except ImportError:
    sys.exit(
        "Missing dependencies. Install with:\n"
        "  python3 -m pip install --user google-api-python-client "
        "google-auth-oauthlib google-auth-httplib2"
    )


def authenticate():
    creds = None
    if TOKEN.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN), SCOPES)
    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
        except Exception as e:
            # Google expires refresh tokens for OAuth apps still in
            # "Testing" publishing status, and revokes them on account
            # changes. There is no non-interactive recovery: the consent
            # screen has to be clicked through by the account owner.
            print(f"Cached token is dead: {e}\n", file=sys.stderr)
            sys.exit(
                "Re-consent is required and only the account owner can do it.\n"
                "  1. rm ~/.config/kernel/youtube-token.json\n"
                "  2. re-run this command; a browser opens on the\n"
                "     kernel.chat@gmail.com consent screen\n"
                "  3. approve, and the new refresh token is cached\n\n"
                "To stop this recurring: Google Cloud Console -> APIs &\n"
                "Services -> OAuth consent screen -> PUBLISH the app.\n"
                "Tokens for apps left in Testing expire after 7 days."
            )
    elif not creds or not creds.valid:
        if not CLIENT_SECRET.exists():
            sys.exit(
                f"No OAuth client secret at {CLIENT_SECRET}\n"
                "Complete the one-time setup in this file's docstring first."
            )
        flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRET), SCOPES)
        creds = flow.run_local_server(port=0)
    CONFIG.mkdir(parents=True, exist_ok=True)
    TOKEN.write_text(creds.to_json())
    os.chmod(TOKEN, 0o600)
    return build("youtube", "v3", credentials=creds)


def upload(youtube, meta, privacy):
    path = Path(meta["file"])
    if not path.exists():
        sys.exit(f"Video not found: {path}")

    body = {
        "snippet": {
            "title": meta["title"],
            "description": meta["description"],
            "tags": meta.get("tags", []),
            "categoryId": meta.get("categoryId", "27"),  # 27 = Education
        },
        "status": {
            "privacyStatus": privacy,
            "selfDeclaredMadeForKids": False,
            # NOTE: there is NO synthetic-media field in the Data API v3 status
            # object. This code used to send "containsSyntheticMedia": True and
            # YouTube silently DROPPED it - unknown fields are ignored rather
            # than rejected, so it looked like it worked for three films and
            # never set anything. Verified 2026-08-01 by reading the status back:
            # only uploadStatus, privacyStatus, license, embeddable,
            # publicStatsViewable, madeForKids, selfDeclaredMadeForKids exist.
            #
            # The disclosure is a Studio-only control ("Altered or synthetic
            # content" under Attributes). It is also NOT REQUIRED for this
            # channel: YouTube's policy applies to content that appears
            # REALISTIC, and explicitly exempts fully animated and non-realistic
            # work. These films are flat cartoon illustration depicting no real
            # person, so they fall outside it.
        },
    }

    media = MediaFileUpload(str(path), chunksize=8 * 1024 * 1024, resumable=True)
    request = youtube.videos().insert(
        part="snippet,status", body=body, media_body=media
    )

    size_mb = path.stat().st_size / 1_048_576
    print(f"Uploading {path.name} ({size_mb:.1f} MB) as {privacy}…")

    response = None
    while response is None:
        try:
            status, response = request.next_chunk()
            if status:
                print(f"  {int(status.progress() * 100)}%", flush=True)
        except HttpError as e:
            if e.resp.status in (500, 502, 503, 504):
                print(f"  transient {e.resp.status}, retrying…")
                continue
            raise

    video_id = response["id"]
    print(f"\nDone. https://youtu.be/{video_id}")
    print(f"Studio: https://studio.youtube.com/video/{video_id}/edit")

    srt = meta.get("captions")
    if srt and Path(srt).exists():
        set_captions(youtube, video_id, srt)

    thumb = meta.get("thumbnail")
    if thumb and Path(thumb).exists():
        # The insert call returns an id before YouTube has finished registering
        # the video, so setting a thumbnail immediately 404s with
        # "videoNotFound" - and the traceback loses the id, which looks like a
        # failed upload when the upload actually succeeded. Retry with backoff.
        for attempt in range(6):
            try:
                youtube.thumbnails().set(
                    videoId=video_id, media_body=MediaFileUpload(thumb)
                ).execute()
                print(f"Thumbnail set from {Path(thumb).name}")
                break
            except HttpError as e:
                if e.resp.status == 404 and attempt < 5:
                    time.sleep(10 * (attempt + 1))
                    continue
                print(f"  thumbnail FAILED (video is still uploaded, id above): {e}")
                break

    return video_id


def set_captions(youtube, video_id, srt_path):
    """Upload an SRT as the video's caption track.

    Worth doing properly rather than leaving to the platform: our captions come
    from the locked script, and YouTube's ASR mangles numbers and proper nouns.
    A film with an act made entirely of percentages cannot ship on ASR.

    The uploaded track does NOT switch auto-captions off by itself. YouTube will
    serve both, and the viewer sees two tracks in the menu. Turning ASR off is a
    manual step in Studio (Subtitles -> the auto-generated track -> unpublish)
    and there is no API for it, so it is printed as a reminder rather than
    silently skipped.
    """
    try:
        youtube.captions().insert(
            part="snippet",
            body={"snippet": {"videoId": video_id, "language": "en",
                              "name": "English", "isDraft": False}},
            media_body=MediaFileUpload(str(srt_path), mimetype="application/octet-stream"),
        ).execute()
        print(f"Captions uploaded from {Path(srt_path).name}")
        print("  ! Now unpublish the AUTO-GENERATED track in Studio - "
              "there is no API for it and YouTube serves both otherwise.")
    except HttpError as e:
        print(f"  caption upload FAILED: {e}")
        print(f"  upload {srt_path} by hand in Studio -> Subtitles")


def set_privacy(youtube, video_id, target="public"):
    """Move an existing video to `target` privacy and prove it landed.

    Also used to retire a superseded upload: YouTube cannot swap the file on a
    published video, so a corrected re-cut is a NEW id and the old one goes
    private. Private, never deleted - taking the video down is reversible and
    is the owner's call, and the id stays resolvable for anyone auditing it.
    """
    current = youtube.videos().list(part="snippet,status", id=video_id).execute()
    if not current["items"]:
        sys.exit(f"No video with id {video_id}")

    # Update STATUS ONLY. Round-tripping the snippet alongside it returns 200
    # and silently leaves privacyStatus unchanged - observed 2026-07-31, the
    # video stayed unlisted and the API reported success. Always read back.
    #
    # Nothing here declares synthetic media: `containsSyntheticMedia` is not a
    # field on videos.status. The API accepts unknown keys and drops them, so
    # sending it looked like it worked for weeks and never did. The real
    # control is the altered-content disclosure in Studio, and non-realistic
    # animation is exempt from it anyway.
    youtube.videos().update(
        part="status",
        body={"id": video_id, "status": {"privacyStatus": target,
                                         "selfDeclaredMadeForKids": False}},
    ).execute()
    time.sleep(3)
    now = youtube.videos().list(part="status", id=video_id).execute()
    got = now["items"][0]["status"]["privacyStatus"]
    if got != target:
        sys.exit(f"Update reported success but video is still {got}")
    print(f"{target}: https://youtu.be/{video_id}")


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--meta", help="JSON file with title/description/tags/file")
    p.add_argument("--privacy", default="unlisted",
                   choices=["private", "unlisted", "public"],
                   help="default: unlisted — watch it before going public")
    p.add_argument("--publish", metavar="VIDEO_ID",
                   help="flip an already-uploaded video to public")
    p.add_argument("--retire", metavar="VIDEO_ID", action="append", default=[],
                   help="set an existing video private (repeatable) — for "
                        "retiring an upload a corrected re-cut supersedes")
    p.add_argument("--check", metavar="IDS",
                   help="comma-separated video ids: print '<id> <privacyStatus>' "
                        "per line, or '<id> missing'. Read-back for verify.mjs.")
    args = p.parse_args()

    youtube = authenticate()

    if args.check:
        ids = [i for i in args.check.split(",") if i]
        # One call per 50 ids is the API's own batching.
        found = {}
        for i in range(0, len(ids), 50):
            r = youtube.videos().list(part="status", id=",".join(ids[i:i+50])).execute()
            for item in r.get("items", []):
                found[item["id"]] = item["status"]["privacyStatus"]
        for vid in ids:
            print(f"{vid} {found.get(vid, 'missing')}")
        return

    if args.retire:
        for vid in args.retire:
            set_privacy(youtube, vid, "private")
        return
    if args.publish:
        set_privacy(youtube, args.publish, "public")
        return
    if not args.meta:
        p.error("--meta is required unless using --publish")

    meta = json.loads(Path(args.meta).read_text())
    upload(youtube, meta, args.privacy)


if __name__ == "__main__":
    main()
