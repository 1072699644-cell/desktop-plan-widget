# -*- coding: utf-8 -*-
"""桌面工作计划日志 —— iOS 风格玻璃卡片
PingFang SC 字体 / 圆角半透明 / 进度环 / iOS 圆形勾选框 / 悬停高亮
子计划 / 优先级 / 每条完成度 + 总完成度
"""
import calendar
import ctypes
import datetime
import json
import os
import sys
import tkinter as tk
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))
import plan as PL
import i18n as I18N

LOG = os.path.join(HERE, "plan_card.log")


def _single_instance():
    """同一时间只允许一个卡片进程，避免守护重复拉起。"""
    try:
        k = ctypes.windll.kernel32
        k.CreateMutexW.argtypes = [ctypes.c_void_p, ctypes.c_bool,
                                   ctypes.c_wchar_p]
        k.CreateMutexW.restype = ctypes.c_void_p
        h = k.CreateMutexW(None, False, "DshWorkPlanCardSingleInstance")
        if ctypes.GetLastError() == 183:      # ERROR_ALREADY_EXISTS
            return None
        return h
    except Exception:
        return True


def _log_exc(exc, val, tb):
    """把异常写进日志：pythonw 没有控制台，不记下来就永远查不到怎么死的。"""
    try:
        with open(LOG, "a", encoding="utf-8") as f:
            f.write("\n=== %s ===\n" %
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            f.write("".join(traceback.format_exception(exc, val, tb)))
    except Exception:
        pass


W = 396
RADIUS = 20
MAX_H = 640

BG = "#191d24"
ROW = "#191d24"
ROW_HOVER = "#232833"
SUB_BG = "#151920"
LINE = "#2c323d"
HI = "#3a4250"
FG = "#f5f7fa"
SUB = "#9ba3af"
DIM = "#6b7380"
ACC = "#e7c18a"
TRACK = "#2b313c"
OK = "#6fd39a"

FONT = "PingFang SC"
F_TITLE = (FONT, 13, "bold")
F_BODY = (FONT, 11)
F_SMALL = (FONT, 9)
F_TINY = (FONT, 8)
F_STRIKE = (FONT, 11, "overstrike")
F_SUB = (FONT, 10)
F_SUB_STRIKE = (FONT, 10, "overstrike")

PRI_STYLE = {
    "高": ("#3b2024", "#ff8f80"),
    "中": ("#3a3222", "#e7c18a"),
    "低": ("#232a34", "#9ba3af"),
}

# 三段：统一表面色，只用一条左侧色条 + 同色标题区分（低饱和，不破坏整体配色）
SEC_BG = "#1b2028"
SEC_HOVER = "#202632"
SEC_BORDER = "#2a313c"
HAIR = "#242b35"
SECTION_STYLE = {
    "每日": (BG, SEC_HOVER, "#d8b478"),
    "阶段": (BG, SEC_HOVER, "#7ba6c9"),
    "长期": (BG, SEC_HOVER, "#a68cc9"),
    "未来": (BG, SEC_HOVER, "#8ec3a6"),
}

INP = "#20262f"        # 输入框 / 内嵌面板底色
CHIPBG = "#29303b"     # 小胶囊底色
FAINT = "#333b47"      # 行尾操作默认（几乎不可见）
HOTFG = "#c9d2de"      # 行尾操作悬停
DANGER = "#d9705f"     # 删除 / 逾期 / 高优先级
ONACC = "#ffffff"      # 强调色上的文字颜色
CARD_HI = "#191d24"    # 卡片主表面
PRI_COLORS = {"高": "#d9705f", "中": "#c9a97a", "低": "#67707d"}
FAM_TITLE = "PingFang SC"   # 标题/段名字体
FAM_NUM = "PingFang SC"     # 数字字体
BTN_MODE = "fill"           # 按钮形态：fill/outline/ink/bracket/seal
BTN_R = 6                   # 按钮圆角
DOT_SHAPE = "circle"        # 段标识形状
CHK_W = 1.6                 # 勾选框描边宽度


# ---------------- 主题 ----------------
def _rgb(h):
    h = h.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def _mix(c1, c2, t):
    a, b = _rgb(c1), _rgb(c2)
    return "#%02x%02x%02x" % tuple(
        int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))


def _light(h, t):
    return _mix(h, "#ffffff", t)


def _dark(h, t):
    return _mix(h, "#000000", t)


THEME_ORDER = ["可爱", "极简", "水墨", "科技", "中式"]
THEMES = {
    # 糖果粉 + 马卡龙四色，圆润轻快
    "可爱": dict(bg="#fdf3f7", fg="#4a3a42", sub="#8d7683", dim="#b3a0aa",
               acc="#e0558a", ok="#3fb98a", on_acc="#ffffff",
               danger="#e0557a", card_hi="#ffffff",
               pri=["#e0557a", "#c98f2e", "#b1aaad"],
               fam="PingFang SC", btn=("fill", 10), dot="circle", chk=2.2,
               sec=["#e0558a", "#6f5cd9", "#1f9fb5", "#d98a1f"]),
    # 近乎纯白 + 全灰阶，只留黑白两色
    "极简": dict(bg="#fafafa", fg="#111111", sub="#6b6b6b", dim="#9a9a9a",
               acc="#111111", ok="#1f8f63", on_acc="#ffffff",
               danger="#c0392b", card_hi="#ffffff",
               pri=["#111111", "#6b6b6b", "#b3b3b3"],
               fam="PingFang SC", btn=("outline", 0), dot="square", chk=1.2,
               sec=["#111111", "#4d4d4d", "#808080", "#a8a8a8"]),
    # 宣纸底 + 墨色 + 朱砂，四段用墨/青墨/赭/苔
    "水墨": dict(bg="#f2eee3", fg="#24211c", sub="#6d6559", dim="#9c9284",
               acc="#8c2f24", ok="#4b7b5a", on_acc="#ffffff",
               danger="#8c2f24", card_hi="#fbf8f1",
               pri=["#8c2f24", "#4b6b52", "#9c9284"],
               fam="楷体", btn=("ink", 0), dot="bar", chk=1.6,
               sec=["#3a352e", "#4f6360", "#7a5c44", "#5f7052"]),
    # 深空黑 + 霓虹青紫粉绿
    "科技": dict(bg="#080d18", fg="#d7e6ff", sub="#7d93b8", dim="#4f6285",
               acc="#00e5ff", ok="#29e58a", on_acc="#04212b",
               danger="#ff4d6d", card_hi="#0f1626",
               pri=["#ff4d6d", "#ffc94d", "#5c6b8a"],
               fam="PingFang SC", btn=("bracket", 0), dot="tick", chk=1.5,
               num="Consolas",
               sec=["#00e5ff", "#7c5cff", "#29e58a", "#ff4d94"]),
    # 乌木漆底 + 中国红 / 青花蓝 / 鎏金 / 青瓷绿
    "中式": dict(bg="#17110f", fg="#f3e9dd", sub="#b9a795", dim="#86776a",
               acc="#d94f3d", ok="#c8a45c", on_acc="#ffffff",
               danger="#d94f3d", card_hi="#221a16",
               pri=["#d94f3d", "#c8a45c", "#86776a"],
               fam="楷体", btn=("seal", 2), dot="diamond", chk=1.8,
               sec=["#d94f3d", "#3f6f9e", "#c8a45c", "#6f9e6f"]),
}


def _is_light(h):
    r, g, b = _rgb(h)
    return (0.299 * r + 0.587 * g + 0.114 * b) > 128


def _shift(bg, t):
    """朝对比方向偏移：深底更亮，浅底更暗。"""
    return _dark(bg, t) if _is_light(bg) else _light(bg, t)


def apply_theme(name):
    """把主题色灌进全局变量；之后新建的控件自动用新颜色。"""
    global BG, ROW, ROW_HOVER, SUB_BG, LINE, HI, FG, SUB, DIM, ACC, TRACK, OK
    global SEC_BG, SEC_HOVER, SEC_BORDER, HAIR, SECTION_STYLE
    global INP, CHIPBG, FAINT, HOTFG, PRI_COLORS, DANGER, ONACC, CARD_HI
    global FAM_TITLE, FAM_NUM, BTN_MODE, BTN_R, DOT_SHAPE, CHK_W
    d = THEMES.get(name) or THEMES[THEME_ORDER[0]]
    bg = d["bg"]
    light = _is_light(bg)
    BG = ROW = bg
    CARD_HI = d.get("card_hi", bg)
    FG, SUB, DIM = d["fg"], d["sub"], d["dim"]
    ACC, OK = d["acc"], d["ok"]
    ONACC = d.get("on_acc", "#ffffff")
    DANGER = d.get("danger", "#d9534f")
    HI = _shift(bg, 0.16)
    LINE = _shift(bg, 0.12)
    ROW_HOVER = _shift(bg, 0.05 if light else 0.07)
    SUB_BG = _dark(bg, 0.05) if light else _dark(bg, 0.28)
    TRACK = _shift(bg, 0.09)
    SEC_BG = _shift(bg, 0.02)
    SEC_HOVER = _shift(bg, 0.05)
    SEC_BORDER = _shift(bg, 0.11)
    HAIR = _shift(bg, 0.07)
    INP = _shift(bg, 0.05)
    CHIPBG = _shift(bg, 0.10)
    FAINT = _shift(bg, 0.11)
    HOTFG = _mix(d["fg"], bg, 0.18)
    FAM_TITLE = d.get("fam", FONT)
    FAM_NUM = d.get("num", FAM_TITLE)
    BTN_MODE, BTN_R = d.get("btn", ("fill", 6))
    DOT_SHAPE = d.get("dot", "circle")
    CHK_W = d.get("chk", 1.6)
    pr = d.get("pri") or [DANGER, ACC, _shift(bg, 0.30)]
    PRI_COLORS = {"高": pr[0], "中": pr[1], "低": pr[2]}
    s = d["sec"]
    SECTION_STYLE = {"每日": (BG, SEC_HOVER, s[0]),
                     "阶段": (BG, SEC_HOVER, s[1]),
                     "长期": (BG, SEC_HOVER, s[2]),
                     "未来": (BG, SEC_HOVER, s[3])}


