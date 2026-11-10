import random
import time

BAG_SIZE = 8
FOOTER = "Runs offline on your computer | No account needed | No personal data collected"
ICONS = {"weapon": "[/]", "armor": "[#]", "potion": "[!]"}

CLASSES = {
    "1": {"name": "Warrior", "hp": 120, "atk": 12, "defense": 10, "desc": "Tough fighter."},
    "2": {"name": "Mage",    "hp": 80,  "atk": 16, "defense": 4,  "desc": "Powerful but fragile."},
    "3": {"name": "Rogue",   "hp": 95,  "atk": 13, "defense": 6,  "desc": "Balanced and quick."},
}

# Each zone has events. An event has some text and (optionally) an item found.
ZONES = {
    "1": {
        "name": "Dark Forest",
        "blurb": "Twisting trees, goblins and wolves.",
        "events": [
            {"text": "A goblin leaps out of the bushes! You scare it off and spot its blade.",
             "loot": {"name": "Rusty Sword", "type": "weapon", "desc": "Old, but still sharp."}},
            {"text": "A wolf pack snarls at you. You back away slowly until they lose interest.",
             "loot": None},
            {"text": "You find a hollow tree with a small bottle tucked inside.",
             "loot": {"name": "Health Potion", "type": "potion", "desc": "Restores health."}},
            {"text": "You stumble into an abandoned hunter's camp.",
             "loot": {"name": "Wooden Shield", "type": "armor", "desc": "Light and sturdy."}},
            {"text": "Giant webs block your path. You cut through and find boots stuck in them.",
             "loot": {"name": "Leather Boots", "type": "armor", "desc": "Good for long walks."}},
        ],
    },
    "2": {
        "name": "Sunken Crypt",
        "blurb": "Damp halls, skeletons and old treasure.",
        "events": [
            {"text": "A skeleton guard rattles to life! It crumbles, leaving a weapon behind.",
             "loot": {"name": "Iron Dagger", "type": "weapon", "desc": "Quick and light."}},
            {"text": "You pry open a dusty chest and find a glowing vial.",
             "loot": {"name": "Health Potion", "type": "potion", "desc": "Restores health."}},
            {"text": "A cold draft blows through the hall. You find nothing but cobwebs.",
             "loot": None},
            {"text": "A cracked statue holds something shiny in its hand.",
             "loot": {"name": "Bronze Helmet", "type": "armor", "desc": "Dented, but protective."}},
            {"text": "A ghostly whisper echoes, then fades. The room is empty.",
             "loot": None},
        ],
    },
}

###################################################################################################
                                 # The prompts asked to the player #


# prompting for user input, with error handling
# for every player choice
def ask(prompt, valid):
    while True:
        answer = input(prompt).strip().lower()
        if answer in valid:
            return answer
        print(f" Sorry. '{answer}' is not an option. Choose one of: {', '.join(valid)}")


# name asking and error handling
def ask_name():
    while True:
        name = input("Hero name (1-16 letters/numbers, or 0 to go back): ").strip()
        if name == "0":
            return None
        if 1 <= len(name) <= 16 and name.isalnum() and any(c.isalpha() for c in name):
            return name
        print("  Names need 1-16 letters or numbers (no spaces) and at least one letter.")


def ask_class():
    show_details = False
    while True:
        print("\n" * 5)
        print("\nStep 2 of 3: Choose a class")
        for key, c in CLASSES.items():
            line = f"  [{key}] {c['name']}"
            if show_details:
                line += f" - HP {c['hp']}, ATK {c['atk']}, DEF {c['defense']} | {c['desc']}"
            print(line)
        print("  [r] Not sure? Use the recommended class (Warrior)")
        print(f"  [d] {'Hide' if show_details else 'Show'} class details")
        print("  [0] Back")
        print("\n" * 5)
        choice = ask("> ", ["1", "2", "3", "r", "d", "0"])
        if choice == "d":
            show_details = not show_details
        elif choice == "0":
            return None
        elif choice == "r":
            return CLASSES["1"]
        else:
            return CLASSES[choice]


