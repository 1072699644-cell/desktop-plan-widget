# -*- coding: utf-8 -*-
"""极简中英双语词表。

设计：**用中文原文当 key**。中文模式原样返回，所以界面代码只需要把文案包一层
`L("打卡")`，不用另起一套 key 体系，也不会漏翻。

数据文件里的键（每日 / 阶段 / 条目 …）保持中文不变，
这样老数据不用迁移；界面显示时才翻译。
"""
import datetime
import os

LANGS = ("auto", "zh", "en")
LANG_NAMES = {"auto": "跟随系统 / Auto", "zh": "中文", "en": "English"}

_lang = "zh"          # 实际生效的语言：zh / en
_pref = "auto"        # 用户的选择：auto / zh / en

# ---------------- 词表 ----------------
EN = {
    # —— 窗口与设置 ——
    "工作计划": "Plan Card",
    "计划表设置": "Settings",
    "名称（回车生效）": "Name (Enter to apply)",
    "名称回车生效": "Enter to apply name",
    "主题": "Theme",
    "透明度": "Opacity",
    "语言": "Language",
    "完成": "Done",
    "取消": "Cancel",
    "保存": "Save",

    # —— 分段 ——
    "每日": "Daily",
    "阶段": "Stage",
    "长期": "Long-term",
    "未来": "Future",
    "暂无": "Empty",
    "还没有计划": "No plans yet",

    # —— 顶部元信息 ——
    "· 未安排打卡": " · no check-ins",
    "· 已打卡 %d/%d": " · checked %d/%d",
    "· 打卡 %d/%d": " · %d/%d checked",
    "· 目标 %d/%d": " · goals %d/%d",
    "· 目标达成": " · all goals done",

    # —— 行 ——
    "打卡": "Check in",
    "已打卡": "Checked",
    "详情": "History",
    "期限": "Date",
    "设期限": "Set date",
    "今天": "Today",
    "逾期%d": "%dd late",
    "%d天": "%dd",
    "移到 %s": "Move to %s",
    "（当前）": " (current)",
    "已移到「%s」": "Moved to %s",
    "新计划将归入「%s」": "New plans go to %s",
    "编辑内容": "Edit",
    "回车保存 · Esc 取消": "Enter to save · Esc to cancel",
    "添加一条计划，回车确认": "Add a plan, press Enter",

    # —— 自我总结 ——
    "自我总结": "Self-review",
    "自动生成 · 点开查看": "Auto-generated · click to open",
    "日": "Day",
    "周": "Week",
    "月": "Month",

    # —— 打卡时间详情 ——
    "打卡 %d 天 · 连续 %d 天 · 近30天 %d%%":
        "%d check-ins · %d-day streak · %d%% in 30d",
    "还没有记录\n勾选一次打卡就会记下来":
        "No records yet\ncheck in once and it's recorded",
    "✓ 打卡": "✓ Done",
    "· 未打卡": "· Missed",
    "共记录 %d 天，这里显示最近 %d 天":
        "%d days recorded, showing last %d",

    # —— 日历 ——
    "%d年%d月": "%s %d",
    "清除期限": "Clear date",

    # —— 自动总结（tools/plan.py） ——
    "全部打卡完成": "All check-ins done",
    "，连续 %d 天": ", %d-day streak",
    "今天一条都还没打卡，共 %d 条待打":
        "Nothing checked in yet — %d to go",
    "打卡完成 %d/%d，还差 %d 条": "%d/%d done — %d to go",
    "这一天没有安排每日打卡": "No daily check-ins that day",
    "每日打卡": "Check-ins",
    "连续打卡": "Streak",
    "阶段目标": "Stage goals",
    "长期目标": "Long-term",
    "有记录天数": "Days logged",
    "打卡次数": "Check-ins",
    "日均完成": "Daily avg",
    "最长连续": "Best streak",
    "未安排": "None",
    "%d 天": "%d days",
    "%d 次": "%d",
    "本周": "This week",
    "上周": "Last week",
    "本月": "This month",
    "上月": "Last month",
    "本周 %d 天有记录，打卡 %d 次，日均完成 %d%%":
        "This week: %d days logged, %d check-ins, %d%% daily avg",
    "本月 %d 天有记录，打卡 %d 次，日均完成 %d%%":
        "This month: %d days logged, %d check-ins, %d%% daily avg",
    "本周还没有任何打卡记录": "No check-ins this week",
    "本月还没有任何打卡记录": "No check-ins this month",
    "（%s）": "(%s)",

    # —— 优先级单字（列宽只有一个字） ——
    "高": "H",
    "中": "M",
    "低": "L",

    # —— 主题名（只在设置面板显示，数据里仍存中文） ——
    "可爱": "Cute",
    "极简": "Minimal",
    "水墨": "Ink",
    "科技": "Tech",
    "中式": "Chinese",
}

# 英文月份与星期
MON_EN = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
WD_EN = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
WD_CN = "一二三四五六日"


# ---------------- 语言切换 ----------------
def detect():
    """跟随系统语言：中文环境给中文，其它一律英文。"""
    try:
        import locale
        loc = (locale.getdefaultlocale()[0] or "").lower()
    except Exception:
        loc = ""
    if not loc:
        loc = (os.environ.get("LANG") or "").lower()
    return "zh" if ("zh" in loc or "chinese" in loc) else "en"


def set_lang(pref):
    """pref: auto / zh / en，返回实际生效的语言。"""
    global _lang, _pref
    _pref = pref if pref in LANGS else "auto"
    _lang = detect() if _pref == "auto" else _pref
    return _lang


def lang():
    return _lang


def pref():
    return _pref


def is_cn():
    return _lang == "zh"


def lang_label(code):
    """语言选项的显示名（自动项按当前界面语言取名）。"""
    if code == "auto":
        return "跟随系统" if is_cn() else "Auto"
    return {"zh": "中文", "en": "English"}.get(code, code)


def L(s):
    """取文案：中文原样返回，英文查表（查不到就回退中文，保证不会崩）。"""
    if _lang == "zh":
        return s
    return EN.get(s, s)


# ---------------- 本地化格式 ----------------
def weekday(d):
    """周一=0。中文「周一」，英文「Mon」。"""
    return (("周" + WD_CN[d.weekday()]) if is_cn() else WD_EN[d.weekday()])


def date_label(d):
    """11月8日 周日 / Sun, Nov 8"""
    if is_cn():
        return "%d月%d日 %s" % (d.month, d.day, weekday(d))
    return "%s, %s %d" % (WD_EN[d.weekday()], MON_EN[d.month - 1], d.day)


def month_label(y, m):
    """2026年11月 / Nov 2026"""
    return "%d年%d月" % (y, m) if is_cn() else "%s %d" % (MON_EN[m - 1], y)


def week_head():
    """日历表头：一 二 三 四 五 六 日 / M T W T F S S"""
    return list(WD_CN) if is_cn() else ["M", "T", "W", "T", "F", "S", "S"]


def day_label(iso_date):
    """日历里的日期标签：11月8日 周六 / Sat, Nov 8"""
    try:
        d = datetime.datetime.strptime(iso_date, "%Y-%m-%d").date()
    except Exception:
        return iso_date
    return date_label(d)
