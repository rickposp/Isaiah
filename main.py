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

    def __init__(self):
        self.player = Player(self)
        self.enemy = Enemy(self)

    def enter_combat_loop(self):
        while(self.enemy.alive() and self.player.alive()):
            self.player.take_turn()
            self.enemy.take_turn()


class Character:

    def __init__(self, combat_controller, health, name):
        self.combat_controller = combat_controller
        self.health = health
        self.name = name
        self.block = 0

    def take_turn(self):
        move = self.get_move()
        move.do

    def alive(self):
        return self.health > 0


class Enemy(Character):
    def __init__(self, combat_controller, health, name):
        self.super(combat_controller, health, name)
    
    def get_move(self):
        # cool AI stuff will go here
        return CombatMove("attack", 1, 0)


class Player(Character):

    def __init__(self, combat_controller):
        self.super(combat_controller, 100, game_state["name"])
        self.health = 100
        self.inventory = []

    def get_move(self, user_input):
        self.super()
        user_input = input("A: attack  B: block  C: ranged attack")
        clean_user_input = user_input.lower()
        match(clean_user_input):
            case "a":
                return Attack("attack", self.combat_controller.enemy, 10)
            case "b":
                return CombatMove("block", self, 9)
            case _:
                return None

class CombatMove:

    def __init__(self, target):
        self.target = target

class Attack(CombatMove):

    def __init__(self, target, damage):
        self.super(target)
        self.damage = damage

    def do(self):
        self.target.health = self.target.health - self.damage

class Block(CombatMove):

    def __init__(self, block):
        self.super(target)
        self.block = self.block
    
    def do(self):
        self.target.block = self.target.block + self.block


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
    