def ask_dashboard():
    print("\n" * 5)
    choice = ask("> ", ["1", "2", "0"])
    if choice == "1":
        return "zone_select"
    elif choice == "2":
        return "inventory"
    print("\nReturn to the title screen? Your current hero and items will be lost.")
    print("  [y] Yes, return to title   [n] No, stay here")
    if ask("> ", ["y", "n"]) == "y":
        return "title"
    return "dashboard"


###################################################################################################
                            # The Screens that the player will see #


# the title of the game as
# well as the choices for the user
def title_screen():
    print("\n" * 5)
    print("=" * 60)
    print("                 _____   _____    ____    ")
    print("                |     \\  |    \\  /    \\   ")
    print("                |  D  |  |  D | /  --__|  ")
    print("                | __  /  |  __/ | |  ___  ")
    print("                | | \\ \\  | |    | | |_ |  ")
    print("                | |  \\ \\ | |    \\ \\__/ /   ")
    print("                |_|  |_| |_|     \\____/    ")
    print("=" * 60)
    print("   Create a hero, explore dungeons, and collect loot.")
    print()
    print("[1] New Game   - create a hero and start exploring")
    print("[0] Quit       - close the game")
    print()
    print(FOOTER)
    print("\n" * 3)
    choice = ask("> ", ["1", "0"])
    return "create_hero" if choice == "1" else "quit"


def create_hero_screen(game):
    print("\n" * 5)
    print("\n=== CREATE YOUR HERO ===")
    print("Steps: 1. Name your hero    2. Choose a class    3. Start your adventure")
    step = 1
    while True:
        if step == 1:
            print("\nStep 1 of 3: Name your hero")
            print("\n" * 5)
            name = ask_name()
            if name is None:
                return "title"
            step = 2

        elif step == 2:
            cls = ask_class()
            step = 1 if cls is None else 3

        else:
            print("\n" * 5)
            print(f"\nStep 3 of 3: Start your adventure as {name} the {cls['name']}?")
            print("  [y] Yes, start  [n] No, go back")
            print("\n" * 5)
            if ask("> ", ["y", "n"]) == "y":
                game["hero"] = {
                    "name": name, "class": cls["name"], "level": 1,
                    "hp": cls["hp"], "max_hp": cls["hp"],
                    "atk": cls["atk"], "defense": cls["defense"],
                }
                game["inventory"] = []
                return "dashboard"
            step = 2


def dashboard_screen(game):
    h = game["hero"]
    print("\n" * 5)
    print("=== DASHBOARD ===")
    print("+" + "-" * 38 + "+")
    line1 = f"{h['name']} the {h['class']}   Lv {h['level']}"
    line2 = f"HP {h['hp']}/{h['max_hp']}   ATK {h['atk']}   DEF {h['defense']}"
    line3 = f"Bag: {len(game['inventory'])}/{BAG_SIZE} items"
    for line in (line1, line2, line3):
        print(f"| {line:<36} |")
    print("+" + "-" * 38 + "+")
    print()
    print(" [1] Explore    - visit a zone to find loot (free, no HP lost)")
    print(" [2] Inventory  - view and sort the items you have found")
    print(" [0] Title      - leave this hero (asks you first)")
    print()
    print(FOOTER)
    return ask_dashboard()


def zone_select_screen(game):
    print("\n" * 5)
    print("=== CHOOSE A ZONE ===")
    for key, z in ZONES.items():
        print(f" [{key}] {z['name']:<13} {z['blurb']}")
    print(" [r] Random zone - can't decide? Let the game pick")
    print(" [0] Back")
    print()
    print("Cost: free. You won't lose HP or items.")
    print("\n" * 3)
    choice = ask("> ", list(ZONES.keys()) + ["r", "0"])
    if choice == "0":
        return "dashboard"
    if choice == "r":
        choice = random.choice(list(ZONES.keys()))
    game["zone"] = choice
    return "explore"


