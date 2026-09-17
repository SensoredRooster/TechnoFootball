# TechnoFootball - README for absolute beginners

**Yes, it is playable right now — and it has a Football Mogul-style desktop UI.**

## Play the GUI (recommended)

1. Install Python 3.10+ from https://www.python.org/downloads/ (tick Add to PATH).
2. Open a terminal in this folder and install the UI toolkit once:

`powershell
pip install -r requirements.txt
`

3. Double-click **
un_gui.bat** or run:

`powershell
python mogul_app.py
`

You get a dark front-office window: sidebar (Office / Week Plan / Ledger / Rival / Season), stat cards, clickable weekly plays, week report, save/resume. Same career rules as the old text build — just not stuck in a terminal.

---

## Optional: classic text mode

`powershell
python techno_football.py
`

---

## What is this game?

Think **Football Mogul / Baseball Mogul**, but instead of an NFL team you run a **streamer / content creator**.

You do **not** play matches with graphics. You:

1. Look at your stats (subs, cash, energy, …)
2. Pick **one** action for the week
3. The game rolls the “algo” (good week / normal week / bad week)
4. Rent and income resolve
5. Next week

Survive **12 weeks** without going broke or burning out.

The name **TechnoFootball** is the project name. It is **not** an NFL video game. “Football” here means *Mogul-style season management*.

---

## What you need (checklist)

| Need | Notes |
|---|---|
| A computer | Windows, Mac, or Linux |
| **Python 3.10 or newer** | Free. The game uses only the Python standard library (no `pip install` list) |
| This repo | Download ZIP **or** `git clone` |
| A terminal (optional) | Only required for text mode or installing deps |

You do **not** need:

- Node, Unity, Steam, a GPU, or an account to play offline
- To know how to code (you only run one command)

---

## Step A — Install Python (if you don’t have it)

### Windows

1. Open https://www.python.org/downloads/
2. Download the latest Python 3
3. Run the installer
4. **Important:** check **“Add python.exe to PATH”**
5. Click Install
6. Close and reopen your terminal
7. Test:

```powershell
python --version
```

You want something like `Python 3.12.x` or `Python 3.14.x`.

If `python` is not found, try:

```powershell
py --version
```

### Mac

```bash
python3 --version
```

If missing, install from https://www.python.org/downloads/ or `brew install python`.

### Linux

```bash
python3 --version
```

Install via your package manager if needed (`sudo apt install python3`, etc.).

---

## Step B — Get the game files

### Option 1 — Download ZIP (easiest)

1. Open https://github.com/SensoredRooster/TechnoFootball
2. Click the green **Code** button
3. Click **Download ZIP**
4. Unzip it somewhere simple, for example:
   - `C:\Users\YOURNAME\Downloads\TechnoFootball-main`
5. Remember that folder path

### Option 2 — Git clone

```powershell
cd $HOME\source\repos
git clone https://github.com/SensoredRooster/TechnoFootball.git
cd TechnoFootball
```

---

## Step C — Run the game

1. Open a terminal
2. `cd` into the folder that contains `techno_football.py`

Windows example:

```powershell
cd C:\Users\YOURNAME\Downloads\TechnoFootball-main
python techno_football.py
```

If `python` fails:

```powershell
py techno_football.py
```

Mac / Linux:

```bash
cd ~/Downloads/TechnoFootball-main
python3 techno_football.py
```

You should see a title like **TECHNOFOOTBALL** and a prompt for your creator name.

---

## First launch — what to type

1. **Creator name** — anything (`Neo`, `Sensored`, your handle)
2. **Niche** — one of:
   - `fps`
   - `justchatting`
   - `tech`
   - `variety` (default if you just press Enter)
3. Each week, type **`1`**, **`2`**, **`3`**, or **`4`** then Enter
4. Or:
   - **`s`** = save and quit
   - **`q`** = quit without saving this moment (autosave may already have last week)

If a save exists, it asks **Resume … ?**  
- Enter / `Y` = continue  
- `n` = start fresh

---

## How a week works (the whole game)

Every week is the same pipeline:

```
show stats
   → you pick ONE action
   → action changes your numbers
   → algo roll (good / steady / bad)
   → bills + passive income
   → autosave
   → week += 1
```

There is no combat screen. The “drama” is the spreadsheet + the random platform roll.

---

## Stats explained (dummy edition)

