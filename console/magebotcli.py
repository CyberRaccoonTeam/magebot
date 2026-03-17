# MageBot CLI - Console version of MageBot with Rich UI
# Notes: When a duel starts, the system activates MageBot AI since CLI mode is against AI.

# Import necessary modules
import asyncio
import random
from difflib import get_close_matches
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.layout import Layout
from rich.text import Text
from rich.live import Live
from rich.style import Style

# Import centralized configuration
from config.config import (
    MAX_HP, MAX_MANA, DEFAULT_MANA_REGEN, BURN_DAMAGE,
    DUEL_CONFIG, ATTACK_SPELLS, RESISTANCE_SPELLS, HEALING_SPELLS,
    MINIMAX_DEPTH, EVALUATION_WEIGHTS, VERSION, BANNER_WIDTH, MENU_WIDTH,
    QUIT_COMMANDS, SPELL_MATCH_CUTOFF, SPELL_MATCH_LIMIT, SPELL_ALIASES, SPELL_HOTKEYS
)

# Initialize Rich Console
console = Console()

# Merge all spells into a single dictionary (imported from config)
all_spells = {}
all_spells.update(ATTACK_SPELLS)
all_spells.update(RESISTANCE_SPELLS)
all_spells.update(HEALING_SPELLS)


def create_banner():
    """Create ASCII art banner with Rich styling."""
    banner_text = Text()
    banner_text.append("""
███╗   ███╗ █████╗  ██████╗ ███████╗    ██████╗  ██████╗ ████████╗
████╗ ████║██╔══██╗██╔════╝ ██╔════╝    ██╔══██╗██╔═══██╗╚══██╔══╝
██╔████╔██║███████║██║  ███╗█████╗      ██████╔╝██║   ██║   ██║   
██║╚██╔╝██║██╔══██║██║   ██║██╔══╝      ██╔══██╗██║   ██║   ██║   
██║ ╚═╝ ██║██║  ██║╚██████╔╝███████╗    ██████╔╝╚██████╔╝   ██║   
╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝    ╚═════╝  ╚═════╝    ╚═╝   
""", style="bold cyan")
    return Panel(banner_text, title="[bold cyan]MageBot CLI[/bold cyan]", subtitle=f"[cyan]v{VERSION}[/cyan]", border_style="cyan")


def create_duel_state_panel(player_hp, player_res, player_mana, magebot_hp, magebot_res, magebot_mana, player_effects=None, magebot_effects=None):
    """Create a beautiful duel state display using Rich Table."""
    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column("Player", style="green", justify="center")
    table.add_column("VS", style="yellow bold", justify="center")
    table.add_column("MageBot", style="magenta", justify="center")
    
    # Player effects
    player_effect_str = ""
    if player_effects:
        active = [k for k, v in player_effects.items() if v > 0]
        if active:
            player_effect_str = f"\n[yellow]⚡ {', '.join(active)}[/yellow]"
    
    # MageBot effects
    magebot_effect_str = ""
    if magebot_effects:
        active = [k for k, v in magebot_effects.items() if v > 0]
        if active:
            magebot_effect_str = f"\n[yellow]⚡ {', '.join(active)}[/yellow]"
    
    table.add_row(
        f"[bold green]❤️  HP: {player_hp}/{DUEL_CONFIG['player']['max_hp']}[/bold green]\n"
        f"[bold blue]🛡️  RES: {player_res}[/bold blue]\n"
        f"[bold cyan]💎 MANA: {player_mana}/{DUEL_CONFIG['player']['max_mana']}[/bold cyan]"
        f"{player_effect_str}",
        "[bold yellow]⚔️[/bold yellow]",
        f"[bold magenta]❤️  HP: {magebot_hp}/{DUEL_CONFIG['magebot']['max_hp']}[/bold magenta]\n"
        f"[bold blue]🛡️  RES: {magebot_res}[/bold blue]\n"
        f"[bold cyan]💎 MANA: {magebot_mana}/{DUEL_CONFIG['magebot']['max_mana']}[/bold cyan]"
        f"{magebot_effect_str}"
    )
    
    return Panel(table, title="[bold yellow]Duel State[/bold yellow]", border_style="yellow")


