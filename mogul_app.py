from __future__ import annotations

import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

import techno_football as game

BG = "#0b1220"
PANEL = "#121c2f"
PANEL2 = "#182438"
EDGE = "#2a3b55"
TEXT = "#e7eef8"
MUTED = "#9aa8bd"
GOLD = "#d4b45a"
GREEN = "#3fae7a"
RED = "#c85b5b"
BLUE = "#4d7ec8"

STYLESHEET = f"""
QMainWindow, QDialog {{
  background: {BG};
  color: {TEXT};
}}
QWidget {{
  color: {TEXT};
  font-size: 13px;
}}
QLabel#Title {{
  font-size: 22px;
  font-weight: 700;
  color: {GOLD};
  letter-spacing: 1px;
}}
QLabel#SubTitle {{
  color: {MUTED};
  font-size: 12px;
}}
QLabel#StatValue {{
  font-size: 20px;
  font-weight: 700;
}}
QLabel#StatName {{
  color: {MUTED};
  font-size: 11px;
}}
QFrame#Card, QFrame#Nav, QFrame#TopBar, QFrame#Report {{
  background: {PANEL};
  border: 1px solid {EDGE};
  border-radius: 10px;
}}
QFrame#StatCard {{
  background: {PANEL2};
  border: 1px solid {EDGE};
  border-radius: 8px;
}}
QPushButton {{
  background: {PANEL2};
  border: 1px solid {EDGE};
  border-radius: 8px;
  padding: 10px 14px;
  text-align: left;
}}
QPushButton:hover {{
  border-color: {GOLD};
  background: #1d2b44;
}}
QPushButton:pressed {{
  background: #243552;
}}
QPushButton#NavBtn {{
  background: transparent;
  border: none;
  border-radius: 6px;
  padding: 12px 14px;
  color: {MUTED};
  font-weight: 600;
}}
QPushButton#NavBtn:checked, QPushButton#NavBtn:hover {{
  background: {PANEL2};
  color: {TEXT};
}}
QPushButton#Primary {{
  background: {GOLD};
  color: #1a1408;
  border: none;
  font-weight: 700;
  text-align: center;
}}
QPushButton#Primary:hover {{
  background: #e0c46a;
}}
QPushButton#Danger {{
  background: #3a1f24;
  border: 1px solid {RED};
  color: {TEXT};
  text-align: center;
}}
QProgressBar {{
  background: #0a101a;
  border: 1px solid {EDGE};
  border-radius: 4px;
  text-align: center;
  max-height: 10px;
}}
QProgressBar::chunk {{
  background: {GREEN};
  border-radius: 3px;
}}
QProgressBar#Warn::chunk {{ background: {GOLD}; }}
QProgressBar#Bad::chunk {{ background: {RED}; }}
QLineEdit, QComboBox, QListWidget {{
  background: {PANEL2};
  border: 1px solid {EDGE};
  border-radius: 6px;
  padding: 8px;
  selection-background-color: {BLUE};
}}
QListWidget::item {{
  padding: 8px;
}}
"""

ACTION_KEYS = ["1", "2", "3", "4"]


class StatCard(QFrame):
    def __init__(self, name: str, parent=None):
        super().__init__(parent)
        self.setObjectName("StatCard")
        lay = QVBoxLayout(self)
        lay.setContentsMargins(12, 10, 12, 10)
        lay.setSpacing(4)
        self.name = QLabel(name)
        self.name.setObjectName("StatName")
        self.value = QLabel("—")
        self.value.setObjectName("StatValue")
        self.bar = QProgressBar()
        self.bar.setRange(0, 100)
        self.bar.setTextVisible(False)
        self.bar.hide()
        lay.addWidget(self.name)
        lay.addWidget(self.value)
        lay.addWidget(self.bar)

    def set_plain(self, text: str) -> None:
        self.bar.hide()
        self.value.setText(text)

    def set_meter(self, text: str, value: int, kind: str = "ok") -> None:
        self.value.setText(text)
        self.bar.show()
        self.bar.setValue(max(0, min(100, int(value))))
        self.bar.setObjectName({"ok": "", "warn": "Warn", "bad": "Bad"}.get(kind, ""))
        self.bar.style().unpolish(self.bar)
        self.bar.style().polish(self.bar)


class NewGameDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("New Career — TechnoFootball")
        self.setMinimumWidth(420)
        lay = QVBoxLayout(self)
        title = QLabel("OPEN A NEW FRONT OFFICE")
        title.setObjectName("Title")
        lay.addWidget(title)
        lay.addWidget(QLabel("Creator name"))
        self.name = QLineEdit()
        self.name.setPlaceholderText("e.g. Neo, Sensored, your handle")
        lay.addWidget(self.name)
        lay.addWidget(QLabel("Niche"))
        self.niche = QComboBox()
        self.niche.addItems(["fps", "justchatting", "tech", "variety"])
        self.niche.setCurrentText("variety")
        lay.addWidget(self.niche)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        lay.addWidget(buttons)

    def values(self) -> tuple[str, str]:
        return (self.name.text().strip() or "Anon", self.niche.currentText())


class MogulWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TechnoFootball — Creator Career Mogul")
        self.resize(1280, 800)
        self.state: dict | None = None
        self._nav_btns: list[QPushButton] = []

        root = QWidget()
        self.setCentralWidget(root)
        outer = QHBoxLayout(root)
        outer.setContentsMargins(14, 14, 14, 14)
        outer.setSpacing(12)

        nav = QFrame()
        nav.setObjectName("Nav")
        nav.setFixedWidth(200)
        nav_l = QVBoxLayout(nav)
        brand = QLabel("TECHNO\nFOOTBALL")
        brand.setObjectName("Title")
        nav_l.addWidget(brand)
        tag = QLabel("Front office · Season sim")
        tag.setObjectName("SubTitle")
        nav_l.addWidget(tag)
        nav_l.addSpacing(12)
        self.stack = QStackedWidget()
        for i, label in enumerate(["Office", "Week Plan", "Ledger", "Rival", "Season"]):
            btn = QPushButton(label)
            btn.setObjectName("NavBtn")
            btn.setCheckable(True)
            btn.clicked.connect(lambda _=False, idx=i: self._goto(idx))
            self._nav_btns.append(btn)
            nav_l.addWidget(btn)
        nav_l.addStretch(1)
        self.btn_new = QPushButton("New Career")
        self.btn_new.setObjectName("Primary")
        self.btn_new.clicked.connect(self.new_career)
        self.btn_save = QPushButton("Save")
        self.btn_save.clicked.connect(self.save_now)
        self.btn_quit = QPushButton("Quit")
        self.btn_quit.setObjectName("Danger")
        self.btn_quit.clicked.connect(self.close)
        nav_l.addWidget(self.btn_new)
        nav_l.addWidget(self.btn_save)
        nav_l.addWidget(self.btn_quit)
        outer.addWidget(nav)

        main_col = QVBoxLayout()
        main_col.setSpacing(12)
        outer.addLayout(main_col, 1)

        top = QFrame()
        top.setObjectName("TopBar")
        top_l = QHBoxLayout(top)
        self.lbl_identity = QLabel("No career loaded")
        self.lbl_identity.setObjectName("Title")
        self.lbl_week = QLabel("")
        self.lbl_week.setObjectName("SubTitle")
        self.lbl_week.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        top_l.addWidget(self.lbl_identity, 1)
        top_l.addWidget(self.lbl_week)
        main_col.addWidget(top)

        self.page_office = self._build_office()
        self.page_week = self._build_week()
        self.page_ledger = self._build_ledger()
        self.page_rival = self._build_rival()
        self.page_season = self._build_season()
        for p in (self.page_office, self.page_week, self.page_ledger, self.page_rival, self.page_season):
            self.stack.addWidget(p)
        main_col.addWidget(self.stack, 1)

        self._goto(0)
        self._boot()

    def _goto(self, idx: int) -> None:
        self.stack.setCurrentIndex(idx)
        for i, b in enumerate(self._nav_btns):
            b.setChecked(i == idx)

    def _build_office(self) -> QWidget:
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setSpacing(12)
        grid = QGridLayout()
        grid.setSpacing(10)
        self.stats: dict[str, StatCard] = {}
        specs = [
            ("subs", "SUBSCRIBERS"),
            ("cash", "CASH"),
            ("energy", "ENERGY"),
            ("hype", "HYPE"),
            ("watch", "WATCH-HRS"),
            ("sponsors", "SPONSORS"),
            ("burnout", "BURNOUT"),
            ("rival", "RIVAL HYPE"),
        ]
        for i, (key, name) in enumerate(specs):
            card = StatCard(name)
            self.stats[key] = card
            grid.addWidget(card, i // 4, i % 4)
        lay.addLayout(grid)

        report = QFrame()
        report.setObjectName("Report")
        rl = QVBoxLayout(report)
        rh = QLabel("WEEK REPORT")
        rh.setObjectName("SubTitle")
        self.lbl_report = QLabel("Pick a weekly action on Week Plan to advance the season.")
        self.lbl_report.setWordWrap(True)
        self.lbl_report.setMinimumHeight(90)
        rl.addWidget(rh)
        rl.addWidget(self.lbl_report)
        lay.addWidget(report)
        lay.addStretch(1)
        return w

    def _build_week(self) -> QWidget:
        w = QWidget()
        lay = QVBoxLayout(w)
        intro = QLabel(
            "Choose ONE play for this week — Mogul style. Click a card; the algo and bills resolve automatically."
        )
        intro.setObjectName("SubTitle")
        intro.setWordWrap(True)
        lay.addWidget(intro)
        grid = QGridLayout()
        grid.setSpacing(12)
        self.action_buttons: dict[str, QPushButton] = {}
        for i, key in enumerate(ACTION_KEYS):
            meta = game.ACTION_META[key]
            label, _deltas = game.ACTIONS[key]
            btn = QPushButton(f"{meta['role']}  ·  {meta['title']}\n{meta['blurb']}\n\n{label}")
            btn.setMinimumHeight(120)
            btn.clicked.connect(lambda _=False, k=key: self.play_action(k))
            self.action_buttons[key] = btn
            grid.addWidget(btn, i // 2, i % 2)
        lay.addLayout(grid)
        tip = QLabel(
            "Tip: Grind = safety · Clips = upside + risk · Collab = hype · Rest before burnout bricks you."
        )
        tip.setObjectName("SubTitle")
        tip.setWordWrap(True)
        lay.addWidget(tip)
        lay.addStretch(1)
        return w

    def _build_ledger(self) -> QWidget:
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.addWidget(QLabel("SEASON LEDGER"))
        self.ledger = QListWidget()
        lay.addWidget(self.ledger, 1)
        return w

    def _build_rival(self) -> QWidget:
        w = QWidget()
        lay = QVBoxLayout(w)
        card = QFrame()
        card.setObjectName("Card")
        cl = QVBoxLayout(card)
        cl.addWidget(QLabel("RIVAL PRESSURE"))
        self.lbl_rival = QLabel("—")
        self.lbl_rival.setWordWrap(True)
        self.rival_bar = QProgressBar()
        self.rival_bar.setRange(0, 100)
        cl.addWidget(self.lbl_rival)
        cl.addWidget(self.rival_bar)
        note = QLabel(
            "When rival hype outruns yours, doom weeks get meaner and blessings rarer. "
            "Collabs and clips are how you punch back without living on pure grind."
        )
        note.setObjectName("SubTitle")
        note.setWordWrap(True)
        cl.addWidget(note)
        lay.addWidget(card)
        lay.addStretch(1)
        return w

    def _build_season(self) -> QWidget:
        w = QWidget()
        lay = QVBoxLayout(w)
        card = QFrame()
        card.setObjectName("Card")
        cl = QVBoxLayout(card)
        cl.addWidget(QLabel("SEASON OBJECTIVES"))
        self.lbl_season = QLabel("—")
        self.lbl_season.setWordWrap(True)
        cl.addWidget(self.lbl_season)
        self.week_bar = QProgressBar()
        self.week_bar.setRange(0, game.SEASON_WEEKS)
        cl.addWidget(self.week_bar)
        lay.addWidget(card)
        lay.addStretch(1)
        return w

    def _boot(self) -> None:
        existing = game.load_game()
        if existing:
            r = QMessageBox.question(
                self,
                "Resume career?",
                f"Resume {existing.get('name', 'save')} at week {existing.get('week')}?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.Yes,
            )
            if r == QMessageBox.Yes:
                self.state = existing
                self.refresh()
                return
            game.clear_save()
        self.new_career()

    def new_career(self) -> None:
        dlg = NewGameDialog(self)
        if dlg.exec() != QDialog.Accepted:
            return
        name, niche = dlg.values()
        self.state = game.new_game(name, niche)
        game.save_game(self.state)
        self.lbl_report.setText("New career opened. Head to Week Plan and call the first play.")
        self.refresh()
        self._goto(1)

    def save_now(self) -> None:
        if not self.state:
            return
        game.save_game(self.state)
        QMessageBox.information(self, "Saved", f"Career written to {game.SAVE_PATH.name}.")

    def play_action(self, key: str) -> None:
        if not self.state:
            return
        dead = game.fail_check(self.state)
        won = game.win_check(self.state)
        if dead or won:
            QMessageBox.information(self, "Season over", dead or won)
            return
        report = game.resolve_week(self.state, key)
        self.lbl_report.setText(f"{report['action']}\n{report['algo']}\n{report['bills']}")
        self.refresh()
        self._goto(0)
        if report.get("fail"):
            QMessageBox.critical(self, "Season over", report["fail"])
            game.clear_save()
            self._lock_actions(True)
        elif report.get("win"):
            QMessageBox.information(self, "Season clear", report["win"])
            game.clear_save()
            self._lock_actions(True)

    def _lock_actions(self, locked: bool) -> None:
        for b in self.action_buttons.values():
            b.setEnabled(not locked)

    def refresh(self) -> None:
        s = self.state
        if not s:
            return
        self.lbl_identity.setText(f"{s['name']}  ·  {s['niche'].upper()}")
        self.lbl_week.setText(f"WEEK {s['week']} / {game.SEASON_WEEKS}")
        self.stats["subs"].set_plain(f"{s['subs']:,}")
        self.stats["cash"].set_plain(f"${s['cash']:,}")
        e = int(s["energy"])
        self.stats["energy"].set_meter(f"{e}/100", e, "bad" if e < 30 else "warn" if e < 55 else "ok")
        h = int(s["hype"])
        self.stats["hype"].set_meter(f"{h}/100", h, "ok" if h >= 35 else "warn")
        self.stats["watch"].set_plain(f"{s['watch']:,}")
        self.stats["sponsors"].set_plain(str(s["sponsors"]))
        b = int(s["burnout"])
        self.stats["burnout"].set_meter(str(b), min(100, b * 25), "bad" if b >= 3 else "warn" if b else "ok")
        rh = int(s["rival_hype"])
        self.stats["rival"].set_meter(f"{rh}/100", rh, "bad" if rh > h + 10 else "warn")

        gap = rh - h
        self.lbl_rival.setText(
            f"Rival hype {rh} vs your hype {h}. "
            + ("They are eating the feed — expect meaner algo weeks." if gap > 0 else "You are holding the timeline.")
        )
        self.rival_bar.setValue(rh)

        week = int(s["week"])
        self.week_bar.setValue(min(game.SEASON_WEEKS, max(0, week - 1)))
        self.lbl_season.setText(
            f"Survive {game.SEASON_WEEKS} weeks without bankruptcy, burnout, or collapse.\n"
            f"Grades at clear: Scraping by · Working creator · Breakout · Cult.\n"
            f"Current week marker: {week}/{game.SEASON_WEEKS}."
        )

        self.ledger.clear()
        for row in reversed(s.get("history", [])):
            label = game.ACTIONS.get(str(row.get("action")), ("?",))[0]
            self.ledger.addItem(f"Week {row.get('week')}: {label} — {row.get('algo')}")

        over = bool(game.fail_check(s) or game.win_check(s))
        self._lock_actions(over)


def main() -> int:
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet(STYLESHEET)
    app.setFont(QFont("Segoe UI", 10))
    win = MogulWindow()
    win.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
