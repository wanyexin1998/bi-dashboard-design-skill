# 图表语言 — Wyexin BI 图表规范(ECharts)

图表是这套 DNA 最有辨识度的部分。先读「全局规则」,再按需查具体图型。代码片段基于 ECharts 5,可直接改造。

## 目录
1. 全局规则(轴/网格/标签/图例)
2. 系列颜色语义(恒定约定)
3. 签名图型:目标达成组合图
4. 常用图型速查(柱/条/线/面积/环/漏斗等)
5. 高级图型(拆解树/帕累托/桑基/散点象限/热力/地图/小多图)
6. ECharts 公共配置片段

---

## 1. 全局规则

- **数据标签常开**:11px,颜色随系列或 `#4E5969`。因为标签常开,y 轴可以整体隐藏——这是本风格"密而不乱"的关键交换。
- 网格线:仅保留横向 `#EEF1F6` 实线(或全部隐藏);x 轴线 `#E5E6EB`,刻度不外露。
- 轴标签:11px `#86909C`;类目多时 0° 不倾斜、隔项显示,宁可省略不可斜排。
- 图例:顶部居中,10–11px,圆点/短条 icon;系列 ≤2 且含义自明时省略图例。
- 留白:`grid:{top:36,right:16,bottom:28,left:16,containLabel:true}`。
- 动效:初次渲染 500ms 缓动即可,不做循环动画。
- tooltip:白底、`--hairline` 描边、圆角 6px、小阴影;`axisPointer:'shadow'`。
- **防溢出七条**(权威清单与阈值在 layouts.md §6;此处是写 ECharts 配置时的速记):①`containLabel:true`;②柱顶标签留头 `yAxis.max:v=>v.max*1.15+`;③横向条 `grid.right≥48`;④长类目名 formatter 截断;⑤窄卡环图禁引出标签改图例;⑥大数值换「万/亿」;⑦容器固定高度+`resize` 监听。

## 2. 系列颜色语义(恒定约定,跨看板不变)

| 系列 | 颜色 | 形态 |
|---|---|---|
| 去年/基期 | 灰渐变 `#9CA3AF→#D6DAE1` | 柱,排组内第一位 |
| 当期(月) | 主题主色渐变 | 柱 |
| 当期(年/年累计) | 橙渐变 `#F59A3C→#FBD3A2` | 柱/环/进度条 |
| 目标 | 珊瑚渐变 `#F08A7E→#F5B1A8` | 柱,排组内最后 |
| 达成率 | `#E64C45` 红实线 | 折线,浮于柱区上方 |
| 同比/环比率 | `#6B7280` 深灰实线 | 折线,浮于最上层 |
| 时间进度 | `#E64C45` 竖直虚线 markLine | 贯穿参考线 |
| 收入/流入 | 主题主色 | 任意 |
| 支出/流出/风险 | `#E64C45` | 任意 |

「月蓝年橙、灰是过去、红是差距」——记住这句即可徒手配色。

## 3. 签名图型:目标达成组合图

一张图讲完「去年—今年—目标—达成率—同比」。布局特征:**柱群贴地,双折线悬浮于上方独立空域**,上下不打架。实现:柱与两条率线各绑一条独立 y 轴;率线的轴范围**按数据自身值域反推**(而非写死偏移),把线锁进指定的纵向带,任何量级的数据都不会错层或压柱。

