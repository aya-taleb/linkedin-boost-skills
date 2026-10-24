#!/usr/bin/env python3
"""Keep one post log per business: posts.csv in the business folder.

linkedin-post adds a row when the user says they posted. linkedin-plan reads it to rotate
topics. linkedin-audit reads it once the user fills in the numbers from LinkedIn analytics.

Usage:
  python3 postlog.py add  --log posts.csv --date 2026-10-23 --type proof \
      --topic "office lunch" --pattern number --first-line "We delivered 212 lunches..."
  python3 postlog.py list --log posts.csv [--last 10]
  python3 postlog.py save --from draft.md --to ~/.founder/social/linkedin/<slug>/drafts/x.md

save copies a draft you wrote in the project into the business folder, making folders as
needed. It never overwrites a file unless you pass --force. A path starting with ~/.founder
goes to $FOUNDER_HOME instead when that is set (tests use this).

Columns (keep this order, the other skills read it):
  date, type, topic, pattern, first_line, chars, impressions, reactions, comments,
  reposts, saves, sends
Numbers stay blank until the user types them in. Never fill them with guesses.
Standard library only.
"""
import argparse
import csv
import os
import sys

COLUMNS = ["date", "type", "topic", "pattern", "first_line", "chars",
           "impressions", "reactions", "comments", "reposts", "saves", "sends"]


def read_rows(path):
    if not os.path.exists(path):
        return []
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def add_row(path, row):
    exists = os.path.exists(path) and os.path.getsize(path) > 0
    folder = os.path.dirname(os.path.abspath(path))
    os.makedirs(folder, exist_ok=True)
    clean = {c: str(row.get(c, "") or "").replace("\n", " ").strip() for c in COLUMNS}
    with open(path, "a", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=COLUMNS)
        if not exists:
            writer.writeheader()
        writer.writerow(clean)
    return clean


def resolve(path):
    """Expand ~ and, when FOUNDER_HOME is set, map a leading ~/.founder onto it.

    User data lives in ~/.founder (Claude Code protects ~/.claude). Tests set FOUNDER_HOME.
    """
    env = os.environ.get("FOUNDER_HOME")
    norm = path.replace("\\", "/")
    if env and (norm == "~/.founder" or norm.startswith("~/.founder/")):
        path = os.path.join(os.path.expanduser(env), norm[len("~/.founder/"):])
    return os.path.expanduser(path)


def save_draft(src, dest, force=False):
    """Copy a draft into the business folder, making folders. Refuses to overwrite."""
    dest = resolve(dest)
    if os.path.exists(dest) and not force:
        raise FileExistsError(dest)
    with open(src, encoding="utf-8") as fh:
        text = fh.read()
    os.makedirs(os.path.dirname(os.path.abspath(dest)), exist_ok=True)
    with open(dest, "w", encoding="utf-8") as fh:
        fh.write(text)
    return dest


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add")
    a.add_argument("--log", required=True)
    a.add_argument("--date", required=True)
    a.add_argument("--type", default="")
    a.add_argument("--topic", default="")
    a.add_argument("--pattern", default="")
    a.add_argument("--first-line", default="")
    a.add_argument("--chars", default="")
    ls = sub.add_parser("list")
    ls.add_argument("--log", required=True)
    ls.add_argument("--last", type=int, default=10)
    sv = sub.add_parser("save")
    sv.add_argument("--from", dest="src", required=True)
    sv.add_argument("--to", dest="dest", required=True)
    sv.add_argument("--force", action="store_true")
    args = parser.parse_args(argv)
    if args.cmd == "save":
        try:
            print("saved: %s" % save_draft(args.src, args.dest, args.force))
        except FileExistsError as exc:
            print("exists, not overwritten (add --force): %s" % exc)
            return 1
        return 0
    if args.cmd == "add":
        row = add_row(resolve(args.log), {
            "date": args.date, "type": args.type, "topic": args.topic,
            "pattern": args.pattern, "first_line": args.first_line, "chars": args.chars,
        })
        print("logged: %s | %s | %s" % (row["date"], row["topic"], row["first_line"][:60]))
        return 0
    rows = read_rows(resolve(args.log))
    for row in rows[-args.last:]:
        print("%s | %-8s | %-20s | %s" % (row.get("date", ""), row.get("type", ""),
                                          row.get("topic", "")[:20], row.get("first_line", "")[:60]))
    if not rows:
        print("no posts logged yet")
    return 0


if __name__ == "__main__":
    sys.exit(main())