def create_spells_table():
    """Create a beautiful spell selection table with hotkeys."""
    table = Table(show_header=True, header_style="bold cyan", border_style="cyan")
    table.add_column("#", style="bold yellow", justify="center")
    table.add_column("Spell", style="bold white")
    table.add_column("Type", justify="center")
    table.add_column("Effect", style="italic")
    table.add_column("Cost", justify="center")
    
    spell_order = [
        ("1", "Ignis", ATTACK_SPELLS, "🔥 Attack"),
        ("2", "Glacies", ATTACK_SPELLS, "🔥 Attack"),
        ("3", "Fulmen", ATTACK_SPELLS, "🔥 Attack"),
        ("4", "Fortitudo", RESISTANCE_SPELLS, "🛡️ Defense"),
        ("5", "Praesidium", RESISTANCE_SPELLS, "🛡️ Defense"),
        ("6", "Tutela", RESISTANCE_SPELLS, "🛡️ Defense"),
        ("7", "Vitalis", HEALING_SPELLS, "💚 Healing"),
        ("8", "Vitae", HEALING_SPELLS, "💚 Healing"),
        ("9", "Sanare", HEALING_SPELLS, "💚 Healing"),
    ]
    
    for hotkey, name, spell_dict, spell_type in spell_order:
        spell = spell_dict[name]
        effect = ""
        cost = ""
        
        if "damage" in spell:
            effect = f"{spell['damage']} dmg"
            if "effect" in spell:
                effect += f" + {spell['effect']} ({int(spell['chance']*100)}%)"
            cost = f"{spell['mana_cost']} 💎"
        elif "healing" in spell:
            effect = f"+{spell['healing']} HP"
            cost = f"{spell['mana_cost']} 💎"
        elif "resistance_boost" in spell:
            effect = f"+{spell['resistance_boost']} RES"
            cost = f"{spell['mana_cost']} 💎"
        
        # Get first alias for display
        alias = ""
        for k, v in SPELL_ALIASES.items():
            if v == name:
                alias = f"\n[dim]({k})[/dim]"
                break
        
        table.add_row(hotkey, f"{name}{alias}", spell_type, effect, cost)
    
    return Panel(table, title="[bold cyan]Available Spells[/bold cyan]", subtitle="[dim]Type number, name, or alias (e.g., '1', 'Ignis', 'fire')[/dim]", border_style="cyan")


def create_action_log(message, style="white"):
    """Create a styled action log message."""
    console.print(f"[{style}]>{message}[/{style}]")


# Heuristic evaluation function for Minimax
def evaluate_state(player_hp, player_res, player_mana, magebot_hp, magebot_res, magebot_mana,
                   w_hp=None, w_res=None, w_mana=None):
    if w_hp is None: w_hp = EVALUATION_WEIGHTS["hp"]
    if w_res is None: w_res = EVALUATION_WEIGHTS["resistance"]
    if w_mana is None: w_mana = EVALUATION_WEIGHTS["mana"]
    
    hp_score = (magebot_hp - player_hp) * w_hp
    res_score = (magebot_res - player_res) * w_res
    mana_score = ((magebot_mana - player_mana) / MAX_MANA) * w_mana * MAX_HP
    return hp_score + res_score + mana_score

