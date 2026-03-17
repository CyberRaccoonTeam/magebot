# MageBot Console Configuration
# Centralized game settings and constants

# === Game Constants ===
MAX_HP = 20
MAX_MANA = 25
DEFAULT_MANA_REGEN = 2
BURN_DAMAGE = 1

# === Duel Default Stats ===
DUEL_CONFIG = {
    "player": {
        "hp": 10,
        "resistance": 5,
        "mana": 15,
        "max_hp": 20,
        "max_mana": 25
    },
    "magebot": {
        "hp": 10,
        "resistance": 5,
        "mana": 15,
        "max_hp": 20,
        "max_mana": 25
    }
}

# === Spell Definitions ===
ATTACK_SPELLS = {
    "Ignis": {
        "description": "Deals fire damage and may burn the enemy.",
        "damage": 3,
        "mana_cost": 3,
        "effect": "burn",
        "duration": 2,
        "chance": 0.6
    },
    "Glacies": {
        "description": "Deals ice damage and may freeze the enemy.",
        "damage": 4,
        "mana_cost": 2,
        "effect": "freeze",
        "duration": 1,
        "chance": 0.3
    },
    "Fulmen": {
        "description": "Deals lightning damage and may paralyze the enemy.",
        "damage": 2,
        "mana_cost": 2,
        "effect": "paralyze",
        "duration": 1,
        "chance": 0.4
    },
}

RESISTANCE_SPELLS = {
    "Fortitudo": {
        "description": "Increases the caster's magical resistance.",
        "resistance_boost": 3,
        "mana_cost": 2
    },
    "Praesidium": {
        "description": "Temporary magical shield.",
        "resistance_boost": 2,
        "mana_cost": 1
    },
    "Tutela": {
        "description": "Light magical protection.",
        "resistance_boost": 1,
        "mana_cost": 1
    },
}

HEALING_SPELLS = {
    "Vitalis": {
        "description": "Heals the caster's wounds.",
        "healing": 6,
        "mana_cost": 4
    },
    "Vitae": {
        "description": "Restores some of the caster's health.",
        "healing": 4,
        "mana_cost": 3
    },
    "Sanare": {
        "description": "Light healing.",
        "healing": 2,
        "mana_cost": 1
    },
}

# === AI Configuration ===
MINIMAX_DEPTH = 2
EVALUATION_WEIGHTS = {
    "hp": 1.0,
    "resistance": 0.5,
    "mana": 0.4
}

# === UI Configuration ===
VERSION = "1.3.0"
BANNER_WIDTH = 60
MENU_WIDTH = 40
QUIT_COMMANDS = ['quit', 'exit', 'q']

# === Effect Configuration ===
EFFECT_NAMES = {
    "frozen": "frozen",
    "paralyzed": "paralyzed",
    "burned": "burned"
}

# === Match Configuration ===
SPELL_MATCH_CUTOFF = 0.6
SPELL_MATCH_LIMIT = 3
