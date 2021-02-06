#!/usr/bin/env python3
import sys
import os,json
import re
assert sys.version_info >= (3,9), "This script requires at least Python 3.9"

def load(l):
    f = open(os.path.join(sys.path[0], l))
    data = f.read()
    j = json.loads(data)
    return j
def find_passage(game_desc, pid):
    for p in game_desc["passages"]:
        if p["pid"] == pid:
            return p
    return{}

def format_passage(description):
    description = re.sub(r'//([^/]*)//',r'\1',description)
    description = re.sub(r"''([^']*)''",r'\1',description)
    description = re.sub(r'~~([^~]*)~~',r'\1',description)
    description = re.sub(r'\*\*([^\*]*)\*\*',r'\1',description)
    description = re.sub(r'\*([^\*]*)\*',r'\1',description)
    description = re.sub(r'\^\^([^\^]*)\^\^',r'\1',description)
    description = re.sub(r'(\[\[[^\|]*?)\|([^\]]*?\]\])',r'\1->\2',description)
    description = re.sub(r'\[\[([^(->\])]*?)->[^\]]*?\]\]',r'[ \1 ]',description)
    description = re.sub(r'\[\[(.+?)\]\]',r'[ \1 ]',description)
    return description

def update(current, choice, game_desc):
    if choice == "":
        return current
    for l in current["links"]:
        if l["name"].lower() == choice:
            current = find_passage(game_desc, l["pid"])
            return current
    
    print("You are not the smartest student, and do not know how to do that. Please try again. ")
    return current

    

def render(current):
    #print(current["name"])
    print("\n\n")
    print(format_passage(current["text"]))
    print("\n")
    

def get_input():
    choice = input("What do you choose? (Type quit to magically teleport to your dorm) ")
    choice = choice.lower().strip()
    return choice

def main():
    game_desc = load("game.json")
    current = find_passage(game_desc, game_desc["startnode"])
    choice = ""

    while choice != "quit" and current != {}:
        current = update(current, choice, game_desc)
        render(current)
        if "links" in current:
            choice = get_input()
        else:
            current = {}
    print("Thanks for playing!")
if __name__ == "__main__":
    main()