# Minimax algorithm for MageBot's decision-making
def minimax(player_hp, player_res, player_mana, magebot_hp, magebot_res, magebot_mana, depth, maximizing):
    if player_hp <= 0:
        return 100
    if magebot_hp <= 0:
        return -100
    if depth == 0:
        return evaluate_state(player_hp, player_res, player_mana, magebot_hp, magebot_res, magebot_mana)
    
    if maximizing:
        max_eval = -float('inf')
        for name, spell in all_spells.items():
            cost = spell.get("mana_cost", 0)
            if cost > magebot_mana:
                continue
            if "damage" in spell:
                dmg = max(0, spell["damage"] - player_res)
                eval_score = minimax(player_hp - dmg, 0, player_mana, magebot_hp, magebot_res, magebot_mana - cost, depth-1, False)
            elif "healing" in spell:
                new_hp = min(MAX_HP, magebot_hp + spell["healing"])
                eval_score = minimax(player_hp, player_res, player_mana, new_hp, magebot_res, magebot_mana - cost, depth-1, False)
            elif "resistance_boost" in spell:
                new_res = magebot_res + spell["resistance_boost"]
                eval_score = minimax(player_hp, player_res, player_mana, magebot_hp, new_res, magebot_mana - cost, depth-1, False)
            else:
                eval_score = evaluate_state(player_hp, player_res, player_mana, magebot_hp, magebot_res, magebot_mana)
            max_eval = max(max_eval, eval_score)
        return max_eval
    else:
        min_eval = float('inf')
        for name, spell in all_spells.items():
            cost = spell.get("mana_cost", 0)
            if cost > player_mana:
                continue
            if "damage" in spell:
                dmg = max(0, spell["damage"] - magebot_res)
                eval_score = minimax(player_hp, player_res, player_mana - cost, magebot_hp - dmg, 0, magebot_mana, depth-1, True)
            elif "healing" in spell:
                new_hp = min(MAX_HP, player_hp + spell["healing"])
                eval_score = minimax(new_hp, player_res, player_mana - cost, magebot_hp, magebot_res, magebot_mana, depth-1, True)
            elif "resistance_boost" in spell:
                new_res = player_res + spell["resistance_boost"]
                eval_score = minimax(player_hp, new_res, player_mana - cost, magebot_hp, magebot_res, magebot_mana, depth-1, True)
            else:
                eval_score = evaluate_state(player_hp, player_res, player_mana, magebot_hp, magebot_res, magebot_mana)
            min_eval = min(min_eval, eval_score)
        return min_eval

def magebot_choose_spell(player_hp, player_res, player_mana, magebot_hp, magebot_res, magebot_mana, magebot_max_hp, possible_spells):
    best_score = -float('inf')
    best_spell = None
    filtered_spells = []
    for name in possible_spells:
        spell = all_spells[name]
        if "healing" in spell and magebot_hp >= magebot_max_hp:
            continue
        filtered_spells.append(name)
    if not filtered_spells:
        filtered_spells = possible_spells

    for name in filtered_spells:
        spell = all_spells[name]
        cost = spell.get("mana_cost", 0)
        if cost > magebot_mana:
            continue
        if "damage" in spell:
            dmg = max(0, spell["damage"] - player_res)
            score = minimax(player_hp - dmg, 0, player_mana, magebot_hp, magebot_res, magebot_mana - cost, MINIMAX_DEPTH, False)
        elif "healing" in spell:
            new_hp = min(MAX_HP, magebot_hp + spell["healing"])
            score = minimax(player_hp, player_res, player_mana, new_hp, magebot_res, magebot_mana - cost, MINIMAX_DEPTH, False)
        elif "resistance_boost" in spell:
            new_res = magebot_res + spell["resistance_boost"]
            score = minimax(player_hp, player_res, player_mana, magebot_hp, new_res, magebot_mana - cost, MINIMAX_DEPTH, False)
        else:
            score = evaluate_state(player_hp, player_res, player_mana, magebot_hp, magebot_res, magebot_mana)
        if score > best_score:
            best_score = score
            best_spell = name
    return best_spell

