# Conversation Record — v1.2 Review Fixes + Remote Merge (2026-07-13)

## English

### Task
User asked to (1) commit my review-fix changes and push to GitHub, then (2) build a new
business-analysis skill (separate task). This record covers (1).

### What happened during push
My local commit (f89954f) was rejected: the remote `main` already had a *different* v1.2
(`60117a8 "fix+feat: v1.2 — 现象级问题修复"`) that I did not create — an independent fix of the
same review. I stopped and asked the user how to handle the divergence. **User chose: integrate both.**

### The two v1.2's (both children of v1.1 `183ed64`)
- **Remote had, mine lacked**: `?qa=1` geometry self-check harness (in template), `scripts/check.py`
  regression asserter, a simple `scripts/check_sync.py`, plus SKILL.md upgrades (Step 0 three
  questions, single-source DATA rule, `[原生]/[近似]/[舍弃]` landing tags, 适用边界 section).
- **Mine had, remote lacked**: the P0 token-name fix (remote still had `--target-bar-*` in tables),
  the data-driven combo chart (remote still had `+520` magic offset), `--accent-warm-soft` doc↔template
  sync, sample screenshots, 2 adversarial overflow eval cases, a stronger check_sync (scans prose
  refs + block-by-block), and a Step 2.5 skeleton-confirmation checkpoint.
- Notably: the review the user pasted was written against the **remote** v1.2 (it praised
  check_sync/check.py/?qa=1 as existing) — which is why those "features" seemed to not exist when I
  first looked at my local v1.1.

### Integration approach
Reset local `main` to the remote (`git reset --hard origin/main`), then surgically re-applied my
improvements on top of the remote base — keeping ALL of remote's additions, losing nothing:
- design-tokens.md: renamed §3/§5 tables to `--target-*/--lastyear-*`; added `--accent-warm-soft`
  to §8 (4 themes) + §2.5 + custom placeholder + sync note.
- charts.md §3 + template combo: replaced remote's `+520` combo with the data-driven `bandAxis`
  (3 hidden axes; bars bottom ~50%, rate line 58–76%, yoy line 84–98%).
- SKILL.md: added Step 2.5 checkpoint; trimmed the overflow checklist to defer to layouts §6 (kept
  remote's 数字勾稽 + ?qa=1 items); added a caveat that `?qa=1` depends on template class names.
- layouts.md §6: marked as the single authority. charts.md §1: reframed "防溢出七条" as a §6 excerpt.
- evals.json: added adversarial cases 4/5 (12-month combo in narrow card; TOP15 in 1/3 width).
- scripts/check.py: made it handle eids 4/5 gracefully (print → exit 0) instead of KeyError.
- scripts/check_sync.py: replaced remote's simple version with my stronger one (path-adjusted to
  `<skill>/scripts/`): scans prose refs + diffs §8 vs template block-by-block, value-by-value.
- docs/samples: 4 rendered combo PNGs. README: added scripts/docs to structure, samples section,
  check_sync + 6-eval mentions in 定制.
- Rebuilt dist/bi-dashboard-design.skill (now includes scripts/).

### Verification (in-browser, integrated artifact)
- `check_sync.py` PASS (5 blocks / 42 defs; all refs defined).
- Template served locally with `?qa=1`: combo has 3 axes, no NaN, bars top 0.50 / rate [0.58,0.76]
  / yoy [0.84,0.98]; the built-in `runQA()` returns `[]` (zero geometry issues). All 4 themes:
  6/6 charts init, no NaN, 0 QA issues.
- `check.py 5` exits 0 with the adversarial-case message.

### Result / push
Fast-forward push onto origin/main (parent = remote 60117a8). Nothing from either side was lost.
My original pre-merge commit is preserved locally as tag `my-v12-local` (f89954f).

### Data sources
None external. Samples are ECharts renders of the template's fabricated demo data.

---

## 中文

### 任务
用户要求:(1) 提交我的评审修复并推送 GitHub;(2) 新建一个经营分析 skill(独立任务)。本记录覆盖 (1)。

### 推送时发生了什么
我的本地提交(f89954f)被拒:远端 `main` 已有一份**不同的** v1.2(`60117a8`),不是我做的——是对同一
评审的独立修复。我停下问用户如何处理分叉。**用户选择:整合两份。**

### 两份 v1.2(都是 v1.1 `183ed64` 的子代)
- **远端有、我缺**:`?qa=1` 几何自检(模板内)、`scripts/check.py` 回归断言器、简版 check_sync,
  以及 SKILL 升级(Step 0 三问、造数单一源、`[原生]/[近似]/[舍弃]` 落地标注、适用边界)。
- **我有、远端缺**:P0 token 名修复(远端表格仍 `--target-bar-*`)、data-driven 组合图(远端仍 `+520`
  魔法数)、`--accent-warm-soft` 文档↔模板同源、样例截图、2 个对抗溢出用例、更强的 check_sync
  (扫表格引用+逐块逐值)、Step 2.5 骨架确认。
- 值得注意:用户贴的评审其实是照**远端** v1.2 写的(它夸 check_sync/check.py/?qa=1 已存在)——所以
  我最初看本地 v1.1 时觉得这三样"不存在"。

### 整合做法
把本地 `main` 重置到远端(`git reset --hard origin/main`),再把我的改进外科式叠加到远端基线上——
保留远端全部新增,一样不丢(细节见上英文)。

### 验证(浏览器,整合后产物)
- `check_sync.py` PASS(5 块/42 定义;引用全有定义)。
- 本地带 `?qa=1` 打开:组合图三轴、无 NaN、柱顶 0.50/达成率带 [0.58,0.76]/同比带 [0.84,0.98];
  内置 `runQA()` 返回 `[]`(零几何问题)。四主题:6/6 渲染、无 NaN、QA 0 问题。
- `check.py 5` 以对抗用例提示优雅退出 0。

### 结果 / 推送
以 fast-forward 推到 origin/main(父提交=远端 60117a8),两边成果均无损失。我合并前的原始提交以标签
`my-v12-local`(f89954f)保留在本地。

### 数据来源
无外部数据;样例为模板造数的 ECharts 渲染。
