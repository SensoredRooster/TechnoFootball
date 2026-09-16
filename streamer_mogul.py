"""Streamer Mogul — tiny text career sim (Football Mogul energy, creator life)."""

from __future__ import annotations

import random
import sys


ACTIONS = {
    "1": ("Grind a longform stream", {"energy": -18, "cash": 40, "subs": 8, "watch": 120, "hype": 2}),
    "2": ("Ship short-form clips", {"energy": -10, "cash": 15, "subs": 20, "watch": 40, "hype": 6}),
    "3": ("Collab / networking", {"energy": -12, "cash": -20, "subs": 25, "watch": 60, "hype": 10}),
    "4": ("Rest + admin", {"energy": 28, "cash": -10, "subs": 0, "watch": 0, "hype": -3}),
}


def clamp(n: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, n))


def new_save() -> dict:
    return {
        "week": 1,
        "name": "",
        "niche": "variety",
        "subs": 120,
        "cash": 400,
        "energy": 80,
        "watch": 0,  # hours this season
        "hype": 5,  # 0-100 algo luck meter
        "sponsors": 0,
        "burnout": 0,
    }


def status(s: dict) -> str:
    return (
        f"\n=== WEEK {s['week']} | {s['name']} ({s['niche']}) ===\n"
        f"Subs: {s['subs']:,}   Cash: ${s['cash']:,}   Energy: {s['energy']}/100\n"
        f"Season watch-hrs: {s['watch']}   Hype: {s['hype']}/100   Sponsors: {s['sponsors']}\n"
    )


def algo_roll(s: dict) -> str:
    """One weekly platform roll — Mogul-style randomness on top of your plan."""
    roll = random.random()
    luck = clamp(0.35 + s["hype"] / 200 + s["sponsors"] * 0.05, 0.2, 0.85)
    if roll < 0.12:
        hit = int(40 + s["subs"] * 0.08)
        s["subs"] += hit
        s["hype"] = int(clamp(s["hype"] + 12, 0, 100))
        return f"Algo blessing: a clip popped (+{hit} subs)."
    if roll > luck:
        loss = int(10 + s["subs"] * 0.02)
        s["subs"] = max(0, s["subs"] - loss)
        s["hype"] = int(clamp(s["hype"] - 8, 0, 100))
        return f"Shadowban week: reach tanked (-{loss} subs)."
    bonus = int(5 + s["hype"] * 0.4)
    s["subs"] += bonus
    return f"Steady week on the For You page (+{bonus} subs)."


def apply_action(s: dict, key: str) -> str:
    label, delta = ACTIONS[key]
    before = (s["energy"], s["cash"], s["subs"])
    for k, v in delta.items():
        if k == "energy":
            s["energy"] = int(clamp(s["energy"] + v, 0, 100))
        elif k == "hype":
            s["hype"] = int(clamp(s["hype"] + v, 0, 100))
        else:
            s[k] = max(0, s[k] + v)
    # Passive-low work hurts more.
    if before[0] < 25 and key != "4":
        s["burnout"] += 1
        s["energy"] = int(clamp(s["energy"] - 8, 0, 100))
        note = " You pushed through empty — burnout ticked up."
    else:
        note = ""
    # Soft sponsor unlock.
    if s["subs"] >= 1000 and s["sponsors"] == 0 and s["hype"] >= 25:
        s["sponsors"] = 1
        s["cash"] += 250
        note += " First brand deal lands (+$250)."
    elif s["subs"] >= 5000 and s["sponsors"] == 1 and s["hype"] >= 40:
        s["sponsors"] = 2
        s["cash"] += 800
        note += " Mid-tier sponsor stack (+$800)."
    return f"You: {label}.{note}"


def weekly_costs(s: dict) -> str:
    rent = 120 + s["sponsors"] * 40
    s["cash"] -= rent
    passive = s["sponsors"] * 60 + s["subs"] // 50
    s["cash"] += passive
    return f"Bills -${rent}, creator income +${passive}."


def fail_check(s: dict) -> str | None:
    if s["cash"] < 0:
        return "BANKRUPT — you can't float rent. Season over."
    if s["energy"] <= 0 and s["burnout"] >= 3:
        return "BURNOUT — you ghosted the audience for a month. Season over."
    if s["subs"] <= 0:
        return "CHANNEL DEAD — zero subs. Season over."
    return None


def win_check(s: dict) -> str | None:
    if s["week"] > 12:
        return (
            f"SEASON CLEAR — 12 weeks in. Ending: {s['subs']:,} subs, ${s['cash']:,}, "
            f"{s['sponsors']} sponsors, burnout marks={s['burnout']}."
        )
    return None


def prompt_choice() -> str:
    print("Actions:")
    for k, (label, _) in ACTIONS.items():
        print(f"  {k}) {label}")
    print("  q) Quit")
    while True:
        raw = input("> ").strip().lower()
        if raw in ACTIONS or raw == "q":
            return raw
        print("Pick 1-4 or q.")


def main() -> int:
    random.seed()
    s = new_save()
    print("STREAMER MOGUL — text prototype")
    print("Build a career one week at a time. Don't go broke. Don't burn out.\n")
    s["name"] = input("Creator name: ").strip() or "Anon"
    niche = input("Niche (fps / justchatting / tech / variety) [variety]: ").strip().lower()
    s["niche"] = niche if niche in {"fps", "justchatting", "tech", "variety"} else "variety"

    while True:
        print(status(s))
        dead = fail_check(s)
        if dead:
            print(dead)
            return 1
        won = win_check(s)
        if won:
            print(won)
            return 0

        choice = prompt_choice()
        if choice == "q":
            print("Paused. Your save lived only in this run — restart to try again.")
            return 0

        print(apply_action(s, choice))
        print(algo_roll(s))
        print(weekly_costs(s))
        s["week"] += 1


if __name__ == "__main__":
    sys.exit(main())