def resolve_spell(user_input):
    """
    Resolve user input to a spell name using priority-based matching.
    Priority: Exact match → Aliases → Hotkeys → Fuzzy match
    Returns: spell name (e.g., "Ignis") or None if no match
    """
    if not user_input:
        return None
    
    user_input = user_input.strip()
    user_input_lower = user_input.lower()
    user_input_title = user_input.title()
    
    # 1. Exact match (case-insensitive)
    if user_input_title in all_spells:
        return user_input_title
    
    # 2. Aliases (common names like "fire", "ice", "heal")
    if user_input_lower in SPELL_ALIASES:
        return SPELL_ALIASES[user_input_lower]
    
    # 3. Hotkeys (numbered 1-9)
    if user_input in SPELL_HOTKEYS:
        return SPELL_HOTKEYS[user_input]
    
    # 4. Fuzzy match (typo correction)
    suggestions = get_close_matches(user_input, all_spells.keys(), n=1, cutoff=SPELL_MATCH_CUTOFF)
    if suggestions:
        return suggestions[0]
    
    return None


async def activate_magebot_ai():
    console.print("[bold magenta]MageBot AI:[/bold magenta] activated.")
    await asyncio.sleep(1)

async def duel_vs_magebot():
    await activate_magebot_ai()
    console.print("[bold yellow]The duel begins![/bold yellow]\n")
    
    player_hp = DUEL_CONFIG["player"]["hp"]
    player_res = DUEL_CONFIG["player"]["resistance"]
    player_mana = DUEL_CONFIG["player"]["mana"]
    player_max_hp = DUEL_CONFIG["player"]["max_hp"]
    player_max_mana = DUEL_CONFIG["player"]["max_mana"]
    
    magebot_hp = DUEL_CONFIG["magebot"]["hp"]
    magebot_res = DUEL_CONFIG["magebot"]["resistance"]
    magebot_mana = DUEL_CONFIG["magebot"]["mana"]
    magebot_max_hp = DUEL_CONFIG["magebot"]["max_hp"]
    magebot_max_mana = DUEL_CONFIG["magebot"]["max_mana"]
    
    player_effects = {"frozen": 0, "paralyzed": 0, "burned": 0}
    magebot_effects = {"frozen": 0, "paralyzed": 0, "burned": 0}

    while player_hp > 0 and magebot_hp > 0:
        # Display duel state
        duel_panel = create_duel_state_panel(
            player_hp, player_res, player_mana,
            magebot_hp, magebot_res, magebot_mana,
            player_effects, magebot_effects
        )
        console.print(duel_panel)
        
        # Display spells
        spells_panel = create_spells_table()
        console.print(spells_panel)
        
        console.print("[bold cyan]=== Your Turn ===[/bold cyan]\n")

        # Apply player effects
        if player_effects["burned"] > 0:
            player_hp -= BURN_DAMAGE
            console.print(f"[red][Burn] You take {BURN_DAMAGE} burn damage![/red]")
            player_effects["burned"] -= 1
        if player_effects["frozen"] > 0 or player_effects["paralyzed"] > 0:
            effect_name = "frozen" if player_effects["frozen"] > 0 else "paralyzed"
            console.print(f"[blue][Effect] You are {effect_name} and skip your turn![/blue]")
            player_effects["frozen"] = max(0, player_effects["frozen"] - 1)
            player_effects["paralyzed"] = max(0, player_effects["paralyzed"] - 1)
        else:
            user_input = console.input("[bold green]Cast spell:[/bold green] ").strip()
            
            if not user_input:
                console.print("[yellow]Please enter a spell number, name, or alias.[/yellow]")
                continue
            
            if user_input.lower() in QUIT_COMMANDS:
                console.print("[yellow]You fled the duel![/yellow]")
                break
            
            spell_name = resolve_spell(user_input)
            
            if spell_name:
                spell = all_spells[spell_name]
                mana_cost = spell.get("mana_cost", 0)
                if player_mana < mana_cost:
                    console.print(f"[red][Error] Not enough mana! Need {mana_cost}, have {player_mana}[/red]")
                else:
                    player_mana -= mana_cost
                    if "damage" in spell:
                        if magebot_res > 0 and spell["damage"] >= magebot_res:
                            console.print("[yellow][Info] Enemy resistance broken! (RES:0)[/yellow]")
                        dmg = max(0, spell["damage"] - magebot_res)
                        magebot_hp -= dmg
                        create_action_log(f"You cast {spell_name}: {dmg} damage to MageBot!", "red")
                        magebot_res = 0
                        if "effect" in spell and random.random() < spell["chance"]:
                            magebot_effects[spell["effect"]] = spell["duration"]
                            console.print(f"[yellow][Effect] MageBot is now {spell['effect']} for {spell['duration']} turn(s)![/yellow]")
                    elif "healing" in spell:
                        player_hp += spell["healing"]
                        if player_hp > player_max_hp:
                            player_hp = player_max_hp
                            console.print("[green][Info] Maximum HP reached![/green]")
                        create_action_log(f"You cast {spell_name}: +{spell['healing']} HP", "green")
                    elif "resistance_boost" in spell:
                        player_res += spell["resistance_boost"]
                        create_action_log(f"You cast {spell_name}: +{spell['resistance_boost']} RES", "cyan")
            else:
                suggestions = get_close_matches(user_input, list(SPELL_ALIASES.keys()) + list(all_spells.keys()), n=3, cutoff=0.4)
                if suggestions:
                    console.print(f"[red]Unknown spell. Did you mean: {', '.join(suggestions)}?[/red]")
                else:
                    console.print(f"[red]Unknown spell. Use numbers (1-9), names (Ignis), or aliases (fire).[/red]")
                continue

        # Player mana regeneration
        if player_mana < player_max_mana:
            player_mana += DEFAULT_MANA_REGEN
            if player_mana > player_max_mana:
                player_mana = player_max_mana
            console.print(f"[blue][Mana] Recovered {DEFAULT_MANA_REGEN} mana ({player_mana}/{player_max_mana})[/blue]")

        if magebot_hp <= 0:
            duel_panel = create_duel_state_panel(
                player_hp, player_res, player_mana,
                magebot_hp, magebot_res, magebot_mana,
                player_effects, magebot_effects
            )
            console.print(duel_panel)
            console.print("[bold green]🎉 Congratulations, you defeated MageBot![/bold green]")
            break

        # MageBot's turn
        await asyncio.sleep(1)
        console.print("[bold magenta]=== MageBot's Turn ===[/bold magenta]\n")

        if magebot_effects["burned"] > 0:
            magebot_hp -= BURN_DAMAGE
            console.print(f"[red][Burn] MageBot takes {BURN_DAMAGE} burn damage![/red]")
            magebot_effects["burned"] -= 1
        if magebot_effects["frozen"] > 0 or magebot_effects["paralyzed"] > 0:
            effect_name = "frozen" if magebot_effects["frozen"] > 0 else "paralyzed"
            console.print(f"[blue][Effect] MageBot is {effect_name} and skips its turn![/blue]")
            magebot_effects["frozen"] = max(0, magebot_effects["frozen"] - 1)
            magebot_effects["paralyzed"] = max(0, magebot_effects["paralyzed"] - 1)
        else:
            magebot_possible_spells = [name for name, s in all_spells.items() if s.get("mana_cost", 0) <= magebot_mana]
            if not magebot_possible_spells:
                console.print("[magenta]MageBot doesn't have enough mana! It passes its turn...[/magenta]")
                magebot_mana += DEFAULT_MANA_REGEN
                if magebot_mana > magebot_max_mana:
                    magebot_mana = magebot_max_mana
                console.print(f"[magenta][Mana] MageBot recovered {DEFAULT_MANA_REGEN} mana ({magebot_mana}/{magebot_max_mana})[/magenta]")
            else:
                magebot_action = magebot_choose_spell(player_hp, player_res, player_mana, magebot_hp, magebot_res, magebot_mana, magebot_max_hp, magebot_possible_spells)
                spell = all_spells[magebot_action]
                mana_cost = spell.get("mana_cost", 0)
                magebot_mana -= mana_cost
                console.print("[magenta][MageBot] MageBot acts deterministically.[/magenta]")
                if "damage" in spell:
                    if player_res > 0 and spell["damage"] >= player_res:
                        console.print("[yellow][Info] Your resistance is broken! (RES:0)[/yellow]")
                    dmg = max(0, spell["damage"] - player_res)
                    player_hp -= dmg
                    create_action_log(f"MageBot cast {magebot_action}: {dmg} damage to you!", "magenta")
                    player_res = 0
                    if "effect" in spell and random.random() < spell["chance"]:
                        player_effects[spell["effect"]] = spell["duration"]
                        console.print(f"[yellow][Effect] You are now {spell['effect']} for {spell['duration']} turn(s)![/yellow]")
                elif "healing" in spell:
                    magebot_hp += spell["healing"]
                    if magebot_hp > magebot_max_hp:
                        magebot_hp = magebot_max_hp
                        console.print("[green][Info] MageBot reached maximum HP![/green]")
                    create_action_log(f"MageBot cast {magebot_action}: +{spell['healing']} HP", "magenta")
                elif "resistance_boost" in spell:
                    magebot_res += spell["resistance_boost"]
                    create_action_log(f"MageBot cast {magebot_action}: +{spell['resistance_boost']} RES", "magenta")

        if magebot_mana < magebot_max_mana:
            magebot_mana += DEFAULT_MANA_REGEN
            if magebot_mana > magebot_max_mana:
                magebot_mana = magebot_max_mana
            console.print(f"[magenta][Mana] MageBot recovered {DEFAULT_MANA_REGEN} mana ({magebot_mana}/{magebot_max_mana})[/magenta]")

        if player_hp <= 0:
            duel_panel = create_duel_state_panel(
                player_hp, player_res, player_mana,
                magebot_hp, magebot_res, magebot_mana,
                player_effects, magebot_effects
            )
            console.print(duel_panel)
            console.print("[bold red]💀 You lost against MageBot...[/bold red]")
            break

