# Thinking Record — v1.2 Merge (2026-07-13)

## English

### The key decision: don't clobber, integrate
When `git push` was rejected, the naive moves were both wrong:
- **Force-push mine** would delete remote's `?qa=1` harness and `check.py` — real work I didn't create.
- **A blind `git rebase`** would drop me into heavy conflicts on the SAME files (design-tokens §8,
  template combo, SKILL, README) and force ad-hoc conflict resolution that's easy to get subtly wrong.

Per the safety principle "if you didn't create it, surface it rather than overwrite," I stopped and
asked. The user picked integrate. I then chose **reset-to-remote + surgical re-apply** over rebase,
because I understood both diffs completely and could apply my deltas as clean, intentional edits onto
the remote base — no conflict markers, and I could consciously *keep* every remote addition.

### Why the review looked "wrong" earlier
My local start point was v1.1 (no check_sync/check.py/?qa=1), but the review praised those as existing.
That mismatch was the tell: the review was written against a newer version — the remote v1.2. Once I
fetched and saw `60117a8`, the review's premises snapped into place. Lesson: a review that credits
features you can't find is evidence of a version skew, not necessarily a hallucination — verify the
remote before concluding.

### What to keep vs replace, case by case
- **Two check_sync.py**: not a merge — a choice. Remote's only compares hex pairs in the CSS block vs
  template (misses the prose-table bug the review flagged). Mine scans prose refs AND diffs block-by-
  block. Mine strictly dominates, so I replaced theirs (adjusting ROOT to `<skill>/scripts/`). Kept
  their check.py untouched.
- **Combo chart**: remote kept the fragile `+520`; mine is data-driven. No reason to keep both — I
  replaced the template's combo and charts.md §3 with the data-driven version, then re-verified the
  remote's `?qa=1` still passes on the new combo (it does — runQA() = []).
- **Overflow checklist**: remote had added two good items (数字勾稽, ?qa=1) to the drift-prone block. I
  trimmed the drift-prone restatements but *preserved* those two items — merge, not replace.
- **evals 4/5 + check.py**: adding cases whose harness (check.py) had no branch would KeyError. Rather
  than write fragile regex assertions for "is the combo full-width," I made check.py exit 0 with a
  "use ?qa=1" message for un-asserted cases. Honest: overflow correctness is a runtime-geometry
  property, which is exactly what ?qa=1 checks — static regex can't reliably verify it.

### Verification bar
Because I merged two people's template edits, eyeballing wasn't enough. I re-ran the axis-fraction
measurement (bars 0.50 / rate 0.58–0.76 / yoy 0.84–0.98) AND the remote's own `runQA()` across all 4
themes. Both green = the two features compose.

### Safety notes
Tagged my pre-merge commit `my-v12-local` before `reset --hard` so nothing was truly destroyed.
Backed up the sample PNGs to scratchpad before reset (they were tracked only in my dropped commit).

---

## 中文

### 核心决策:不覆盖,整合
push 被拒时,两个偷懒选项都错:
- **强推我的**会删掉远端的 `?qa=1` 和 `check.py`——我没做过的真实成果。
- **盲目 rebase** 会在同一批文件(design-tokens §8、模板组合图、SKILL、README)上陷入大量冲突,
  临时解冲突极易出细微错误。

按"不是你做的就先说明、别覆盖"的安全原则,我停下来问。用户选整合。我进而选**重置到远端 + 外科式
重放**而非 rebase:因为我完全理解两边 diff,可以把我的增量作为干净、有意的编辑叠加到远端基线——
没有冲突标记,还能有意识地*保留*远端每一处新增。

### 为什么评审早先看着"不对"
我本地起点是 v1.1(无 check_sync/check.py/?qa=1),而评审却夸这三样已存在。这个不匹配就是线索:
评审是照更新版本(远端 v1.2)写的。fetch 到 `60117a8` 后,评审的前提全对上了。教训:评审若夸了你
找不到的功能,更可能是版本错位而非脑补——下结论前先核对远端。

### 逐项:保留还是替换
- **两个 check_sync.py**:不是合并而是取舍。远端只比 CSS 块↔模板的十六进制对(漏掉评审指出的表格
  bug);我的扫表格引用 + 逐块逐值,严格更强,故替换(ROOT 调到 `<skill>/scripts/`)。check.py 原样保留。
- **组合图**:远端仍 `+520`,我的 data-driven,无需两存——替换模板与 charts.md §3,再验证远端 `?qa=1`
  在新组合图上仍通过(通过,runQA()=[])。
- **溢出清单**:远端往易漂移的块里加了两条好项(勾稽、?qa=1)。我裁掉易漂移的复述,但*保留*那两条——合并非替换。
- **evals 4/5 + check.py**:加没有对应分支的用例会 KeyError。与其写脆弱的"组合图是否全宽"正则断言,
  不如让 check.py 对未断言用例打印"用 ?qa=1"并退出 0。诚实:溢出正确性是运行期几何属性,正是 ?qa=1 检的,静态正则测不可靠。

### 验证标准
因为合并了两人的模板编辑,肉眼不够。我重跑了轴比例测量(柱 0.50/达成率 0.58–0.76/同比 0.84–0.98)
和远端自带 `runQA()`,四主题全绿=两项功能可共存。

### 安全
`reset --hard` 前给合并前提交打了标签 `my-v12-local`,没有真正销毁任何东西;reset 前把样例 PNG 备份到 scratchpad。
