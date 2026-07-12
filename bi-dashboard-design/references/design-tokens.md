# Design Tokens — Wyexin BI 视觉基因

所有颜色、字体、间距的唯一事实来源。构建 HTML 看板时直接使用文末的 CSS 变量块；在 BI 工具中搭建时按十六进制值手动配置。

## 1. 中性色(所有主题共用)

| Token | 值 | 用途 |
|---|---|---|
| `--canvas` | `#F7F8FA` | 页面画布底色。永远不用纯白做页面底 |
| `--card` | `#FFFFFF` | 卡片底色 |
| `--hairline` | `#E9EDF3` | 卡片描边、分隔线 |
| `--grid-line` | `#EEF1F6` | 图表网格线(极淡) |
| `--text-1` | `#1D2129` | 标题、KPI 大数字 |
| `--text-2` | `#4E5969` | 正文、表格内容 |
| `--text-3` | `#86909C` | 辅助说明、轴标签、图例、单位 |
| `--text-disabled` | `#C9CDD4` | 占位、禁用 |

## 2. 主题色族(预设为默认,用户需求优先)

**优先级:用户指定 > 业务域预设 > 默认 blue。** 四套预设是"没有明确要求时"的默认;当用户提出品牌色、指定色系、深色背景等任何主题诉求时,以用户需求为准重新设计主题与背景,方法见 2.5。每主题给出:主色 / 主色浅端(渐变用) / 辅助色 / 点缀色。

### Theme A `blue` — 商务蓝(默认:集团经营、业绩、销售、通用)

| Token | 值 | 说明 |
|---|---|---|
| `--primary` | `#3370EB` | 主色:当期值、月维度、主趋势 |
| `--primary-soft` | `#B9D3FA` | 柱形渐变浅端、面积图渐变端 |
| `--secondary` | `#A5B8E8` | 薰衣草蓝:次要系列、目标(浅) |
| `--accent-warm` | `#F59A3C` | 橙:年维度、年累计 |
| `--tint` | `#EAF2FB` | 表头底、选中态、KPI chip 底 |

### Theme B `teal` — 医养青绿(医院、健康、商城、活动、监测)

| Token | 值 | 说明 |
|---|---|---|
| `--primary` | `#21968F` | 主色青绿 |
| `--primary-soft` | `#A6DCC3` | 渐变浅端(薄荷) |
| `--secondary` | `#52B78A` | 绿:第二系列、同期对比 |
| `--accent-warm` | `#F5A54A` | 橙:第二维度(如床日数、年维度) |
| `--tint` | `#E6F4F2` | 表头底、chip 底 |

### Theme C `navy` — 藏蓝薰衣草(渠道月报、代理体系、沉稳汇报)

| Token | 值 | 说明 |
|---|---|---|
| `--primary` | `#2E4180` | 藏蓝:强调块、chip 深端 |
| `--primary-soft` | `#B4C2EE` | 薰衣草浅端 |
| `--secondary` | `#5B7CE6` | 中间蓝:主图表系列 |
| `--accent-warm` | `#F2A8A0` | 鲑鱼粉:目标系列 |
| `--tint` | `#ECEFF9` | 表头底、chip 底 |

### Theme D `pop` — 洋红青黄(营销专项、大促、需要高注目度的临时看板)

| Token | 值 | 说明 |
|---|---|---|
| `--primary` | `#E8188C` | 洋红 |
| `--primary-soft` | `#F9BBDD` | 洋红浅端 |
| `--secondary` | `#00AEEF` | 青 |
| `--accent-warm` | `#FFC53D` | 黄 |
| `--tint` | `#FDEEF6` | 表头底 |

### 2.5 自定义主题推导法(用户给了主题需求时)

给一个主色(如品牌色 `#7C3AED`),按下式生成整套 token,其余规范不变:

