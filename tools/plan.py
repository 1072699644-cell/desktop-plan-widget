# -*- coding: utf-8 -*-
"""工作计划日志：按天存储，支持子计划、重要性、完成度，未完成自动顺延。"""
import calendar
import datetime
import json
import os
import sys
import uuid

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import i18n as I18N          # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PATH = os.path.join(ROOT, "plan_data.json")            # 数据就近存放
DEMO = os.path.join(ROOT, "sample", "plan_data.json")      # 首次运行的示例（中文）
DEMO_EN = os.path.join(ROOT, "sample", "plan_data.en.json")  # 英文示例

EMPTY = {"位置": [56, 300], "天": {}}

PRIORITIES = ["高", "中", "低"]
PRI_COLOR = {"高": "#e0564a", "中": "#e3bd82", "低": "#6b7684"}


def _norm_item(it):
    """补齐字段：文字 / 完成 / 重要 / 细节。"""
    out = {
        "文字": (it.get("文字") or "").strip(),
        "完成": bool(it.get("完成")),
        "重要": it.get("重要") if it.get("重要") in PRIORITY_SET else "中",
        "细节": [],
    }
    for s in (it.get("细节") or []):
        t = (s.get("文字") or "").strip()
        if t:
            out["细节"].append({"文字": t, "完成": bool(s.get("完成"))})
    for k in ("开始日期", "结束日期"):
        v = (it.get(k) or "").strip()
        if v:
            out[k] = v
    if it.get("id"):
        out["id"] = str(it["id"])
    return out


# ---------------- 每日打卡：ID + 记录 ----------------
def _new_id():
    return uuid.uuid4().hex[:8]


def ensure_id(it):
    """每日计划跨天要保持同一个 ID，打卡记录才挂得住。"""
    if not it.get("id"):
        it["id"] = _new_id()
    return it["id"]


def record_day(data, it, day=None):
    """记录这条每日计划当天「做了 / 没做」，返回该条的记录表。"""
    iid = ensure_id(it)
    recs = data.setdefault("打卡记录", {})
    rec = recs.setdefault(iid, {})
    rec[(day or datetime.date.today()).isoformat()] = bool(is_done(it))
    return rec


def history_of(data, iid):
    return dict(((data.get("打卡记录") or {}).get(iid)) or {})


def history_stats(rec, days=30):
    """返回 (打卡天数, 记录天数, 最近30天打卡率)。"""
    if not rec:
        return 0, 0, 0
    done = sum(1 for v in rec.values() if v)
    total = len(rec)
    cutoff = (datetime.date.today() -
              datetime.timedelta(days=days - 1)).isoformat()
    recent = [v for k, v in rec.items() if k >= cutoff]
    rate = int(round(100.0 * sum(1 for v in recent if v) / len(recent))) if recent else 0
    return done, total, rate


def streak(rec):
    """从今天往前数，连续打卡了几天（今天没打就从昨天开始算）。"""
    if not rec:
        return 0
    d = datetime.date.today()
    if not rec.get(d.isoformat()):
        d -= datetime.timedelta(days=1)
    n = 0
    while rec.get(d.isoformat()):
        n += 1
        d -= datetime.timedelta(days=1)
    return n


PRIORITY_SET = set(PRIORITIES)


def _seed_demo():
    """把示例数据搬成「今天」的版本：日期全部相对今天重排，过期也不会变成逾期。"""
    src_path = DEMO
    if not I18N.is_cn() and os.path.exists(DEMO_EN):
        src_path = DEMO_EN          # 英文环境用英文示例
    if not os.path.exists(src_path):
        return None
    try:
        with open(src_path, encoding="utf-8") as f:
            d = json.load(f)
    except Exception:
        return None
    today = datetime.date.today()
    src = None
    for _k, v in (d.get("天") or {}).items():
        src = v
        break
    d["天"] = {today.isoformat(): (src or {"条目": []})}

    offs = [60, 30, 90, 21, 45, 120]     # 阶段期限排成未来 21~120 天
    for i, it in enumerate((d.get("阶段计划") or {}).get("条目") or []):
        if i < len(offs):
            it["结束日期"] = (today +
                            datetime.timedelta(days=offs[i])).isoformat()

    recs = d.get("打卡记录") or {}
    keys = sorted({k for r in recs.values() for k in r})
    if keys:
        last = datetime.datetime.strptime(keys[-1], "%Y-%m-%d").date()
        shift = (today - last).days
        new = {}
        for iid, r in recs.items():
            nr = {}
            for k, v in r.items():
                dt = datetime.datetime.strptime(k, "%Y-%m-%d").date()
                nr[(dt + datetime.timedelta(days=shift)).isoformat()] = v
            new[iid] = nr
        d["打卡记录"] = new
    d["位置"] = [56, 300]
    return d


