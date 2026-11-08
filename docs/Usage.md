# Plan Card — User Guide

Everything you can click, in the order you'll need it.
中文版：[使用说明.md](使用说明.md) · 项目首页：[README](../README.md)

---

## 1. First run

Double-click **`plan_card.pyw`**.

- On first launch the card seeds **sample plans** so it isn't empty. Edit or
  delete them — they're just examples.
- Your data is written to **`plan_data.json`**, next to the script.
- If anything breaks, **`plan_card.log`** gets a stack trace.
- Delete `plan_data.json` to start over (the samples come back).

The card is **not a normal window**: no title bar, no taskbar button, and it stays
below your other windows. **Drag the header to move it** — the position is saved.

## 2. What you're looking at

```
┌──────────────────────────────────────────────────────┐
│ Plan Card                        ⚙        ╭───╮      │ ← ⚙ = settings
│ Sun, Nov 8 · 3/7 checked · goals 0/9      │ 0 │      │ ← ring = goal progress
├──────────────────────────────────────────────────────┤
│ Self-review   Auto-generated · click to open       › │ ← click to expand
├──────────────────────────────────────────────────────┤
│ ▪ Daily  ⌄ ─────────────────────────────────── 3/7   │ ← click name to fold
│   [Checked]  Wake at 7:00, read 30 pages      ✕  History │
│   [Check in] Walk 6000 steps                  ✕  History │
│ ▪ Stage  ⌄ ─────────────────────────────────── 0/6   │
│   H  60d  ○ Finish the thesis first draft  ✕   0%    │
│ ▪ Long-term ⌄ ──────────────────────────────── 0/3   │
│ ▪ Future ⌄ ─────────────────────────────────── 0/4   │
├──────────────────────────────────────────────────────┤
│ [Daily ▾]  Add a plan, press Enter               ＋  │ ← always visible
└──────────────────────────────────────────────────────┘
```

The three faint symbols at the right of each row (`⇄` `›` `✕`) **appear when you
hover that row**. Nothing is hidden — they're just quiet until you need them.

## 3. Add a plan

1. Click the **chip on the left of the input box** to choose which section the
   next plan goes into: `Daily → Stage → Long-term → Future`.
2. Type the plan in the box and press **`Enter`** (or click `＋`).

The card grows to fit — it never pushes the input box off-screen.

## 4. Daily check-ins

Daily rows have exactly one control on the left:

| | Meaning |
|---|---|
| **Check in** (dark) | not done today |
| **Checked** (green) | done today |

- Click to check in, click again to undo. **Both are recorded.**
- The row text is **never struck through** — a daily item is a habit, not a
  one-off task.
- Every morning the list **resets** (all checkmarks cleared) but it keeps the same
  plans, so you check in again the next day.

### History

Click **History** at the right end of a daily row:

```
Wake at 7:00, read 30 pages
6 check-ins · 3-day streak · 71% in 30d
──────────────────────────────────
Sat, Nov 7    ✓ Done
Fri, Nov 6    ✓ Done
Thu, Nov 5    · Missed
...
```