| Stat | Plain English | Why you care |
|---|---|---|
| **Week** | How far you are in the 12-week season | Reach week 13 = you cleared the season |
| **Subs** | Audience size | Growth goal; too low for too long can kill the channel |
| **Cash** | Money | Hits below $0 → **BANKRUPT** (season over) |
| **Energy** | Your body/brain meter (0–100) | Grinding while empty raises burnout |
| **Watch-hrs** | How much watch time you banked this season | Helps passive income a bit |
| **Hype** | Algo / buzz meter (0–100) | Higher hype = better odds of a good algo week |
| **Sponsors** | Brand deals unlocked by growth + hype | More cash over time, but rent scales up |
| **Burnout** | Stress marks | High burnout + low energy → **BURNOUT** ending |
| **Rival hype** | Competing creators eating the feed | When rivals are hotter, bad algo weeks get meaner |

---

## Actions (what each button means)

Type the number shown in the menu:

| Key | Action | Usually good for | Tradeoff |
|---|---|---|---|
| **1** | Grind a longform stream | **Cash** + watch hours; safer lane | Costs energy; slow sub growth |
| **2** | Ship short-form clips | **Subs / growth** | Still costs energy; more variance with the algo |
| **3** | Collab / networking | **Hype** + solid subs | Not a money printer by itself |
| **4** | Rest + admin | **Energy** + lower burnout | Mild cash drain; little growth |

### Simple strategy cheat-sheet

- **About to go broke?** Prefer **1** (grind) or mix grind with rest.
- **Want growth?** Prefer **2** (clips), sometimes **3** (collab).
- **Energy low / burnout rising?** Hit **4** (rest) before you brick the season.
- **Pure grind every week** often survives but stalls growth (safe, not flashy).
- **Pure clips** can boom or sting — higher ceiling, more risk.

---

## Algo roll (the “football bounce”)

After your action, the game secretly rolls the platform week:

- **Blessing** — clip pops, bigger sub jump
- **Steady** — modest growth
- **Dip** — reach drops / rival ate the feed (hurts, but should not usually delete your whole channel in one roll)

Your **hype**, **sponsors**, and **rival hype** nudge those odds.  
This is intentional Mogul chaos: plan well, still respect variance.

---

## How you win

Survive through **week 12**. Then you get an ending grade based on how strong you finished (examples: scraping by → working creator → breakout → cult).

You do **not** need a perfect run. Living is winning the prototype.

---

## How you lose (season over)

| Ending | Meaning |
|---|---|
| **BANKRUPT** | Cash went below $0 after bills |
| **BURNOUT** | You kept grinding empty and stress stacked too high |
| **CHANNEL COLLAPSED** | Audience cratered too hard |

After a loss or a clear season, the save is cleared so the next launch is a new run.

---

## Saving and loading

| Behavior | Detail |
|---|---|
| Autosave | After each resolved week → writes `save.json` next to the script |
| `s` | Save and quit immediately |
| `q` | Quit; does not write a brand-new save at that second |
| Next launch | Asks if you want to resume |

**Dummy tip:** `save.json` is your career slot. Delete that file manually if you want a forced fresh start while a mid-season save exists.

---

## Example first 3 minutes

```text
python techno_football.py
Creator name: Neo
Niche: variety

(look at stats)
> 1          ← grind for cash
(read algo + bills)
> 2          ← clips for growth
> 4          ← rest if energy dipped
> s          ← save and quit for now
```

Later:

```text
python techno_football.py
Resume Neo at week 4? [Y/n] Y
```

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `python` not found | Reinstall Python with PATH checked, or use `py` / `python3` |
| `No such file: techno_football.py` | `cd` into the folder that actually contains the file (`dir` / `ls` to confirm) |
| Game looks “stuck” | It’s waiting for input. Type `1`–`4`, `s`, or `q`, then Enter |
| Want a full reset | Delete `save.json`, run again |
| Weird characters in the terminal | Use Windows Terminal or a modern console; still fully playable |
| I’m not a coder | You don’t need to be. Install Python → open folder → run the one command |

---

## Files in this repo (only what matters)

| File | What it is |
|---|---|
| `techno_football.py` | The whole game |
| `README.md` | This guide |
| `.gitignore` | Tells git to ignore junk like `save.json` |
| `save.json` | Created when **you** play (not shipped) |

Balance knobs for tinkerers live inside `techno_football.py`:

- `ACTIONS` — what each weekly choice does
- `algo_roll` — blessing / steady / dip odds
- `weekly_costs` — rent + passive income

---

## Project status

| Item | Status |
|---|---|
| Playable CLI prototype | **Yes** |
| Graphics / Steam build | No (text only) |
| Online servers | No |
| Multiplayer | No |
| Season length | 12 weeks |

Former repo name: `StreamerMogul` (GitHub redirects after rename to **TechnoFootball**).

---

## One-sentence summary

**Install Python, open this folder, run `python techno_football.py`, pick a weekly action for 12 weeks, don’t go broke or burn out.**
