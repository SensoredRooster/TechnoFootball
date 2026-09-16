# Streamer Mogul

Text-based **streamer / content-creator career sim** in the spirit of Football Mogul / Baseball Mogul: weekly decisions, a few core stats, and an algo roll that can make or break the week.

## Run

```bash
python streamer_mogul.py
```

No dependencies beyond Python 3.10+.

## Prototype loop

Each week you pick **one** action (max four):

1. Grind a longform stream
2. Ship short-form clips
3. Collab / networking
4. Rest + admin

Then the game resolves:

- action deltas (subs, cash, energy, hype)
- one **algo roll** (blessing / steady / shadowban)
- rent + passive creator income

### Fail states

- **Bankrupt** — cash below $0
- **Burnout** — energy empty with repeated grind marks
- **Channel dead** — 0 subs

### Win (prototype)

Survive **12 weeks** and see your ending sheet.

## Why this shape

Mogul games are spreadsheet seasons with personality. This MVP keeps that: tiny action set, readable numbers, one random platform swing — not a chat RPG.

## Status

Playable CLI prototype. Next ideas: save files, rival creators, platform contracts, multi-week content calendar.
