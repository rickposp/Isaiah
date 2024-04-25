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


# Combat
# *companions
# A little randomness (critical hits)
# inventory could take up a turn
# *three atacks per turn
# potions
#  * player inventory
#  * option during combat
#  * God cheese
# properties of your character factor in

import random
import numpy as np

class CombatController:

    def __init__(self):
        self.player = Player(self)
        self.enemy = Enemy(self, 50, "Bad Billybob")

    def enter_combat_loop(self):
        print("You encounter an enemy!")
        while(self.enemy.alive() and self.player.alive()):
            print("Your health: {}  Enemy health: {}".format(self.player.health, self.enemy.health))

            self.enemy.signal_intent()
            self.player.signal_intent()

            self.player.take_turn()
            self.enemy.take_turn()

            # combat is over, reset
            self.player.block = 0
            self.enemy.block = 0
        if self.enemy.alive():
            print("you lose")
        else:
            print("you win!")


class Character:

    def __init__(self, combat_controller, health, name):
        self.combat_controller = combat_controller
        self.health = health
        self.name = name
        self.block = 0
        self.conceal = False

    def take_turn(self):
        self.intent.execute()

    def alive(self):
        return self.health > 0
    
    def get_intent(self):
        raise Exception("not implemented")
    
    def signal_intent(self):
        self.intent = self.get_intent()
        if not self.conceal or isinstance(self.intent, Conceal):
            self.intent.signal()
        if self.conceal:
            self.conceal = False


class Enemy(Character):
    def __init__(self, combat_controller, health, name):
        super().__init__(combat_controller, health, name)
    
    def get_intent(self):
        # cool AI stuff will go here
        random_index = random.randrange(0, 3)
        match(random_index):
            case 0:
                mu = 16                                 # average attack
                sigma = 8                               # 68% of attacks will be this distanced from the average
                scalar = np.random.normal(mu, sigma, 1) # get a random number from the distribution
                unpacked = scalar[0]                    # unpack the result from the array
                attack = round(unpacked)                # round the float to an integer
                return Attack(self, self.combat_controller.player, attack) 
            case 1:
                block = round(np.random.normal(10, 4, 1)[0])
                return Block(self, self, block)
            case 2:
                return Conceal(self, self)

class Player(Character):

    def __init__(self, combat_controller):
        super().__init__(combat_controller, 100, game_state["name"])
        self.inventory = []

    def get_intent(self):
        running = True
        while(running):
            user_input = input("A: attack  B: block  C: conceal\n")
            clean_user_input = user_input.strip().lower()
            match(clean_user_input):
                case "a":
                    return Attack(self, self.combat_controller.enemy, 10)
                case "b":
                    return Block(self, self, 20)
                case "c":
                    return Conceal(self, self)

class CombatMove:

    def __init__(self, source, target):
        self.source = source
        self.target = target

class Attack(CombatMove):

    def __init__(self, source, target, damage):
        super().__init__(source, target)
        self.base_damage = damage

    def execute(self):
        crit = random.randrange(0, 100)
        if crit == 0:
            multiple = self.base_damage
            self.base_damage = self.base_damage * self.base_damage
            print("{} got a rare critical hit for {} times the damage!".format(self.source.name, multiple))
        elif crit < 10:
            self.base_damage = self.base_damage * 2
            print("{} got a critical hit for double damage!".format(self.source.name))
        effective_damage = max(self.base_damage - self.target.block, 0)
        self.target.health = max(self.target.health - effective_damage, 0)
        if(self.base_damage < 8):
            print("{} did a wimpy attack and did {} damage".format(self.source.name, effective_damage))
        elif(self.base_damage < 16):
            print("{} did an ok attack and did {} damage".format(self.source.name, effective_damage))
        elif(self.base_damage < 32):
            print("{} did a strong attack and did {} damage!".format(self.source.name, effective_damage))
        else:
            print("{} did a very strong attack and did {} damage!!".format(self.source.name, effective_damage))

    def signal(self):
        print("{} raised their sword".format(self.source.name))

class Block(CombatMove):

    def __init__(self, source, target, block):
        super().__init__(source, target)
        self.block = block
    
    def execute(self):
        if(self.block < 8):
            print("{} did a wimpy block for {} protection".format(self.source.name, self.block))
        elif(self.block < 16):
            print("{} did an ok block for {} protection".format(self.source.name, self.block))
        elif(self.block < 32):
            print("{} did a strong block for {} protection!".format(self.source.name, self.block))
        else:
            print("{} did a very strong block for {} protection!!".format(self.source.name, self.block))

    def signal(self):
        self.target.block = self.block
        print("{} held up their shield giving them {} block!".format(self.target.name, self.block))

class Conceal(CombatMove):

    def __init__(self, source, target):
        super().__init__(source, target)
        source.conceal = True

    def execute(self):
        pass

    def signal(self):
        print("{} feinted with their right hand".format(self.source.name))


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

def handle_combat(prompt):
    CombatController().enter_combat_loop()
    
game_state = {
    "name" : "",
    "inventory" : []
}

monster = {
    "name" : "scele_boy", 
    "heath" : 50
    }

prompts = [
    {
        "action" : "get_name",
        "text" : "Hello, what is your name?\n"
    },
    {
        "action": "combat"
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
    user_input = input("press enter to continue")
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
        if action == "combat":
            code = handle_combat(prompt)
    elif user_input == "i":
        print_inventory()
    
    if code == 1:
        break;
    if len(prompts) == 0:
        break;
    