# 项目说明 · How Plan Card is built

写给想改它、扩展它、或者单纯好奇“一个 70 KB 的 Tkinter 脚本怎么做出一张像样的桌面卡片”的人。

- 只是想用？看 [使用说明](使用说明.md)
- 想装／下载？看 [README](../README.md)
- English summary at the bottom.

---

## 0. 三分钟读懂

```
┌─────────────────────┐
│   plan_card.pyw     │  窗口 · 布局 · 交互 · 主题 · i18n 装配
│     70 KB           │  全部 UI 在这里，没有框架
└─────────┬───────────┘
          │ import
   ┌──────┴───────┐
   ▼              ▼
┌──────────┐  ┌──────────┐
│tools/    │  │tools/    │
│plan.py   │  │i18n.py   │
│数据层    │  │词表      │
└────┬─────┘  └──────────┘
     │ 读写
     ▼
 plan_data.json        ← 唯一的持久化，纯本地
```

三层，没有更多：

| 层 | 文件 | 职责 | 不负责什么 |
|---|---|---|---|
| UI | `plan_card.pyw` | 画窗口、收点击、算高度、换主题 | 不碰文件 IO |
| 数据 | `tools/plan.py` | 读/写 JSON、打卡记录、自动总结、示例播种 | 不知道控件的存在 |
| 文案 | `tools/i18n.py` | 中英词表、语言检测、本地化日期 | 不引用 TK |

三个都是纯标准库。`plan_card.pyw` 只 `import plan`，没有第三方包，也没有隐藏的
运行依赖。

---

## 1. 为什么是 Tkinter + Win32

要的东西很具体：**一张贴在壁纸上的卡片**——无边框、圆角、半透明、沉在别的窗口下面。

| 需求 | 实现 | 为什么不用更“现代”的方案 |
|---|---|---|
| 无边框 | `root.overrideredirect(True)` | Tk 原生支持，一行 |
| 圆角 | `CreateRoundRectRgn` + `SetWindowRgn` | Tk 无法给窗口做圆角，必须走 Win32 |
| 半透明 | `root.attributes("-alpha", v)` | 分层窗口，Tk 封装好了 |
| 沉在下面 | 不加 `WS_EX_TOPMOST` | 默认就是普通层级，切窗口时自动让位 |
| 拖动 | 自己绑 `<ButtonPress-1>` / `<B1-Motion>` | 无边框窗口没有系统标题栏可拖 |

**为什么不 Qt / Electron**：为了一个挂件引入 50 MB 运行时，和“下载就能跑”的定位冲突。
这个项目的硬约束一直是「**装过 Python 就能运行**」，所以宁可自己画按钮，也不引 UI 库。

代价也要承认：Tk 的控件不能单独圆角（见第 6 节），界面能力上限不高。

---

## 2. 启动顺序（这顺序有讲究）

```python
main()
 └─ _single_instance()        # 命名互斥量，防止开两张卡
 └─ root = tk.Tk(); root.overrideredirect(True)
 └─ Card(root)
     ├─ 读一下 plan_data.json 里的 "语言"     ← 必须最先做
     ├─ I18N.set_lang(pref)                  ← 因为下一步可能播种示例
     ├─ PL.load()                            ← 没有数据文件就复制示例
     ├─ apply_theme(主题)                     ← 把调色板灌进全局变量
     ├─ _build()                             ← 建静态骨架（表头/输入框/滚动区）
     ├─ refresh()                            ← 建所有行
     ├─ _fit()                               ← 迭代算高度
     └─ _fade_in()                           ← 透明度淡入
```

**为什么语言要排在读数据前面**：首次运行会从 `sample/` 播种示例数据，中文环境要用
中文示例、英文环境用英文示例。谁先谁后错了，英文用户第一次打开会看到中文示例。

**为什么主题在 `_build` 前面**：所有控件在创建时就从**全局变量**取色
（`bg=BG` 这种写法），所以先把主题灌进全局变量，后面新建的一切自然是对的。

---

## 3. 窗口与自适应高度

### 布局骨架

```
root
└─ outer
   ├─ bar              (60px, 标题 + 元信息 + ⚙ + 进度环)
   ├─ hairline         (1px)
   ├─ bottom  ← 先 pack(side="bottom")   ← 关键
   └─ scroll (fill both, expand)
      └─ inner          (所有段和行都在这)
```

