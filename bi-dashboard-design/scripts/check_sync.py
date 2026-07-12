#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_sync.py — Design-token 同源守卫 / single-source-of-truth guard.
确保 references/design-tokens.md 与 assets/starter-template.html 不漂移。

检查两件事 / Two checks:
  1. UNDEFINED-REF: design-tokens.md 里任何被引用(表格/正文/渐变)的 `--token`,
     都必须在 §8 的 ```css``` 变量块中定义。抓命名不一致(如 --target-bar-1 vs --target-1)。
  2. DOC-VS-TEMPLATE DRIFT: §8 的每个 `:root` / `[data-theme=...]` 块,
     必须与模板 <style> 逐块逐值一致(缺块/多 token/值不同都报错)。

用法 / Usage:
  python bi-dashboard-design/scripts/check_sync.py   # 退出码 0=通过 1=不一致
无第三方依赖 / stdlib only.
"""
import re
import sys
from pathlib import Path

# 本脚本位于 <skill>/scripts/ 下,ROOT = skill 目录(scripts 的父目录)。
ROOT = Path(__file__).resolve().parent.parent
DOC = ROOT / "references" / "design-tokens.md"
TPL = ROOT / "assets" / "starter-template.html"

REF_ALLOWLIST = set()   # 允许被引用而不在 §8 定义的 token(占位/示例)。目前无。

# token 名:`--` 后必须字母开头、段间单连字符——不会误匹配 `---`(Markdown 分隔线/表格线)。
_NAME = r"--[a-z][a-z0-9]*(?:-[a-z0-9]+)*"
TOKEN_REF = re.compile(_NAME)
TOKEN_DEF = re.compile(r"(" + _NAME + r")\s*:\s*([^;]+);")
CSS_FENCE = re.compile(r"```css\s*\n(.*?)\n```", re.DOTALL)
STYLE_TAG = re.compile(r"<style>(.*?)</style>", re.DOTALL)
COMMENT_C = re.compile(r"/\*.*?\*/", re.DOTALL)                # /* ... */(含占位 custom 主题)
BLOCK = re.compile(r'(:root|\[data-theme="?\w+"?\s*\])\s*\{([^}]*)\}')


def _norm(v: str) -> str:
    return re.sub(r"\s+", " ", v).strip()


def parse_blocks(css: str):
    """把 CSS 文本解析成 {选择器: {token: value}}(先剥掉 /* */ 注释)。"""
    css = COMMENT_C.sub("", css)
    blocks = {}
    for sel, body in BLOCK.findall(css):
        blocks[_norm(sel)] = {m.group(1): _norm(m.group(2)) for m in TOKEN_DEF.finditer(body)}
    return blocks


def main() -> int:
    errors = []
    if not DOC.exists() or not TPL.exists():
        print(f"[FATAL] 找不到 {DOC} 或 {TPL}")
        return 1

    doc_text = DOC.read_text(encoding="utf-8")
    tpl_text = TPL.read_text(encoding="utf-8")

    m = CSS_FENCE.search(doc_text)
    if not m:
        print("[FATAL] design-tokens.md §8 未找到闭合的 ```css``` 块(可能被截断?)")
        return 1
    doc_blocks = parse_blocks(m.group(1))

    defined = set()
    for toks in doc_blocks.values():
        defined |= set(toks.keys())

    # 检查 1:围栏块之外的正文/表格引用,必须都能在 §8 找到定义。
    doc_prose = doc_text[: m.start()] + doc_text[m.end():]
    for t in sorted(t for t in set(TOKEN_REF.findall(doc_prose)) if t not in defined and t not in REF_ALLOWLIST):
        errors.append(f"[UNDEFINED-REF] `{t}` 在正文/表格中被引用,但 §8 未定义它。")

    ms = STYLE_TAG.search(tpl_text)
    if not ms:
        print("[FATAL] starter-template.html 未找到 <style> 块")
        return 1
    tpl_blocks = {k: v for k, v in parse_blocks(ms.group(1)).items()
                  if k == ":root" or k.startswith("[data-theme")}

    # 检查 2:文档 §8 与模板逐块逐值对比。
    for sel in sorted(set(doc_blocks) | set(tpl_blocks)):
        d, t = doc_blocks.get(sel), tpl_blocks.get(sel)
        if d is None:
            errors.append(f"[DRIFT] 选择器 `{sel}` 只在模板里有,§8 缺失。"); continue
        if t is None:
            errors.append(f"[DRIFT] 选择器 `{sel}` 只在 §8 里有,模板缺失。"); continue
        for tok in sorted(set(d) | set(t)):
            dv, tv = d.get(tok), t.get(tok)
            if dv is None:
                errors.append(f"[DRIFT] `{sel}` 的 `{tok}` 只在模板定义(§8 缺)。")
            elif tv is None:
                errors.append(f"[DRIFT] `{sel}` 的 `{tok}` 只在 §8 定义(模板缺)。")
            elif dv.lower() != tv.lower():
                errors.append(f"[DRIFT] `{sel}` 的 `{tok}` 值不一致:§8=`{dv}` vs 模板=`{tv}`。")

    if errors:
        print("check_sync: FAIL — {} 处不一致:\n".format(len(errors)))
        for e in errors:
            print("  " + e)
        print("\n修复:design-tokens.md §8 是唯一事实源;让模板 <style> 与之逐值对齐,")
        print("并确保表格里引用的 token 名都能在 §8 找到定义。")
        return 1

    ndef = sum(len(v) for v in doc_blocks.values())
    print("check_sync: PASS — §8 与模板逐块逐值一致,{} 块 / {} 定义;所有被引用 token 均有定义。".format(
        len(doc_blocks), ndef))
    return 0


if __name__ == "__main__":
    sys.exit(main())
