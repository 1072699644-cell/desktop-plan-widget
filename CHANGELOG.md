# Changelog

All notable changes to Plan Card are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [1.0.0] — 2026-11-08

First public release.

### Added

- **Four sections** always visible at once: Daily / Stage / Long-term / Future.
- **Daily check-in** — one button per habit; each click records the day.
- **History per daily plan** — last 14 days plus total check-ins, current streak
  and 30-day rate. Records survive the daily list reset thanks to a stable
  per-plan ID.
- **Auto self-review** — collapsed by default, expands to days logged, check-ins,
  daily average, best streak and goal progress, switchable Day / Week / Month.
- **Calendar deadline picker** for stage plans (`12d` / `Today` / `3d late`).
- **Move plans between sections** — `⇄` menu or drag a row onto another section.
- **Collapsible sections** with remembered state; thin scroll indicator.
- **Five themes** — Cute, Minimal, Ink, Tech, Chinese — each changing palette,
  fonts, button shape (`fill` / `outline` / `ink` / `bracket` / `seal`) and
  section marker (`circle` / `square` / `bar` / `tick` / `diamond`).
- **Opacity slider** (30–100 %) and **renameable card title**.
- **Bilingual UI** — Chinese / English, follows the system language, switchable
  in settings. Sample plans are seeded in the matching language.
- **Settings panel** behind the ⚙ in the header.
- Crash log (`plan_card.log`), no telemetry, no network code.

### Notes

- Data keys in `plan_data.json` are Chinese on purpose: it keeps existing data
  files compatible across language switches.
- Windows-only: the frameless, rounded, translucent window relies on Win32 APIs.