- `--primary` = 用户主色(若过亮/过灰,微调至中明度高饱和,保证白字可读)
- `--primary-soft` = 主色与白 30:70 混合(渐变浅端)
- `--secondary` = 主色的邻近色(色相 ±30°)或用户给的第二色
- `--accent-warm` = 与主色互补的暖色(橙/琥珀系),用于年维度与第二强调
- `--accent-warm-soft` = 暖色与白 30:70 混合(年维度柱/进度条的渐变浅端)
- `--tint` = 主色 8–12% 不透明度铺在白上(表头/选中态)
- 中性色、语义色(涨跌/目标/达成率红)**不随主题变**——除非用户明确要求
- 深色背景需求:画布可换深色(如 `#0E1526`),此时卡片用 `#161F33`、文字反白、hairline 换 `rgba(255,255,255,.08)`,但组件结构、图表语言、语义色逻辑全部保留
- 对比度底线:正文对底 ≥4.5:1,大数字 ≥3:1

## 3. 语义色(跨主题恒定,不随主题变)

| Token | 值 | 用途 |
|---|---|---|
| `--up` | `#18A058` | 正向变化:同比/环比上涨、达标。箭头 ↑ 与数值同色 |
| `--down` | `#E64C45` | 负向变化:下跌、缺口、风险、支出 |
| `--rate-line` | `#E64C45` | 达成率折线(签名元素) |
| `--time-marker` | `#E64C45` | 时间进度虚线标记(dashed) |
| `--target-1` | `#F5B1A8` | 目标柱渐变浅端(珊瑚) |
| `--target-2` | `#F08A7E` | 目标柱渐变深端 |
| `--lastyear-1` | `#D6DAE1` | 去年/基期柱渐变浅端(灰) |
| `--lastyear-2` | `#9CA3AF` | 去年/基期柱渐变深端 |
| `--yoy-line` | `#6B7280` | 同比折线(深灰) |

