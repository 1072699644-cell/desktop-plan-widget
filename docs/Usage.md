# Usage · Plan Card

A complete manual for the Plan Card desktop widget.
中文版见 [使用说明.md](使用说明.md)。

---

## 1. First run

Double-click `plan_card.pyw`. On first launch the card seeds a set of **sample
plans** (in English if your system language is not Chinese) so you can see
everything working right away.

- Data file: `plan_data.json`, created next to the script.
- Crash log: `plan_card.log` — only written if something actually goes wrong.
- Delete `plan_data.json` to start over (the samples come back).

The card is **not** a normal window: no title bar, no taskbar entry, and it stays
below your other windows like a wallpaper widget. Drag the header to move it —
the position is remembered.

---

## 2. The four sections

| Section | Purpose | Percent shown |
|---|---|---|
| **Daily** | today's habits — resets every morning | no (check-in based) |
| **Stage** | goals with a deadline | yes |
| **Long-term** | ongoing things | yes |
| **Future** | someday list | no |

Sections are always visible at once. Click a section name (or the `⌄` next to it)
to **fold** it; the folded state is remembered.

---

## 3. Daily check-ins

Every daily row has exactly one button on the left:

- **Check in** (dark) — not done today
- **Checked** (green) — done today

Click to check in; click again to undo (the record is updated too).
The row text is never struck through — daily items are habits, not tasks.

**History**: click `History` at the right end of a daily row.

```
Wake at 7:00, read 30 pages
6 check-ins · 3-day streak · 71% in 30d
──────────────────────────────
Sat, Nov 7    ✓ Done
Fri, Nov 6    ✓ Done
Thu, Nov 5    · Missed
...
```

- **check-ins** — total days checked in
- **streak** — consecutive days ending today (or yesterday if today isn't done)
- **% in 30d** — share of the last 30 days that were checked in

Every daily plan keeps a stable internal ID across days, so the history stays
attached even though the list itself resets each morning.

---

## 4. Deadlines (stage plans)

Each stage row shows a chip on the left:

| Chip | Meaning |
|---|---|
| `Date` (grey) | no deadline yet — click to set one |
| `12d` (blue) | 12 days left |
| `Today` (amber) | due today |
| `3d late` (red) | overdue by 3 days |

Click it to open a **month calendar**: `◀ ▶` to change month, click a day to
apply, or use **Today** / **Clear date**. `Esc` cancels.

---

## 5. Editing

| Action | How |
|---|---|
| Edit text | **double-click** the row text |
| Delete a plan | click `✕` at the right (visible on hover) |
| Change priority | click the `H` / `M` / `L` letter at the left |
| Reorder | drag a row up or down |
| Move to another section | click `⇄` → pick a section, or drag onto that section |
| Add a sub-task | click `›` at the right, then `+ Add`
| Complete a sub-task | click its small circle |

Single click on a row text = check / uncheck (it waits 0.23 s so that a
double-click can open the editor instead of toggling twice).

---

## 6. Self-review (automatic)

The first block is **Self-review**. It is collapsed by default:

```
Self-review    Auto-generated · click to open        ›
```

Click anywhere on that line to expand:

```
Self-review    Sun, Nov 8 · 3/7 done — 4 to go        ⌄
[Day][Week][Month]
Days logged 1/7     Check-ins 15
Daily avg 43%       Best streak 1 days
Stage goals 0/6     Long-term 0/3
```

You never write it — the numbers come straight from your data.
`Day` / `Week` / `Month` switch the period.

---

## 7. Settings (⚙)

Click the gear at the top right:

| Setting | Notes |
|---|---|
| **Name** | the card title; press `Enter` to apply |
| **Theme** | 5 styles, applied instantly — see below |
| **Language** | Auto / 中文 / English. Auto follows your system language |
| **Opacity** | 30 %–100 %, saved on release |

All four are stored in `plan_data.json`.

### Themes

| Theme | Look | Buttons | Section marker |
|---|---|---|---|
| **Cute** | pale pink, pastel sections | rounded filled pills | circle |
| **Minimal** | near-white, greyscale | 1 px square outline | small square |
| **Ink** | rice paper, `楷体` | text + a short ink stroke | vertical bar |
| **Tech** | deep navy, neon | double brackets `│x│` | diagonal tick |
| **Chinese** | dark lacquer, 国色 | seal-style outlined box | diamond |

Changing the theme rebuilds the whole card: colours, fonts, button shapes,
markers and checkbox stroke widths all change together.

---

## 8. Start with Windows (optional)

The tool does not install itself. To launch it at login:

1. Press `Win + R`, type `shell:startup`, press `Enter`.
2. Put a shortcut to `plan_card.pyw` in that folder.

> The shortcut must point at `pythonw.exe` (not `python.exe`) if you don't want
> a console window:
> `"C:\Program Files\Python39\pythonw.exe" "D:\path\to\plan_card.pyw"`

---

## 9. Troubleshooting

| Symptom | Fix |
|---|---|
| Nothing appears on double-click | Check `plan_card.log` next to the script |
| Card is invisible | It may be off-screen after a monitor change — edit `"位置": [x, y]` in `plan_data.json` to `[100, 100]` |
| Sample plans won't go away | Delete `plan_data.json` and create the plans you want |
| Text looks like boxes | Install a Chinese font, or switch the language to English in settings |
| Wrong language | Settings → Language → 中文 / English |
