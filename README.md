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
│   │  ❤️ HP: 20  │◄────────────►│  ❤️ HP: 20  │             │
│   │  🛡️ RES: 0  │              │  🛡️ RES: 0  │             │
│   │  💎 MANA: 25│              │  💎 MANA: 25│             │
│   └─────────────┘              └─────────────┘             │
│                                                             │
│   Available Spells:                                         │
│   🔥 Ignis    - Fire damage, may burn                      │
│   ❄️ Glacies  - Ice damage, may freeze                     │
│   ⚡ Fulmen   - Lightning damage, may paralyze             │
│   🛡️ Fortitudo - Boost resistance                          │
│   💚 Curatio  - Restore HP                                  │
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
| `quit` | Exit the game |

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
| **Praesidium** 🛡️ | +5 Resistance | 4 |

### Healing Spells
| Spell | Healing | Mana |
|-------|---------|------|
| **Curatio** 💚 | +4 HP | 3 |
| **Sanatio** 💚 | +8 HP | 6 |

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
│   ├── magebotcli.py    # Main CLI game
│   └── README.md        # Console documentation
├── discord/
│   └── readme.md        # Discord bot (upcoming)
└── README.md            # This file
```

---

## 🛠️ Development

**Contributors:** ZIOS Team

**License:** MIT

---

## 📜 Changelog

| Date | Version | Changes |
|------|---------|---------|
| 2025-12-10 | 1.1.7 | Balanced Glacies spell |
| 2025-12-10 | 1.1.6 | Added spell effects (freeze, paralyze, burn) |
| 2025-12-10 | 1.1.4 | AI improvements, colored UI |
| 2025-09-24 | 0.1.0 | Project creation |

---

*May your spells find their mark. 🧙‍♂️*
