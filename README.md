<div align="center">

# Plan Card

**A frameless Windows desktop plan card — it just sits on your wallpaper.**

Daily check-ins · staged goals · auto self-review · 5 themes

<img src="https://img.shields.io/badge/platform-Windows-0078d4?logo=windows&logoColor=white" alt="Windows">
<img src="https://img.shields.io/badge/python-3.8%2B-3776ab?logo=python&logoColor=white" alt="Python 3.8+">
<img src="https://img.shields.io/badge/license-MIT-2ea44f" alt="MIT">
<img src="https://img.shields.io/badge/dependencies-0-brightgreen" alt="No dependencies">
<img src="https://img.shields.io/badge/UI-%E4%B8%AD%E6%96%87%20%2F%20English-e0558a" alt="Bilingual">

<img src="docs/shots/demo.gif" width="360" alt="Five themes">

[Get started](#get-started) · [Features](#features) · [Themes](#themes) · [中文](#中文)

</div>

---

## What it is

A single-file Tkinter widget that pins itself to your desktop, below every other
window, and keeps four kinds of plans visible at once:

| | Section | For | Progress |
|---|---|---|---|
| 🟡 | **Daily** | today's habits | check-in, resets each morning |
| 🔵 | **Stage** | goals with a deadline | `12d` / `Today` / `3d late` |
| 🟣 | **Long-term** | ongoing things | percentage |
| 🟢 | **Future** | someday / maybe | plain list |

No account. No sync. No `pip install`. One JSON file next to the script.

## Get started

1. Install **Python 3.8+** for Windows (tkinter is bundled).
2. Grab `plan_card.pyw` **and** the `tools/` folder — keep them side by side.
3. Double-click **`plan_card.pyw`**.

First launch seeds a set of sample plans so the card isn't empty — edit or delete
them. Data lands in `plan_data.json` next to the script.

> Downloading as ZIP is fine too — no build step, no dependencies.

## Features

- **Daily check-in with memory** — one *Check in* button per habit. Each click is
  recorded; open *History* to see `6 check-ins · 3-day streak · 71% in 30d`.
- **Auto self-review** — collapsed to one line, click to expand. Days logged,
  check-ins, daily average, best streak, goal progress. Day / Week / Month.
- **Calendar deadlines** — click the date chip, pick a day. No typing dates.
- **Move plans around** — click `⇄`, or just drag a row onto another section.
- **Collapsible sections** + thin scroll indicator + always-visible input box.
- **Five themes**, each with its own fonts, button shapes and section markers.
- **Opacity 30–100 %** and a **renameable title**.
- **Bilingual UI** — follows your system language, switchable in settings.
- **Crash log, no telemetry** — nothing leaves your machine.

⭐ **If this saves you a few seconds a day, a star helps other people find it.**

## Themes

| Cute | Minimal | Ink |
|:---:|:---:|:---:|
| <img src="docs/shots/theme-cute.png" width="200"> | <img src="docs/shots/theme-minimal.png" width="200"> | <img src="docs/shots/theme-ink.png" width="200"> |
| pastel, rounded pills | greyscale, 1px outlines | rice paper, brush strokes |

| Tech | Chinese | English UI |
|:---:|:---:|:---:|
| <img src="docs/shots/theme-tech.png" width="200"> | <img src="docs/shots/theme-cn.png" width="200"> | <img src="docs/shots/theme-english.png" width="200"> |
| neon, brackets | 楷体, seal buttons | same card, English |

## Docs

| | |
|---|---|
| [Usage](docs/Usage.md) | full English manual |
| [使用说明](docs/使用说明.md) | 中文完整说明书 |
| [Architecture](docs/Architecture.md) | how it's built (Win32 tricks, data model, theme engine) |

## Requirements

- **Windows 10 / 11** — the frameless, rounded, translucent window needs Win32
  APIs, so macOS and Linux are not supported
- **Python 3.8+**, standard library only

## Privacy

Everything is local. There is no network code in this project — `plan_data.json`
never leaves your machine.

## License

MIT — see [LICENSE](LICENSE).

---

<div align="center" id="中文">

## 中文

**一张贴在 Windows 桌面上的计划卡片——像壁纸挂件一样，一直看得见。**

每日打卡 · 阶段目标 · 自动自我总结 · 5 套主题

</div>

| | 段落 | 用途 | 进度 |
|---|---|---|---|
| 🟡 | **每日** | 今天的习惯 | 打卡，每天重置 |
| 🔵 | **阶段** | 有期限的目标 | `剩 12 天` / `今天` / `逾期 3 天` |
| 🟣 | **长期** | 长期要做的事 | 百分比 |
| 🟢 | **未来** | 以后想做的 | 纯清单 |

### 快速开始

1. 装 **Python 3.8+**（Windows 版自带 tkinter）
2. 下载 `plan_card.pyw` **和** `tools/` 文件夹，放在同一目录
3. 双击 **`plan_card.pyw`**

第一次启动会载入一组示例计划，随便改随便删。数据写在同目录的 `plan_data.json`。

### 特性

- **打卡带记忆** — 每条习惯一个「打卡」按钮，点一次记一天；点行尾「详情」看
  `打卡 6 天 · 连续 3 天 · 近 30 天 71%`
- **自动自我总结** — 默认收起一行，点开看有记录天数、打卡次数、日均完成、最长连续
- **日历选期限** — 不用手打日期
- **换分类** — 点 `⇄` 或直接把行拖到别的段
- **段可收起**、细滚动条、输入框永远可见
- **5 套主题** — 可爱 / 极简 / 水墨 / 科技 / 中式，字体、按钮形态、段标识全都不同
- **透明度 30%–100%**、**标题可改名**、**中英双语界面**（跟随系统语言）

⭐ 如果它每天帮你省下几秒钟，给个 star 能让更多人发现它。

完整说明见 [docs/使用说明.md](docs/使用说明.md)，技术实现见 [docs/Architecture.md](docs/Architecture.md)。

### 环境要求

**Windows 10 / 11** + **Python 3.8+**，只用标准库。macOS / Linux 不支持（无边框、
圆角、半透明依赖 Win32 API）。

### 隐私与许可

全部本地运行，没有任何联网代码。MIT 许可，见 [LICENSE](LICENSE)。
