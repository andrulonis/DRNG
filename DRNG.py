from operator import mod
from random import randint, randrange
from tkinter import *
from PIL import ImageTk, Image
import json

PICKAXE_MODS_PATTERN = [1, 3]
ARMOR_MODS_PATTERN = [3, 2, 1, 3]
DWARF_CLASSES = ["gunner", "scout", "engineer", "driller"]

class Weapon:
    def __init__(self, name, overclock, mods_pattern, image):
        self.name = name
        self.overclock = overclock
        self.mods_pattern = mods_pattern
        self.image = image

class Gadget:
    def __init__(self, name, mods_pattern, image):
        self.name = name
        self.mods_pattern = mods_pattern
        self.image = image

class Loadout:
    def __init__(self, primary, secondary, first_gadget, second_gadget, grenade, armor, pickaxe):
        self.primary = primary
        self.secondary = secondary
        self.first_gadget = first_gadget
        self.second_gadget = second_gadget
        self.grenade = grenade
        self.armor = armor
        self.pickaxe = pickaxe

def randomise_loadout(dwarf_class, data):
    random_primary = data[dwarf_class]["primaries"][randrange(len(data[dwarf_class]["primaries"]))]
    primary_weapon = Weapon(random_primary["name"], random_primary["overclocks"][randrange(len(random_primary["overclocks"]))], [randint(1, mod) for mod in random_primary["mods_pattern"]], random_primary["image"])

    random_secondary = data[dwarf_class]["secondaries"][randrange(len(data[dwarf_class]["secondaries"]))]
    secondary_weapon = Weapon(random_secondary["name"], random_secondary["overclocks"][randrange(len(random_secondary["overclocks"]))], [randint(1, mod) for mod in random_secondary["mods_pattern"]], random_secondary["image"])

    first_gadget = Gadget(data[dwarf_class]["first_gadget"]["name"], [randint(1, mod) for mod in data[dwarf_class]["first_gadget"]["mods_pattern"]], data[dwarf_class]["first_gadget"]["image"])

    second_gadget = Gadget(data[dwarf_class]["second_gadget"]["name"], [randint(1, mod) for mod in data[dwarf_class]["second_gadget"]["mods_pattern"]], data[dwarf_class]["second_gadget"]["image"])

    grenade = data[dwarf_class]["grenades"][randrange(len(data[dwarf_class]["grenades"]))]

    armor = [randint(1,mod) for mod in ARMOR_MODS_PATTERN]

    pickaxe = [randint(1,mod) for mod in PICKAXE_MODS_PATTERN]

    return Loadout(primary_weapon, secondary_weapon, first_gadget, second_gadget, grenade, armor, pickaxe)

