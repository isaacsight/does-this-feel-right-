#!/usr/bin/env python3
"""meeting-search — full-text search over every meeting transcript.

  meeting-search <query>          search all transcripts (FTS5)
  meeting-search --reindex        rebuild the index from ~/Meetings

Index lives at ~/Meetings/.index.db. Reindex is incremental-cheap
(full rebuild each run; transcript corpus is small text).
"""
import os
import sqlite3
import sys
import glob

ROOT = os.path.expanduser("~/Meetings")
DB = os.path.join(ROOT, ".index.db")


def reindex():
    con = sqlite3.connect(DB)
    con.execute("DROP TABLE IF EXISTS seg")
    con.execute(
        "CREATE VIRTUAL TABLE seg USING fts5(meeting, file, line, text)"
    )
    n = 0
    patterns = ["*/transcript.txt", "*/transcript-speakers.txt", "live/*.txt"]
    for pat in patterns:
        for path in glob.glob(os.path.join(ROOT, pat)):
            meeting = os.path.relpath(path, ROOT).split(os.sep)[0]
            if meeting == "live":
                meeting = "live/" + os.path.basename(path).rsplit(".", 1)[0]
            with open(path, errors="replace") as f:
                for i, line in enumerate(f, 1):
                    line = line.strip()
                    if line:
                        con.execute(
                            "INSERT INTO seg VALUES (?,?,?,?)",
                            (meeting, path, i, line),
                        )
                        n += 1
    con.commit()
    con.close()
    print(f"indexed {n} lines from {ROOT}")


def search(query):
    if not os.path.exists(DB):
        reindex()
    con = sqlite3.connect(DB)
    rows = con.execute(
        "SELECT meeting, line, snippet(seg, 3, '>>', '<<', '…', 18) "
        "FROM seg WHERE seg MATCH ? ORDER BY rank LIMIT 25",
        (query,),
    ).fetchall()
    if not rows:
        print("no matches (try --reindex if transcripts are new)")
        return
    for meeting, line, snip in rows:
        print(f"{meeting}:{line}  {snip}")


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print(__doc__.strip())
    elif args[0] == "--reindex":
        reindex()
    else:
        search(" ".join(args))
