# 发布手册 · Launch playbook

维护者用的发帖清单：写什么、发哪里、什么时候发、发完做什么。
每次发版本都可以直接复用。

> 这不是给使用者看的文档，是给"让更多人找到这个仓库"用的。

---

## 0. 发布前检查（2 分钟）

在 GitHub 仓库 **Settings** 里确认四项：

| 项 | 内容 |
|---|---|
| **Description** | `A desktop sticky note for plans on Windows: daily check-ins, staged goals, auto self-review, 5 themes. Zero dependencies, single file.` |
| **Topics** | 见下方（18 个，按优先级排） |
| **Social preview** | 上传 `docs/shots/social-preview.png`（1280×630） |
| **Template repository** | **取消勾选**（不然仓库顶上会有 "Use this template" 按钮） |

**Topics（复制粘贴，一行一个）**

```
sticky-notes
desktop
windows
productivity
minimalist
todo
planner
note-taking
habit-tracker
python
tkinter
desktop-app
clean-design
offline
local-first
no-dependencies
bilingual
dark-mode
```

然后刷新仓库首页，确认三件事：**动图会动**、**主题大图显示**、**Description 是英文那句**。这三样决定别人点不点进来。

---

## 1. 定位：为什么打"便签"这张牌

2026-11 在 GitHub 搜索 API 上的实测：

| 查询 | 结果 |
|---|---|
| `sticky notes desktop` | **592** 个仓库 |
| 该品类头部项目 PaperTodo | **2,725 ⭐**（Windows 桌面便签 + 待办 + 极简） |
| PaperTodo 的 topics | `sticky-notes` `note-taking` `notes` `todo` `productivity` `desktop` `windows` `minimalist` — **没有 plan** |

结论：

1. **"桌面便签"是有规模、有搜索的品类**，天花板在几千星，值得争取
2. 这个品类的受众按"便签 / 笔记 / 待办 / 生产力"搜索，**不按"计划"搜索**
3. 但不能改名叫便签——用户进来发现不是白纸会走。所以：**借便签的流量进来，用"四段结构化"的差异留住人**

对应到文案：标题/第一句用 `desktop sticky note`，第二句立刻说清"它不是白纸"。

**不要用 `widget` 这个词**：搜 widget 的人期待 Rainmeter 那种可拼装组件，固定形态的卡片会让人失望。

---

## 2. 时间表

| 时间 | 平台 |
|---|---|
| 发布当天白天 | V2EX「分享创造」· 即刻 · 少数派 |
| 当天 **21:00–23:00**（北京） | Show HN —— 对应美东上午 8–10 点 |
| +1 天 | r/SideProject · r/Windows10 |
| +2 天 | Product Hunt（需要预热） |
| +3 天起 | 给 awesome 列表提 PR |

一天最多发两个平台。同一天全平台铺开会被当营销号。

---

## 3. 英文文案

### Show HN

**标题**

```
Show HN: A desktop sticky note for plans – one Tkinter file, no dependencies
```

**首条自评（发完立刻贴）**

```
Author here. My plans kept dying in an app I had to remember to open, so I made
something that sits on the wallpaper instead: no title bar, no taskbar entry,
below every window, never covering what I'm working on.

It looks like a sticky note but isn't free-form, which is the whole point:

- Daily: habits with one Check in button. Every click is recorded, so you get a
  streak and a 30-day rate. The list resets each morning, the history doesn't.
- Stage: goals with a deadline picked from a calendar; the row counts down and
  turns red when late.
- Long-term: ongoing things, shows a percentage.
- Future: a someday list, with no percentage at all.

The self-review at the top is generated from the data (days logged, check-ins,
daily average, best streak) — I never write those by hand.

Tech: pure Tkinter plus a few Win32 calls — SetWindowRgn for the rounded corners,
a layered window for the alpha, and no WS_EX_TOPMOST so it stays below. Zero
third-party dependencies, data in one local JSON file, no account, no network
code. Five themes change fonts, button shapes and section markers, not just
colours.

Windows only, since the Win32 bits are load-bearing. I'd like to know which of the
four sections you'd cut.
```

### r/SideProject

**标题**

```
I built a desktop sticky note for plans — always visible, zero dependencies, 5 themes
```

**正文**

```
My plans kept dying in a notes app I had to remember to open, so I made a card
that sits on the wallpaper: no title bar, no taskbar entry, stays below every
other window.

It looks like a sticky note but it isn't free-form, and that's deliberate:

• Daily — habits with a Check in button; every click is recorded so you get a
  streak and a 30-day rate. The list resets each morning, the history doesn't.
• Stage — goals with a deadline picked from a calendar; the row counts down,
  turns red when late.
• Long-term — ongoing, with a percentage.
• Future — plain someday list, no percentage.
• Auto self-review at the top: days logged, check-ins, daily average, best
  streak — generated, never written by hand.
• 5 themes that change fonts and button shapes, not just colours.
• Opacity slider, renameable title, Chinese/English UI.

No install, no account, no sync, no telemetry. Python stdlib + tkinter only,
data in one JSON file next to the script. Windows 10/11.

Repo + GIF: https://github.com/1072699644-cell/desktop-plan-widget

Feedback welcome — especially on which section you'd cut.
```

### r/Windows10

**标题**

```
A desktop plan widget that sits *under* your windows (Rainmeter-style, but for plans) — no install needed
```

**正文**

```
Sharing a small thing I made for my own desktop.

It behaves like a wallpaper widget: frameless, no taskbar entry, stays below
your other windows, so it never covers what you're working on. Drag it anywhere;
the position is remembered.

Inside: daily habits with check-in history (streaks, 30-day rate), staged goals
with a calendar deadline that counts down and turns red when late, long-term
items with a percentage, and a "future / someday" list. Plus an auto-generated
self-review of the day / week / month.

Five themes (pastel, minimal, ink-wash, neon, Chinese lacquer) — each one also
changes the fonts and button shapes.

Runs on stock Python (tkinter only), single file, no installer, no background
service, no network. Windows 10/11.

GIF and code: https://github.com/1072699644-cell/desktop-plan-widget
```