def display_loadout(selected_class, data, root, loadout_labels):
    loadout = randomise_loadout(selected_class, data)
    
    for label in loadout_labels:
        label.grid_forget()
    loadout_labels.clear()

    loadout_labels.append(primary_label := Label(root, text=loadout.primary.name + "\n" + loadout.primary.overclock + " " + " ".join(map(str, loadout.primary.mods_pattern))))
    primary_label.grid(column=1, row=2, padx=20, pady=20)

    global primary_image
    primary_image = ImageTk.PhotoImage(Image.open(loadout.primary.image))
    loadout_labels.append(primary_image_label := Label(root, image=primary_image))
    primary_image_label.grid(column=2, row=2, padx=20, pady=20)

    loadout_labels.append(secondary_label := Label(root, text=loadout.secondary.name + "\n" + loadout.secondary.overclock + " " + " ".join(map(str, loadout.secondary.mods_pattern))))
    secondary_label.grid(column=1, row=3, padx=20, pady=20)

    global secondary_image
    secondary_image = ImageTk.PhotoImage(Image.open(loadout.secondary.image))
    loadout_labels.append(secondary_image_label := Label(root, image=secondary_image))
    secondary_image_label.grid(column=2, row=3, padx=20, pady=20)

    loadout_labels.append(first_gadget_label := Label(root, text=loadout.first_gadget.name + "\n" + " ".join(map(str, loadout.first_gadget.mods_pattern))))
    first_gadget_label.grid(column=1, row=4, padx=20, pady=20)

    global first_gadget_image
    first_gadget_image = ImageTk.PhotoImage(Image.open(loadout.first_gadget.image))
    loadout_labels.append(first_gadget_image_label := Label(root, image=first_gadget_image))
    first_gadget_image_label.grid(column=2, row=4, padx=20, pady=20)

    loadout_labels.append(second_gadget_label := Label(root, text=loadout.second_gadget.name + "\n" + " ".join(map(str, loadout.second_gadget.mods_pattern))))
    second_gadget_label.grid(column=1, row=5, padx=20, pady=20)
    #TODO: continue here with iamges and globals
    loadout_labels.append(grenade_label := Label(root, text=loadout.grenade))
    grenade_label.grid(column=1, row=6, padx=20, pady=20)

    loadout_labels.append(pickaxe_label := Label(root, text= "Armor\n" + " ".join(map(str, loadout.armor))))
    pickaxe_label.grid(column=1, row=7, padx=20, pady=20)

    loadout_labels.append(pickaxe_label := Label(root, text= "Pickaxe\n" + " ".join(map(str, loadout.pickaxe))))
    pickaxe_label.grid(column=1, row=8, padx=20, pady=20)

def main():
    fp = open("data.json")
    data = json.load(fp)

    root = Tk()
    root.title("DRNG")
    root.resizable(False, False)
    root.geometry("800x1000")
    root.grid()
    root.grid_columnconfigure((0, 1, 2, 3), weight = 1)
    selected_class = StringVar(root, "gunner")

    buttons_frame = Frame(root)
    buttons_frame.grid(column=0, row=0, columnspan=4)

    gunner_icon = PhotoImage(file="./resources/icons/gunner_icon.png")
    scout_icon = PhotoImage(file="./resources/icons/scout_icon.png")
    engineer_icon = PhotoImage(file="./resources/icons/engineer_icon.png")
    driller_icon = PhotoImage(file="./resources/icons/driller_icon.png")
    Radiobutton(buttons_frame, value="gunner", image=gunner_icon, indicatoron=0, variable=selected_class).grid(column=0, row=0, padx=40, pady=40) #,borderwidth=0, ).grid(column=0, row=0, padx=40, pady=40)
    Radiobutton(buttons_frame, value="scout", image=scout_icon, indicatoron=0, variable=selected_class).grid(column=1, row=0, padx=40, pady=40)
    Radiobutton(buttons_frame, value="engineer", image=engineer_icon, indicatoron=0, variable=selected_class).grid(column=2, row=0, padx=40, pady=40)
    Radiobutton(buttons_frame, value="driller", image=driller_icon, indicatoron=0, variable=selected_class).grid(column=3, row=0, padx=40, pady=40)

    Button(root, text="Randomise loadout for selected class", command=lambda : display_loadout(selected_class.get(), data, root)).grid(column=1, row=1, padx=40, pady=40)
    Button(root, text="Randomise class and loadout", command=lambda : display_loadout(DWARF_CLASSES[randrange(len(DWARF_CLASSES))], data, root)).grid(column=2, row=1, padx=40, pady=40)

    loadout_labels = []
    Button(root, text="Randomise loadout for selected class", command=lambda : display_loadout(selected_class.get(), data, root, loadout_labels)).grid(column=1, row=1, padx=40, pady=40)
    Button(root, text="Randomise class and loadout", command=lambda : display_loadout(DWARF_CLASSES[randrange(len(DWARF_CLASSES))], data, root, loadout_labels)).grid(column=2, row=1, padx=40, pady=40)
    #TODO: add class display or change button pressed

    root.mainloop()

    fp.close()

if __name__ == "__main__":
    main()