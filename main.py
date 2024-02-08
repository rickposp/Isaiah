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
    