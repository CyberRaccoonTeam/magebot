# 🧙 MageBot

> *A magical duel game where you face an AI opponent using spells inspired by the wizarding world.*

MageBot is a turn-based magical duel game. Face an intelligent opponent that uses Minimax AI to counter your every move. Manage your HP, mana, and resistance while casting devastating spells.

---

## 🎮 Game Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      THE DUEL                               │
│                                                             │
│   ┌─────────────┐              ┌─────────────┐             │
│   │   PLAYER    │              │   MAGEBOT   │             │
│   │             │    ⚡⚔️⚡    │             │             │
│   │  ❤️ HP: 10  │◄────────────►│  ❤️ HP: 10  │             │
│   │  🛡️ RES: 0  │              │  🛡️ RES: 0  │             │
│   │  💎 MANA: 15│              │  💎 MANA: 15│             │
│   └─────────────┘              └─────────────┘             │
│                                                             │
│   Available Spells:                                         │
│   🔥 Ignis    - Fire damage, may burn                      │
│   ❄️ Glacies  - Ice damage, may freeze                     │
│   ⚡ Fulmen   - Lightning damage, may paralyze             │
│   🛡️ Fortitudo - Boost resistance                          │
│   💚 Vitae    - Restore HP                                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 📦 Versions

| Version | Status | Description |
|---------|--------|-------------|
| **Console** | ✅ Complete | Full-featured CLI duel experience |
| **Discord** | 🚧 Upcoming | Bot integration for Discord servers |
| **Browser** | 📋 Planned | Web version with 2D graphics |

---

## ⚡ Quick Start

### Console Version (Recommended)

```bash
# Clone the repository
git clone https://github.com/TheKeepersTeam/magebot.git
cd magebot

# Install dependencies
pip install colorama

# Run the game
python console/magebotcli.py
```

### In-Game Commands

| Command | Description |
|---------|-------------|
| `start_duel` | Begin a new duel against the AI |
| `help` | Show available commands |
| `about` | Game information |
| `quit` / `exit` / `q` | Exit the game (also works during duels) |

### Duel Commands

| Command | Description |
|---------|-------------|
| **Hotkeys** `1-9` | Cast spells instantly (e.g., `1`=Ignis, `2`=Glacies) |
| **Shortcuts** `i,g,f,s,p,t,v,h,a` | Single-letter spell casting |
| **Aliases** `fire`, `ice`, `light`, etc. | Common English names |
| **Spell names** (e.g., `Ignis`, `Glacies`) | Full Latin names (case-insensitive) |
| `quit` / `exit` / `q` | Flee the duel and return to main menu |

**v1.4.0+ Input Methods:** Cast spells four ways - hotkeys (fastest), shortcuts, aliases, or exact names. The game resolves input in priority order: exact match → aliases → shortcuts → hotkeys → fuzzy match.

---

## 🎯 Spell System

### Attack Spells
| Spell | Damage | Mana | Effect | Chance |
|-------|--------|------|--------|--------|
| **Ignis** 🔥 | 3 | 3 | Burn (2 turns) | 60% |
| **Glacies** ❄️ | 4 | 2 | Freeze (1 turn) | 30% |
| **Fulmen** ⚡ | 2 | 2 | Paralyze (1 turn) | 40% |

### Defense Spells
| Spell | Effect | Mana |
|-------|--------|------|
| **Fortitudo** 🛡️ | +3 Resistance | 2 |
| **Praesidium** 🛡️ | +2 Resistance | 1 |
| **Tutela** 🛡️ | +1 Resistance | 1 |

### Healing Spells
| Spell | Healing | Mana |
|-------|---------|------|
| **Vitalis** 💚 | +6 HP | 4 |
| **Vitae** 💚 | +4 HP | 3 |
| **Sanare** 💚 | +2 HP | 1 |

---

## 🤖 AI Opponent

MageBot uses a **Minimax algorithm** with heuristic evaluation:
- Evaluates HP, resistance, and mana states
- Considers active effects (burn, freeze, paralyze)
- Makes strategic decisions about attack vs defense vs healing

---

## 📁 Project Structure

```
magebot/
├── console/
│   ├── magebotcli.py          # Main CLI game
│   ├── config/
│   │   ├── __init__.py        # Config package init
│   │   └── config.py          # Centralized game configuration
│   └── README.md              # Console documentation
├── discord/
│   └── readme.md              # Discord bot (upcoming)
├── requirements.txt
├── LICENSE
└── README.md                  # This file
```

---

## 🛠️ Development

**Contributors:** ZIOS Team

**License:** MIT

---

## 📜 Changelog

| Date | Version | Changes |
|------|---------|---------|
| **2026-03-17** | **1.4.0** | **⚡ Multiple spell input methods - Added hotkeys (1-9), shortcuts (single letters), and aliases (common names). New `resolve_spell()` function with priority-based resolution. Updated UI shows numbered spell list for faster, more intuitive casting.** |
| **2026-03-17** | **1.3.0** | **🎯 Configuration optimization - Centralized all game constants into `config/config.py`. Moved spell definitions, duel stats, AI parameters, and UI settings. Improved code maintainability and balance tuning.** |
| **2026-03-16** | **1.2.0** | **✨ Input validation overhaul - case-insensitive spells, quit command, typo suggestions** |
| **2026-03-16** | **1.1.8** | **🔧 Critical fixes - requirements.txt, MIT LICENSE, documentation accuracy** |
| 2025-12-10 | 1.1.7 | Balanced Glacies spell |
| 2025-12-10 | 1.1.6 | Added spell effects (freeze, paralyze, burn) |
| 2025-12-10 | 1.1.4 | AI improvements, colored UI |
| 2025-09-24 | 0.1.0 | Project creation |

---

*May your spells find their mark. 🧙‍♂️*