| Number | Meaning |
|---|---|
| **check-ins** | total days checked in |
| **streak** | consecutive days ending today (yesterday if today isn't done yet) |
| **% in 30d** | share of the last 30 days that were checked in |

Shows the last 14 days; older days still count towards the totals.
Each daily plan keeps a stable internal ID across days, which is why the history
survives the morning reset.

## 5. Stage goals and deadlines

Stage rows show a chip on the left:

| Chip | Meaning |
|---|---|
| `Date` (grey) | no deadline yet — click to set one |
| `12d` (blue) | 12 days left |
| `Today` (amber) | due today |
| `3d late` (red) | overdue by 3 days |

Click it to open the **calendar**:

- `◀` `▶` change month
- clicking a day applies it immediately
- **Today** sets today; **Clear date** removes it; `Esc` closes

## 6. Long-term and Future

- **Long-term** — ongoing things. Shows a completion percentage, no deadline.
- **Future** — a plain list for "someday". **No percentage at all**, and it does
  not affect the progress ring.

The ring at the top counts **Stage + Long-term only** — the two sections where a
percentage means something. `checked 3/7` next to the date is the daily routine.

## 7. Edit, reorder, move, delete

| Action | How |
|---|---|
| Edit the text | **double-click** the row |
| Delete | `✕` at the right |
| Change priority | click the `H` / `M` / `L` letter at the left |
| Reorder | drag the row up or down |
| Move to another section | `⇄` → pick a section, **or** drag the row onto that section |
| Sub-tasks | `›` at the right, then `+ Add` |
| Complete a sub-task | click its small circle |
| Fold a section | click the section name (state is remembered) |

A single click on the row text checks it — it waits 0.23 s first, so a
double-click opens the editor instead of toggling twice.

## 8. Self-review

The first block is generated from your data; you never write it. Collapsed by
default:

```
Self-review    Auto-generated · click to open        ›
```

Click anywhere on that line to expand:

```
Self-review    Sun, Nov 8 · 3/7 done — 4 to go       ⌄
[Day][Week][Month]
Days logged 1/7     Check-ins 15
Daily avg 43%       Best streak 1 days
Stage goals 0/6     Long-term 0/3
```

| Tab | What it counts |
|---|---|
| **Day** | daily check-in n/m, streak, stage n/m, long-term n/m |
| **Week / Month** | days with records, total check-ins, daily average, best streak, goals |

"Daily avg" is the weighted average of completion across the days in the period,
not the average of day percentages.

## 9. Settings (⚙)

Click the gear at the top right.

| Setting | Notes |
|---|---|
| **Name** | the card title, up to 20 characters — press `Enter` to apply |
| **Theme** | five styles, applied instantly |
| **Language** | `Auto` / `中文` / `English` — Auto follows your system language |
| **Opacity** | 30 %–100 %, applied live, saved when you release the slider |

The settings panel itself stays fully opaque, so you can still read it at 30 %.

### The five themes

| Theme | Palette | Buttons | Section markers |
|---|---|---|---|
| **Cute** | pale pink, pastel sections | rounded filled pill | circle |
| **Minimal** | near-white, greyscale | 1 px square outline | small square |
| **Ink** | rice paper, 楷体 | text + a brush stroke | vertical bar |
| **Tech** | deep navy, neon | double brackets `│x│` | diagonal tick |
| **Chinese** | dark lacquer, 国色 | seal-style outlined box | diamond |

Changing a theme rebuilds the whole card: palette, fonts, button shapes, markers
and checkbox stroke widths all change together — it's not a colour swap.

## 10. Start it with Windows (optional)

Plan Card does **not** install itself into autostart.

1. `Win + R` → type `shell:startup` → `Enter`
2. Put a shortcut to `plan_card.pyw` in that folder

> Use `pythonw.exe` in the shortcut if you don't want a console window:
> `"C:\Program Files\Python39\pythonw.exe" "D:\path\to\plan_card.pyw"`

## 11. Your data

| File | What it is |
|---|---|
| `plan_data.json` | all plans, check-in records, settings — **the only thing worth backing up** |
| `plan_card.log` | crash log, only written when something goes wrong |

Everything is local. There is no network code in this project.

To move the card to another PC: copy `plan_card.pyw`, `tools/` and
`plan_data.json` together.

## 12. Troubleshooting

| Symptom | Fix |
|---|---|
| Nothing happens on double-click | Open `plan_card.log`; also check you have Python 3.8+ (`python --version`) |
| The card is invisible | After a monitor change it may be off-screen: set `"位置": [100, 100]` in `plan_data.json` |
| Sample plans won't go away | Delete `plan_data.json`, then create your own |
| Text shows as boxes | Install a Chinese font, or switch the language to English |
| Wrong language | Settings → Language → `中文` / `English` |
| It disappears after a reboot | It doesn't autostart by design — see section 10 |
| Everything is too big/small | Windows display scaling affects the card; it's designed for 100 % at 1080p |
