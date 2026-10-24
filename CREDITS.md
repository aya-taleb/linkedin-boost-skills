# Credits

## Jake Schincariol, linkedin-agent-skill (MIT)

Repo: https://github.com/Jakeschincariol/linkedin-agent-skill
Commit used: add2c23882fe79180737d242ff80a5da205eda6a

Three skills here started from Jake's files and were changed by Aya Taleb:

| our skill | his skill | what changed |
| --- | --- | --- |
| linkedin-post | skills/li-post/SKILL.md | one business per post from founder-context, a measured "see more" preview tool, per-business post log, hooks scored by our own tool, humanize |
| linkedin-plan | skills/li-plan/SKILL.md | one plan per business, topic rotation from the post log, a weekly post budget across ventures |
| linkedin-dm | skills/li-dm/SKILL.md | real leads from sales/leads.csv, a daily invite limit and an outreach log tool, sourced note limit |

His hooks.json, slop.json, rubric.json and Python tools were not copied.

```
MIT License

Copyright (c) 2026 Jake Schincariol

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Thank-you lines (ideas only, nothing copied)

- Jake Schincariol's li-comment, li-reply, li-inbox, li-carousel, li-repurpose, li-profile and li-audit showed which jobs a LinkedIn pack needs. Our versions were written from our own job specs (see each skill's `references/job-spec.md`) and use our own structure.
- Jake's Instagram hookscore gave the idea of scoring hooks with a local tool. Our linkedin-hooks tool, its checks and its word lists are our own.
- Jake's ig-viral and x-viral gave the idea of judging a post against its own account's normal. linkedin-viral works only from posts the user pastes or exports.
- Jake's "you post it, not the tool" rule, which every skill here keeps.