**`bottom` 必须先 pack**：Tk 的 pack 按顺序分配空间，如果把 `expand=True` 的滚动区
先 pack，它会吃掉全部高度，输入框就被压成 0——这是本项目的第一个坑。

### 高度怎么算

卡片高度不是写死的，是**迭代收敛**出来的：

```python
for _ in range(4):
    bh = self.bottom.winfo_reqheight()
    need  = 61 + self.inner.winfo_reqheight() + bh + 22   # 表头+内容+输入框+余量
    floor = 61 + bh + 22 + 34                             # 至少「表头+输入框+一行」
    avail = max(220, scr_h - taskbar - py)                # 最多到屏幕底部
    h2 = max(150, floor, min(avail, need))
    geometry(...)
    if abs(h2 - h) <= 1: break
```

为什么要循环 4 次：**宽度决定文字换行，换行决定内容高度，高度又影响是否需要滚动条**。
一次算不准。用 `_fitting` 标志挡住 `geometry()` 回调引发的递归。

两个兜底保证「输入框永不消失」：

1. `floor`：至少留出表头 + 输入框 + 一行
2. 屏幕底部放不下 → 整体上移；实在放不下再压高度

---

## 4. 数据模型

`plan_data.json`，**键名是中文，这是有意的**（见第 10 节）。

```jsonc
{
  "位置": [56, 300],           // 窗口坐标，拖动后写回
  "名称": "",                  // 空 = 用默认标题（跟随语言）
  "语言": "auto",              // auto / zh / en
  "主题": "水墨",              // 主题名（中文键）
  "透明度": 0.9,               // 0.30 – 1.00
  "总结页": "日",              // 自我总结记住的页签
  "折叠": ["阶段"],            // 收起的段
  "新计划归入": "每日",         // 输入框左侧的目标段

  "天": {
    "2026-11-08": {
      "条目": [
        {
          "文字": "早上 7:00 起床，读 30 页书",
          "完成": true,
          "重要": "高",              // 高 / 中 / 低
          "细节": [                  // 子计划
            { "文字": "第三章", "完成": false }
          ],
          "id": "demo0001"           // 只有每日计划有，跨天不变
        }
      ]
    }
  },

  "阶段计划": { "条目": [ { "…": "…", "结束日期": "2027-01-07" } ] },
  "长期计划": { "条目": [ … ] },
  "未来计划": { "条目": [ … ] },

  "打卡记录": {
    "demo0001": { "2026-11-07": true, "2026-11-08": false }
  }
}
```

三条设计取舍：

1. **每日按天存**（`天[日期]`），其它三段存独立键 —— 因为只有每日需要翻页
2. **每日计划带 `id`** —— 清单每天重置，但记录必须挂在同一条习惯上
3. **打卡记录与清单解耦** —— `id → 日期 → bool`，这样查历史不用扫所有天

字段全集见 `tools/plan.py` 的 `_norm_item()`，它会把读到的数据补齐成这个形状。

---

## 5. 每日打卡：为什么是“复制清单”而不是“顺延未完成”

```
点击打卡 → 改 完成 → record_day() 写入 打卡记录[id][今天] = is_done
跨天     → carry_over() 把昨天整张清单复制过来，完成状态清零（子计划也清零）
```

一开始的实现是「把昨天没做完的搬到今天」，结果发现对习惯类计划是错的：

- 今天三项全打完 → 明天清单是**空的**，习惯消失了
- 而打卡制的语义应该是「**每天都重新来一遍**」

所以改成整表复制 + 清零。要彻底删掉某条习惯，点 `✕`。

**ID 必须跨天不变**，否则「连续 3 天」「近 30 天 71%」这种聚合根本串不起来。
`ensure_id()` 在 `load()` 时给缺 ID 的条目补一个 `uuid4().hex[:8]`。

有子计划的条目：**子计划全部完成**才算这条完成（`is_done()`）。

---

## 6. 主题引擎：配色 + 形态

主题不只是颜色，还带**形态参数**：

```python
"水墨": dict(
    bg="#f2eee3", fg="#24211c", sub="#6d6559", dim="#9c9284",
    acc="#8c2f24", ok="#4b7b5a", on_acc="#ffffff",
    danger="#8c2f24", card_hi="#fbf8f1",
    pri=["#8c2f24", "#4b6b52", "#9c9284"],   # 高 / 中 / 低
    fam="楷体",            # 标题、段名、按钮文字
    btn=("ink", 0),        # 按钮形态 + 圆角
    dot="bar",             # 段标识形状
    chk=1.6,               # 勾选框描边宽度
    sec=["#3a352e", "#4f6360", "#7a5c44", "#5f7052"],   # 四段色
)
```