**涨跌标准:绿=向好,红=向差**(常规指标:↑绿 #18A058 / ↓红 #E64C45)。**逆向指标**(流失率、爽约率、投诉量、退货率等越低越好)按业务向好着色——下降标绿、上升标红;箭头 ↑↓ 永远指示数值方向,颜色表达好坏。历史作品存在红涨绿跌版本,新看板一律采用本标准,同一看板内绝不混用。红色在本体系身兼三职:目标系列、达成率线、负向变化——它们语义相通(都指向"差距与压力"),这是刻意设计。

**收支对置**:收入/流入用主题主色(蓝或青),支出/流出用 `--down` 红,常用于发散条形图与双轴线图。

## 4. 分类色板(环图、堆叠柱、多系列)

按主题取前 N 个,顺序固定:

- blue: `#3370EB` `#52B78A` `#F5A54A` `#8D6BE8` `#F27E9D` `#38B4E0` `#F7C04A` `#A5B8E8`
- teal: `#21968F` `#52B78A` `#F5A54A` `#38B4E0` `#8D6BE8` `#F7C04A` `#A6DCC3` `#F27E9D`
- navy: `#2E4180` `#5B7CE6` `#B4C2EE` `#F2A8A0` `#52B78A` `#F5A54A` `#38B4E0` `#F7C04A`
- pop:  `#E8188C` `#00AEEF` `#FFC53D` `#8D6BE8` `#52B78A` `#F5A54A` `#F27E9D` `#38B4E0`

超过 6 个分类考虑合并为「其他」,环图分类 ≤6 为佳。

## 5. 渐变(签名元素:凡柱必渐变)

| 场景 | 渐变 |
|---|---|
| 竖向柱 | 180°:顶部 `--primary` → 底部 `--primary-soft`(饱和在上,视觉重心托起数值标签) |
| 横向条 | 90°:左 `--primary-soft` → 右 `--primary`(深端指向数值端点) |
| 面积图 | 线用 `--primary`,填充 180°:`--primary` 22% 不透明 → 0% 透明 |
| 目标柱 | 180°:`--target-2` → `--target-1` |
| 去年柱 | 180°:`--lastyear-2` → `--lastyear-1` |
| 页头横幅(可选) | 135°:主色深端 → 主色亮端,叠加六边形纹理或细光斑 |

## 6. 字体

| Token | 值 |
|---|---|
| 字族 | `"PingFang SC","Microsoft YaHei","HarmonyOS Sans SC",system-ui,sans-serif` |
| 数字 | 同字族 + `font-variant-numeric: tabular-nums`(等宽数字,对齐是尊严) |
| 页面主标题 | 20–22px / 700 / `letter-spacing:.35em`(**字距拉开是签名**,如「集 团 业 绩 驾 驶 舱」) |
| 分区丝带标题 | 16px / 700 / `letter-spacing:.5em`,两侧加「— 」破折号 |
| 卡片标题 | **16px(默认)–18px(强调)** / 600 / `--text-1` / **居中**,计量单位以「(万)」形式缀在标题尾,不在每个数字上重复 |
| KPI 大数字 | 30–38px / 700 / `--text-1`;千分位分隔 |
| KPI 标签 | 12px / 400 / `--text-3` |
| 涨跌幅 | 12px / 600 / `--up` 或 `--down`,带 ↑↓ 箭头 |
| 轴标签·数据标签·图例 | 11px / `--text-3`;数据标签可随系列同色 |
| 表格 | 12px,行高 36–40px |

## 7. 尺寸·间距·形状

| Token | 值 |
|---|---|
| 页面宽度 | 1920 设计稿(内容区 ~1888),纵向长滚动;移动端另行单列 |
| 页面内边距 | 16px |
| 卡片间距 | 12px |
| 卡片内边距 | 16px;标题区高 ~40px |
| 卡片圆角 | 8px(chip/标签 4px,药丸全圆角) |
| 卡片描边+投影 | `1px solid #E9EDF3` + `0 1px 4px rgba(29,33,41,.04)`。扁平克制,禁止厚重投影 |
| 柱宽 | ≤22px,组内柱间距 2–4px |
| 环图内外径 | 58% / 78% |
| 进度环 | 轨道 `#EEF1F6` 10px,进度圆头(roundCap) |

## 8. CSS 变量块(HTML 看板直接粘贴)

```css
:root{
  --canvas:#F7F8FA; --card:#FFFFFF; --hairline:#E9EDF3; --grid-line:#EEF1F6;
  --text-1:#1D2129; --text-2:#4E5969; --text-3:#86909C; --text-disabled:#C9CDD4;
  --up:#18A058; --down:#E64C45; --rate-line:#E64C45; --time-marker:#E64C45;
  --target-1:#F5B1A8; --target-2:#F08A7E;
  --lastyear-1:#D6DAE1; --lastyear-2:#9CA3AF; --yoy-line:#6B7280;
  --font:"PingFang SC","Microsoft YaHei","HarmonyOS Sans SC",system-ui,sans-serif;
}
[data-theme="blue"]{ --primary:#3370EB; --primary-soft:#B9D3FA; --secondary:#A5B8E8; --accent-warm:#F59A3C; --accent-warm-soft:#FBD3A2; --tint:#EAF2FB; }
[data-theme="teal"]{ --primary:#21968F; --primary-soft:#A6DCC3; --secondary:#52B78A; --accent-warm:#F5A54A; --accent-warm-soft:#FBDDB4; --tint:#E6F4F2; }
[data-theme="navy"]{ --primary:#2E4180; --primary-soft:#B4C2EE; --secondary:#5B7CE6; --accent-warm:#F2A8A0; --accent-warm-soft:#FBDCD8; --tint:#ECEFF9; }
[data-theme="pop"] { --primary:#E8188C; --primary-soft:#F9BBDD; --secondary:#00AEEF; --accent-warm:#FFC53D; --accent-warm-soft:#FFE8B0; --tint:#FDEEF6; }
/* 自定义主题:用户有品牌色/背景需求时按 §2.5 推导,复制此行填值即可
[data-theme="custom"]{ --primary:?; --primary-soft:主色30:70混白; --secondary:邻近色; --accent-warm:互补暖色; --accent-warm-soft:暖色浅端; --tint:主色10%铺白; } */
```

> `--accent-warm-soft` 是点缀暖色的浅端(年维度柱/进度条渐变用,如年度进度条 `linear-gradient(90deg,--accent-warm-soft,--accent-warm)`)。本块与 `assets/starter-template.html` 的 `<style>` 逐值同源;改任一处都要同步另一处,可用 `scripts/check_sync.py` 校验。