def _rr(cv, x0, y0, x1, y1, r, **kw):
    """圆角矩形（r<=0 就是直角）"""
    if r <= 0:
        return cv.create_rectangle(x0, y0, x1, y1, **kw)
    pts = [x0 + r, y0, x1 - r, y0, x1, y0, x1, y0 + r,
           x1, y1 - r, x1, y1, x1 - r, y1, x0 + r, y1,
           x0, y1, x0, y1 - r, x0, y0 + r, x0, y0]
    return cv.create_polygon(pts, smooth=True, **kw)


def _round_region(win, w, h, r=RADIUS):
    try:
        hwnd = ctypes.windll.user32.GetParent(win.winfo_id()) or win.winfo_id()
        rgn = ctypes.windll.gdi32.CreateRoundRectRgn(0, 0, w + 1, h + 1, r, r)
        ctypes.windll.user32.SetWindowRgn(hwnd, rgn, True)
    except Exception:
        pass


class Card(object):
    def __init__(self, root):
        self.root = root
        # 先定语言：首次运行播种示例数据时要按语言挑中文版 / 英文版
        _tmp_pref = "auto"
        try:
            with open(PL.PATH, encoding="utf-8") as _f:
                _tmp_pref = json.load(_f).get("语言", "auto")
        except Exception:
            _tmp_pref = "auto"
        if _tmp_pref not in I18N.LANGS:
            _tmp_pref = "auto"
        I18N.set_lang(_tmp_pref)
        self.data = PL.load()
        PL.carry_over(self.data)
        self.add_target = self.data.get("新计划归入", "每日")
        if self.add_target not in PL.MODES:
            self.add_target = "每日"
        self.sum_scope = self.data.get("总结页", "日")
        if self.sum_scope not in PL.SUMS:
            self.sum_scope = "日"
        self.sum_open = False        # 自我总结默认收起，点开才看
        self.folded = set(x for x in (self.data.get("折叠") or [])
                          if x in PL.MODES)
        self._pending_toggle = None  # 单击延迟勾选（让双击编辑能插进来）
        self._dbl_guard = False

        # 语言（默认跟随系统）
        self.lang_pref = self.data.get("语言", "auto")
        if self.lang_pref not in I18N.LANGS:
            self.lang_pref = "auto"
        I18N.set_lang(self.lang_pref)   # 数据里可能修正过，再设一次
        # 外观设置
        self.theme = self.data.get("主题", THEME_ORDER[0])
        if self.theme not in THEMES:
            self.theme = THEME_ORDER[0]
        apply_theme(self.theme)
        _nm = (self.data.get("名称") or "").strip()
        self.name_custom = bool(_nm)      # 用户改过名字才用自定义标题
        self.card_name = _nm
        try:
            self.alpha = min(1.0, max(0.30, float(self.data.get("透明度", 0.90))))
        except Exception:
            self.alpha = 0.90
        self._ranges = []
        self.items = []
        self._refresh_view()
        self.expanded = set()
        _exp = os.environ.get("DSH_PLAN_EXPAND", "").strip()
        for x in (_exp.split(",") if _exp else []):
            try:
                self.expanded.add(int(x))
            except Exception:
                pass
        self.adding_sub = None
        self._drag = None

        root.overrideredirect(True)
        root.configure(bg=BG)
        try:
            root.attributes("-alpha", 0.0)
        except Exception:
            pass
        pos = self.data.get("位置", [56, 320])
        if not isinstance(pos, (list, tuple)) or len(pos) < 2:
            pos = [56, 320]
        root.geometry("+%d+%d" % (int(pos[0]), int(pos[1])))
        self._build()
        self.refresh()
        self._fade_in()

    # ---------------- 视图：三类平铺，全部可见 ----------------
    def _refresh_view(self):
        """把三类条目拼成一个视图列表（里都是同一批 dict，改它就是改数据）。
        同时记下每类的 [起, 止) 区间；行号用全局下标，操作时回推所属分类。
        """
        self._ranges = []
        view = []
        p = 0
        for m in PL.MODES:
            lst = PL.get_list(self.data, m, create=True)
            self._ranges.append((m, p, p + len(lst)))
            view.extend(lst)
            p += len(lst)
        self.items = view
        return view

    def _locate(self, i):
        """全局行号 → (分类, 该分类内的下标)。"""
        for m, a, b in getattr(self, "_ranges", []):
            if a <= i < b:
                return m, i - a
        return None, None

    def _fade_in(self, cur=0.0, target=None):
        target = self.alpha if target is None else target
        try:
            cur = min(target, cur + 0.07)
            self.root.attributes("-alpha", cur)
            if cur < target:
                self.root.after(16, lambda: self._fade_in(cur, target))
        except Exception:
            pass

    # ---------------- 结构 ----------------
    def _build(self):
        for w in self.root.winfo_children():
            try:
                w.destroy()
            except Exception:
                pass
        tk.Frame(self.root, bg=HI, height=1).pack(fill="x")
        self.outer = tk.Frame(self.root, bg=CARD_HI)
        self.outer.pack(fill="both", expand=True)

        bar = tk.Frame(self.outer, bg=BG, height=60)
        bar.pack(fill="x")
        bar.pack_propagate(False)
        left = tk.Frame(bar, bg=BG)
        left.pack(side="left", padx=(16, 0), pady=(11, 0))
        self.lb_title = tk.Label(left, text=self.title_text(), fg=FG, bg=BG,
                                 font=(FAM_TITLE, 14, "bold"))
        self.lb_title.pack(anchor="w")
        meta = tk.Frame(left, bg=BG)
        meta.pack(anchor="w", pady=(2, 0))
        self.lb_date = tk.Label(meta, text="", fg=DIM, bg=BG, font=F_TINY)
        self.lb_date.pack(side="left")
        self.lb_check = tk.Label(meta, text="", fg=SUB, bg=BG, font=F_TINY)
        self.lb_check.pack(side="left", padx=(7, 0))
        self.lb_pct = tk.Label(meta, text="", fg=SUB, bg=BG, font=F_TINY)
        self.lb_pct.pack(side="left", padx=(7, 0))

        right = tk.Frame(bar, bg=BG)
        right.pack(side="right", padx=(0, 16), pady=(4, 0))
        self.ring = tk.Canvas(right, width=44, height=44, bg=BG,
                              highlightthickness=0, bd=0)
        self.ring.pack(side="right")
        self.gear = tk.Label(right, text="⚙", fg=DIM, bg=BG,
                             font=(FONT, 13), cursor="hand2", padx=7)
        self.gear.pack(side="left", pady=(6, 0))
        self.gear.bind("<Button-1>", lambda e: self.open_settings())
        self.gear.bind("<Enter>", lambda e: self.gear.config(fg=ACC))
        self.gear.bind("<Leave>", lambda e: self.gear.config(fg=DIM))

        for w in (bar, left, self.lb_title, self.lb_date, self.lb_check,
                  self.lb_pct):
            w.configure(cursor="fleur")
            w.bind("<ButtonPress-1>", self._drag_start)
            w.bind("<B1-Motion>", self._drag_move)
            w.bind("<ButtonRelease-1>", self._drag_end)
        tk.Frame(self.outer, bg=HAIR, height=1).pack(fill="x")

        # 底部输入区先打包，否则会被 expand 的滚动区挤成 0 高度
        self.bottom = tk.Frame(self.outer, bg=BG)
        self.bottom.pack(side="bottom", fill="x", padx=14, pady=(6, 14))
        pill = tk.Frame(self.bottom, bg=INP)
        pill.pack(side="left", fill="x", expand=True)
        # 新计划归到哪一类：点一下循环切换 每日 → 阶段 → 长期 → 未来
        self.addmode = tk.Label(pill, text=I18N.L(self.add_target) + " ▾", fg=ACC,
                                bg=CHIPBG, font=F_TINY, padx=7, pady=3,
                                cursor="hand2")
        self.addmode.pack(side="left", padx=(8, 0))
        self.addmode.bind("<Button-1>", lambda e: self.cycle_target())
        self.entry = tk.Entry(pill, bg=INP, fg=FG, bd=0, font=F_BODY,
                              insertbackground=ACC)
        self.entry.pack(side="left", fill="x", expand=True, padx=(8, 6), pady=7)
        self.entry.bind("<Return>", lambda e: self.add())
        self._ph = I18N.L("添加一条计划，回车确认")
        self.entry.insert(0, self._ph)
        self.entry.config(fg=DIM)

        def _in(_=None):
            if self.entry.get() == self._ph:
                self.entry.delete(0, "end")
                self.entry.config(fg=FG)

        def _out(_=None):
            if not self.entry.get().strip():
                self.entry.delete(0, "end")
                self.entry.insert(0, self._ph)
                self.entry.config(fg=DIM)

        self.entry.bind("<FocusIn>", _in)
        self.entry.bind("<FocusOut>", _out)
        self.plus = tk.Label(pill, text="＋", fg=ACC, bg="#22262e",
                             font=(FONT, 13), width=2, cursor="hand2")
        self.plus.pack(side="right", padx=(0, 8))
        self.plus.bind("<Button-1>", lambda e: self.add())

        self.scroll = tk.Canvas(self.outer, bg=BG, highlightthickness=0, bd=0)
        self.scroll.pack(fill="both", expand=True)
        self.inner = tk.Frame(self.scroll, bg=BG)
        self._win = self.scroll.create_window((0, 0), window=self.inner, anchor="nw")
        self.inner.bind("<Configure>", self._on_inner)
        self.scroll.bind("<Configure>", self._on_scroll_configure)
        for seq in ("<MouseWheel>", "<Button-4>", "<Button-5>"):
            try:
                self.root.unbind_all(seq)
            except Exception:
                pass
            self.scroll.bind_all(seq, self._on_wheel)

        # 细滚动条：只在内容超出一屏时才出现，平时不占地方
        self.sbar = tk.Frame(self.outer, bg=SEC_BORDER, width=3)
        self.scroll.configure(yscrollcommand=self._on_yscroll)

    def _on_yscroll(self, first, last):
        try:
            f, l = float(first), float(last)
            h = self.scroll.winfo_height()
        except Exception:
            return
        if l - f >= 0.999 or h <= 1:
            try:
                self.sbar.place_forget()
            except Exception:
                pass
            return
        try:
            self.sbar.place(in_=self.scroll, relx=1.0, x=-3,
                            y=int(f * h), width=3,
                            height=max(20, int((l - f) * h)))
        except Exception:
            pass

    # ---------------- 拖动 / 尺寸 ----------------
    def _drag_start(self, e):
        self._drag = (e.x_root, e.y_root, self.root.winfo_x(), self.root.winfo_y())

    def _drag_move(self, e):
        if not self._drag:
            return
        dx = e.x_root - self._drag[0]
        dy = e.y_root - self._drag[1]
        if abs(dx) < 3 and abs(dy) < 3:
            return
        self.root.geometry("+%d+%d" % (self._drag[2] + dx, self._drag[3] + dy))

    def _drag_end(self, e):
        if self._drag:
            self.data["位置"] = [self.root.winfo_x(), self.root.winfo_y()]
            PL.save(self.data)
            self._drag = None

    def _on_inner(self, e=None):
        self.scroll.configure(scrollregion=self.scroll.bbox("all"))
        self.scroll.itemconfigure(self._win, width=self.scroll.winfo_width())
        self._fit()

    def _on_scroll_configure(self, e=None):
        self.scroll.itemconfigure(self._win, width=self.scroll.winfo_width())
        # 尺寸变化只更新滚动区，不再递归触发 _fit（否则会和 setWindow 互相触发）
        self.scroll.configure(scrollregion=self.scroll.bbox("all"))

    def _fit(self):
        """迭代收敛：宽度定下来后文字才换行，高度得再算几次才准。
        用 _fitting 防止 geometry 变化回调再进来递归。
        """
        if getattr(self, "_fitting", False):
            return
        self._fitting = True
        try:
            pos = self.data.get("位置", [56, 320])
            if not isinstance(pos, (list, tuple)) or len(pos) < 2:
                pos = [56, 320]
            px, py = int(pos[0]), int(pos[1])
            try:
                scr_h = self.root.winfo_screenheight()
            except Exception:
                scr_h = 1080
            taskbar = 56
            h = None
            for _ in range(4):
                self.root.update_idletasks()
                bh = self.bottom.winfo_reqheight()
                need = 61 + self.inner.winfo_reqheight() + bh + 22
                # 兜底：至少留出「表头 + 输入框 + 一行」的高度，输入框不可能被挤掉
                floor = 61 + bh + 22 + 34
                # 全部显示优先：能长多高就长多高，一直长到屏幕底部（留任务栏）
                avail = max(220, scr_h - taskbar - py)
                h2 = max(150, floor, min(avail, need))
                # 屏幕底部放不下就整体上移，保证输入框永远在屏幕里
                if py + h2 > scr_h - taskbar:
                    py = max(0, scr_h - taskbar - h2)
                    if py + h2 > scr_h - taskbar:      # 屏幕实在太矮
                        h2 = max(150, scr_h - taskbar - py)
                self.root.geometry("%dx%d+%d+%d" % (W, h2, px, py))
                if h is not None and abs(h2 - h) <= 1:
                    break
                h = h2
            self.root.update_idletasks()
            _round_region(self.root, W, h or 200, RADIUS)
            if [px, py] != list(pos):
                self.data["位置"] = [px, py]
        finally:
            self._fitting = False

    def _on_wheel(self, e):
        # 只有鼠标在卡片上时才滚动，避免抢别的窗口的滚轮
        try:
            x, y = self.root.winfo_pointerxy()
            rx, ry = self.root.winfo_rootx(), self.root.winfo_rooty()
            if not (rx <= x <= rx + self.root.winfo_width() and
                    ry <= y <= ry + self.root.winfo_height()):
                return
        except Exception:
            pass
        if not self.scroll.winfo_ismapped():
            return
        if getattr(e, "num", None) == 4:
            d = -1
        elif getattr(e, "num", None) == 5:
            d = 1
        else:
            d = -1 if e.delta > 0 else 1
        self.scroll.yview_scroll(d, "units")

    # ---------------- 进度环 ----------------
    def _draw_ring(self, pct):
        c = self.ring
        c.delete("all")
        pad = 4
        r = (46 - 2 * pad) / 2.0
        cx = cy = 23
        c.create_oval(cx - r, cy - r, cx + r, cy + r, outline=TRACK, width=4)
        if pct > 0:
            col = OK if pct >= 100 else ACC
            c.create_arc(cx - r, cy - r, cx + r, cy + r, start=90,
                         extent=-359.9 * pct / 100.0, style="arc",
                         outline=col, width=4)
        c.create_text(cx, cy, text=("%d" % pct),
                      fill=(OK if pct >= 100 else ACC),
                      font=(FAM_NUM, 10, "bold"))

    def cycle_target(self):
        """切换新计划归入的分类：每日 → 阶段 → 长期 → 每日。"""
        i = PL.MODES.index(self.add_target) if self.add_target in PL.MODES else 0
        self.add_target = PL.MODES[(i + 1) % len(PL.MODES)]
        self.data["新计划归入"] = self.add_target
        try:
            self.addmode.config(text=I18N.L(self.add_target) + " ▾")
        except Exception:
            pass
        self._save()
        self._toast(I18N.L("新计划将归入「%s」") % I18N.L(self.add_target))

    def set_due(self, i):
        """阶段计划：点开日历选结束日期（不需要手打）。"""
        if not (0 <= i < len(self.items)):
            return
        cur = self.items[i].get("结束日期", "")
        base = datetime.date.today()
        if cur:
            try:
                base = datetime.datetime.strptime(cur, "%Y-%m-%d").date()
            except Exception:
                pass
        self._calendar(i, base.year, base.month, cur)

    def _set_due(self, i, iso, win=None):
        if win is not None:
            try:
                win.destroy()
            except Exception:
                pass
        if not (0 <= i < len(self.items)):
            return
        if iso:
            self.items[i]["结束日期"] = iso
        else:
            self.items[i].pop("结束日期", None)
        self._save()
        self.refresh()

    def _calendar(self, i, year, month, cur):
        """一个月历弹层：点日期直接生效，◀▶ 翻月，今天/清除/取消。"""
        win = tk.Toplevel(self.root)
        win.overrideredirect(True)
        win.configure(bg="#22272f")
        win.attributes("-topmost", True)

        head = tk.Frame(win, bg="#22272f")
        head.pack(fill="x", padx=10, pady=(9, 5))

        def nav(dd):
            y, m = year, month + dd
            if m < 1:
                y, m = y - 1, 12
            elif m > 12:
                y, m = y + 1, 1
            win.destroy()
            self._calendar(i, y, m, cur)

        for sym, dd, side in (("◀", -1, "left"), ("▶", 1, "right")):
            b = tk.Label(head, text=sym, fg=SUB, bg=CHIPBG, font=F_TINY,
                         padx=8, pady=2, cursor="hand2")
            b.pack(side=side)
            b.bind("<Button-1>", lambda e, x=dd: nav(x))
        tk.Label(head, text=I18N.month_label(year, month), fg=FG, bg="#22272f",
                 font=(FONT, 10, "bold")).pack(side="left", expand=True)

        grid = tk.Frame(win, bg="#22272f")
        grid.pack(padx=10, pady=(0, 4))
        for c, nm in enumerate(I18N.week_head()):
            tk.Label(grid, text=nm, fg="#5d6675", bg="#22272f",
                     font=F_TINY, width=3).grid(row=0, column=c, pady=(0, 3))

        today = datetime.date.today()
        first = datetime.date(year, month, 1)
        ndays = calendar.monthrange(year, month)[1]
        r, c = 1, first.weekday()          # 周一 = 0
        for dnum in range(1, ndays + 1):
            day = datetime.date(year, month, dnum)
            iso = day.isoformat()
            sel = (iso == cur)
            ist = (day == today)
            if sel:
                bgc, fgc = ACC, ONACC
            elif ist:
                bgc, fgc = "#2f3a49", ACC
            else:
                bgc, fgc = "#22272f", FG
            lb = tk.Label(grid, text=str(dnum), fg=fgc, bg=bgc, font=F_TINY,
                          width=3, pady=3, cursor="hand2")
            lb.grid(row=r, column=c, padx=1, pady=1)
            lb.bind("<Button-1>", lambda e, x=iso: self._set_due(i, x, win))
            c += 1
            if c > 6:
                c = 0
                r += 1

        tk.Frame(win, bg=CHIPBG, height=1).pack(fill="x", padx=10, pady=(2, 6))
        bar = tk.Frame(win, bg="#22272f")
        bar.pack(fill="x", padx=10, pady=(0, 10))
        for txt_, fn in ((I18N.L("今天"),
                          lambda: self._set_due(i, today.isoformat(), win)),
                         (I18N.L("清除期限"),
                          lambda: self._set_due(i, "", win))):
            b = tk.Label(bar, text=txt_, fg=SUB, bg=CHIPBG, font=F_TINY,
                         padx=9, pady=3, cursor="hand2")
            b.pack(side="left", padx=(0, 6))
            b.bind("<Button-1>", lambda e, f=fn: f())
        b = tk.Label(bar, text=I18N.L("取消"), fg="#6d7784", bg="#22272f",
                     font=F_TINY,
                     padx=6, pady=3, cursor="hand2")
        b.pack(side="right")
        b.bind("<Button-1>", lambda e: win.destroy())

        win.update_idletasks()
        try:
            x = self.root.winfo_pointerx() - 12
            y = self.root.winfo_pointery() + 10
            x = min(max(8, x), self.root.winfo_screenwidth() - win.winfo_width() - 8)
            if y + win.winfo_height() > self.root.winfo_screenheight() - 40:
                y = self.root.winfo_pointery() - win.winfo_height() - 10
        except Exception:
            x, y = 400, 300
        win.geometry("+%d+%d" % (x, max(8, y)))
        win.bind("<Escape>", lambda e: win.destroy())
        self._calwin = win

    def _sync_tabs(self):
        pass


    def _section(self, m, lst, base):
        """段标题：彩色小方点 + 段名 + 折叠箭头 + 细线 + 段色计数"""
        pbg, phov, acc = SECTION_STYLE.get(m, (BG, SEC_HOVER, ACC))
        head = tk.Frame(self.inner, bg=BG)
        head.pack(fill="x", padx=16, pady=(11, 1))
        folded = m in self.folded
        dot = self._dot_widget(head, acc, BG)
        dot.pack(side="left", pady=(0, 3))
        lb = tk.Label(head, text=I18N.L(m), fg=acc, bg=BG,
                      font=(FAM_TITLE, 12, "bold"), cursor="hand2")
        lb.pack(side="left", padx=(7, 0))
        arr = tk.Label(head, text=("›" if folded else "⌄"), fg=DIM,
                       bg=BG, font=(FONT, 10), cursor="hand2")
        arr.pack(side="left", padx=(7, 0))
        done, total, _ = PL.stats(lst)
        cnt = tk.Label(head,
                       text=(I18N.L("暂无") if not total
                             else "%d/%d" % (done, total)),
                       fg=(DIM if not total else acc), bg=BG, font=F_TINY,
                       cursor="hand2")
        cnt.pack(side="right")
        tk.Frame(head, bg=HAIR, height=1).pack(side="left", fill="x",
                                               expand=True, padx=(9, 9),
                                               pady=(9, 0))
        self._sec_heads[m] = (head, lb, BG, acc)
        for w in (head, dot, lb, arr, cnt):
            w.bind("<Button-1>", lambda e, x=m: self._toggle_fold(x))
        return BG, phov, acc

    def _toggle_fold(self, m):
        if m in self.folded:
            self.folded.discard(m)
        else:
            self.folded.add(m)
        self.data["折叠"] = sorted(self.folded)
        self._save()
        self.refresh()

    # ---------------- 设置：名称 / 主题 / 透明度 ----------------
    def _rebuild(self):
        self._build()
        self.refresh()

    def _set_theme(self, name):
        if name not in THEMES:
            return
        self.theme = name
        self.data["主题"] = name
        self._save()
        apply_theme(name)
        try:
            self.root.configure(bg=CARD_HI)
        except Exception:
            pass
        self._rebuild()
        try:
            self.root.attributes("-alpha", self.alpha)
        except Exception:
            pass
        self.open_settings()

    def _set_lang(self, code):
        """切换界面语言：auto / zh / en"""
        if code not in I18N.LANGS:
            return
        self.lang_pref = code
        self.data["语言"] = code
        I18N.set_lang(code)
        self._save()
        self._rebuild()
        try:
            self.root.attributes("-alpha", self.alpha)
        except Exception:
            pass
        self.open_settings()

    def title_text(self):
        """默认标题跟随语言，改过名字就一直用自定义的。"""
        return self.card_name if self.name_custom else I18N.L("工作计划")

    def _save_name(self, v):
        v = (v or "").strip()[:20]
        self.card_name = v
        self.name_custom = bool(v)
        self.data["名称"] = v
        self._save()
        try:
            self.lb_title.config(text=self.title_text())
        except Exception:
            pass
        self._fit()

    def _draw_alpha(self, wd=None):
        cv = getattr(self, "_alpha_cv", None)
        if cv is None:
            return
        if wd is None:
            wd = cv.winfo_width() or 252
        cv.delete("all")
        pad = 9
        wd = max(80, wd)
        w = wd - 2 * pad
        y = 11
        cv.create_line(pad, y, pad + w, y, fill=TRACK, width=3,
                       capstyle="round")
        k = (self.alpha - 0.30) / 0.70
        x = pad + w * max(0.0, min(1.0, k))
        cv.create_line(pad, y, x, y, fill=ACC, width=3, capstyle="round")
        cv.create_oval(x - 6, y - 6, x + 6, y + 6, fill=FG, outline=BG, width=1)

    def open_settings(self):
        win = tk.Toplevel(self.root)
        win.overrideredirect(True)
        win.configure(bg=SEC_BG)
        win.attributes("-topmost", True)
        try:
            win.attributes("-alpha", 1.0)     # 设置面板自己不受卡片透明度影响
        except Exception:
            pass
        self._setwin = win

        box = tk.Frame(win, bg=SEC_BG)
        box.pack(padx=16, pady=14)

        tk.Label(box, text=I18N.L("计划表设置"), fg=FG, bg=SEC_BG,
                 font=(FONT, 11, "bold")).pack(anchor="w")
        tk.Frame(box, bg=HAIR, height=1).pack(fill="x", pady=(8, 0))

        tk.Label(box, text=I18N.L("名称（回车生效）"), fg=DIM, bg=SEC_BG,
                 font=F_TINY).pack(anchor="w", pady=(10, 3))
        name_var = tk.StringVar(value=self.title_text())
        ent = tk.Entry(box, textvariable=name_var, bg=INP, fg=FG, bd=0,
                       font=F_BODY, insertbackground=ACC, width=26)
        ent.pack(fill="x", ipady=5)
        ent.bind("<Return>", lambda e: self._save_name(name_var.get()))

        tk.Label(box, text=I18N.L("主题"), fg=DIM, bg=SEC_BG,
                 font=F_TINY).pack(anchor="w", pady=(12, 4))
        sw = tk.Frame(box, bg=SEC_BG)
        sw.pack(fill="x")
        for tname in THEME_ORDER:
            d = THEMES[tname]
            on = (tname == self.theme)
            cell = tk.Frame(sw, bg=SEC_BG)
            cell.pack(side="left", padx=(0, 9))
            chip = tk.Frame(cell, bg=d["bg"], width=44, height=30,
                            highlightthickness=2,
                            highlightbackground=(ACC if on else SEC_BORDER))
            chip.pack()
            chip.pack_propagate(False)
            tk.Frame(chip, bg=d["acc"], height=5).pack(side="bottom", fill="x")
            lab = tk.Label(cell, text=I18N.L(tname), bg=SEC_BG, font=F_TINY,
                           fg=(ACC if on else DIM))
            lab.pack(pady=(3, 0))
            for w in (cell, chip, lab):
                w.bind("<Button-1>", lambda e, n=tname: self._set_theme(n))

        tk.Label(box, text=I18N.L("语言"), fg=DIM, bg=SEC_BG,
                 font=F_TINY).pack(anchor="w", pady=(12, 4))
        lseg = tk.Frame(box, bg=SEC_BG)
        lseg.pack(fill="x")
        for code in I18N.LANGS:
            on = (code == self.lang_pref)
            b = tk.Label(lseg, text=I18N.lang_label(code), bg=SEC_BG,
                         font=F_TINY, cursor="hand2", padx=9, pady=2,
                         fg=(ONACC if on else DIM),
                         highlightthickness=1,
                         highlightbackground=SEC_BORDER)
            if on:
                b.configure(bg=ACC)
            b.pack(side="left", padx=(0, 6))
            b.bind("<Button-1>", lambda e, c=code: self._set_lang(c))

        row = tk.Frame(box, bg=SEC_BG)
        row.pack(fill="x", pady=(14, 0))
        tk.Label(row, text=I18N.L("透明度"), fg=DIM, bg=SEC_BG,
                 font=F_TINY).pack(side="left")
        self._alpha_lb = tk.Label(row, text="%d%%" % round(self.alpha * 100),
                                  fg=ACC, bg=SEC_BG, font=F_TINY)
        self._alpha_lb.pack(side="right")

        cv = tk.Canvas(box, width=252, height=22, bg=SEC_BG,
                       highlightthickness=0, bd=0, cursor="hand2")
        cv.pack(fill="x", pady=(3, 0))
        self._alpha_cv = cv
        self._draw_alpha(252)

        def drag(e):
            self.alpha = max(0.30, min(1.0, (e.x - 9) / 234.0))
            try:
                self.root.attributes("-alpha", self.alpha)
            except Exception:
                pass
            self._draw_alpha(cv.winfo_width())
            self._alpha_lb.config(text="%d%%" % round(self.alpha * 100))

        def drop(e):
            drag(e)
            self.data["透明度"] = round(self.alpha, 2)
            self._save()

        cv.bind("<Button-1>", drag)
        cv.bind("<B1-Motion>", drag)
        cv.bind("<ButtonRelease-1>", drop)

        bar = tk.Frame(box, bg=SEC_BG)
        bar.pack(fill="x", pady=(12, 0))

        def close(_=None):
            self._save_name(name_var.get())
            self.data["透明度"] = round(self.alpha, 2)
            self._save()
            win.destroy()

        done_btn = self._btn_widget(bar, I18N.L("完成"), False, SEC_BG, close,
                                    w=76, h=28)
        done_btn.pack(side="right")
        tk.Label(bar, text=I18N.L("名称回车生效"), fg=DIM, bg=SEC_BG,
                 font=F_TINY).pack(side="left")

        win.bind("<Escape>", close)
        win.update_idletasks()
        x = self.root.winfo_rootx() + self.root.winfo_width() - win.winfo_width()
        y = self.root.winfo_rooty() + 46
        win.geometry("+%d+%d" % (max(8, x), max(8, y)))

    def _sec_at(self, x_root, y_root):
        for m, t in getattr(self, "_sec_heads", {}).items():
            head = t[0]
            try:
                if not head.winfo_ismapped():
                    continue
                x0, y0 = head.winfo_rootx(), head.winfo_rooty()
                x1, y1 = x0 + head.winfo_width(), y0 + head.winfo_height()
            except Exception:
                continue
            if x0 - 6 <= x_root <= x1 + 6 and y0 - 4 <= y_root <= y1 + 4:
                return m
        return None

    def _paint_sec(self, name):
        for m, t in getattr(self, "_sec_heads", {}).items():
            lb, acc = t[1], t[3]
            try:
                lb.config(fg=("#ffffff" if m == name else acc))
            except Exception:
                pass

    # ---------------- 刷新 ----------------
    def refresh(self):
        for w in self.inner.winfo_children():
            w.destroy()
        self._row_frames = []
        self._row_widgets = {}
        self._sec_heads = {}
        d = datetime.date.today()
        self.lb_date.config(text=I18N.date_label(d))

        self._refresh_view()
        # 顶部总进度 = 阶段 + 长期（有百分比的分类）；
        # 每日是打卡制、未来计划是纯清单，都不进这个数
        goal = []
        daily = []
        for m, a, b in self._ranges:
            if m == "每日":
                daily.extend(self.items[a:b])
            elif m in ("阶段", "长期"):
                goal.extend(self.items[a:b])
        g_done, g_total, _ = PL.stats(goal)
        self._draw_ring(PL.overall_percent(goal))
        d_done, d_total, _ = PL.stats(daily)
        # 顶部元信息：日期 · 打卡 · 目标，一行读完（不再用胶囊/多块）
        if not d_total:
            self.lb_check.config(text=I18N.L("· 未安排打卡"), fg=DIM)
        elif d_done == d_total:
            self.lb_check.config(text=I18N.L("· 已打卡 %d/%d") % (d_done, d_total),
                                 fg=OK)
        else:
            self.lb_check.config(text=I18N.L("· 打卡 %d/%d") % (d_done, d_total),
                                 fg=PRI_COLORS["中"])
        if not g_total:
            self.lb_pct.config(text="")
        elif g_done == g_total:
            self.lb_pct.config(text=I18N.L("· 目标达成"), fg=OK)
        else:
            self.lb_pct.config(text=I18N.L("· 目标 %d/%d") % (g_done, g_total),
                               fg=SUB)
        try:
            self.addmode.config(text=I18N.L(self.add_target) + " ▾")
        except Exception:
            pass

        # 最顶部：自我总结（日 / 周 / 月）
        self._summary_panel()

        for m, a, b in self._ranges:
            lst = self.items[a:b]
            pbg, phov, acc = self._section(m, lst, a)
            if m in self.folded:
                continue
            if not lst:
                tk.Label(self.inner, text=I18N.L("还没有计划"), fg=DIM, bg=BG,
                         font=F_TINY).pack(anchor="w", padx=24, pady=(1, 2))
                continue
            for k, it in enumerate(lst):
                self._row(a + k, it, self.inner, pbg, phov, acc)

        self._fit()
        # 布局稳定后再拟合一次，避免刚加完条目时高度算少了、把输入框挤掉
        self.root.after(60, self._fit)

    # ---------------- 自我总结（自动生成，日 / 周 / 月） ----------------
    def _set_sum_scope(self, scope):
        if scope not in PL.SUMS:
            return
        self.sum_scope = scope
        self.data["总结页"] = scope
        self._save()
        self.refresh()

    def _toggle_sum(self, open_=None):
        self.sum_open = (not self.sum_open) if open_ is None else bool(open_)
        self.refresh()

    def _summary_panel(self):
        info = PL.auto_summary(self.data, self.sum_scope)
        _k, label = PL.period_key(self.sum_scope)

        box = tk.Frame(self.inner, bg=BG)
        box.pack(fill="x", padx=16, pady=(8, 0))

        head = tk.Frame(box, bg=BG)
        head.pack(fill="x", pady=(2, 4))
        lb_top = tk.Label(head, text=I18N.L("自我总结"), fg=SUB, bg=BG,
                          font=(FONT, 10, "bold"), cursor="hand2")
        lb_top.pack(side="left")
        if self.sum_open:
            sub = "%s · %s" % (label, info["head"])
            sub_fg = SUB
        else:
            sub = I18N.L("自动生成 · 点开查看")
            sub_fg = DIM
        lb_sub = tk.Label(head, text=sub, fg=sub_fg, bg=BG, font=F_TINY,
                          cursor="hand2", anchor="w", justify="left",
                          wraplength=W - 150)
        lb_sub.pack(side="left", padx=(9, 0))
        arr = tk.Label(head, text=("⌄" if self.sum_open else "›"), fg=DIM,
                       bg=BG, font=(FONT, 11), width=2, cursor="hand2")
        arr.pack(side="right")

        for w in (box, head, lb_top, lb_sub, arr):
            w.bind("<Button-1>", lambda e: self._toggle_sum())

        if not self.sum_open:
            tk.Frame(box, bg=HAIR, height=1).pack(fill="x", pady=(6, 0))
            return

        seg = tk.Frame(box, bg=BG)
        seg.pack(anchor="w", pady=(0, 6))
        for s in ("日", "周", "月"):          # 数据键仍用中文
            on = (s == self.sum_scope)
            b = tk.Label(seg, text=I18N.L(s), fg=(ONACC if on else DIM),
                         bg=(ACC if on else CHIPBG), font=F_TINY,
                         padx=10, pady=1, cursor="hand2")
            b.pack(side="left", padx=(0, 5))
            b.bind("<Button-1>", lambda e, x=s: self._set_sum_scope(x))

        grid = tk.Frame(box, bg=BG)
        grid.pack(fill="x", pady=(0, 2))
        for idx, (k, v) in enumerate(info["rows"]):
            r, c = divmod(idx, 2)
            cell = tk.Frame(grid, bg=BG)
            cell.grid(row=r, column=c, sticky="w", padx=(0, 18), pady=1)
            tk.Label(cell, text=k, fg=DIM, bg=BG,
                     font=F_TINY).pack(side="left")
            tk.Label(cell, text=v, fg=FG, bg=BG,
                     font=F_TINY).pack(side="left", padx=(6, 0))
        tk.Frame(box, bg=HAIR, height=1).pack(fill="x", pady=(6, 0))

    # ---------------- 行 ----------------
    def _row(self, i, it, parent=None, pbg=BG, phov=SEC_HOVER, acc=ACC):
        parent = parent if parent is not None else self.inner
        wp = tk.Frame(parent, bg=pbg)
        wp.pack(fill="x", padx=12, pady=0)
        self._row_frames.append((wp, i))

        row = tk.Frame(wp, bg=pbg)
        row.pack(fill="x")
        line = tk.Frame(row, bg=pbg)
        line.pack(fill="x", pady=3)

        done = PL.is_done(it)
        mine = self._locate(i)[0]

        # 左栏固定宽度：每日/阶段/长期/未来的正文左边缘全部对齐
        colw = 86 if I18N.is_cn() else 108
        col = tk.Frame(line, bg=pbg, width=colw, height=22)
        col.pack(side="left")
        col.pack_propagate(False)
        # 先放一个可伸缩的空格，让左侧标签整体靠右，紧贴正文
        tk.Frame(col, bg=pbg).pack(side="left", fill="both", expand=True)

        chip = cb = btn = None
        if mine == "每日":
            # 每日是打卡制：只有一个打卡按钮，别的都不给
            btn = self._btn_widget(col, (I18N.L("已打卡") if done
                                    else I18N.L("打卡")),
                                   done, pbg, lambda idx=i: self.toggle(idx))
            btn.pack(side="left", padx=(6, 0))
        else:
            # 重要性：只用一个带色的小字，不再用实心色块，视觉更安静
            pri = it.get("重要", "中")
            pcol = PRI_COLORS.get(
                pri, "#c9a97a")
            chip = tk.Label(col, text=I18N.L(pri), fg=pcol, bg=pbg,
                            font=F_TINY,
                            width=1, cursor="hand2")
            chip.pack(side="left", padx=(6, 6))
            chip.bind("<Button-1>", lambda e, idx=i: self.cycle_priority(idx))

        due = None
        if mine == "阶段":
            left_days = PL.days_left(it)
            if left_days is None:
                dtext, dcol = I18N.L("期限"), DIM
            elif left_days < 0:
                dtext, dcol = I18N.L("逾期%d") % (-left_days), "#d9705f"
            elif left_days == 0:
                dtext, dcol = I18N.L("今天"), "#e3bd82"
            else:
                dtext, dcol = I18N.L("%d天") % left_days, "#7ba6c9"
            due = tk.Label(col, text=dtext, fg=dcol, bg=pbg, font=F_TINY,
                           width=3, cursor="hand2")
            due.pack(side="left", padx=(0, 5))
            due.bind("<Button-1>", lambda e, idx=i: self.set_due(idx))

        if mine != "每日":
            cb = tk.Canvas(col, width=17, height=17, bg=pbg,
                           highlightthickness=0, bd=0, cursor="hand2")
            cb.pack(side="left")
            self._draw_check(cb, done)
            cb.bind("<Button-1>", lambda e, idx=i: self.toggle(idx))

        wl = (W - 188) if I18N.is_cn() else (W - 210)
        if mine == "每日":
            # 每日打卡不划横线，文字保持原样；打了没打看按钮 + 详情记录
            tfont, tfg = F_BODY, FG
        else:
            tfont = F_STRIKE if done else F_BODY
            tfg = DIM if done else FG
        txt = tk.Label(line, text=it.get("文字", ""),
                       fg=tfg, bg=pbg,
                       font=tfont, anchor="w",
                       justify="left", wraplength=wl, cursor="hand2")
        txt.pack(side="left", fill="x", expand=True)
        txt.bind("<Double-Button-1>", lambda e, idx=i: self._on_dbl(idx))
        # 单击勾选 / 上下拖动排序
        for w in (line, txt):
            w.bind("<ButtonPress-1>", lambda e, idx=i: self._dnd_start(e, idx))
            w.bind("<B1-Motion>", self._dnd_move)
            w.bind("<ButtonRelease-1>", lambda e, idx=i: self._dnd_end(e, idx))
            w.bind("<Enter>", lambda e, ws=None: None)

        subs = it.get("细节") or []
        pct = PL.item_percent(it)
        if mine == "每日":
            # 每日是打卡制：行尾就是「时间详情」入口，打卡记录都在里面
            lb = tk.Label(line, text=I18N.L("详情"), bg=pbg, fg=DIM, font=F_TINY,
                          width=3, cursor="hand2")
            lb.bind("<Button-1>", lambda e, idx=i: self.show_history(idx))
        elif mine == "未来":
            lb = None      # 未来计划：纯清单，没有百分比
        else:
            # 阶段 / 长期：有进度百分比
            lb = tk.Label(line, text="%d%%" % pct, bg=pbg,
                          fg=(OK if pct >= 100 else DIM), font=F_TINY,
                          width=3)
        if lb is not None:
            lb.pack(side="right", padx=(0, 2))

        x = tk.Label(line, text="✕", fg=FAINT, bg=pbg, font=F_TINY, width=2,
                     cursor="hand2")
        x.pack(side="right")
        x.bind("<Button-1>", lambda e, idx=i: self.delete(idx))

        arrow = tk.Label(line, text=("⌄" if i in self.expanded else "›"),
                         fg=(acc if subs else FAINT), bg=pbg,
                         font=(FONT, 12), width=2, cursor="hand2")
        arrow.pack(side="right")
        arrow.bind("<Button-1>", lambda e, idx=i: self.toggle_expand(idx))

        # ⇄ 归类：把这条计划移到 每日 / 阶段 / 长期
        mv = tk.Label(line, text="⇄", fg=FAINT, bg=pbg, font=F_TINY,
                      width=2, cursor="hand2")
        mv.pack(side="right")
        mv.bind("<Button-1>",
                lambda e, idx=i: self.move_menu(idx, e.x_root, e.y_root))

        # cb / due 跟着整行换色；chip、btn 自己有底色，只负责触发整行亮起
        others = [row, line, txt, x, arrow, mv]
        for extra in (lb, cb, due):
            if extra is not None:
                others.append(extra)
        self._row_widgets[i] = others

        # 行尾操作默认很淡，鼠标进这一行才点亮（✕ 亮起变红，提示是删除）
        acts = [(x, FAINT, DANGER),
                (arrow, (acc if subs else FAINT), HOTFG),
                (mv, FAINT, HOTFG)]

        def _hot(_=None):
            for w, _d, hc in acts:
                try:
                    w.configure(fg=hc)
                except Exception:
                    pass

        def _cold(_=None):
            for w, dc, _h in acts:
                try:
                    w.configure(fg=dc)
                except Exception:
                    pass

        for w in others:
            w.bind("<Enter>", lambda e, ws=others: (self._hover(ws, phov), _hot()))
            w.bind("<Leave>", lambda e, ws=others: (self._hover(ws, pbg), _cold()))
        for w in (chip, btn):
            if w is not None:
                w.bind("<Enter>", lambda e, ws=others: (self._hover(ws, phov), _hot()))
                w.bind("<Leave>", lambda e, ws=others: (self._hover(ws, pbg), _cold()))

        if i in self.expanded:
            box = tk.Frame(wp, bg=SUB_BG)
            box.pack(fill="x", padx=(26, 6), pady=(2, 6))
            for j, s in enumerate(subs):
                sr = tk.Frame(box, bg=SUB_BG)
                sr.pack(fill="x", pady=1)
                sd = bool(s.get("完成"))
                cb2 = tk.Canvas(sr, width=16, height=16, bg=SUB_BG,
                                highlightthickness=0, bd=0, cursor="hand2")
                cb2.pack(side="left", padx=(8, 6))
                self._draw_check(cb2, sd, small=True)
                cb2.bind("<Button-1>", lambda e, a=i, b=j: self.toggle_sub(a, b))
                t2 = tk.Label(sr, text=s.get("文字", ""),
                              fg=(DIM if sd else SUB), bg=SUB_BG,
                              font=(F_SUB_STRIKE if sd else F_SUB), anchor="w",
                              justify="left", wraplength=W - 190, cursor="hand2")
                t2.pack(side="left", fill="x", expand=True)
                t2.bind("<Double-Button-1>", lambda e, a=i, b=j: self.edit_sub(a, b))
                d2 = tk.Label(sr, text="✕", fg="#3d4551", bg=SUB_BG, font=F_TINY,
                              width=2, cursor="hand2")
                d2.pack(side="right", padx=(0, 6))
                d2.bind("<Button-1>", lambda e, a=i, b=j: self.del_sub(a, b))

            if self.adding_sub == i:
                er = tk.Frame(box, bg=SUB_BG)
                er.pack(fill="x", pady=(4, 2), padx=(8, 8))
                e = tk.Entry(er, bg="#1d222a", fg=FG, bd=0, font=F_SUB,
                             insertbackground=ACC)
                e.pack(fill="x", ipady=4, padx=4)
                e.focus_set()
                e.bind("<Return>", lambda ev, a=i: self.commit_sub(a, e))
                e.bind("<FocusOut>", lambda ev, a=i: self.commit_sub(a, e))
            else:
                add = tk.Label(box, text="＋ 添加细节", fg="#5a6270", bg=SUB_BG,
                               font=F_TINY, cursor="hand2")
                add.pack(anchor="w", padx=10, pady=(3, 4))
                add.bind("<Button-1>", lambda e, idx=i: self.start_sub(idx))

    def _hover(self, widgets, color):
        for w in widgets:
            try:
                w.configure(bg=color)
            except Exception:
                pass

    # ---------------- 拖动排序 ----------------
    def _dnd_start(self, e, i):
        self._dnd = {"i": i, "y0": e.y_root, "moved": False, "target": i,
                     "tab": None, "sec": None}

    def _dnd_move(self, e):
        d = getattr(self, "_dnd", None)
        if not d:
            return
        if not d["moved"] and abs(e.y_root - d["y0"]) < 7:
            return
        if not d["moved"]:
            d["moved"] = True
            try:
                self.root.configure(cursor="fleur")
            except Exception:
                pass
        # 拖到别的分类标题/条目上 → 松手就归类
        src = self._locate(d["i"])[0]
        sec = self._sec_at(e.x_root, e.y_root)
        if sec and sec != src:
            d["sec"] = sec
            d["tab"] = sec
            self._paint_sec(sec)
            self._paint_dnd(d["i"], -1)
            return
        d["sec"] = None
        d["tab"] = None
        self._paint_sec(None)
        tgt = self._index_at(e.y_root)
        if tgt is None:
            return
        d["target"] = tgt
        self._paint_dnd(d["i"], tgt)

    def _index_at(self, y_root):
        best, bi = 1e9, None
        for w, idx in self._row_frames:
            try:
                y = w.winfo_rooty() + w.winfo_height() / 2.0
            except Exception:
                continue
            dist = abs(y - y_root)
            if dist < best:
                best, bi = dist, idx
        return bi

    def _paint_dnd(self, src, tgt):
        for idx, ws in getattr(self, "_row_widgets", {}).items():
            m = self._locate(idx)[0]
            pbg, phov, _acc = SECTION_STYLE.get(m, (SEC_BG, SEC_HOVER, ACC))
            if idx == src:
                col = phov
            elif idx == tgt:
                col = "#303a49"
            else:
                col = pbg
            self._hover(ws, col)

    def _dnd_end(self, e, i):
        d = getattr(self, "_dnd", None)
        self._dnd = None
        try:
            self.root.configure(cursor="")
        except Exception:
            pass
        if not d:
            return
        if not d.get("moved"):
            # 单击：延迟一点点再勾选，好让双击（编辑）有机会插进来
            if getattr(self, "_dbl_guard", False):
                self._dbl_guard = False
                return
            self._pending_toggle = i
            self.root.after(230, lambda: self._fire_toggle(i))
            return
        sec = d.get("sec")
        if sec:
            self.move_to(i, sec)    # 拖到别类标题上 → 换分类
            return
        tgt = d.get("target")
        src, i1 = self._locate(i)
        tm, i2 = self._locate(tgt) if tgt is not None else (None, None)
        if src is None or tgt is None or tgt == i or tm is None:
            self.refresh()
            return
        if tm != src:               # 拖进别类的条目里 → 也算归类
            self.move_to(i, tm)
            return
        lst = PL.get_list(self.data, src, create=True)
        if not (0 <= i1 < len(lst)):
            self.refresh()
            return
        it = lst.pop(i1)
        if i1 < i2:
            i2 -= 1
        lst.insert(max(0, min(i2, len(lst))), it)
        self.expanded = set()
        self._save()
        self.refresh()

    # ---------------- 归类：移到别的分类 ----------------    def _tab_at(self, x_root, y_root):
        for name, (lb, ul) in getattr(self, "tabs", {}).items():
            try:
                if not lb.winfo_ismapped() or lb.winfo_width() < 12:
                    continue
                x0, y0 = lb.winfo_rootx(), lb.winfo_rooty()
                x1 = x0 + lb.winfo_width()
                y1 = y0 + lb.winfo_height()
            except Exception:
                continue
            if x0 - 12 <= x_root <= x1 + 12 and y0 - 8 <= y_root <= y1 + 10:
                return name
        return None

    def _paint_tab_target(self, name):
        self._paint_sec(name)

    def move_menu(self, i, x_root, y_root):
        if not (0 <= i < len(self.items)):
            return
        cur = self._locate(i)[0]
        m = tk.Menu(self.root, tearoff=0, bg="#22262e", fg=FG, bd=0,
                    activebackground=ACC, activeforeground="#191d24",
                    font=F_SMALL)
        for name in PL.MODES:
            m.add_command(
                label=(I18N.L("移到 %s") % I18N.L(name)) +
                (I18N.L("（当前）") if name == cur else ""),
                command=lambda n=name: self.move_to(i, n),
                state=("disabled" if name == cur else "normal"))
        self._menu = m          # 防止被 GC
        try:
            m.tk_popup(x_root, y_root)
        finally:
            try:
                m.grab_release()
            except Exception:
                pass

    def move_to(self, i, target):
        """把第 i 条搬到 target 分类（内容、子计划、优先级、完成度一起搬）。"""
        src, idx = self._locate(i)
        if src is None or target not in PL.MODES or target == src:
            return
        it = self.items[i]
        lst = PL.get_list(self.data, src, create=True)
        if 0 <= idx < len(lst):
            del lst[idx]
        PL.get_list(self.data, target, create=True).append(it)
        if target == "每日":
            PL.ensure_id(it)
        self.expanded = set()
        self.adding_sub = None
        self._save()
        self.refresh()
        self._toast(I18N.L("已移到「%s」") % I18N.L(target))

    def _toast(self, text):
        try:
            win = tk.Toplevel(self.root)
            win.overrideredirect(True)
            win.configure(bg="#2b3038")
            win.attributes("-topmost", True)
            tk.Label(win, text=text, fg=ACC, bg="#2b3038", font=F_SMALL,
                     padx=14, pady=7).pack()
            win.update_idletasks()
            x = self.root.winfo_rootx() + (self.root.winfo_width() -
                                           win.winfo_width()) // 2
            y = self.root.winfo_rooty() + self.root.winfo_height() + 8
            if y + win.winfo_height() > self.root.winfo_screenheight() - 8:
                y = max(8, self.root.winfo_rooty() - win.winfo_height() - 8)
            win.geometry("+%d+%d" % (max(8, x), y))
            win.after(1300, win.destroy)
        except Exception:
            pass

    def _record(self, i):
        """每日计划：把今天「做了/没做」写进打卡记录。"""
        try:
            m, _idx = self._locate(i)
            if m != "每日":
                return
            PL.record_day(self.data, self.items[i])
        except Exception:
            pass

    def show_history(self, i):
        """时间详情：这条每日计划最近每天打没打卡。"""
        if not (0 <= i < len(self.items)):
            return
        it = self.items[i]
        iid = PL.ensure_id(it)
        rec = PL.history_of(self.data, iid)
        done_n, total_n, rate = PL.history_stats(rec)
        stk = PL.streak(rec)

        win = tk.Toplevel(self.root)
        win.overrideredirect(True)
        win.configure(bg="#22272f")
        win.attributes("-topmost", True)
        box = tk.Frame(win, bg="#22272f")
        box.pack(padx=14, pady=12)

        tk.Label(box, text=it.get("文字", ""), fg=FG, bg="#22272f",
                 font=(FONT, 10, "bold"), anchor="w",
                 wraplength=250, justify="left").pack(anchor="w")
        tk.Label(box, text=I18N.L("打卡 %d 天 · 连续 %d 天 · 近30天 %d%%")
                          % (done_n, stk, rate),
                 fg=ACC, bg="#22272f", font=F_TINY).pack(anchor="w", pady=(3, 6))
        tk.Frame(box, bg="#333a45", height=1).pack(fill="x", pady=(0, 6))

        if not rec:
            tk.Label(box, text=I18N.L("还没有记录\n勾选一次打卡就会记下来"),
                     fg="#6d7784", bg="#22272f", font=F_TINY,
                     justify="left").pack(anchor="w")
        else:
            rows = sorted(rec.items(), reverse=True)[:14]
            for k, v in rows:
                r = tk.Frame(box, bg="#22272f")
                r.pack(fill="x", pady=1)
                label = I18N.day_label(k)
                tk.Label(r, text=label, fg=SUB, bg="#22272f", font=F_TINY,
                         width=14, anchor="w").pack(side="left")
                tk.Label(r, text=(I18N.L("✓ 打卡") if v else I18N.L("· 未打卡")),
                         fg=(OK if v else "#6d7784"), bg="#22272f",
                         font=F_TINY).pack(side="left")
            if len(rec) > len(rows):
                tk.Label(box, text=I18N.L("共记录 %d 天，这里显示最近 %d 天")
                                   % (len(rec), len(rows)),
                         fg="#5d6675", bg="#22272f",
                         font=F_TINY).pack(anchor="w", pady=(5, 0))

        win.update_idletasks()
        w_h = win.winfo_height()
        try:
            rx = self.root.winfo_rootx() + self.root.winfo_width() - win.winfo_width()
            ry = self.root.winfo_pointery() + 12
            if ry + w_h > self.root.winfo_screenheight() - 40:
                ry = self.root.winfo_pointery() - w_h - 12
        except Exception:
            rx, ry = 400, 300
        win.geometry("+%d+%d" % (max(8, rx), max(8, ry)))
        win.bind("<Escape>", lambda _: win.destroy())
        win.bind("<FocusOut>", lambda _: win.destroy())
        win.after(20000, win.destroy)
        self._hist = win

    def _btn_widget(self, parent, text, done, pbg, cmd, w=None, h=22):
        if w is None:
            w = 56 if I18N.is_cn() else 78
        """按主题形态绘制的按钮：圆角填充 / 描边 / 墨线 / 科技括号 / 印章"""
        cv = tk.Canvas(parent, width=w, height=h, bg=pbg,
                       highlightthickness=0, bd=0, cursor="hand2")
        col = OK if done else ACC
        mode, r = BTN_MODE, BTN_R
        try:
            if mode == "fill":
                _rr(cv, 1, 1, w - 1, h - 1, r, fill=col, outline="")
                tcol = ONACC
            elif mode == "seal":
                _rr(cv, 1, 1, w - 1, h - 1, r, fill=INP, outline=col)
                tcol = col
            elif mode == "outline":
                _rr(cv, 1, 1, w - 1, h - 1, r, fill="", outline=col)
                tcol = col
            elif mode == "ink":
                cv.create_rectangle(3, h - 3, w - 3, h - 1, fill=col,
                                    outline="")
                tcol = col
            else:                      # bracket
                cv.create_rectangle(1, 3, 3, h - 3, fill=col, outline="")
                cv.create_rectangle(w - 3, 3, w - 1, h - 3, fill=col,
                                    outline="")
                tcol = col
            cv.create_text(w // 2, h // 2 - 1, text=text, fill=tcol,
                           font=(FAM_TITLE, 8))
            cv.bind("<Button-1>", lambda e: cmd())
        except Exception:
            pass
        return cv

    def _dot_widget(self, parent, color, pbg):
        """段标识：圆点 / 方块 / 墨条 / 科技刻度 / 菱形"""
        sh = DOT_SHAPE
        size = {"bar": (4, 12), "tick": (11, 11), "diamond": (10, 10),
                "square": (6, 6)}.get(sh, (8, 8))
        cv = tk.Canvas(parent, width=size[0], height=size[1], bg=pbg,
                       highlightthickness=0, bd=0)
        try:
            if sh == "bar":
                cv.create_rectangle(0, 0, 4, 12, fill=color, outline="")
            elif sh == "tick":
                cv.create_line(1, 10, 9, 1, fill=color, width=3,
                               capstyle="round")
            elif sh == "diamond":
                cv.create_polygon(5, 0, 10, 5, 5, 10, 0, 5, fill=color,
                                  outline="")
            elif sh == "square":
                cv.create_rectangle(0, 0, 6, 6, fill=color, outline="")
            else:
                cv.create_oval(0, 0, 8, 8, fill=color, outline="")
        except Exception:
            pass
        return cv

    def _draw_check(self, cv, done, small=False):
        cv.delete("all")
        n = 16 if small else 18
        pad = 2
        if done:
            cv.create_oval(pad, pad, n - pad, n - pad, fill=OK, outline="")
            cv.create_line(n * 0.28, n * 0.52, n * 0.44, n * 0.68,
                           n * 0.73, n * 0.34, fill="#12281c", width=2,
                           capstyle="round", joinstyle="round")
        else:
            cv.create_oval(pad, pad, n - pad, n - pad, outline="#5c6472",
                           width=CHK_W)

    # ---------------- 操作 ----------------
    def add(self):
        t = self.entry.get().strip()
        if not t or t == getattr(self, "_ph", None):
            return
        it = {"文字": t, "完成": False, "重要": "中", "细节": []}
        if self.add_target == "每日":
            it["id"] = PL._new_id()
        PL.get_list(self.data, self.add_target, create=True).append(it)
        self.entry.delete(0, "end")
        self.entry.config(fg=DIM)
        self.entry.insert(0, self._ph)
        self._save()
        self.refresh()

    def toggle(self, i):
        if 0 <= i < len(self.items):
            self.items[i]["完成"] = not self.items[i].get("完成")
            self._record(i)
            self._save()
            self.refresh()

    def delete(self, i):
        m, idx = self._locate(i)
        if m is None:
            return
        lst = PL.get_list(self.data, m, create=True)
        if 0 <= idx < len(lst):
            del lst[idx]
        self.expanded = set()
        self.adding_sub = None
        self._save()
        self.refresh()

    def cycle_priority(self, i):
        if 0 <= i < len(self.items):
            cur = self.items[i].get("重要", "中")
            nxt = PL.PRIORITIES[(PL.PRIORITIES.index(cur) + 1) % len(PL.PRIORITIES)]
            self.items[i]["重要"] = nxt
            self._save()
            self.refresh()

    def toggle_expand(self, i):
        if i in self.expanded:
            self.expanded.discard(i)
        else:
            self.expanded.add(i)
        self.refresh()

    def start_sub(self, i):
        self.adding_sub = i
        self.expanded.add(i)
        self.refresh()

    def commit_sub(self, i, entry):
        v = entry.get().strip()
        self.adding_sub = None
        if v and 0 <= i < len(self.items):
            self.items[i].setdefault("细节", []).append({"文字": v, "完成": False})
            self._record(i)
            self._save()
        self.refresh()

    def toggle_sub(self, i, j):
        try:
            s = self.items[i]["细节"][j]
            s["完成"] = not s.get("完成")
            self._record(i)
            self._save()
            self.refresh()
        except Exception:
            pass

    def del_sub(self, i, j):
        try:
            del self.items[i]["细节"][j]
            self._record(i)
            self._save()
            self.refresh()
        except Exception:
            pass

    def edit(self, i):
        if 0 <= i < len(self.items):
            self._dialog(self.items[i].get("文字", ""), lambda v: self._set_text(i, v))

    def _on_dbl(self, i):
        """双击文字 = 编辑内容；顺手取消刚才单击排队的打卡/勾选。"""
        self._pending_toggle = None
        self._dbl_guard = True
        try:
            self.root.after(600, lambda: setattr(self, "_dbl_guard", False))
        except Exception:
            pass
        self.edit(i)
        return "break"

    def _fire_toggle(self, i):
        if getattr(self, "_pending_toggle", None) != i:
            return
        self._pending_toggle = None
        self.toggle(i)

    def edit_sub(self, i, j):
        try:
            cur = self.items[i]["细节"][j].get("文字", "")
        except Exception:
            return
        self._dialog(cur, lambda v: self._set_sub_text(i, j, v))

    def _set_text(self, i, v):
        if v and 0 <= i < len(self.items):
            self.items[i]["文字"] = v
            self._save()
        self.refresh()

    def _set_sub_text(self, i, j, v):
        try:
            if v:
                self.items[i]["细节"][j]["文字"] = v
                self._save()
        except Exception:
            pass
        self.refresh()

    def _dialog(self, cur, on_ok):
        win = tk.Toplevel(self.root)
        win.overrideredirect(True)
        win.configure(bg="#22272f")
        win.attributes("-topmost", True)

        box = tk.Frame(win, bg="#22272f")
        box.pack(padx=14, pady=12)
        tk.Label(box, text=I18N.L("编辑内容"), fg="#5d6675", bg="#22272f",
                 font=F_TINY).pack(anchor="w")
        e = tk.Entry(box, bg=INP, fg=FG, bd=0, font=F_BODY, width=30,
                     insertbackground=ACC)
        e.pack(fill="x", pady=(5, 8), ipady=5)
        e.insert(0, cur)
        e.focus_set()
        e.select_range(0, "end")

        bar = tk.Frame(box, bg="#22272f")
        bar.pack(fill="x")

        def ok(_=None):
            v = e.get().strip()
            win.destroy()
            on_ok(v)

        b1 = tk.Label(bar, text=I18N.L("保存"), fg="#14251b", bg=ACC,
                      font=F_SMALL,
                      padx=14, pady=3, cursor="hand2")
        b1.pack(side="right")
        b1.bind("<Button-1>", ok)
        b2 = tk.Label(bar, text=I18N.L("取消"), fg=SUB, bg=CHIPBG, font=F_SMALL,
                      padx=10, pady=3, cursor="hand2")
        b2.pack(side="right", padx=(0, 8))
        b2.bind("<Button-1>", lambda ev: win.destroy())
        tk.Label(bar, text=I18N.L("回车保存 · Esc 取消"), fg="#4d5663",
                 bg="#22272f",
                 font=F_TINY).pack(side="left")

        e.bind("<Return>", ok)
        e.bind("<Escape>", lambda ev: win.destroy())

        win.update_idletasks()
        x = (self.root.winfo_rootx() +
             (self.root.winfo_width() - win.winfo_width()) // 2)
        y = self.root.winfo_rooty() + 130
        win.geometry("+%d+%d" % (max(8, x), max(8, y)))
        self._editwin = win

    def _save(self):
        PL.save(self.data)


def main():
    if _single_instance() is None:      # 已经有一个在跑了
        return
    root = tk.Tk()
    try:
        root.tk.call("tk", "scaling", 1.15)
    except Exception:
        pass
    # 这是桌面挂件：Alt+F4 / 误触关闭都不该让它消失
    root.protocol("WM_DELETE_WINDOW", lambda: None)
    root.report_callback_exception = _log_exc
    try:
        Card(root)
        root.mainloop()
    except SystemExit:
        raise
    except Exception:
        _log_exc(*sys.exc_info())
        raise


if __name__ == "__main__":
    main()