### 次级色自动推导

浅色主题和深色主题，次级色的**变化方向是相反的**（一个要变暗、一个要变亮）：

```python
def _shift(bg, t):
    """朝对比方向偏移：深底更亮，浅底更暗。"""
    return _dark(bg, t) if _is_light(bg) else _light(bg, t)
```

于是悬停底色、分割线、输入框、小胶囊、行尾图标的淡色全部由 `bg` 推导出来——
**新加主题只需要给底色 + 强调色**，其余自动协调。

### 按钮与标识必须自绘

Tk 的 `Label` 不支持单独圆角，所以打卡按钮、段标识、勾选框都是 `Canvas`：

```python
def _rr(cv, x0, y0, x1, y1, r, **kw):
    """圆角矩形：r<=0 时退化成 create_rectangle"""
    pts = [x0+r,y0, x1-r,y0, x1,y0, x1,y0+r,
           x1,y1-r, x1,y1, x1-r,y1, x0+r,y1,
           x0,y1, x0,y1-r, x0,y0+r, x0,y0]
    return cv.create_polygon(pts, smooth=True, **kw)   # smooth 让棱角变圆
```

五种按钮形态：`fill` 圆角实心 / `outline` 直角描边 / `ink` 墨线 / `bracket` 双括号 /
`seal` 印章。五种段标识：`circle` / `square` / `bar` / `tick` / `diamond`。

**换主题 = 整卡重建**（`apply_theme()` → `_build()` → `refresh()`）。看起来粗暴，
但比“遍历控件改色”可靠得多——因为形态（圆角、描边、字体）也变了，改色改不了形状。
重建一次约 20 ms，人感觉不到。

---

## 7. 国际化

```python
L("打卡")     # 中文原样返回；英文查表 → "Check in"
```

**用中文原文当 key**，好处是界面代码只需包一层 `L()`：

- 漏翻会立刻暴露（英文界面里冒出中文），不会悄悄用错 key
- 不用维护第二套命名，改文案时改一处
- 查不到就回退原文，**永远不会崩**

语言：`auto`（跟系统）/ `zh` / `en`，存进数据文件。切换语言同样是整卡重建。

英文下额外适配（不能只换文字）：

| 项 | 中文 | 英文 |
|---|---|---|
| 行内左栏宽度 | 86 px | 108 px |
| 打卡按钮宽度 | 56 px | 78 px |
| 日期格式 | `11月8日 周日` | `Sun, Nov 8` |
| 数字字体（科技主题） | 苹方 | Consolas |

**坑**：语言必须在 `load()` 之前确定（第 2 节），否则示例数据语言会选错。

---

## 8. 行是怎么画出来的

每行结构（`_row()`）：

```
wp (行容器)
└─ row
   └─ line
      ├─ col (固定宽度 86/108)      ← 左栏：打卡按钮 / 重要性 / 期限 / 勾选框
      │    └─ 先塞一个 expand=True 的空 Frame 当弹簧，把内容推到右边
      ├─ txt                        ← 正文，wraplength = W - 188
      └─ 右侧：⇄  ›  ✕  + 详情/百分比
```

**左栏固定宽度 + 弹簧**，是为了让四段的**正文左边缘完全对齐**。否则中文字段宽度不同，
正文会参差不齐。

**行尾三个符号平时很淡**（`FAINT` 色），鼠标进入该行才点亮（`HOTFG`，`✕` 变红）。
这是刻意的：平时只留内容，减少视觉噪音。

**每次 `refresh()` 都重建所有行**，不做增量更新。理由：行数最多几十条，重建成本远低于
维护差分的复杂度；而折叠、换主题、换语言、拖动排序都需要重建，统一处理反而更少 bug。

### 单击 vs 双击

单击行文字 = 勾选。但双击要用来编辑，所以单击会**延迟 230 ms** 执行：

```python
self._pending_toggle = i
self.root.after(230, lambda: self._fire_toggle(i))
```

双击时 `_on_dbl()` 把 `_pending_toggle` 清空并置 `_dbl_guard`，排队的勾选就不会触发。
不这么做的话，双击一次会勾两次、**记两条打卡**。

---

## 9. 自动总结的算法

```python
_day_stats(d, day)      # 某天 (完成数, 总数)
_streak_upto(d, day)    # 从某天往前数，连续「当天全打完」的天数
_range_days(scope, off) # 周 / 月的日期区间
```

