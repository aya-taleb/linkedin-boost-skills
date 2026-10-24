#!/usr/bin/env python3
"""Score LinkedIn hook lines (line 1 of a post) on six local checks, 0 to 100.

The checks, and why each one is there:
  FOLD      15  Does it fit before "see more" on a phone (about 140 characters)?
                A hook that gets cut off is not a hook.
  CONCRETE  25  Numbers, money, times, names. Specific lines get read; vague ones scroll by.
  TENSION   20  A gap the reader wants closed: a change, a cost, a "but", a refusal.
  PERSON    10  A person is in it: "I", "we", or "you". Feeds are people talking to people.
  PLAIN     20  No stock phrases and few vague words. Readers skip lines that sound like ads.
  NO BAIT   10  No "Agree?" or "comment below". LinkedIn and readers both discount it.

Optional:
  --topics "lunch,offices,street food"   reports topic fit for the active business (no points,
                                         a hook can be on topic without using the word)
  --avoid  "cheap,hack"                   extra banned words from founder-context; each hit
                                         costs PLAIN points like stock phrases do

These are heuristics written for this repo. They rank options; they do not predict reach.

Usage:
  python3 hookscore.py hooks.txt                 # one hook per line, ranked
  python3 hookscore.py --line "I quit my job..." # score one
  python3 hookscore.py hooks.txt --json
Standard library only.
"""
import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FOLD_MOBILE = 140
FOLD_DESKTOP = 210

WEIGHTS = {"fold": 15, "concrete": 25, "tension": 20, "person": 10, "plain": 20, "no_bait": 10}

NUMBER = re.compile(r"(?<![\w{])(\$|€|£)?\d[\d,.]*(k|m|%|x)?(?![\w}])", re.I)
WORDNUM = re.compile(r"\b(two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|"
                     r"twenty|thirty|forty|fifty|hundred|thousand|million|half|once|twice)\b", re.I)
PLACEHOLDER = re.compile(r"\{\{[^}]+\}\}")
PERSON = re.compile(r"\b(i|i'm|i've|i'd|my|me|we|we're|we've|our|us|you|you're|your)\b", re.I)


def load_words(path=None):
    with open(path or os.path.join(HERE, "hook_words.json"), encoding="utf-8") as fh:
        return json.load(fh)


def phrase_hits(text, phrases):
    low = " " + text.lower() + " "
    hits = []
    for p in phrases:
        if p.endswith("?"):
            if p in low:
                hits.append(p)
            continue
        pattern = r"(?<![a-z0-9'])" + re.escape(p) + r"(?![a-z0-9'])"
        if re.search(pattern, low):
            hits.append(p)
    return hits


def proper_nouns(text):
    """Capitalised words that are not the first word of a sentence and not 'I'."""
    words = re.findall(r"[A-Za-z][\w'&-]*", text)
    found = []
    sentence_start = True
    for token in re.findall(r"[A-Za-z][\w'&-]*|[.!?]", text):
        if token in ".!?":
            sentence_start = True
            continue
        if not sentence_start and token[0].isupper() and token not in ("I", "I'm", "I've", "I'd"):
            found.append(token)
        sentence_start = False
    return found if words else []


def score_fold(n):
    if n <= 110:
        return 1.0
    if n <= FOLD_MOBILE:
        return 0.8
    if n <= FOLD_DESKTOP:
        return 0.35
    return 0.0


def score(line, words=None, topics=None, avoid=None):
    words = words or load_words()
    text = " ".join(line.strip().split())
    n = len(text)
    notes = []
    parts = {}

    parts["fold"] = score_fold(n)
    if n > FOLD_MOBILE:
        notes.append("%d characters: cut off on mobile (about %d show)" % (n, FOLD_MOBILE))

    numbers = NUMBER.findall(text)
    num_count = len(numbers) + len(WORDNUM.findall(text))
    placeholders = PLACEHOLDER.findall(text)
    times = phrase_hits(text, words["time"])
    names = proper_nouns(text)
    concrete = 0.0
    if num_count or placeholders:
        concrete += 0.6
    if times:
        concrete += 0.25
    if names:
        concrete += 0.25
    parts["concrete"] = min(concrete, 1.0)
    if placeholders:
        notes.append("has a placeholder: fill %s with a real number before posting"
                     % ", ".join(placeholders))
    if not (num_count or placeholders or times or names):
        notes.append("nothing concrete: add a number, a time or a name")

    tension = phrase_hits(text, words["tension"])
    question = text.endswith("?")
    t = 0.0
    if tension:
        t = 0.7 if len(tension) == 1 else 1.0
    if question and (num_count or names):
        t = max(t, 0.7)
    elif question:
        t = max(t, 0.3)
        notes.append("a vague question; make it one only you could ask")
    parts["tension"] = t
    if not t:
        notes.append("no tension: what changed, what it cost, or what went wrong?")

    parts["person"] = 1.0 if PERSON.search(text) else 0.0

    stock = phrase_hits(text, words["stock"] + [w.strip().lower() for w in (avoid or []) if w.strip()])
    vague = phrase_hits(text, words["vague"])
    plain = 1.0 - 0.5 * len(stock) - 0.15 * len(vague)
    long_words = [w for w in re.findall(r"[A-Za-z]+", text) if len(w) >= 13]
    plain -= 0.1 * len(long_words)
    parts["plain"] = max(plain, 0.0)
    if stock:
        notes.append("stock phrase: " + ", ".join(stock))
    if vague:
        notes.append("vague word: " + ", ".join(vague))

    bait = phrase_hits(text, words["bait"])
    parts["no_bait"] = 0.0 if bait else 1.0
    if bait:
        notes.append("engagement bait: " + ", ".join(bait))

    total = round(sum(WEIGHTS[k] * parts[k] for k in WEIGHTS))
    topic_hits = phrase_hits(text, [t.strip().lower() for t in (topics or []) if t.strip()])
    return {
        "hook": text,
        "score": total,
        "chars": n,
        "parts": {k: round(WEIGHTS[k] * parts[k], 1) for k in WEIGHTS},
        "topic_words": topic_hits,
        "notes": notes,
    }


def rank(lines, **kw):
    words = load_words()
    results = [score(l, words=words, **kw) for l in lines if l.strip() and not l.lstrip().startswith("#")]
    return sorted(results, key=lambda r: -r["score"])


def render(results):
    out = []
    for i, r in enumerate(results, 1):
        p = r["parts"]
        out.append("%d. %3d  %s" % (i, r["score"], r["hook"]))
        out.append("        fold %s  concrete %s  tension %s  person %s  plain %s  no-bait %s  (%d chars)"
                   % (p["fold"], p["concrete"], p["tension"], p["person"], p["plain"], p["no_bait"], r["chars"]))
        if r["topic_words"]:
            out.append("        on topic: " + ", ".join(r["topic_words"]))
        for note in r["notes"]:
            out.append("        - " + note)
    return "\n".join(out)


def split_list(value):
    return [v for v in (value or "").split(",") if v.strip()]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("file", nargs="?", help="text file, one hook per line")
    parser.add_argument("--line", action="append", help="score this line (repeatable)")
    parser.add_argument("--topics", default="")
    parser.add_argument("--avoid", default="")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    lines = list(args.line or [])
    if args.file:
        with open(args.file, encoding="utf-8") as fh:
            lines += fh.read().splitlines()
    if not lines:
        parser.error("give a file or --line")
    results = rank(lines, topics=split_list(args.topics), avoid=split_list(args.avoid))
    print(json.dumps(results, indent=2) if args.json else render(results))
    return 0


if __name__ == "__main__":
    sys.exit(main())
