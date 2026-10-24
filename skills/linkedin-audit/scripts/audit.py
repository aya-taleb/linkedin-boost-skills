#!/usr/bin/env python3
"""Rank a business's LinkedIn posts against the account's own normal, from numbers the user exported.

Reads posts.csv (written by linkedin-post's postlog.py, numbers filled in by the user) or
any CSV with similar columns, for example a copy of LinkedIn's post analytics export.

For each post:
  engagement   reactions + comments + reposts (+ saves + sends when present)
  rate         engagement / impressions
  vs median    rate / the median rate of all posts with impressions in this file
  weighted     comments count 3x, reposts 2x, saves and sends 2x: they mean more than a tap
Then groups by type, topic, pattern and length band so the skill can say what the top posts share.

Usage:
  python3 audit.py posts.csv
  python3 audit.py posts.csv --json
  python3 audit.py posts.csv --since 2026-08-01
Rows with blank impressions are listed as "no numbers yet" and left out of the math.
Standard library only.
"""
import argparse
import csv
import json
import statistics
import sys

ALIASES = {
    "date": ["date", "created", "post date", "published"],
    "type": ["type", "post type", "format"],
    "topic": ["topic", "theme", "pillar"],
    "pattern": ["pattern", "hook", "hook pattern"],
    "first_line": ["first_line", "first line", "post", "post title", "text", "commentary"],
    "chars": ["chars", "characters", "length"],
    "impressions": ["impressions", "views"],
    "reactions": ["reactions", "likes"],
    "comments": ["comments"],
    "reposts": ["reposts", "shares"],
    "saves": ["saves"],
    "sends": ["sends", "sends on linkedin"],
}
MIN_SAMPLE = 8


def to_num(value):
    if value is None:
        return None
    text = str(value).replace(",", "").strip()
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def load(path):
    with open(path, newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        headers = {h.strip().lower(): h for h in (reader.fieldnames or [])}
        cols = {}
        for k, names in ALIASES.items():
            cols[k] = next((headers[n] for n in names if n in headers), None)
        rows = []
        for raw in reader:
            row = {k: (raw.get(c) or "").strip() if c else "" for k, c in cols.items()}
            rows.append(row)
    return rows


def length_band(row):
    n = to_num(row.get("chars"))
    if n is None:
        return ""
    if n < 600:
        return "short (<600)"
    if n < 1300:
        return "medium (600-1299)"
    return "long (1300+)"


def analyse(rows, since=None):
    scored, pending = [], []
    for row in rows:
        if since and row.get("date") and row["date"] < since:
            continue
        imp = to_num(row.get("impressions"))
        if not imp:
            pending.append(row)
            continue
        parts = {k: to_num(row.get(k)) or 0 for k in ("reactions", "comments", "reposts", "saves", "sends")}
        eng = sum(parts.values())
        weighted = (parts["reactions"] + 3 * parts["comments"] + 2 * parts["reposts"]
                    + 2 * parts["saves"] + 2 * parts["sends"])
        scored.append(dict(row, engagement=eng, rate=eng / imp, weighted_rate=weighted / imp,
                           impressions_n=imp, band=length_band(row)))
    if not scored:
        return {"posts": [], "pending": pending, "median_rate": None, "groups": {}, "warnings":
                ["no posts with impressions yet; fill in numbers from LinkedIn analytics first"]}
    med = statistics.median(p["rate"] for p in scored)
    med_imp = statistics.median(p["impressions_n"] for p in scored)
    for p in scored:
        p["vs_median"] = p["rate"] / med if med else None
        p["reach_vs_median"] = p["impressions_n"] / med_imp if med_imp else None
    scored.sort(key=lambda p: -p["weighted_rate"])
    groups = {}
    for field in ("type", "topic", "pattern", "band"):
        buckets = {}
        for p in scored:
            label = p.get(field) or "(blank)"
            buckets.setdefault(label, []).append(p["rate"])
        groups[field] = {k: {"posts": len(v), "median_rate": statistics.median(v)} for k, v in buckets.items()}
    warnings = []
    if len(scored) < MIN_SAMPLE:
        warnings.append("only %d posts with numbers; treat patterns as hints, not findings" % len(scored))
    return {"posts": scored, "pending": pending, "median_rate": med, "median_impressions": med_imp,
            "groups": groups, "warnings": warnings}


def pct(x):
    return "%.1f%%" % (100 * x)


def render(res):
    out = []
    if res["median_rate"] is None:
        return "\n".join(res["warnings"])
    out.append("%d posts with numbers | median engagement rate %s | median impressions %d"
               % (len(res["posts"]), pct(res["median_rate"]), res["median_impressions"]))
    out.append("")
    out.append("rank  rate    x median  reach x  weighted  date        type      first line")
    for i, p in enumerate(res["posts"], 1):
        out.append("%4d  %-6s  %-8s  %-7s  %-8s  %-10s  %-8s  %s" % (
            i, pct(p["rate"]), "%.2f" % p["vs_median"], "%.2f" % p["reach_vs_median"],
            pct(p["weighted_rate"]), p.get("date", ""), (p.get("type") or "")[:8],
            (p.get("first_line") or "")[:50]))
    for field, buckets in res["groups"].items():
        out.append("")
        out.append("by %s:" % field)
        for label, b in sorted(buckets.items(), key=lambda kv: -kv[1]["median_rate"]):
            out.append("  %-24s %2d posts  median %s" % (label[:24], b["posts"], pct(b["median_rate"])))
    if res["pending"]:
        out.append("")
        out.append("no numbers yet: %d posts" % len(res["pending"]))
    for w in res["warnings"]:
        out.append("warning: " + w)
    return "\n".join(out)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("file")
    parser.add_argument("--since")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    res = analyse(load(args.file), since=args.since)
    if args.json:
        print(json.dumps(res, indent=2, default=str))
    else:
        print(render(res))
    return 0


if __name__ == "__main__":
    sys.exit(main())