def load():
    if not os.path.exists(PATH):
        demo = _seed_demo()        # 第一次运行：载入示例计划，开箱即有内容
        if demo is not None:
            try:
                with open(PATH, "w", encoding="utf-8") as dst:
                    json.dump(demo, dst, ensure_ascii=False, indent=1)
            except Exception:
                pass
    try:
        with open(PATH, encoding="utf-8") as f:
            d = json.load(f)
    except Exception:
        d = json.loads(json.dumps(EMPTY))
    d.setdefault("位置", [56, 300])
    d.setdefault("天", {})
    d.setdefault("打卡记录", {})
    d.setdefault("总结", {})
    for s in SUMS:
        d["总结"].setdefault(s, {})
    for k, day in d["天"].items():
        day["条目"] = [_norm_item(x) for x in day.get("条目", [])
                       if (x.get("文字") or "").strip()]
        for it in day["条目"]:
            ensure_id(it)
    for keyname in ("阶段计划", "长期计划", "未来计划"):
        d.setdefault(keyname, {"条目": []})
        d[keyname]["条目"] = [_norm_item(x) for x in d[keyname].get("条目", [])
                            if (x.get("文字") or "").strip()]
    d.setdefault("模式", "每日")
    return d


def save(d):
    try:
        with open(PATH, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=1)
    except Exception:
        pass


def key(day=None):
    return (day or datetime.date.today()).isoformat()


MODES = ["每日", "阶段", "长期", "未来"]


def get_day(d, day=None, create=True):
    k = key(day)
    if k not in d["天"]:
        if not create:
            return None
        d["天"][k] = {"条目": []}
    return d["天"][k]


def get_list(d, mode, create=True):
    """取某一类的条目列表：每日 / 阶段 / 长期 / 未来。"""
    if mode == "每日":
        if not create and key() not in d["天"]:
            return []
        return get_day(d, create=create)["条目"]
    keyname = {"阶段": "阶段计划", "长期": "长期计划",
               "未来": "未来计划"}.get(mode, "长期计划")
    if keyname not in d:
        if not create:
            return []
        d[keyname] = {"条目": []}
    d[keyname].setdefault("条目", [])
    return d[keyname]["条目"]


# ---------------- 自我总结：日 / 周 / 月 ----------------
SUMS = ["日", "周", "月"]
WEEKDAY_CN = "一二三四五六日"


def _month_shift(y, m, off):
    m2 = m - 1 + off
    return y + m2 // 12, m2 % 12 + 1


def period_key(scope, offset=0, today=None):
    """返回 (存储键, 显示文字)。offset 0=本期，-1=上一期。"""
    t = today or datetime.date.today()
    if scope == "周":
        mon = t - datetime.timedelta(days=t.weekday()) + \
            datetime.timedelta(weeks=offset)
        y, w, _ = mon.isocalendar()
        sun = mon + datetime.timedelta(days=6)
        if I18N.is_cn():
            label = "%d月%d日–%d月%d日" % (mon.month, mon.day,
                                          sun.month, sun.day)
        else:
            label = "%s %d – %s %d" % (I18N.MON_EN[mon.month - 1], mon.day,
                                       I18N.MON_EN[sun.month - 1], sun.day)
        return ("%04d-W%02d" % (y, w), label)
    if scope == "月":
        y, m = _month_shift(t.year, t.month, offset)
        return ("%04d-%02d" % (y, m), I18N.month_label(y, m))
    d = t + datetime.timedelta(days=offset)
    return (d.isoformat(), I18N.date_label(d))


def _day_stats(d, day):
    """某一天的每日清单：(完成数, 总数)。"""
    rec = (d.get("天") or {}).get(day.isoformat())
    if not rec:
        return 0, 0
    items = rec.get("条目") or []
    return sum(1 for it in items if is_done(it)), len(items)


def _streak_upto(d, day):
    """从某天往前数，连续「当天清单全部打完」的天数。"""
    n = 0
    t = day
    for _ in range(400):
        dn, tt = _day_stats(d, t)
        if tt and dn == tt:
            n += 1
            t -= datetime.timedelta(days=1)
        else:
            break
    return n


def _range_days(today, scope, offset):
    if scope == "周":
        start = (today - datetime.timedelta(days=today.weekday()) +
                 datetime.timedelta(weeks=offset))
        return [start + datetime.timedelta(days=i) for i in range(7)]
    if scope == "月":
        y, m = _month_shift(today.year, today.month, offset)
        n = calendar.monthrange(y, m)[1]
        return [datetime.date(y, m, i) for i in range(1, n + 1)]
    return [today + datetime.timedelta(days=offset)]


