# Plan Card · 桌面计划表

A tiny **Windows desktop plan card** that sits on your wallpaper: daily check-ins,
staged goals, long-term and future plans — with an auto-generated self-review,
a date-picker for deadlines, and 5 hand-tuned themes.

**One file · zero dependencies · data stays on your machine.**

[English](#english) · [中文](#中文)

![Plan Card](docs/shots/theme-ink.png)

---

## English

### What it is

A frameless, always-available plan card for Windows. It is a plain Tkinter app
that does not install anything and does not phone home — every plan lives in one
JSON file next to the script.

Four sections, always visible at once:

| Section | What it's for | Behaviour |
|---|---|---|
| **Daily** | today's habits | one **Check in** button per row; each click records today. The list resets every morning |
| **Stage** | goals with a deadline | pick a deadline from a **calendar**; shows `12d` / `Today` / `3d late` |
| **Long-term** | ongoing things | no deadline, shows progress % |
| **Future** | someday / maybe | a plain list, no percentages |

### Features

- **Daily check-in with history** — click *Check in*, it turns green and is
  recorded. Open **History** on any daily row to see the last 14 days plus
  `N check-ins · N-day streak · N% in 30 days`.
- **Auto self-review** — collapses to one line; click to expand. Computed from
  your data: days logged, check-ins, daily average, best streak, stage/long-term
  progress. Day / Week / Month switch.
- **Deadline calendar** — click the date chip, pick a day, done. No typing.
- **Move plans between sections** — click `⇄` or just drag a row onto another
  section.
- **Collapsible sections**, thin scroll indicator, and an input box that is
  always visible.
- **5 themes** — Cute / Minimal / Ink / Tech / Chinese. Each changes colours,
  **fonts, button shapes and section markers**, not just a colour swap.
- **Opacity 30–100 %** and a **renameable title**.
- **Bilingual UI** — Chinese or English, follows your system language, switchable
  in settings.

### Themes

| | | |
|---|---|---|
| ![cute](docs/shots/theme-cute.png) | ![minimal](docs/shots/theme-minimal.png) | ![ink](docs/shots/theme-ink.png) |
| **Cute** | **Minimal** | **Ink** |
| ![tech](docs/shots/theme-tech.png) | ![cn](docs/shots/theme-cn.png) | ![english](docs/shots/theme-english.png) |
| **Tech** | **Chinese** | **English UI** |

### Quick start

1. Install **Python 3.8+** for Windows (tkinter is included).
2. Download `plan_card.pyw` and the `tools/` folder, keeping them side by side.
3. Double-click **`plan_card.pyw`**.

On first launch it seeds a set of **sample plans** so you see the card in
action — edit or delete them freely. Your data is written to `plan_data.json`
next to the script.

### Using it

| Action | How |
|---|---|
| Add a plan | type in the bottom box, press `Enter` |
| Choose which section it goes to | click the small chip on the left of the input box |
| Check in (daily) | click **Check in** |
| Edit text | **double-click** the row |
| Delete | click `✕` at the right of the row (appears on hover) |
| Reorder | drag a row up or down |
| Move to another section | click `⇄`, or drag onto the other section |
| Sub-tasks | click `›` on the right of a row |
| Deadline (stage) | click the `date` chip → calendar |
| Settings | click the ⚙ at the top right |

Full manual: [docs/Usage.md](docs/Usage.md) ·
中文版: [docs/使用说明.md](docs/使用说明.md) ·
How it's built: [docs/Architecture.md](docs/Architecture.md)

### Requirements

- **Windows 10 / 11** (uses Win32 APIs for the frameless, rounded, transparent
  window — macOS and Linux are not supported)
- **Python 3.8+**, standard library only (no `pip install`)
- Fonts: uses Windows fonts (PingFang SC / 楷体 when available, otherwise the
  system default)

### Privacy

Everything is local. `plan_data.json` never leaves your machine; there is no
network code in this project.

### License

MIT — see [LICENSE](LICENSE).

---

## 中文

### 这是什么

一张贴在 Windows 桌面上的**无边框计划卡片**：每日打卡、阶段目标、长期规划、未来清单，
四段**同时铺开**，配自动生成的自我总结、日历选期限、5 套主题。

**单文件 · 零依赖 · 数据只在你本机。**

### 四段计划

| 段落 | 用途 | 特点 |
|---|---|---|
| **每日** | 今天的习惯 | 每行只有一个 **打卡** 按钮，点一次记录一天；第二天清单重置，记录保留 |
| **阶段** | 有期限的目标 | 点 **期限** 弹日历选日期；自动显示 `剩 12 天` / `今天` / `逾期 3 天` |
| **长期** | 长期要做的事 | 不设期限，显示完成百分比 |
| **未来** | 以后想做的 | 纯清单，不显示百分比 |

### 功能

- **打卡 + 时间详情** — 点「打卡」变绿并记录；点行尾「详情」看最近 14 天，以及
  `打卡 N 天 · 连续 N 天 · 近 30 天 N%`
- **自动自我总结** — 默认收起一行，点开看：有记录天数、打卡次数、日均完成、
  最长连续、阶段/长期进度，可切 **日 / 周 / 月**
- **日历选期限** — 点「期限」直接点日子，不用手打
- **换分类** — 点 `⇄` 菜单，或把整条拖到别的段
- **段可收起**、细滚动条、输入框永远钉在底部
- **5 套主题** — 可爱 / 极简 / 水墨 / 科技 / 中式，除了配色，
  **字体、按钮形态、段标识形状**全都不同
- **透明度 30%–100%**、**标题可改名**
- **中英双语界面** — 跟随系统语言，设置里可手动切

### 快速开始

1. 装 **Python 3.8+**（Windows 版自带 tkinter）
2. 下载 `plan_card.pyw` 和 `tools/` 文件夹，放在同一目录
3. 双击 **`plan_card.pyw`**

第一次启动会**自动载入一组示例计划**，随便改随便删。数据写在同目录的
`plan_data.json`。

### 常用操作

| 做什么 | 怎么做 |
|---|---|
| 加一条计划 | 底部输入框写，回车 |
| 选加进哪一段 | 点输入框左边的小胶囊 |
| 每日打卡 | 点 **打卡** |
| 改文字 | 行上**双击** |
| 删除 | 点行尾 `✕`（鼠标移上去才出现） |
| 排序 | 按住行上下拖 |
| 换分类 | 点 `⇄`，或拖到别的段 |
| 子计划 | 点行尾 `›` |
| 设期限（阶段） | 点 `期限` → 日历 |
| 设置（主题/透明度/改名/语言） | 点右上角 ⚙ |

完整说明：[docs/使用说明.md](docs/使用说明.md) ·
技术实现：[docs/Architecture.md](docs/Architecture.md)

### 环境要求

- **Windows 10 / 11**（无边框、圆角、半透明用了 Win32 API，macOS / Linux 不支持）
- **Python 3.8+**，只用标准库，不需要 `pip install`
- 字体：优先用系统的苹方 / 楷体，没有就回退默认字体

### 隐私

全部本地运行，`plan_data.json` 不会上传到任何地方，代码里没有任何联网逻辑。

### 许可

MIT，见 [LICENSE](LICENSE)。