```js
// 把某序列压进绘图区的一条纵向带 [f0,f1](0=底 1=顶),按该序列自身值域反推轴 min/max。
// 关键:不用 +offset 魔法数,换任何量级的数据(百分率/小数/极端值)两条率线都稳定分层、悬浮于柱上。
function bandAxis(arr, f0, f1){
  const dmin=Math.min(...arr), dmax=Math.max(...arr);
  const span=(dmax-dmin)||Math.abs(dmax)||1;        // 单值/全零兜底,避免除零
  const range=span/(f1-f0), min=dmin-f0*range;
  return {type:'value', show:false, min, max:min+range};
}
function targetComboOption(cats, lastYear, current, target, rate, yoy, theme){
  const g=(c1,c2)=>({type:'linear',x:0,y:0,x2:0,y2:1,colorStops:[{offset:0,color:c1},{offset:1,color:c2}]});
  return {
    legend:{top:0,itemWidth:8,itemHeight:8,textStyle:{fontSize:10,color:'#86909C'}},
    grid:{top:110,left:8,right:8,bottom:24,containLabel:true},
    xAxis:{type:'category',data:cats,axisTick:{show:false},
      axisLine:{lineStyle:{color:'#E5E6EB'}},axisLabel:{fontSize:11,color:'#86909C'}},
    yAxis:[
      {type:'value',show:false,min:0,max:v=>v.max*2}, // 柱轴:柱群只占底部约一半,给上方两条率线让出空域
      bandAxis(rate, 0.58, 0.76),                     // 达成率线带
      bandAxis(yoy,  0.84, 0.98)                      // 同比线带(更靠上,与达成率分层)
    ],
    series:[
      {name:'去年',type:'bar',yAxisIndex:0,data:lastYear,barMaxWidth:16,itemStyle:{color:g('#9CA3AF','#D6DAE1'),borderRadius:[3,3,0,0]},
       label:{show:true,position:'top',fontSize:10,color:'#9CA3AF'}},
      {name:'当期',type:'bar',yAxisIndex:0,data:current,barMaxWidth:16,itemStyle:{color:g(theme.primary,theme.primarySoft),borderRadius:[3,3,0,0]},
       label:{show:true,position:'top',fontSize:10,color:theme.primary,fontWeight:600}},
      {name:'目标',type:'bar',yAxisIndex:0,data:target,barMaxWidth:16,itemStyle:{color:g('#F08A7E','#F5B1A8'),borderRadius:[3,3,0,0]},
       label:{show:true,position:'top',fontSize:10,color:'#F08A7E'}},
      {name:'达成率',type:'line',yAxisIndex:1,data:rate,symbol:'circle',symbolSize:5,
       lineStyle:{color:'#E64C45',width:2},itemStyle:{color:'#E64C45'},
       label:{show:true,position:'top',fontSize:10,color:'#E64C45',formatter:'{c}%'}},
      {name:'同比',type:'line',yAxisIndex:2,data:yoy,symbol:'circle',symbolSize:5,
       lineStyle:{color:'#6B7280',width:2},itemStyle:{color:'#6B7280'},
       label:{show:true,position:'top',fontSize:10,color:'#6B7280',formatter:'{c}%'}}
    ]};
}
```
**为什么按值域反推**:柱群绑轴 0(`max:v=>v.max*2`,只占底部约一半);两条率线各绑一条隐藏轴,`bandAxis()` 按各自 min/max 把线锁进固定纵向带(达成率 58–76%、同比 84–98%)。于是 `data` 直接传真实值,标签用 `{c}%`、tooltip 也显示真值——彻底去掉 `+150` 这类魔法偏移和还原逻辑。换数据只改数组,无需手调轴范围。若某指标达成率天然超 300% 或同比跨越极端负值,带内自动缩放仍成立。

## 4. 常用图型速查

### 4.1 竖向柱
渐变必开:`{type:'linear',y:0,y2:1}` 顶部主色→底部 `--primary-soft`;`borderRadius:[3,3,0,0]`;`barMaxWidth:18`;标签置顶。双色简化场景(如仅 预约/履约)可用 浅蓝/藏青 两阶。

### 4.2 横向条(排名 TOP-N)
- 类目倒序(第一名在顶);条渐变左浅右深;值标签在条尾外侧。
- `barMaxWidth:12`,行高稀疏;超过 15 行考虑分页或截断 TOP15。
- 极简变体:无轴无网格,细条 4px + 右侧纯数值(轻量排行榜)。
- 加达成率红线的横向版:预约/履约横条 + 红线履约率(横条版组合图)。

### 4.3 折线与面积
- 趋势主线:主题色 2px,`smooth:true`,symbol circle 4,关键点标签常开。
- 面积图:线下渐变 `rgba(primary,.22)→透明`;日趋势、访客趋势用。
- 双轴收支线:收入主题色 vs 支出红,零轴分明;适合积分/现金流监测。
- 历史-预测并置:「前14日 | 后14日」两张镜像卡并排,预测线用虚线。