def auto_summary(d, scope, offset=0):
    """自动生成的自我总结：{"head": 一句话, "rows": [(标签, 值), ...]}"""
    L = I18N.L
    today = datetime.date.today()
    g1 = (d.get("阶段计划") or {}).get("条目") or []
    g2 = (d.get("长期计划") or {}).get("条目") or []
    gd1 = sum(1 for it in g1 if is_done(it))
    gd2 = sum(1 for it in g2 if is_done(it))
    rows = [(L("阶段目标"), "%d/%d" % (gd1, len(g1))),
            (L("长期目标"), "%d/%d" % (gd2, len(g2)))]

    if scope == "日":
        t = today + datetime.timedelta(days=offset)
        dn, tt = _day_stats(d, t)
        stk = _streak_upto(d, t)
        rows.insert(0, (L("连续打卡"), L("%d 天") % stk))
        rows.insert(0, (L("每日打卡"),
                        ("%d/%d" % (dn, tt)) if tt else L("未安排")))
        if not tt:
            head = L("这一天没有安排每日打卡")
        elif dn == tt:
            head = L("全部打卡完成") + ((L("，连续 %d 天") % stk)
                                      if stk > 1 else "")
        elif dn == 0:
            head = L("今天一条都还没打卡，共 %d 条待打") % tt
        else:
            head = L("打卡完成 %d/%d，还差 %d 条") % (dn, tt, tt - dn)
        if offset != 0:
            head = "%s · %s" % (period_key("日", offset)[1], head)
        return {"head": head, "rows": rows}

    days = _range_days(today, scope, offset)
    have = [(x, _day_stats(d, x)) for x in days]
    have = [(x, v) for x, v in have if v[1]]
    dn_sum = sum(v[0] for _, v in have)
    tt_sum = sum(v[1] for _, v in have)
    avg = int(round(100.0 * dn_sum / tt_sum)) if tt_sum else 0

    lo, hi = days[0].isoformat(), days[-1].isoformat()
    hits = 0
    for rec in (d.get("打卡记录") or {}).values():
        for k, v in rec.items():
            if v and lo <= k <= hi:
                hits += 1

    best = run = 0
    for x in days:
        a, b = _day_stats(d, x)
        if b and a == b:
            run += 1
            best = max(best, run)
        else:
            run = 0

    if scope == "周":
        label = L("本周") if offset == 0 else L("上周")
    else:
        label = L("本月") if offset == 0 else L("上月")
    rows.insert(0, (L("最长连续"), L("%d 天") % best))
    rows.insert(0, (L("日均完成"), "%d%%" % avg))
    rows.insert(0, (L("打卡次数"), L("%d 次") % hits))
    rows.insert(0, (L("有记录天数"), "%d/%d" % (len(have), len(days))))
    if have:
        head = L("%s %d 天有记录，打卡 %d 次，日均完成 %d%%") % (
            label, len(have), hits, avg)
    else:
        head = L("%s还没有任何打卡记录") % label
    return {"head": head, "rows": rows}


def days_left(it):
    """阶段计划：距离结束还有几天（None 表示没设期限或已过）。"""
    """阶段计划：距离结束还有几天（None 表示没设期限或已过）。"""
    end = (it.get("结束日期") or "").strip()
    if not end:
        return None
    try:
        e = datetime.datetime.strptime(end, "%Y-%m-%d").date()
    except Exception:
        return None
    return (e - datetime.date.today()).days


def carry_over(d, now=None):
    """今天还没有条目时，把昨天的清单整体搬过来。

    每日是**打卡制**：不管昨天打没打完，第二天整张清单重新出现、勾选全部清零，
    所以「每天早上读书」这种习惯不会因为昨天打完了就消失。
    （要彻底不要某一条，点该条的 ✕ 删掉。）
    """
    today = (now or datetime.date.today())
    k = key(today)
    if k in d["天"] and d["天"][k].get("条目"):
        return 0
    prev = (today - datetime.timedelta(days=1)).isoformat()
    old = d["天"].get(prev)
    if not old:
        return 0
    items = []
    for it in old.get("条目", []):
        cp = {"文字": it["文字"], "完成": False,
              "重要": it.get("重要", "中"),
              "id": it.get("id") or _new_id(),
              "细节": [{"文字": s["文字"], "完成": False}
                       for s in it.get("细节", [])]}
        for f in ("开始日期", "结束日期"):
            if it.get(f):
                cp[f] = it[f]
        items.append(cp)
    if not items:
        return 0
    get_day(d, today)["条目"] = items
    save(d)
    return len(items)


# ---------------- 完成度 ----------------
def item_percent(it):
    """单条完成度：有细节按细节算，没细节按自身勾选算。"""
    subs = it.get("细节") or []
    if subs:
        return int(round(100.0 * sum(1 for s in subs if s.get("完成")) / len(subs)))
    return 100 if it.get("完成") else 0


def is_done(it):
    """有细节时，细节全完成也算这条完成。"""
    if it.get("完成"):
        return True
    subs = it.get("细节") or []
    return bool(subs) and all(s.get("完成") for s in subs)


def stats(items):
    total = len(items)
    done = sum(1 for it in items if is_done(it))
    pct = int(round(100.0 * done / total)) if total else 0
    return done, total, pct


def overall_percent(items):
    """总进度：按每条的完成度平均。"""
    if not items:
        return 0
    return int(round(sum(item_percent(it) for it in items) / len(items)))
