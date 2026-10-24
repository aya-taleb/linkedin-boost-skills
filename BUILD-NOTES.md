# Build notes

Built 2026-10-23, unattended. What is not finished, what needs Aya, and the calls she
should look at. Test numbers are in TESTING.md.

## Not finished

- Synced skills are not in the repo yet: humanize and founder-context (home
  entrepreneur-skills), transcribe and talking-head-cards (home multimedia-skills). They
  are listed in skills.json and arrive with the sync step. Until then every skill falls back
  to `references/writing-check.md` and says so in its output.
- humanize and founder-context showed up in entrepreneur-skills near the end of this build,
  but no test run here had them installed. Every run used the by-hand writing check. Rerun
  linkedin-post and linkedin-dm once the sync step copies them in.
- linkedin-repurpose stopped for time before the two-round plateau (r3 +6, r4 -5, r4
  reverted). It beats Jake's baseline (82 vs 62), but it still adds small framing lines on
  short sources.
- LinkedIn Help pages block automated reading, so every limit in `references/limits.md`
  comes from third-party pages that quote or measure LinkedIn. Worth a 5-minute check by
  hand on linkedin.com/help (invitation note length, free-account note cap, document limits).

## Needs Aya

- **Default daily invite limit.** linkedin-dm defaults to 5 a day and stops at 50 a week (Aya's call, Oct 24; was 15 and 100).
  If Aya has Premium or Sales Navigator, she may want a different number; it is one flag
  (`--limit`).
- **The weighted rate in linkedin-audit** (comments 3x; reposts, saves, sends 2x) is our
  judgment, not LinkedIn's. Keep it, change it, or drop to the plain rate.
- **warm-leads.csv vs sales/leads.csv.** People who comment or message go to a LinkedIn-only
  `warm-leads.csv` in the business folder. Should biz-boost's lead-gen merge them into
  `sales/leads.csv`? That would need a call in biz-boost.
- **Resolved: no more writes to `~/.claude/`.** Claude Code asks before writing there.
  The fix round moved every business folder to `~/.founder/social/linkedin/<business>/`
  (CONVENTIONS section 5), so saves no longer prompt.
- **linkedin-dm is the home of a shared skill.** biz-boost gets a synced copy. Any fix goes
  here first.

## Calls to review

- Scores are self-graded and noisy (one run per case per round). Five skills had their last
  round reverted after a drop: hooks, plan, reply, repurpose, profile. Shipped files were
  checked line by line against the version each final score measured.

- linkedin-post shows two fold previews (mobile and desktop) from a local tool. The numbers
  are observed values, not LinkedIn's, and the tool says so with a date.
- linkedin-hooks uses our own six checks and eight patterns. The weights are a first guess.
  linkedin-audit can compare hook scores with real results later and tell us if they help.
- linkedin-carousel's PDF is plain (built-in font, no images) so it needs no design app.
  The skill also writes a design brief for Canva or Figma.
- Test harness choices (sandbox HOME, Jake's tools not run, regrading with one grader
  version) are in TESTING.md under "Calls I made".

## Fix round after review

- User data moved out of `~/.claude` (protected by Claude Code) to `~/.founder`: business files, social folders and the media ledger. Tools honor `FOUNDER_HOME`; tests use a temp one.
- linkedin-dm: `dmqueue.py pick` skips leads with an empty `linkedin_url` and reports a missing column (tests added); the skill names its next step (`/follow-up` from biz-boost, `/linkedin-plan`, or `/call-prep`). lunch-leads-batch eval gained a no-link lead and a next-skill grader.
- `postlog.py` maps `~/.founder/...` onto `FOUNDER_HOME` (test added). Eval fixtures moved to `files/home/.founder`.
