# Testing

How these numbers were made, said once and plainly: every score here comes from my own
test runs, graded by a separate model pass. They are not user results.

- **Runs.** Each case ran blind with headless Claude (`claude -p`) in a fresh sandbox
  folder with a sandbox `HOME`. The run saw only the installed skills, a made-up
  founder-context for two test businesses (Lunch Lane, a street food lunch subscription,
  and Frameleaf, a kids' story video app), and the case's input files. It did not see
  this file, the job specs' tests, or the graders.
- **Grading.** A second, separate Claude pass with no tools read the case, the grader
  statements, the skill's SKILL.md, the run's transcript and the files it wrote, and
  marked each grader pass or fail with evidence. It also scored rules, made-up facts,
  tone and handoff. Trigger fit came from a third blind pass that routed the 12 prompts
  in `evals/triggers.json` across all skills in the repo (or all of Jake's) plus a few
  neighbours from Aya's other repos.
- **Rubric.** TEST-PROTOCOL.md section 2: graders 40, own rules 15, nothing made up 15,
  tone 10, handoff 10, trigger fit 10. Rules and made-up use the worst case of the three
  (one slip anywhere costs), tone and handoff use the average.
- **Baselines.** Reworked and rewritten skills: Jake Schincariol's li- skill run on the
  same 3 cases. His Python tools were not installed, because we never run upstream code,
  and the run was told to do those steps by hand. His skills read a `voice.md` that held
  the same two business files ours read, so both had the same facts. Ours (linkedin-hooks,
  linkedin-viral): no skill at all, scored out of the 90 non-trigger points and scaled
  to 100.
- **Noise.** Each case ran once per round, so a score can move a few points from run to
  run with no change to the skill. Treat gaps under about 5 points as a tie.
- **Rerun.** Aya can rerun any case with `claude plugin eval`. Cases that need
  `~/.claude` state put it in `files/home/`; `place-files.sh` copies it into `$HOME` only
  when `EVAL_SANDBOX_HOME=1` is set, so a rerun never touches a real `~/.claude` by
  accident.

Run outputs are under `/home/claude/build/_work/linkedin-boost-skills/<skill>/round-N/`
on the build machine and are not part of the repo.

## Results

| skill | status | baseline | final | rounds | beats baseline? |
| --- | --- | --- | --- | --- | --- |
| linkedin-post | reworked | 52 | 86 | 4 | yes |
| linkedin-plan | reworked | 73 | 88 | 5 | yes |
| linkedin-hooks | ours | 53 | 93 | 5 | yes |
| linkedin-dm | reworked | 58 | 85 | 4 | yes |
| linkedin-viral | ours | 48 | 89 | 5 | yes |
| linkedin-comment | rewritten | 61 | 92 | 4 | yes |
| linkedin-reply | rewritten | 67 | 91 | 4 | yes |
| linkedin-inbox | rewritten | 66 | 89 | 3 | yes |
| linkedin-carousel | rewritten | 69 | 89 | 4 | yes |
| linkedin-repurpose | rewritten | 62 | 82 | 4 | yes |
| linkedin-profile | rewritten | 61 | 86 | 4 | yes |
| linkedin-audit | rewritten | 71 | 90 | 4 | yes |

Baselines: reworked and rewritten skills are measured against Jake Schincariol's li- skill on the same cases; linkedin-hooks and linkedin-viral against no skill. "final" is the shipped version's score, which is the best of several noisy runs for some skills (see Noise above and Calls I made).


## Per skill

```
### linkedin-post  (reworked)
baseline: 52 (Jake's li-post on the same 3 cases, his Python tools not installed; graders 7/15)
final: 86 (shipped version: r4) after 4 rounds. Stopped because r3 (-6) and r4 (+4) were both under +5 (plateau rule).
rounds:
- r1: 83 (+31), graders 14/15. v1: founder-context business pick, scored hooks, fold.py preview, posts.csv log, invented-framing rule, show fold previews in the reply
- r2: 88 (+5), graders 14/15. no derived numbers or 'we never pitched' claims, name the business even when refusing, rescore reworded hooks, name the next skill; tool paths from the skill folder
- r3: 82 (-6), graders 13/15. at most one or two file facts per post, fix a desktop preview that ends badly
- r4: 86 (+4), graders 14/15. refusal section (say no first, user posts, password not repeated), fold re-run on final text, proof is not a promise
open issues: a few runs still add a short framing line the user did not say
```

```
### linkedin-plan  (reworked)
baseline: 73 (Jake's li-plan, same 3 cases, his log and voice file given in his own folder; graders 10/14)
final: 88 (shipped version: r4) after 5 rounds. Stopped because r4 (+2) and r5 (-7) were both under +5. r5's changes were reverted, so the shipped skill is the r4 version (88).
rounds:
- r1: 83 (+10), graders 12/14. v1: one plan per business, topic rotation from posts.csv, weekly budget across ventures, no invented people
- r2: 81 (-2), graders 12/14. say 'you post it' in the close, use the news across slots and label slots from the file, thin-week plan still written, keep 'this week' as this week
- r3: 86 (+5), graders 13/14. no change to the skill; rerun to check noise after the r2 drop
- r4: 88 (+2), graders 13/14. refusal section for schedule or auto-post requests
- r5: 81 (-7), graders 12/14. news carried across most slots of its business, 'this week' stays this week even if short, no added order of events (reverted after the round)
open issues: the 'this week vs next week' call is inconsistent when the request comes on a Friday
```

```
### linkedin-hooks  (ours)
baseline: 53 (no skill, plain answer; graders 6/12)
final: 93 (shipped version: r4) after 5 rounds. Stopped because r4 (+1) and r5 (-14) were both under +5. r5's change was reverted, so the shipped skill is the r4 version (93).
rounds:
- r1: 74 (+21), graders 11/12. v1: hookscore.py with six own checks, eight own patterns, business topics and avoid words
- r2: 77 (+3), graders 11/12. no pictured scenes, feelings or derived numbers in hooks, confirm facts in the user's own hooks, handoff line even when asking
- r3: 92 (+15), graders 12/12. habits and opinions count as made up, pick the top scorer or say why not; hookscore.py tension words widened (late, missed, broke, ran out...) after the tool under-scored plain lateness hooks, with a new unit test; hooks.md heading uses a comma
- r4: 93 (+1), graders 12/12. no change; rerun to check the r3 jump holds
- r5: 79 (-14), graders 10/12. save only what was shown, same labels (reverted after the round)
open issues: hookscore.py's word lists are a first guess; check them against real results with linkedin-audit
```

```
### linkedin-dm  (reworked)
baseline: 58 (Jake's li-dm, same 3 cases; graders 6/14)
final: 85 (shipped version: r4) after 4 rounds. Stopped because r3 (+3) and r4 (+0) were both under +5 (plateau rule).
rounds:
- r1: 78 (+20), graders 12/14. v1: dmqueue.py pick/mark/due/count, daily limit 15 and weekly 100, shared sales/leads.csv layout filtered by business_slug, status and last_contact update
- r2: 82 (+4), graders 14/14. invite note says who you are, not what you sell; first message counted to 4 sentences; always run 'due'; follow-ups only add real new facts
- r3: 85 (+3), graders 13/14. no 'what customers usually say' claims; product description allowed after accept
- r4: 85 (+0), graders 14/14. refusal section (say no first, user sends by hand, the log is not automation); run to check the change
open issues: first messages sometimes include a general claim about customers
```

```
### linkedin-viral  (ours)
baseline: 48 (no skill, plain answer; graders 5/12)
final: 89 (shipped version: r5) after 5 rounds. Stopped because r4 (+6) then r5 (-1); stopped at r5 because 90 vs 89 is a tie and the remaining failures were small style notes. r5's change is kept.
rounds:
- r1: 77 (+29), graders 11/12. v1: pasted or exported posts only, size-fair comparison, breakdown block, swipe file with short excerpts, adapt with own proof
- r2: 78 (+1), graders 11/12. no numbers or events in example hooks, swipe file follows writing rules, no performance promises
- r3: 84 (+6), graders 11/12. description covers comparing two own posts, name the business first
- r4: 90 (+6), graders 12/12. say plainly when the sample is under 5 posts, no guessing causes of numbers
- r5: 89 (-1), graders 12/12. 'why it worked' limited to visible text, no guessed tone or causes
open issues: none
```

```
### linkedin-comment  (rewritten)
baseline: 61 (Jake's li-comment on the same 3 cases, his Python tools not installed; graders 7/12)
final: 92 (shipped version: r4) after 4 rounds. Stopped because r3 (-1) and r4 (+1) were both under +5. r4 made no change, so it is a repeat run of the r3 skill.
rounds:
- r1: 67 (+6), graders 8/12. v1 from the job spec in references/job-spec.md
- r2: 92 (+25), graders 12/12. sensitive posts get one short note or a skip, no experience job without proof, no service description, always name next step
- r3: 91 (-1), graders 12/12. general claims as a view or a question, not fact
- r4: 92 (+1), graders 12/12. no change to the skill, repeat run to check the plateau
open issues: none
```

```
### linkedin-reply  (rewritten)
baseline: 67 (Jake's li-reply on the same 3 cases, his Python tools not installed; graders 9/13)
final: 91 (shipped version: r3) after 4 rounds. Stopped because r3 (+1) and r4 (-6) were both under +5. r4's change was reverted, so the shipped skill is the r3 version (91).
rounds:
- r1: 80 (+13), graders 12/13. v1 from the job spec in references/job-spec.md
- r2: 90 (+10), graders 13/13. replies capped at 3 sentences, kind words are not leads, critics answered with existing facts only
- r3: 91 (+1), graders 13/13. no unsourced estimates even in refusals
- r4: 85 (-6), graders 11/13. say plainly when pricing is not set (reverted after the round)
open issues: none
```

```
### linkedin-inbox  (rewritten)
baseline: 66 (Jake's li-inbox on the same 3 cases, his Python tools not installed; graders 8/13)
final: 89 (shipped version: r3) after 3 rounds. Stopped because r2 (+1) and r3 (+4) were both under +5.
rounds:
- r1: 84 (+18), graders 13/13. v1 from the job spec in references/job-spec.md
- r2: 85 (+1), graders 12/13. no commitments the founder did not make, name next skill, never claim placeholders are filled
- r3: 89 (+4), graders 13/13. drafts 2 to 4 sentences counted; only real buy, partner or invest asks are leads + log each lead in its own business's folder; describe the business only in its file's words (one round: the first r3 run read mixed old and new inputs and was discarded, see Calls I made)
open issues: none
```

```
### linkedin-carousel  (rewritten)
baseline: 69 (Jake's li-carousel on the same 3 cases, his Python tools not installed; graders 9/12)
final: 89 (shipped version: r4) after 4 rounds. Stopped because r3 (+3) and r4 (+0) were both under +5.
rounds:
- r1: 83 (+14), graders 11/12. v1 from the job spec in references/job-spec.md
- r2: 86 (+3), graders 11/12. one action on the last slide, no claims about what people think, no persona, rerun fold after edits
- r3: 89 (+3), graders 12/12. no added facts about people in the user's story
- r4: 89 (+0), graders 12/12. post length range written as approximate
open issues: none
```

```
### linkedin-repurpose  (rewritten)
baseline: 62 (Jake's li-repurpose on the same 3 cases, his Python tools not installed; graders 6/13)
final: 82 (shipped version: r3) after 4 rounds. Stopped because r3 (+6) then r4 (-5). I reverted r4 and shipped the r3 version (82). Not at the two-round plateau; stopped for time. Biggest gap left: drafts still add small framing lines and bundle facts on short sources.
rounds:
- r1: 76 (+14), graders 11/13. v1 from the job spec in references/job-spec.md
- r2: 76 (+0), graders 11/13. no added story details or promises, one idea per post means cutting a second fact
- r3: 82 (+6), graders 12/13. length follows the source (400 to 1,300), line-by-line source check before showing, rerun fold + no business-file facts added to repurposed posts (one round: the first r3 run read mixed old and new inputs and was discarded, see Calls I made)
- r4: 77 (-5), graders 11/13. short sources give fewer posts, no round-up posts, source line names where each claim came from (reverted after the round)
open issues: drafts sometimes add small framing lines or bundle several facts when the source is short
```

```
### linkedin-profile  (rewritten)
baseline: 61 (Jake's li-profile on the same 3 cases, his Python tools not installed; graders 7/13)
final: 86 (shipped version: r3) after 4 rounds. Stopped because r3 (-3) and r4 (-3) were both under +5. r4 was reverted; the shipped version is r3 (86). r2 scored 89, but r3 added the 'titles exactly as given' and 'lead business first' rules after a real title-swap failure, so I kept r3.
rounds:
- r1: 77 (+16), graders 11/13. v1 from the job spec in references/job-spec.md
- r2: 89 (+12), graders 13/13. no invented buyer pains, keep facts as written, always save profile.md, say which cleanup
- r3: 86 (-3), graders 13/13. full text in profile.md, not a pointer + every headline option names the lead business first; titles used exactly as given (one round: the first r3 run read mixed old and new inputs and was discarded, see Calls I made)
- r4: 83 (-3), graders 11/13. always save profile.md when any rewrite is written (reverted after the round)
open issues: headline options do not always lead with the business name
```

```
### linkedin-audit  (rewritten)
baseline: 71 (Jake's li-audit on the same 3 cases, his Python tools not installed; graders 9/13)
final: 90 (shipped version: r4) after 4 rounds. Stopped because r3 (+3) and r4 (-1) were both under +5.
rounds:
- r1: 88 (+17), graders 13/13. v1 from the job spec in references/job-spec.md
- r2: 88 (+0), graders 12/13. copy the script's ranking instead of re-ranking, confirm audit.md exists
- r3: 91 (+3), graders 13/13. bottom 3 are the script's last rows; eval fix: one grader's expected rate corrected to 12.5%
- r4: 90 (-1), graders 13/13. no change to the skill, repeat run to check the plateau
open issues: none
```

## Calls I made

- "See more" cutoffs: LinkedIn does not publish them. We use about 3 lines or 140 characters on mobile and about 5 lines or 210 on desktop (3 lines for posts with media), from four third-party pages checked 2026-10-23 (sources in references/limits.md). LinkedIn Help pages block automated reading, so they could not be checked directly.
- Invitation note limit: 200 characters (it used to be 300), and free accounts get about 3 personalized notes a month, per Hublead's reading of LinkedIn Help on 2026-09-19.
- Daily invite limit: default 5 a day and a hard stop at 50 a week (changed Oct 24 from 15 and 100). LinkedIn publishes no number; 100 a week is a widely observed ceiling, and 15 a day leaves room. The tool warns above 20.
- humanize and founder-context did not exist yet in entrepreneur-skills, so every skill calls humanize when installed and otherwise follows references/writing-check.md by hand, and says which it used.
- Per-business folder ~/.founder/social/linkedin/<slug>/ holds posts.csv, plan.md, drafts/, hooks.md, swipe.md, outreach.csv, warm-leads.csv, comments.md, inbox.md, carousels/, profile.md, audit.md. posts.csv is the one log every skill shares; its column order is fixed in postlog.py.
- warm-leads.csv (from reply and inbox) is a LinkedIn-only file with columns date,name,role,company,source,reason,status. It is not sales/leads.csv, because those people came to us and have no fit score yet. Aya may want lead-gen to merge it later.
- linkedin-dm reads the shared sales/leads.csv layout (CONVENTIONS section 5), keeps only rows for the active business_slug, always skips do-not-contact, and treats contacted, replied, meeting, won and lost as already in progress. Rows with an empty business_slug are skipped with a note, not guessed. After the user confirms a send, `dmqueue.py mark --leads` sets status to contacted (or replied) and last_contact; the skill asks before changing the file.
- linkedin-profile and linkedin-inbox read every business file, because one profile and one inbox serve all ventures. The other skills work on one business at a time.
- linkedin-carousel builds the PDF with our own stdlib writer (built-in Helvetica, square 1080 pages). It is plain on purpose; the skill also writes a design brief for Canva or Figma.
- linkedin-audit's weighted rate counts comments 3x and reposts, saves and sends 2x. This is our judgment about what signals interest, not a LinkedIn formula, and the skill says so.
- Baseline fairness: Jake's skills read ~/.claude/linkedin/voice.md and log.md. For his runs we wrote both business files into voice.md and copied the same post log and outreach log into his folder, so both packs saw the same facts. His Python tools were not run (we never run upstream code), and his runs were told to do those steps by hand. That costs him some points on tool-heavy cases, and is noted.
- Test runs used headless `claude -p` with a sandbox HOME. Other repo builds were running on the same machine, so some runs came back empty under load; those were rerun, never graded as failures.
- Claude Code asks before any write inside ~/.claude/, and a headless test run cannot approve it, so some runs' Write calls to the social folder (then under ~/.claude) were blocked (others wrote through Bash). From round 2 on, the grader counts a file as written when the transcript shows the right path and content and the only failure was that prompt. I did not turn on a permission bypass for test runs. Real users approve the prompt once. Consider telling users in the README that the skills write to ~/.founder/social/linkedin/ and will ask once.
- linkedin-audit eval frameleaf-pasted-numbers: my grader statement said 'about 12.6%' for a post whose rate is 512/4100 = 12.5%. I corrected the statement in round 3. Earlier rounds were graded against the wrong number; that cost ours one grader in r2.
- Public repo: the test businesses are fictional (Lunch Lane, a lunch subscription; Frameleaf, a kids' story video app), and the founder in test inputs is a fictional 'Rosa Mendes'. Mid-build I removed a few details that echoed the real owner (a school name, a former employer, a tech stack) from inputs and fixtures. Runs from round 3 on for comment to audit, and round 4 on for the first five, use the cleaned inputs; earlier runs used the older wording. The facts the graders check did not change.
- Round 3 for linkedin-profile, linkedin-inbox and linkedin-repurpose first ran while I was renaming test inputs, so some cases read a mix of old and new files (for example the prompt said one job title and the fixture another). I discarded that run (kept on disk as discarded-round-3-mixed-inputs) and ran round 3 again with the round-3 and round-4 edits together, counted as one round.
- Noise and reverts: each case runs once per round and one model pass grades it, so a skill can move 5 to 10 points with no real change (linkedin-comment and linkedin-audit moved -1/+1 on repeat runs of the same skill; I also caught the grader marking a statement failed while its own evidence said it passed, and calling '9 trucks' invented when it is in the business file). When the last round of a skill dropped by 5 or more points, I reverted that round's changes and shipped the best measured version. The final score in the table is that version's measured score, which is likely a few points optimistic because it is the best of several noisy runs.
- After testing, linkedin-dm's 'Tool paths' paragraph was reworded to say it needs no sibling skill's tools (so its synced copy in biz-boost works alone). Instruction-wise nothing changed; it was not retested for that edit.

## Independent review (blind)

A second agent reviewed linkedin-repurpose (final 82 above, stopped for time). Goal: every
post traces to the source, with no invented framing, numbers or claims. Same harness as the
builder (fresh `claude -p` runs, own HOME, separate grader), outputs in
`/home/claude/build/_work/review/weakest/`. A new case, short-memo-no-framing, was added: a
four-line voice memo that tempts a cause ("the veggie truck did it"), a percent change and a
lesson.

| skill | case | winner | ours score | baseline score | fix rounds | one-line reason |
| --- | --- | --- | --- | --- | --- | --- |
| linkedin-repurpose | lunch-talk | ours (both label orders) | 45 / 42 | 42 / 39 | 0 | start version adds framing such as "that was the lesson on pricing"; ours adds nothing |
| linkedin-repurpose | short-memo-no-framing | ours (both label orders) | 45 / 45 | 36 / 38 | 0 | start version adds "Those are different lessons" and implies the truck caused the jump; ours keeps the memo's open question |

Baseline = the version this review started from (the shipped r3). Scores are the blind
judge's 0 to 50 totals, one per label order (ours as A, then as B).

Grader fix: the grader's file listing used a glob that skips hidden folders, so it never saw
drafts saved under `~/.founder/social/` and some runs lost the "drafts are saved" grader. The
review copy of the grader walks every folder and also shows the case's input files. Start
and r3 on are graded with the fixed grader; r1 and r2 used the old one.

### linkedin-repurpose  (review rounds, 4 cases)
start: 85 on the 3 old cases with the old grader, 80 with the fixed grader; 78 on all 4 cases.
final: 91 after 4 rounds. Stopped because r3 (+4) and r4 (+2) both gained under 5.
rounds:
- r1: 84 (old grader), draft section rewritten: build each post from source lines, a list of line types that never go in (lessons, framing, claims about readers, added story, a repeated intro), numbers exactly as given, causes only if the source states them, a `from:` line under each draft, show the idea map, no 400-character minimum.
- r2: 85 (old grader), take the user's word that the talk is theirs; save drafts without asking; the next-step line ends every reply; three strength labels only.
- r3: 89, draft every strong idea; no repeated intro line; the `from:` line saved in the draft file.
- r4: 91, a number the source states makes an idea strong; the repeated-intro rule covers source lines too.
open issues: a short newsletter still gets 2 posts where 3 would fit, and tool runs (fold, hookscore) sometimes error and get skipped.

### Spot check: blind head-to-head against Jake

Spot check by an independent reviewer on 2026-10-23, run blind against the baseline.
Each case ran in a fresh `claude -p` (Sonnet) with its own empty HOME, seeing only that
skill's folder (plus founder-context and humanize where ours uses them), the case prompt
and its input files. The baseline saw only the upstream SKILL.md and non-code files; its
Python tools were left out (never run upstream code), with a note telling it to do their
job by hand. A separate Opus judge saw the request, the expected outcome, the inputs and
both results as A and B in random order (key kept apart), and scored each 0 to 10 on five
lines (did the job, nothing made up, safety, clear and usable, tone), so totals are out
of 50. Close calls were judged a second time with A and B swapped. Outputs, keys and
verdicts: `/home/claude/build/_work/review/spot/`.

Our arms got founder-context and humanize from `skills/`, and the business files in
`~/.founder/`. Jake's arms got the same business files plus an equivalent
`~/.claude/linkedin/voice.md` built from the same fields, a `log.md` mirroring the posts
and outreach logs, and li-human as text only (no humanize.py or detect.py).

| skill | case | winner | ours score | baseline score | fix rounds | one-line reason |
| --- | --- | --- | --- | --- | --- | --- |
| linkedin-post | lunch-new-office | ours | 44 | 35 | 0 | Right business, fold preview, saved draft, nothing added. Jake's had no fold preview and added framing the user never gave. Ours is short and flat (339 characters) and hooks are not scored. |
| linkedin-post | frameleaf-teacher-story | ours | 44 | 34 | 0 | No child names, no outcome claims, class size left out, saved in the Frameleaf folder. Jake's did not save and guessed why the kids replayed it. Ours reads thin. |
| linkedin-comment | lunch-buyer-post | ours | 41 / 44 (two judges) | 40 / 38 | 0 | Three options with different jobs, no pitch, linkedin-dm later. Jake's gave two and never used the business file. Ours invented an example person ('Priya', sesame allergy), flagged but still made up. |
| linkedin-comment | edge-layoff-post | ours | 45 | 35 | 0 | Said this is not a place to get noticed and offered one short note of support. Jake's wrote two strategic visibility comments on a layoff post. |
| linkedin-dm | lunch-leads-batch | ours | 42 | 30 | 0 | Picked Dana and Jordan, skipped Sam (already contacted), Priya (no reason), Lee (do not contact) and Maria (other business). Jake's skipped Jordan, ignored the log and made claims up. Ours: follow-up 1 drafts are weak with small inferences. |
| linkedin-dm | frameleaf-one-teacher | ours | 40 | 29 | 0 | Full sequence for Maria with counts and no outcome claims. Jake's missed the voice file and asked for facts it had. Ours gives little before the ask and wrongly called '140 beta users' off limits. |

## Polish round (Oct 24)

Method: each fix was rerun in fresh, isolated `claude -p` runs (own HOME, own project folder,
only the skill plus founder-context and humanize where the repo has them). The new version ran
against the current version (the last commit) on the same eval case. A separate `claude -p`
judge saw both outputs as A and B and scored them out of 50, once in each label order. A fix
ships only if it wins or ties in both orders. Scores are new / current. Runs, judge packets
and keys: `/home/claude/build/_work/polish/`.

| skill | case | round | order A-new | order A-current | result |
| --- | --- | --- | --- | --- | --- |
| linkedin-comment | lunch-buyer-post | r1 | won 46/43 | won 45/43 | shipped |
| linkedin-dm | lunch-leads-batch | r1 | won 45/38 | won 42/36 | shipped |
| linkedin-dm | frameleaf-one-teacher | r1 | won 45/41 | won 43/42 | shipped |
| linkedin-post | lunch-new-office | r1 | won 46/43 | won 43/42 | shipped |

What changed:
- linkedin-dm 0.1.1 (synced to biz-boost-skills): proof is cleared for use and only the
  off-limits line is off limits; every sentence traces to the file, the lead row or the user;
  follow-up 1 may use an unused proof item as a plain fact, with nothing added around it.
- linkedin-comment 0.1.1: no made-up example people or cases, even flagged. This is where the
  reviewer's invented example person came from (the review table lists it under
  linkedin-comment, not linkedin-post).
- linkedin-post 0.1.1: one line, no invented example person; proof is cleared for use.
