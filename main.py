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
        self.enemy = NPC(self, 50, "Bad Billybob")
        
        self.players = [
            self.enemy,
            self.player
        ]

    def enter_combat_loop(self):
        print("You encounter an enemy!")
        winner = None
        while winner == None:

            # TODO: ideally this would always be shown at the bottom of the screen
            for player in self.players:
                print("{}'s health: {}".format(player.name, player.health))

            round = Round()
            moves = round.get_moves(self.players)
            round.play(moves)
            winner = self.evaluate_win()
        print("{} wins!".format(winner.name))

    def evaluate_win(self):
        in_game = []
        for player in self.players:
            if player.alive():
                in_game.append(player)

        if len(in_game) == 1:
            return in_game[0]
        else:
            return None

class Round:

    def get_moves(self, players):
        moves = []
        for player in players:
            player.signal_intent()
            moves.append(player.intent)
        return moves

    def play(self, moves):
        blocking_moves = []
        attack_moves = []
        for move in moves:
            if move.is_blocking():
                blocking_moves.append(move)
            else:
                attack_moves.append(move)

        for block in blocking_moves:
            block.execute()

        for attack in attack_moves:
            attack.execute()

class Character:

    def __init__(self, combat_controller, health, name):
        self.combat_controller = combat_controller
        self.health = health
        self.name = name
        self.block = 0
        self.concealed = False
        self.intent = None

    def alive(self):
        return self.health > 0
    
    def get_intent(self):
        raise Exception("not implemented")
    
    def signal_intent(self):
        self.intent = self.get_intent()
        if self.concealed:
            self.concealed = False
        else:
            self.intent.signal()
            
class NPC(Character):
    def __init__(self, combat_controller, health, name):
        super().__init__(combat_controller, health, name)
    
    def get_intent(self):
        # cool AI stuff will go here
        random_index = random.randrange(0, 3)
        match(random_index):
            case 0:
                return Attack(self, self.combat_controller.player) 
            case 1:
                return Block(self)
            case 2:
                return Conceal(self)
            
    def base_damage(self):
        return 16
    
    def base_block(self):
        return 10

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
                    return Attack(self, self.combat_controller.enemy)
                case "b":
                    return Block(self)
                case "c":
                    return Conceal(self)
                
    def base_damage(self):
        return 16
    
    def base_block(self):
        return 10

class CombatMove:

    def __init__(self, player, target = None):
        self.player = player
        self.target = target

    def is_blocking(self):
        False

class Attack(CombatMove):

    def __init__(self, player, target):
        super().__init__(player, target)

    def damage(self):
        damage = randomize(self.player.base_damage())
        crit = random.randrange(0, 100)
        if crit == 0:
            multiple = damage
            damage = damage * damage
            print("{} got a rare critical hit for {} times the damage!".format(self.player.name, multiple))
        elif crit < 10:
            damage = damage
            print("{} got a critical hit for double damage!".format(self.player.name))
        self.base_damage = damage

    def execute(self):
        self.damage()
        effective_damage = max(self.base_damage - self.target.block, 0)
        self.target.health = max(self.target.health - effective_damage, 0)
        if(self.base_damage < 8):
            print("{} did a wimpy attack and did {} damage".format(self.player.name, effective_damage))
        elif(self.base_damage < 16):
            print("{} did an ok attack and did {} damage".format(self.player.name, effective_damage))
        elif(self.base_damage < 32):
            print("{} did a strong attack and did {} damage!".format(self.player.name, effective_damage))
        else:
            print("{} did a very strong attack and did {} damage!!".format(self.player.name, effective_damage))

    def signal(self):
        print("{} raised their sword".format(self.player.name))

class Block(CombatMove):

    def __init__(self, player):
        super().__init__(player)
        self.player.block = randomize(player.base_block())
    
    def execute(self):
        if(self.player.block < 8):
            print("{} did a wimpy block for {} protection".format(self.player.name, self.player.block))
        elif(self.player.block < 16):
            print("{} did an ok block for {} protection".format(self.player.name, self.player.block))
        elif(self.player.block < 32):
            print("{} did a strong block for {} protection!".format(self.player.name, self.player.block))
        else:
            print("{} did a very strong block for {} protection!!".format(self.player.name, self.player.block))
        self.player.block = 0

    def signal(self):
        print("{} held up their shield".format(self.player.name))

    def is_blocking(self):
        return True

class Conceal(CombatMove):

    def __init__(self, player):
        super().__init__(player)

    def execute(self):
        self.player.concealed = True
        print("{} feinted with their right hand".format(self.player.name))

    def signal(self):
        print("{} raised their sword".format(self.player.name))

def randomize(damage):
    mu = damage                             # average attack
    sigma = 2                               # 68% of attacks will be this distance from the average
    scalar = np.random.normal(mu, sigma, 1) # get a random number from the distribution
    unpacked = scalar[0]                    # unpack the result from the array
    return round(unpacked)                  # round the float to an integer
    
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
    