### Product Hunt

- **Name**: `Plan Card`
- **Tagline**: `A desktop sticky note for plans, on Windows`
- **Description**:

```
Plan Card pins your plan to the wallpaper instead of hiding it in an app.
It looks like a sticky note but is structured: daily check-ins with streaks,
staged goals that count down to a date, long-term progress, and a someday list —
plus a self-review generated from your own data. Five themes change fonts and
button shapes. Zero dependencies, one file, local JSON, no account.
```

---

## 4. 中文文案

### V2EX（「分享创造」节点）

**标题**

```
[分享创造] 一张贴在桌面上的便签，但它是四段有规则的计划
```

**正文**

```
计划写在备忘录里最大的问题是——你得先想起来打开它。结果它永远是一天里最后
才看一眼的东西。

所以我做了一张贴在壁纸上的卡片：无标题栏、不进任务栏、始终沉在其它窗口下面，
不挡工作。看着像便签，但内容不是白纸：

· 每日 —— 习惯。一条一个「打卡」按钮，每次点击都记录，能看到连续天数和
  近 30 天打卡率；清单每天早上重置，记录不会。点行尾「详情」看逐日记录。
· 阶段 —— 有期限的目标。点「期限」弹日历选日期，行内显示「剩 12 天 / 今天 /
  逾期 3 天」，超期变红。
· 长期 —— 持续进行的事，显示完成百分比。
· 未来 —— 纯清单，故意不给百分比。

顶部「自我总结」是自动算的：有记录天数、打卡次数、日均完成、最长连续，可切
日 / 周 / 月——这类东西我自己从来不会手写。

技术上是很土但很轻的路线：Tkinter + 几个 Win32 调用（圆角裁剪、分层窗口透明），
零第三方依赖，单文件，数据就一个本地 JSON，没有账号、没有同步、没有联网代码。
五套主题不只是换色——字体、按钮形态、段标识都换。

Windows 10/11 + Python 3.8+ 即可。
https://github.com/1072699644-cell/desktop-plan-widget

想听听建议，比如四段里你会砍掉哪一段。
```

### 少数派 / 即刻

```
我把「今日计划」做成了一张贴在壁纸上的便签

计划写在备忘录里最尴尬的地方是——你得先想起打开它。
所以我做了一张不进任务栏、始终沉在窗口下面的卡片，抬头就在。

看着像便签，但它不是白纸：
· 每日：点一下打卡，清单每天重置，记录不会
· 阶段：日历选期限，自动倒数，超期变红
· 长期 / 未来：一个有百分比，一个是纯清单
· 自我总结：自动生成，日/周/月，不用写
· 5 套主题：可爱、极简、水墨、科技、中式（字体和按钮形状都不同）

开源、零依赖、单文件、数据只存本地：
https://github.com/1072699644-cell/desktop-plan-widget
```

---

## 5. 发布纪律

**必须做**

- 发完 **2 小时内守在评论区** —— 早期回复直接影响后续曝光
- 英文区只发英文，中文区只发中文
- 贴 GIF，别只贴截图（动图点击率明显更高）
- 有人提 bug 就当天回，然后真的修 —— 这是最好的二次曝光

**绝对不要**

- 在 HN 里提 star / 求投票（会被踩到底）
- 同一天在 5 个平台发同一个链接
- 夸大功能（"比 Notion 强"之类）—— 这个圈子对这点特别敏感
- 忽略"为什么不做 Mac"这类问题，直接答"因为用了 Win32 圆角裁剪"，诚实反而加分

---

## 6. 常见提问的回复模板

| 提问 | 回复 |
|---|---|
| 为什么不是任务管理器？ | Deliberate. Projects, tags and reminders pull the thing toward a full app; the point here is a card you cannot miss. Four sections, one file. |
| 支持 Mac / Linux 吗？ | Not yet — SetWindowRgn and layered windows carry the frameless rounded look. A port would need a different window layer. |
| 会同步吗？ | No. One `plan_data.json`; copy it if you move machines. No account, no network code. |
| 为什么 JSON 键是中文？ | So switching the UI language never touches your data — no migration, no lost plans. Only the interface is translated. |
| 能加一个功能 X 吗？ | Open an issue with the problem rather than the solution; if it fits "one card, four sections", it usually ships. |

---

## 7. 长期流量

- **awesome 列表 PR**（`awesome-windows` `awesome-tkinter` `awesome-productivity` `awesome-desktop-customization`）：
  一条 PR 文案见下，一次性提交，长期曝光
- 每个版本发 GitHub Release，写清楚改了什么（Release 页也会被搜索索引）
- 有人的截图用得好，就去 Issue / Discussions 里请他贴，当作二次素材

**awesome PR 条目**

```markdown
- [Plan Card](https://github.com/1072699644-cell/desktop-plan-widget) — A desktop sticky note for plans on Windows: daily check-ins with streaks, staged goals with deadlines, auto self-review, 5 themes. Zero dependencies.
```

**awesome PR 描述**

```
Adds Plan Card, a Windows-only desktop widget written in Python (tkinter, no
third-party dependencies).

It pins itself below other windows as a frameless card and covers daily habit
check-ins (streaks + 30-day rate), staged goals with a calendar deadline,
long-term progress and a "someday" list — plus a self-review generated from the
data. Five themes change fonts, button shapes and section markers.

Data is a local JSON file: no account, no sync, no telemetry. MIT licensed,
single file, no installer.
```
