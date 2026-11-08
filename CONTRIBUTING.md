# Contributing

Thanks for taking a look! This is a small, dependency-free Windows widget, so
contributions stay small too.

## Ways to help

| | |
|---|---|
| 🐞 **Report a bug** | use the bug template — the log and your Windows/Python version matter |
| ✨ **Suggest a feature** | use the feature template; explain the problem, not just the solution |
| 🎨 **Add a theme** | one dict entry in `plan_card.pyw` plus a screenshot — easiest first PR |
| 🌍 **Improve a translation** | `tools/i18n.py` is a plain Chinese → English dictionary |
| 📝 **Fix the docs** | typos and better explanations are always welcome |

## Running from source

```
python plan_card.pyw
```

- **No dependencies.** Standard library only — please keep it that way.
- Data is created next to the script as `plan_data.json` (git-ignored).
- Delete that file to get the sample plans back.

## Code layout

| File | Responsibility |
|---|---|
| `plan_card.pyw` | window, layout, interaction, themes, wiring |
| `tools/plan.py` | data layer: read/write, four sections, check-in records, auto summary |
| `tools/i18n.py` | zh→en dictionary, language detection, localised dates |

Two rules that keep the project small:

1. **No third-party packages.** A user must be able to run it with a stock
   Python install.
2. **Data keys stay Chinese** (`每日` / `条目` / `完成` …). That is intentional:
   it keeps existing data files compatible. Only the *interface* is translated,
   through `i18n.L()`.

## Adding a theme

In `plan_card.pyw`:

```python
THEMES["MyTheme"] = dict(
    bg="#101418", fg="#eef1f5", sub="#8b93a0", dim="#5a6370",
    acc="#e7c18a", ok="#6fd39a", on_acc="#14251b",
    danger="#d9705f", card_hi="#101418",
    pri=["#d9705f", "#c9a97a", "#67707d"],
    fam="PingFang SC",            # title / section font
    btn=("fill", 8),              # fill | outline | ink | bracket | seal
    dot="circle",                 # circle | square | bar | tick | diamond
    chk=1.6,                      # checkbox stroke width
    sec=["#d8b478", "#7ba6c9", "#a68cc9", "#8ec3a6"],
)
THEME_ORDER.append("MyTheme")
```

Also add the display name to `EN` in `tools/i18n.py`. Secondary colours are
derived automatically from `bg` (light backgrounds darken, dark backgrounds
lighten), so you only need the palette above.

Then add a screenshot to `docs/shots/` and mention it in the README.

## Adding a language

1. Copy the `EN` dict in `tools/i18n.py`, translate the values.
2. Register it in `LANGS`, `LANG_NAMES`, and the `L()` lookup.
3. Add a line to `docs/` if you want a full manual.

## Pull requests

- Keep the diff focused; one topic per PR.
- Test on Windows before opening it: check a daily check-in, the history popup,
  one theme switch and one language switch.
- Screenshots for anything visual — the card is a UI, after all.

By contributing you agree your work is released under the MIT license.
