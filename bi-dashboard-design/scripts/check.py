#!/usr/bin/env python3
"""回归断言检查。用法: python check.py <产物文件.html|.md> <用例id 0-5>
用例 prompt 见 ../evals/evals.json。修改 skill 后,用对应用例重新生成产物并跑本脚本,全过才算没回归。
用例 0-3 有静态断言;4-5 是对抗性溢出场景(靠 ?qa=1 几何自检验证,无静态断言)。"""
import re, sys

def build(fname, t):
    def H(*ps): return any(re.search(p, t, re.I) for p in ps)
    n = lambda p: len(re.findall(p, t))
    return {
      0: {  # 会员商城运营月报(HTML,teal)
        "画布 #F7F8FA": H(r"#F7F8FA"),
        "青绿主题 #21968F": H(r"#21968F"),
        "签名组合图系列色(去年灰/目标珊瑚/达成率红)": H(r"#9CA3AF") and H(r"#F08A7E") and H(r"#E64C45"),
        "绿=向好 #18A058": H(r"#18A058"),
        "时间进度虚线": H(r"时间进度") and H(r"dashed"),
        "标题字距 letter-spacing": H(r"letter-spacing\s*:\s*\.?[3-9]"),
        "数据标签常开(≥3处)": n(r"label\s*:\s*\{\s*show\s*:\s*true") >= 3,
        "单文件+ECharts CDN": fname.endswith(".html") and H(r"echarts[^\"']*\.js"),
        "表格含合计行": H(r"合计"),
        "分区丝带": H(r"ribbon", r"— .+ —"),
        "containLabel 开启": H(r"containLabel\s*:\s*true"),
        "resize 监听": H(r"addEventListener\(\s*['\"]resize"),
      },
      1: {  # 门诊驾驶舱 QuickBI 规范(md)
        "青绿主题 #21968F": H(r"#21968F"),
        "token 色值齐备": H(r"#F7F8FA") and H(r"#E64C45") and H(r"#18A058"),
        "分区骨架(丝带/章节)": H(r"丝带") and H(r"章"),
        "逐卡片规格 ≥10 卡": n(r"卡片|指标卡|Card") >= 10 and H(r"组合图|环形图|条形图|折线"),
        "时间进度参考线": H(r"时间进度") and H(r"虚线"),
        "月蓝年橙/进度环": H(r"年.{0,4}橙", r"进度环"),
        "涨跌语义规则": H(r"绿涨红跌", r"绿=向好"),
        "字号规则(16px 标题/11px 标签)": H(r"16px") and H(r"11px"),
        "行型/每行卡数标注": H(r"行型", r"KPI-4", r"构成-3", r"一行[0-9一二三四]", r"每行"),
        "溢出防线 ≥2 项": sum([H(r"containLabel"), H(r"留头|headroom|1\.15"), H(r"截断|省略号"), H(r"grid\.right|右侧留")]) >= 2,
      },
      2: {  # 大促作战看板(HTML,pop)
        "POP 主题 #E8188C": H(r"#E8188C"),
        "浅色画布(非暗黑大屏)": H(r"#F7F8FA") and not H(r"background\s*:\s*#0", r"background\s*:\s*#1[0-9a-f]"),
        "目标达成进度组件": H(r"达成率|进度环|progress"),
        "排行条形图": H(r"排行|排名|TOP"),
        "渐变填充": H(r"linear.?gradient|colorStops"),
        "绿=向好 #18A058": H(r"#18A058"),
        "单文件+ECharts CDN": fname.endswith(".html") and H(r"echarts[^\"']*\.js"),
      },
      3: {  # 品牌紫自定义主题(HTML)
        "品牌紫 #7C3AED 为主色(未套预设)": H(r"#7C3AED") and not H(r"--primary:\s*#3370EB"),
        "推导浅端/tint": H(r"#D8C4FA", r"#F2EBFD", r"primary-soft"),
        "语义色恒定": H(r"#18A058") and H(r"#E64C45"),
        "DNA 结构(字距+画布)": H(r"letter-spacing\s*:\s*\.?[3-9]") and H(r"#F7F8FA"),
        "卡片标题 16px": H(r"card-title\{[^}]*16px", r"font-size:\s*16px[^}]*font-weight:\s*6"),
        "containLabel+y轴留白": H(r"containLabel\s*:\s*true") and H(r"max\s*:\s*[^,]*1\.\d", r"\(v\.max-v\.min\)\s*\*", r"range\s*\*"),
        "resize+固定容器高": H(r"addEventListener\(\s*['\"]resize") and H(r"height\s*:\s*\d{3}px"),
        "单文件+ECharts CDN": fname.endswith(".html") and H(r"echarts[^\"']*\.js"),
        "排行右留白/截断": H(r"right\s*:\s*4[89]", r"right\s*:\s*[5-9]\d", r"slice\(0,\s*\d\)\s*\+\s*['\"]…"),
      },
    }

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__); sys.exit(2)
    fname, eid = sys.argv[1], int(sys.argv[2])
    t = open(fname, encoding="utf-8", errors="ignore").read()
    allchecks = build(fname, t)
    if eid not in allchecks:
        print(f"用例 {eid} 为对抗性溢出场景,无静态断言——请用 ?qa=1 几何自检验证(见 evals.json 的 expected_output)。")
        sys.exit(0)
    checks = allchecks[eid]
    fails = 0
    for k, v in checks.items():
        print(("PASS " if v else "FAIL "), k)
        fails += (not v)
    print(f"\n{len(checks)-fails}/{len(checks)} passed")
    sys.exit(1 if fails else 0)
