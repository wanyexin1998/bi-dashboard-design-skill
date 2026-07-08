#!/usr/bin/env python3
"""tokens 同源校验:比对 references/design-tokens.md 的 CSS 变量块与 assets/starter-template.html。
每个变量名在两边出现的十六进制取值集合必须一致(按主题聚合)。改了任何一边就跑一次。"""
import re, os, sys
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
md  = open(os.path.join(root, "references", "design-tokens.md"), encoding="utf-8").read()
tpl = open(os.path.join(root, "assets", "starter-template.html"), encoding="utf-8").read()
mdcss = re.search(r"```css(.*?)```", md, re.S).group(1)
def collect(s):
    d = {}
    for k, v in re.findall(r"(--[a-z0-9-]+)\s*:\s*(#[0-9A-Fa-f]{3,8})", s):
        d.setdefault(k, set()).add(v.upper())
    return d
a, b = collect(mdcss), collect(tpl)
bad = []
for k, vals in a.items():
    if k not in b:            bad.append(f"{k}: 模板缺失")
    elif vals - b[k]:         bad.append(f"{k}: tokens={sorted(vals)} 模板={sorted(b[k])}")
if bad:
    print("同源校验失败:"); [print(" -", x) for x in bad]; sys.exit(1)
print(f"同源校验通过: {len(a)} 个变量一致")
