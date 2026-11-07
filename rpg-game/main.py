CLASSES = {
        "1": {"name": "Warrior", "hp": 120, "atk": 12, "defense": 10, "desc": "Tough fighter."},
        "2": {"name": "Mage",    "hp": 80,  "atk": 16, "defense": 4,  "desc": "Powerful but fragile"},
        "3": {"name": "Rogue",   "hp": 95,  "atk": 13, "defense": 6,  "desc": "Balanced and quick"},
}

###################################################################################################
                                 # The prompts asked to the player #


# promting user input as well as error handleing
# for every player choice
def ask (prompt, valid):
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
        print("\nStep 2 of 3: Choose a class")
        for key, c in CLASSES.items():
            line = f"  [{key}] {c['name']}"
            if show_details:
                line += f" - HP {c['hp']}, ATK {c['atk']}, DEF {c['defense']} | {c['desc']}"
            print(line)
        print("  [r] Not sure? Use the recomended class (Warrior)")
        print(f"  [d] {'Hide' if show_details else 'Show'} class details")
        print("  [0] Back")
        choice = ask("> ", ["1", "2", "3", "r", "d", "0"])
        if choice == "d":
            show_details = not show_details
        elif choice == "0":
            None
        elif choice == "r":
            return CLASSES["1"]
        else:
            return CLASSES[choice]



###################################################################################################
                            # The Screens that the player will see #


# the title of the game as
# well as the choices for the user
def title_screen():
    print("=" * 40)
    print("        RETRO RPG")
    print("=" * 40)
    print("[1] New Game   - create a hero and start exaploring")
    print("[0] Quit       - close the game")
    choice = ask ("> ", ["1", "0"])
    return "create_hero" if choice == "1" else "quit"


def create_hero_screen(game):
    print("\n=== CREATE YOUR HERO ===")
    print("Steps: 1 Name your hero    2. Choose a class    3. Start your adventure")
    step = 1
    while True:
        if step == 1:
            print("\nStep 1 of 3: Name your hero")
            name = ask_name()
            if name == None:
                return "title"
            step = 2
        elif step == 2:
            cls = ask_class()
            step = 1 if cls is None else 3
        else:
            print(f"\nStep 3 of 3: Start your adventure as {name} the {cls['name']}?")
            print("  [y] Yes, start  [n] No, go back")
            if ask("> ", ["y", "n"]) == "y":
                game["hero"] = {
                    "name": name, "class": cls["name"], "level": 1,
                    "hp": cls["hp"], "max_hp": cls["hp"],
                    "atk": cls["atk"], "defense": cls["defense"],
                }
                return "dashboard"
            step = 2

def dashboard_screen(game):
    h = game["hero"]
    print("\n=== DASHBOARD (placeholder) ===")
    print(f"{h['name']} the {h['class']}  Lv {h['level']}")
    print(f"HP {h['hp']}/{h['max_hp']}  ATK {h['atk']}  DEF {h['defense']}")
    return "title"


###################################################################################################


def main():
    game = {"hero": None, "inventory": []}
    screen = "title"
    while screen != "quit":
        if screen == "title":
            screen = title_screen()

        elif screen == "create_hero":
            screen = create_hero_screen(game)

        elif screen == "dashboard":
            screen = dashboard_screen(game)

    print("Goodbye!")

main()
