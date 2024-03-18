# Make choices
# multiple choice
# free form
# set a time limit for decisions
# player could have sords 
# player could have food
# player could have a break dance mode
# final boss 
# music
# npc

# combat gameplay
# turn based
# A little randomness (critical hits)
# win by killing monster (health is zero)
# Different moves available: attack, block, ranged attack, etc
# inventory could take up a turn
# God cheese


# Combat
# *companions
# *three atacks per turn
# potions
#  * player inventory
#  * option during combat
# properties of your character factor in
# AI???
# God cheese

class CombatController:

    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy

    def enter_combat_loop(self):
        while(self.enemy.alive()):
            user_input = input("A: attack  B: block  C: ranged attack")
            player_move = self.process_user_input_for_move(user_input)
            player_move.do()
            enemy_move = self.get_enemy_move()
            enemy_move.do()
            pass

    def process_user_input_for_move(self, user_input):
        clean_user_input = user_input.lower()
        match(clean_user_input):
            case "a":
                return CombatMove("attack", 10, 0)
            case "b":
                return CombatMove("block", 0, 9)
            case "c":
                return CombatMove("ranged attack", 3, 0)
            case _:
                return None
            
    def get_enemy_move(self):
        return CombatMove("attack", 9, 0)


class Enemy:
    def __init__(self, health, type, name):
        self.health = health
        self.type = type
        self.name = name

    def alive(self):
        return self.health > 0


class CombatMove:

    def __init__(self, name, damage, block):
        self.name = name
        self.damage = damage
        self.block = block


class Player:

    def __init__(self):
        self.health = 100
        self.inventory = {}


def print_inventory():
    inventory = game_state["inventory"]
    for item in inventory:
        print(item)

def handle_griddy(prompt):
    print("hit the Griddy!!")
    print(prompt["text"])
    return 0

def handle_grab_item(prompt):
    print(prompt["text"])
    game_state["inventory"].append("bagel")
    return 0

def handle_start_adventure(prompt):
    full_text = "Hi {}! You have a cool name! Let's go on an adventure!".format(game_state["name"])
    print(full_text)
    return 0
    
def handle_get_name(prompt):
    print(prompt["text"])
    user_input = input()
    game_state["name"] = user_input
    return 0
    
game_state = {
    "name" : "",
    "inventory" : []
}

monster = {
    "name" : "scele_boy", 
    "heath" : 100
    }

prompts = [
    {
        "action" : "get_name",
        "text" : "Hello, what is your name?\n"
    },
    {
        "action" : "start"
    },
    {
        "action" : "you_have_item",
        "text" : "an item has been added"
    },
    {
        "action" : "griddy",
        "text" : "We did it!"
    }
]

code = 0
while True:    
    user_input = input("press any key to continue")
    if user_input == '':
        prompt = prompts.pop(0)

        action = prompt["action"]

        if action == "get_name":
            code = handle_get_name(prompt)
        if action == "start":
            code = handle_start_adventure(prompt)
        if action == "griddy":
            code = handle_griddy(prompt)
        if action == "you_have_item":
            code = handle_grab_item(prompt)
    elif user_input == "i":
        print_inventory()
    
    if code == 1:
        break;
    if len(prompts) == 0:
        break;
    