def main():
    try:
        asyncio.run(init())
    except KeyboardInterrupt:
        console.print("\n[yellow]Closing MageBot CLI.[/yellow]")

async def init():
    console.print(create_banner())
    console.print("[cyan]Type 'help' to see available commands.[/cyan]")
    console.print(f"[dim]Version: {VERSION}[/dim]\n")
    
    while True:
        console.print(Panel.fit(
            "[bold cyan]MageBot CLI - Main Menu[/bold cyan]\n\n"
            "[green]1.[/green] Help\n"
            "[green]2.[/green] About\n"
            "[green]3.[/green] Start Duel\n"
            "[green]4.[/green] Exit",
            border_style="yellow"
        ))
        
        command = console.input("[bold green]Select option (1-4):[/bold green] ").strip()
        
        if command in ["1", "help"]:
            console.print("[yellow]Commands: help, about, start_duel, exit[/yellow]")
            console.print("[dim]Spell input: numbers (1-9), names (Ignis), or aliases (fire, ice, heal)[/dim]")
        elif command in ["2", "about"]:
            console.print(Panel(
                "[magenta]About MageBot[/magenta]\n\n"
                "Created by the ZIOS team.\n"
                "A console-based magical duel game with Rich UI.\n"
                "Defeat MageBot using strategy and spell mastery!",
                border_style="magenta"
            ))
        elif command in ["3", "start_duel", "start_dual"]:
            console.print("[yellow]Starting duel mode...[/yellow]")
            await asyncio.sleep(2)
            console.print("[yellow]Face MageBot AI! Prepare for battle![/yellow]")
            await duel_vs_magebot()
        elif command in ["4", "exit"]:
            console.print("[yellow]Closing MageBot CLI.[/yellow]")
            break
        else:
            console.print(f"[red]Unknown command: {command}[/red]")

if __name__ == "__main__":
    main()
