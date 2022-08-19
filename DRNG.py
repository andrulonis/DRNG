from operator import mod
from random import randint, randrange
from tkinter import *
import json

PICKAXE_MODS_PATTERN = [1, 3]
DWARF_CLASSES = ["gunner", "scout", "engineer", "driller"]

class Weapon:
    def __init__(self, name, overclock, mods_pattern):
        self.name = name
        self.overclock = overclock
        self.mods_pattern = mods_pattern

class Gadget:
    def __init__(self, name, mods_pattern):
        self.name = name
        self.mods_pattern = mods_pattern

class Loadout:
    def __init__(self, primary, secondary, first_gadget, second_gadget, grenade, pickaxe):
        self.primary = primary
        self.secondary = secondary
        self.first_gadget = first_gadget
        self.second_gadget = second_gadget
        self.grenade = grenade
        self.pickaxe = pickaxe
    
    # def randomise(self):
    #     random_primary = self.primaries[randrange(len(self.primaries))]
    #     random_secondary = self.secondaries[randrange(len(self.secondaries))]
    #     random_first_gadget_mods = [randint(0,mod) for mod in self.first_gadget_mods_pattern]
    #     random_second_gadget_mods = [randint(0,mod) for mod in self.second_gadget_mods_pattern]
    #     random_grenade = self.grenades[randrange(len(self.grenades))]
    #     random_pickaxe_mods = [randint(0,mod) for mod in self.pickaxe_mods_pattern]
    #     return Loadout(random_primary, random_secondary, random_first_gadget_mods, random_second_gadget_mods, random_grenade, random_pickaxe_mods)

# class Dwarf:
#     def __init__(self, primaries, secondaries, first_gadget_mods_pattern, second_gadget_mods_pattern, grenades):
#         self.primaries = primaries
#         self.secondaries = secondaries
#         self.first_gadget_mods_pattern = first_gadget_mods_pattern
#         self.second_gadget_mods_pattern = second_gadget_mods_pattern
#         self.grenades = grenades
#         self.pickaxe_mods_pattern = [1, 3]

def randomise_loadout(dwarf_class, data):
    random_primary = data[dwarf_class]["primaries"][randrange(len(data[dwarf_class]["primaries"]))]
    primary_weapon = Weapon(random_primary["name"], random_primary["overclocks"][randrange(len(random_primary["overclocks"]))], random_primary["mods_pattern"][randrange(len(random_primary["mods_pattern"]))])

    random_secondary = data[dwarf_class]["secondaries"][randrange(len(data[dwarf_class]["secondaries"]))]
    secondary_weapon = Weapon(random_secondary["name"], random_secondary["overclocks"][randrange(len(random_secondary["overclocks"]))], random_secondary["mods_pattern"][randrange(len(random_secondary["mods_pattern"]))])

    first_gadget = Gadget(data[dwarf_class]["first_gadget"]["name"], [randint(1, mod) for mod in data[dwarf_class]["first_gadget"]["mods_pattern"]])

    second_gadget = Gadget(data[dwarf_class]["second_gadget"]["name"], [randint(1, mod) for mod in data[dwarf_class]["second_gadget"]["mods_pattern"]])

    grenade = data[dwarf_class]["grenades"][randrange(len(data[dwarf_class]["grenades"]))]

    pickaxe = [randint(1,mod) for mod in PICKAXE_MODS_PATTERN]

    return Loadout(primary_weapon, secondary_weapon, first_gadget, second_gadget, grenade, pickaxe)

def display_loadout(selected_class, data, root):
    loadout = randomise_loadout(selected_class, data)
    Label(root, text=loadout.primary.name).grid(column=1, row=2, padx=20, pady=20)
    Label(root, text=loadout.primary.overclock + " " + loadout.primary.mods_pattern).grid(column=1, row=3, padx=20, pady=20) #TODO: fix array to print

def main():
    fp = open("data.json")
    data = json.load(fp)

    root = Tk()
    root.title("DRNG")
    root.resizable(False, False)
    root.geometry("800x500")
    root.grid()
    root.grid_columnconfigure((0, 1, 2, 3), weight=1)
    selected_class = StringVar(root, "gunner")

    gunner_icon=PhotoImage(file="./icons/gunner_icon.png")
    scout_icon=PhotoImage(file="./icons/scout_icon.png")
    engineer_icon=PhotoImage(file="./icons/engineer_icon.png")
    driller_icon=PhotoImage(file="./icons/driller_icon.png")
    Radiobutton(root, value="gunner", image=gunner_icon, indicatoron=0, variable=selected_class).grid(column=0, row=0, padx=40, pady=40) #,borderwidth=0, ).grid(column=0, row=0, padx=40, pady=40)
    Radiobutton(root, value="scout", image=scout_icon, indicatoron=0, variable=selected_class).grid(column=1, row=0, padx=40, pady=40)
    Radiobutton(root, value="engineer", image=engineer_icon, indicatoron=0, variable=selected_class).grid(column=2, row=0, padx=40, pady=40)
    Radiobutton(root, value="driller", image=driller_icon, indicatoron=0, variable=selected_class).grid(column=3, row=0, padx=40, pady=40)

    Button(root, text="Randomise loadout for selected class", command=lambda : display_loadout(selected_class.get(), data, root)).grid(column=1, row=1, padx=40, pady=40)
    Button(root, text="Randomise class and loadout", command=lambda : display_loadout(DWARF_CLASSES[randrange(len(DWARF_CLASSES))], data, root)).grid(column=2, row=1, padx=40, pady=40)



    root.mainloop()

    fp.close()

if __name__ == "__main__":
    main()