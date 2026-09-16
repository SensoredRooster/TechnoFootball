#!/usr/bin/env python3
"""TechnoFootball — text mogul for a creator career (Football Mogul bones)."""

from __future__ import annotations

import json
import random
import sys
from pathlib import Path

SAVE_PATH = Path(__file__).resolve().parent / "save.json"
SEASON_WEEKS = 12

ACTIONS = {
    # Tuned so grind = cash/watch, clips = growth, collab = hype (not a cash trap),
    # rest = real burnout insurance instead of a weak skip.
    "1": (
        "Grind a longform stream",
        {"energy": -14, "cash": 65, "subs": 8, "watch": 150, "hype": 2, "burn": 0},
    ),
    "2": (
        "Ship short-form clips",
        {"energy": -8, "cash": 18, "subs": 26, "watch": 30, "hype": 6, "burn": 0},
    ),
    "3": (
        "Collab / networking",
        {"energy": -10, "cash": -10, "subs": 24, "watch": 45, "hype": 14, "burn": 0},
    ),
    "4": (
        "Rest + admin",
        {"energy": 34, "cash": -12, "subs": 1, "watch": 0, "hype": -1, "burn": -2},
    ),
}


def clamp(n: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, n))


def new_game(name: str, niche: str) -> dict:
    return {
        "week": 1,
        "name": name,
        "niche": niche,
        "subs": 150,
        "cash": 500,
        "energy": 85,
        "watch": 0,
        "hype": 8,
        "sponsors": 0,
        "burnout": 0,
        "rival_hype": 12,
        "history": [],
    }


def save_game(state: dict) -> None:
    SAVE_PATH.write_text(json.dumps(state, indent=2), encoding="utf-8")