def explore_once(game, zone):
    """Pick a random event. If it has loot and the bag has room, add it."""
    event = random.choice(zone["events"])
    result = {"text": event["text"], "loot": None, "bag_full": False}
    if event["loot"] is not None:
        if len(game["inventory"]) < BAG_SIZE:
            game["inventory"].append(dict(event["loot"]))
            result["loot"] = event["loot"]
        else:
            result["bag_full"] = True
    return result


def print_log(zone, result, show_details):
    print("\n" * 5)
    print(f"=== EXPLORATION LOG: {zone['name']} ===")
    print(f"  {result['text']}")
    if result["loot"] is not None:
        item = result["loot"]
        print(f"  You found: {ICONS[item['type']]} {item['name']}!")
        if show_details:
            print(f"    Type: {item['type']}   Note: {item['desc']}")
    elif result["bag_full"]:
        print("  Your bag is full, so you had to leave the item behind.")
    else:
        print("  You found nothing this time.")


def exploration_screen(game):
    zone = ZONES[game["zone"]]
    show_details = False
    result = None
    elapsed = 0.0
    while True:
        if result is None:
            start = time.perf_counter()
            result = explore_once(game, zone)
            print_log(zone, result, show_details)
            elapsed = time.perf_counter() - start
        else:
            print_log(zone, result, show_details)
        print(f"\n  (log shown in {elapsed * 1000:.2f} ms - limit is 500 ms)")
        print()
        print(" [1] Explore again")
        print(" [2] Inventory")
        print(f" [d] {'Hide' if show_details else 'Show'} log details")
        print(" [0] Back to dashboard")
        print("\n" * 3)
        choice = ask("> ", ["1", "2", "d", "0"])
        if choice == "1":
            result = None
        elif choice == "2":
            return "inventory"
        elif choice == "d":
            show_details = not show_details
        else:
            return "dashboard"


def draw_grid(items):
    cols, rows = 4, BAG_SIZE // 4
    border = "+" + ("-" * 18 + "+") * cols
    print(border)
    for r in range(rows):
        cells = []
        for c in range(cols):
            i = r * cols + c
            text = f" {ICONS[items[i]['type']]} {items[i]['name']}" if i < len(items) else " (empty)"
            cells.append(f"{text:<18}")
        print("|" + "|".join(cells) + "|")
        print(border)


def inventory_screen(game):
    sort_by = None
    show_details = False
    while True:
        items = list(game["inventory"])  # a copy, so sorting never changes the real bag
        if sort_by == "name":
            items.sort(key=lambda i: i["name"])
        elif sort_by == "type":
            items.sort(key=lambda i: (i["type"], i["name"]))
        print("\n" * 5)
        print(f"=== INVENTORY ({len(items)}/{BAG_SIZE}) ===")
        draw_grid(items)
        if not items:
            print("Your bag is empty. Go explore to find items!")
        if show_details:
            for it in items:
                print(f"  {ICONS[it['type']]} {it['name']:<14} {it['type']:<7} {it['desc']}")
        order = sort_by if sort_by else "found order"
        print()
        print(f" [s] Sort items (now: {order}) - cycles name, type, found order")
        print(f" [d] {'Hide' if show_details else 'Show'} item details")
        print(" [0] Back to dashboard")
        print("\n" * 3)
        choice = ask("> ", ["s", "d", "0"])
        if choice == "s":
            sort_by = {None: "name", "name": "type", "type": None}[sort_by]
        elif choice == "d":
            show_details = not show_details
        else:
            return "dashboard"


###################################################################################################


def main():
    game = {"hero": None, "inventory": [], "zone": None}
    screen = "title"
    while screen != "quit":
        if screen == "title":
            screen = title_screen()
        elif screen == "create_hero":
            screen = create_hero_screen(game)
        elif screen == "dashboard":
            screen = dashboard_screen(game)
        elif screen == "zone_select":
            screen = zone_select_screen(game)
        elif screen == "explore":
            screen = exploration_screen(game)
        elif screen == "inventory":
            screen = inventory_screen(game)
    print("Goodbye!")


main()