| 周期 | 统计项 |
|---|---|
| 日 | 每日打卡 n/m、连续打卡、阶段 n/m、长期 n/m |
| 周 / 月 | 有记录天数、打卡次数、日均完成、最长连续、阶段/长期 |

两个容易做错的地方：

- **日均完成**按条目加权（`Σ完成 ÷ Σ总数`），不是“每天百分比的平均”。条目多的那天权重
  应该更大，否则一条计划的轻量日会和五条计划的重度日等价。
- **打卡次数**从 `打卡记录` 里按日期区间统计，不是从清单里数——清单每天重置，数不出来。

总结是**纯函数**：`auto_summary(data, scope, offset) → {head, rows}`，不写数据、不碰 UI，
所以可以单独测。

---

## 10. 有意为之的几个“奇怪决定”

| 决定 | 原因 | 代价 |
|---|---|---|
| **JSON 键用中文**（`每日`/`条目`/`完成`） | 切换语言时旧数据不用迁移；数据即文档 | 英文贡献者第一眼会愣一下 |
| **每次刷新重建全部行** | 逻辑简单，不会出现“状态不同步”的诡异 bug | 行数极大时（>200）会有可见卡顿 |
| **i18n 用中文原文当 key** | 漏翻立刻可见，不维护第二套 key | 词表看起来是同义反复 |
| **不做增量更新、不做事件总线** | 70 KB 的项目不需要架构 | 扩展功能时要改 `refresh()` |
| **示例数据靠播种而不是硬编码** | 用户能改、能删，示例本身也是文档 | 首次运行多一次文件写入 |

---

## 11. 已知边界

- **Windows only** —— 圆角裁剪、分层窗口都依赖 Win32
- **Tk 无法给任意控件圆角** —— 只有「整窗裁剪」和「Canvas 自绘」两条路
- **字体依赖系统** —— 苹方 / 楷体缺失时回退默认字体，观感会降级
- **不是任务管理器** —— 没有项目、标签、提醒、同步；这是产品选择，不是待办
- 显示缩放 ≠ 100% 时布局会偏紧（按 1080p / 100% 设计）

---

## 12. 想改它？从这几处下手

| 想做什么 | 改哪里 |
|---|---|
| 加一套主题 | `THEMES` 加一个 dict + `THEME_ORDER`、`i18n.EN` 加显示名，见 [CONTRIBUTING](../CONTRIBUTING.md) |
| 加一门语言 | `tools/i18n.py` 复制 `EN` 字典翻译，注册到 `LANGS` / `L()` |
| 改行的外观 | `_row()`：左栏 `col`、正文 `txt`、行尾 `acts` |
| 加一段计划 | `plan.py` 的 `MODES` / `load()` / `get_list()`，`plan_card.pyw` 的 `SECTION_STYLE` |
| 改自动总结的统计 | `plan.py` 的 `auto_summary()`（纯函数，随便改） |

**改完的验收清单**（手动）：

1. 四段都还在，正文左边缘对齐
2. 点一次打卡 → 打开「详情」→ 记录出现了
3. 换主题不崩、颜色不串（尤其浅色主题的次级色）
4. 中英切换后没有截断的文字
5. 旧数据文件能正常读入

---

## English summary

Plan Card is a single-file Tkinter desktop widget with three layers and no third
party dependencies.

- **`plan_card.pyw`** — window and UI. A frameless, rounded, translucent window
  built with `overrideredirect` plus `SetWindowRgn`; height is computed
  iteratively because wrapping depends on width and vice versa. Every refresh
  rebuilds the rows — cheap at this scale, and it removes a whole class of
  state-sync bugs.
- **`tools/plan.py`** — the data layer: JSON read/write, the four sections, daily
  check-in records keyed by a stable per-plan ID, and a pure `auto_summary()`
  function.
- **`tools/i18n.py`** — a Chinese→English dictionary keyed by the Chinese source
  string, so the UI only needs `L("打卡")` and an untranslated string is obvious
  rather than silent.

Design notes worth knowing: data keys stay Chinese on purpose (no migration when
the UI language changes), secondary colours are derived from the background
(lighter on dark themes, darker on light ones), and each theme also carries font,
button-shape and marker parameters, so switching themes rebuilds the card instead
of recolouring it.

Known limits: Windows only (Win32 window tricks), intentionally not a task
manager, and it assumes 100 % display scaling.