def load_game() -> dict | None:
    if not SAVE_PATH.exists():
        return None
    try:
        return json.loads(SAVE_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def clear_save() -> None:
    if SAVE_PATH.exists():
        SAVE_PATH.unlink()


def status(s: dict) -> str:
    return (
        f"\n=== TECHNOFOOTBALL — WEEK {s['week']}/{SEASON_WEEKS} | {s['name']} ({s['niche']}) ===\n"
        f"Subs: {s['subs']:,}   Cash: ${s['cash']:,}   Energy: {s['energy']}/100\n"
        f"Watch-hrs: {s['watch']}   Hype: {s['hype']}/100   Sponsors: {s['sponsors']}   "
        f"Burnout: {s['burnout']}   Rival hype: {s['rival_hype']}\n"
    )


def niche_mod(niche: str, action: str) -> dict:
    """Small niche bias so the same action is not identical every run."""
    table = {
        "fps": {"1": {"subs": 4, "hype": 1}, "2": {"subs": 6}, "3": {"hype": 2}},
        "justchatting": {"1": {"cash": 15}, "3": {"subs": 8, "hype": 3}, "4": {"energy": 4}},
        "tech": {"2": {"cash": 10, "subs": 4}, "3": {"cash": -10, "sponsors": 0}, "1": {"watch": 20}},
        "variety": {"2": {"hype": 2}, "3": {"subs": 3}},
    }
    return dict(table.get(niche, {}).get(action, {}))


def apply_action(s: dict, key: str) -> str:
    label, base = ACTIONS[key]
    delta = dict(base)
    for k, v in niche_mod(s["niche"], key).items():
        delta[k] = delta.get(k, 0) + v

    note_bits: list[str] = []
    tired = s["energy"] < 30 and key != "4"

    for k, v in delta.items():
        if k == "energy":
            s["energy"] = int(clamp(s["energy"] + v, 0, 100))
        elif k == "hype":
            s["hype"] = int(clamp(s["hype"] + v, 0, 100))
        elif k == "burn":
            s["burnout"] = max(0, s["burnout"] + v)
        else:
            s[k] = max(0, int(s.get(k, 0) + v))

    if tired:
        s["burnout"] += 1
        s["energy"] = int(clamp(s["energy"] - 6, 0, 100))
        note_bits.append("empty-tank grind (+burnout)")

    # Sponsor ladder
    if s["subs"] >= 1200 and s["sponsors"] < 1 and s["hype"] >= 20:
        s["sponsors"] = 1
        s["cash"] += 300
        note_bits.append("first brand deal +$300")
    elif s["subs"] >= 4500 and s["sponsors"] < 2 and s["hype"] >= 35:
        s["sponsors"] = 2
        s["cash"] += 900
        note_bits.append("mid-tier stack +$900")
    elif s["subs"] >= 12000 and s["sponsors"] < 3 and s["hype"] >= 50:
        s["sponsors"] = 3
        s["cash"] += 2000
        note_bits.append("marquee partner +$2000")

    extra = (" " + "; ".join(note_bits) + ".") if note_bits else ""
    return f"You: {label}.{extra}"


def algo_roll(s: dict) -> str:
    """Weekly platform swing: skill/hype matter more than raw coin-flip variance."""
    # Rival drifts, but not as a runaway snowball.
    s["rival_hype"] = int(clamp(s["rival_hype"] + random.randint(-3, 5), 0, 100))
    rival_gap = s["rival_hype"] - s["hype"]

    roll = random.random()
    # Good play (hype + sponsors) buys blessing odds; rivals tax it lightly.
    bless_chance = clamp(0.08 + s["hype"] / 280 + s["sponsors"] * 0.015 - max(0, rival_gap) / 600, 0.05, 0.28)
    # Doom exists, but sponsors and rest-driven low burnout soften the floor.
    doom_chance = clamp(
        0.11 + max(0, rival_gap) / 420 + s["burnout"] * 0.015 - s["sponsors"] * 0.025,
        0.05,
        0.18,
    )

    if roll < bless_chance:
        hit = int(28 + s["subs"] * 0.035 + s["hype"] * 0.75)
        s["subs"] += hit
        s["hype"] = int(clamp(s["hype"] + 8, 0, 100))
        s["cash"] += 35 + s["sponsors"] * 15
        return f"Algo blessing: clip detonates (+{hit} subs, cash bump)."

    if roll > 1.0 - doom_chance:
        # Soft landing: percentage haircut with a hard floor, not a season-ender.
        loss = int(6 + s["subs"] * 0.008 + max(0, rival_gap) * 0.1)
        floor = 60 + s["sponsors"] * 25
        s["subs"] = max(floor, s["subs"] - loss)
        s["hype"] = int(clamp(s["hype"] - 4, 0, 100))
        return f"Reach dips / rival ate the feed (-{loss} subs)."

    bonus = int(5 + s["hype"] * 0.4 + s["sponsors"] * 4)
    s["subs"] += bonus
    return f"Steady distribution (+{bonus} subs). Rival hype {s['rival_hype']}."


def weekly_costs(s: dict) -> str:
    rent = 100 + s["sponsors"] * 35 + s["week"] * 2
    s["cash"] -= rent
    passive = s["sponsors"] * 75 + s["subs"] // 45 + s["watch"] // 80
    s["cash"] += passive
    # Soft energy recovery if you were not already resting this week is none;
    # natural seep:
    if s["energy"] < 100:
        s["energy"] = int(clamp(s["energy"] + 2, 0, 100))
    return f"Bills -${rent}, creator income +${passive}."


def fail_check(s: dict) -> str | None:
    if s["cash"] < 0:
        return "BANKRUPT — rent cleared the account. Season over."
    if s["burnout"] >= 4 and s["energy"] <= 15:
        return "BURNOUT — you went dark. Season over."
    if s["subs"] < 40 and s["week"] > 3:
        return "CHANNEL COLLAPSED — audience gone. Season over."
    return None


def win_check(s: dict) -> str | None:
    if s["week"] > SEASON_WEEKS:
        grade = "Cult"
        if s["subs"] >= 10000 and s["cash"] >= 2000:
            grade = "Breakout"
        elif s["subs"] >= 4000:
            grade = "Working creator"
        elif s["cash"] < 200:
            grade = "Scraping by"
        return (
            f"SEASON CLEAR ({grade}) — {s['subs']:,} subs, ${s['cash']:,}, "
            f"{s['sponsors']} sponsors, burnout={s['burnout']}, rival hype={s['rival_hype']}."
        )
    return None


def prompt_choice() -> str:
    print("Actions:")
    for k, (label, _) in ACTIONS.items():
        print(f"  {k}) {label}")
    print("  s) Save and quit")
    print("  q) Quit without saving")
    while True:
        raw = input("> ").strip().lower()
        if raw in ACTIONS or raw in {"q", "s"}:
            return raw
        print("Pick 1-4, s, or q.")


def boot() -> dict:
    print("TECHNOFOOTBALL — creator career mogul (text prototype v2.1)\n")
    existing = load_game()
    if existing:
        ans = input(f"Resume {existing.get('name', 'save')} at week {existing.get('week')}? [Y/n] ").strip().lower()
        if ans in {"", "y", "yes"}:
            return existing
        clear_save()

    name = input("Creator name: ").strip() or "Anon"
    niche = input("Niche (fps / justchatting / tech / variety) [variety]: ").strip().lower()
    if niche not in {"fps", "justchatting", "tech", "variety"}:
        niche = "variety"
    return new_game(name, niche)


def main() -> int:
    random.seed()
    s = boot()

    while True:
        print(status(s))
        dead = fail_check(s)
        if dead:
            print(dead)
            clear_save()
            return 1
        won = win_check(s)
        if won:
            print(won)
            clear_save()
            return 0

        choice = prompt_choice()
        if choice == "q":
            print("Quit — save left untouched.")
            return 0
        if choice == "s":
            save_game(s)
            print(f"Saved to {SAVE_PATH.name}.")
            return 0

        line = apply_action(s, choice)
        algo = algo_roll(s)
        bills = weekly_costs(s)
        print(line)
        print(algo)
        print(bills)
        s["history"].append({"week": s["week"], "action": choice, "algo": algo})
        s["week"] += 1
        save_game(s)  # autosave each week


if __name__ == "__main__":
    sys.exit(main())