### 4.4 环图(占比)
- `radius:['58%','78%']`,引出标签两行:`名称`/`值 (占比%)`;标签颜色随扇区。
- 分类 ≤6,超出并入「其他」;分类色板按 tokens 顺序取。
- 中心可放主指标名或总计。
- 双指标图例变体:图例列在左侧,每项「名称 同比% 占比%」。
- 嵌套环:内环大类、外环子类,同色系深浅关联。
- 2×2 画像矩阵:四张小环图(性别/年龄/渠道/新老客)拼一卡。

### 4.5 堆叠柱
分段 ≤5 色(分类色板顺序),顶部总计标签 + 段内值标签(段高不足时省略);用于渠道结构月趋势。

### 4.6 漏斗
梯形渐变(主题色系由深到浅),右侧配转化率箭头标注「82.1% ↓」;或用 ECharts funnel + 自定义 graphic 箭头。销售过程、履约链路用。

### 4.7 雷达
主题色 + 分类色多边形,面积填充 12% 透明度;维度 5–6 个;渠道健康评估用。

## 5. 高级图型

- **指标拆解树**:KPI 因子分解(如 下单金额=活跃代理数×销售力)。节点=蓝底标题白字+白底数值卡(数值+环比),连线灰细线,节点间放「×」「+」运算符圆标。用 HTML/CSS 搭比 ECharts 容易。
- **生命周期 chevron**:纵向蓝渐变箭头段(分享转化→裂变复购→…),右侧对应阶段指标行。HTML/CSS 实现。
- **帕累托(ABC)**:柱(分类色按 A/B/C 分组)+ 累计占比红/灰线 + 80/90% 参考虚线。
- **散点象限**:散点按等级着色,`markLine` 画均值虚线(红)十字分象限;波士顿矩阵/渠道贡献用。
- **桑基**:流转分析;节点色取分类色板,链接半透明。
- **热力表格**:单色阶(主题色 10%→100%),数值常开白字/深字自适应;渠道×业务矩阵用。
- **中国地图**:visualMap 单色阶(主题色),仅标注 TOP 省份数值;客源分布用。
- **小多图行**:行标签 + 行内迷你趋势线,纵向堆叠(设备使用、多科室对比);每行一个 60px 高 mini line。
- **日历热力**:按日巡检场景,选中日主色块。

## 6. ECharts 公共配置片段

```js
const WY_BASE = {
  textStyle:{fontFamily:'"PingFang SC","Microsoft YaHei",system-ui,sans-serif'},
  tooltip:{backgroundColor:'#fff',borderColor:'#E9EDF3',borderWidth:1,
    textStyle:{color:'#1D2129',fontSize:12},extraCssText:'box-shadow:0 4px 12px rgba(29,33,41,.08);border-radius:6px;'},
  grid:{top:36,left:16,right:16,bottom:28,containLabel:true},
  categoryAxis:{axisTick:{show:false},axisLine:{lineStyle:{color:'#E5E6EB'}},
    axisLabel:{fontSize:11,color:'#86909C'}},
  valueAxis:{axisLine:{show:false},axisTick:{show:false},
    splitLine:{lineStyle:{color:'#EEF1F6'}},axisLabel:{fontSize:11,color:'#86909C'}},
};
// 渐变工具
const vGrad=(c1,c2)=>({type:'linear',x:0,y:0,x2:0,y2:1,colorStops:[{offset:0,color:c1},{offset:1,color:c2}]});
const hGrad=(c1,c2)=>({type:'linear',x:0,y:0,x2:1,y2:0,colorStops:[{offset:0,color:c1},{offset:1,color:c2}]});
```

**在 BI 工具(Quick BI / FineBI 等)中落地**:无法写代码时,把上述规则翻译为工具配置——手动指定系列色与渐变、打开数据标签、隐藏 y 轴、图例顶部居中、目标线/辅助线用红色虚线、柱宽收窄。规则本身与工具无关。
