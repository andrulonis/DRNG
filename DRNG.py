from random import randint, randrange, sample
from tkinter import *
from PIL import ImageTk
import json
import sys
import os

class Main_Application:
    def __init__(self, root, data):
        root.title("DRNG")
        icon = ImageTk.PhotoImage(file=resource_path("./resources/icons/dice.ico"))
        root.iconphoto(False, icon)
        root.resizable(False, False)
        root.geometry("1000x700")
        root.grid()
        root.grid_columnconfigure((0, 1, 2, 3), weight = 1)
        
        self.selected_class = StringVar(root)
        buttons_frame = Frame(root)
        buttons_frame.grid(column=0, row=0, columnspan=4)
        self.gunner_icon = PhotoImage(file=resource_path("./resources/icons/gunner_icon.png"))
        self.scout_icon = PhotoImage(file=resource_path("./resources/icons/scout_icon.png"))
        self.engineer_icon = PhotoImage(file=resource_path("./resources/icons/engineer_icon.png"))
        self.driller_icon = PhotoImage(file=resource_path("./resources/icons/driller_icon.png"))
        Radiobutton(buttons_frame, bg="green", value="gunner", image=self.gunner_icon, indicatoron=0, variable=self.selected_class).grid(column=0, row=0, padx=50, pady=20)
        Radiobutton(buttons_frame, bg="blue", value="scout", image=self.scout_icon, indicatoron=0, variable=self.selected_class).grid(column=1, row=0, padx=50, pady=20)
        Radiobutton(buttons_frame, bg="red", value="engineer", image=self.engineer_icon, indicatoron=0, variable=self.selected_class).grid(column=2, row=0, padx=50, pady=20)
        Radiobutton(buttons_frame, bg="yellow", value="driller", image=self.driller_icon, indicatoron=0, variable=self.selected_class).grid(column=3, row=0, padx=50, pady=20)

        loadout_labels = []
        Button(root, text="Randomise loadout for selected class", command=lambda : self.display_loadout(data, root, loadout_labels)).grid(column=1, row=1, padx=40, pady=10)
        Button(root, text="Randomise class and loadout", command=lambda : [self.selected_class.set(DWARF_CLASSES[randrange(len(DWARF_CLASSES))]), self.display_loadout(data, root, loadout_labels)]).grid(column=2, row=1, padx=40, pady=10)
    
    def display_loadout(self, data, root, loadout_labels):
        if (not self.selected_class.get()):
            return
        
        loadout = randomise_loadout(self.selected_class.get(), data)
        
        for label in loadout_labels:
            label.grid_forget()
        loadout_labels.clear()

        loadout_frame = Frame(root)
        loadout_frame.grid(column=0, row=2, columnspan=4)
        loadout_frame.grid_columnconfigure((0, 1, 2, 3), weight = 1, uniform="uniform")

        loadout_labels.append(primary_label := Label(loadout_frame, text=loadout.primary.name + "\n" + loadout.primary.overclock + "\n" + " ".join(map(str, loadout.primary.mods_pattern))))
        primary_label.grid(column=0, row=2, padx=10, pady=10)

        self.primary_image = ImageTk.PhotoImage(file=resource_path(loadout.primary.image))
        loadout_labels.append(primary_image_label := Label(loadout_frame, image=self.primary_image))
        primary_image_label.grid(column=1, row=2, padx=10, pady=10)

        loadout_labels.append(secondary_label := Label(loadout_frame, text=loadout.secondary.name + "\n" + loadout.secondary.overclock + "\n" + " ".join(map(str, loadout.secondary.mods_pattern))))
        secondary_label.grid(column=2, row=2, padx=10, pady=10)

        self.secondary_image = ImageTk.PhotoImage(file=resource_path(loadout.secondary.image))
        loadout_labels.append(secondary_image_label := Label(loadout_frame, image=self.secondary_image))
        secondary_image_label.grid(column=3, row=2, padx=10, pady=10)

        loadout_labels.append(first_gadget_label := Label(loadout_frame, text=loadout.first_gadget.name + "\n" + " ".join(map(str, loadout.first_gadget.mods_pattern))))
        first_gadget_label.grid(column=0, row=3, padx=10, pady=10)

        self.first_gadget_image = ImageTk.PhotoImage(file=resource_path(loadout.first_gadget.image))
        loadout_labels.append(first_gadget_image_label := Label(loadout_frame, image=self.first_gadget_image))
        first_gadget_image_label.grid(column=1, row=3, padx=10, pady=10)

        loadout_labels.append(second_gadget_label := Label(loadout_frame, text=loadout.second_gadget.name + "\n" + " ".join(map(str, loadout.second_gadget.mods_pattern))))
        second_gadget_label.grid(column=2, row=3, padx=10, pady=10)
        
        self.second_gadget_image = ImageTk.PhotoImage(file=resource_path(loadout.second_gadget.image))
        loadout_labels.append(second_gadget_image_label := Label(loadout_frame, image=self.second_gadget_image))
        second_gadget_image_label.grid(column=3, row=3, padx=10, pady=10)

        loadout_labels.append(grenade_label := Label(loadout_frame, text=loadout.grenade.name))
        grenade_label.grid(column=0, row=4, padx=10, pady=10)

        self.grenade_image = ImageTk.PhotoImage(file=resource_path(loadout.grenade.image))
        loadout_labels.append(grenade_image_label := Label(loadout_frame, image=self.grenade_image))
        grenade_image_label.grid(column=1, row=4, padx=10, pady=10)

        loadout_labels.append(pickaxe_label := Label(loadout_frame, text= "Armor Rig\n" + " ".join(map(str, loadout.armor))))
        pickaxe_label.grid(column=2, row=4, padx=10, pady=10)

        self.armor_image = ImageTk.PhotoImage(file=resource_path(data["armor"]["image"]))
        loadout_labels.append(armor_image_label := Label(loadout_frame, image=self.armor_image))
        armor_image_label.grid(column=3, row=4, padx=10, pady=10)

        loadout_labels.append(pickaxe_label := Label(loadout_frame, text= "Pickaxe\n" + " ".join(map(str, loadout.pickaxe))))
        pickaxe_label.grid(column=0, row=5, padx=10, pady=10)

        self.pickaxe_image = ImageTk.PhotoImage(file=resource_path(data["pickaxe"]["image"]))
        loadout_labels.append(pickaxe_image_label := Label(loadout_frame, image=self.pickaxe_image))
        pickaxe_image_label.grid(column=1, row=5, padx=10, pady=10)

        loadout_labels.append(passive_perks_label := Label(loadout_frame, text= "Passive perks:\n" + "\n".join(map(str, loadout.passive_perks))))
        passive_perks_label.grid(column=2, row=5, padx=10, pady=10)

        loadout_labels.append(active_perks_label := Label(loadout_frame, text= "Active perks:\n" + "\n".join(map(str, loadout.active_perks))))
        active_perks_label.grid(column=3, row=5, padx=10, pady=10)

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

class Grenade:
    def __init__(self, name, image):
        self.name = name
        self.image = image

class Loadout:
    def __init__(self, primary, secondary, first_gadget, second_gadget, grenade, armor, pickaxe, passive_perks, active_perks):
        self.primary = primary
        self.secondary = secondary
        self.first_gadget = first_gadget
        self.second_gadget = second_gadget
        self.grenade = grenade
        self.armor = armor
        self.pickaxe = pickaxe
        self.passive_perks = passive_perks
        self.active_perks = active_perks

def randomise_loadout(dwarf_class, data):
    random_primary = data[dwarf_class]["primaries"][randrange(len(data[dwarf_class]["primaries"]))]
    primary_weapon = Weapon(random_primary["name"], random_primary["overclocks"][randrange(len(random_primary["overclocks"]))], [randint(1, mod) for mod in random_primary["mods_pattern"]], random_primary["image"])

    random_secondary = data[dwarf_class]["secondaries"][randrange(len(data[dwarf_class]["secondaries"]))]
    secondary_weapon = Weapon(random_secondary["name"], random_secondary["overclocks"][randrange(len(random_secondary["overclocks"]))], [randint(1, mod) for mod in random_secondary["mods_pattern"]], random_secondary["image"])

    first_gadget = Gadget(data[dwarf_class]["first_gadget"]["name"], [randint(1, mod) for mod in data[dwarf_class]["first_gadget"]["mods_pattern"]], data[dwarf_class]["first_gadget"]["image"])

    second_gadget = Gadget(data[dwarf_class]["second_gadget"]["name"], [randint(1, mod) for mod in data[dwarf_class]["second_gadget"]["mods_pattern"]], data[dwarf_class]["second_gadget"]["image"])

    random_grenade = randrange(len(data[dwarf_class]["grenades"]["names"]))
    grenade = Grenade(data[dwarf_class]["grenades"]["names"][random_grenade], data[dwarf_class]["grenades"]["images"][random_grenade])

    armor = [randint(1,mod) for mod in data["armor"]["mods_pattern"]]

    pickaxe = [randint(1,mod) for mod in data["pickaxe"]["mods_pattern"]]

    passive_perks = sample(data["passive_perks"], 3)

    active_perks = sample(data["active_perks"], 2)

    return Loadout(primary_weapon, secondary_weapon, first_gadget, second_gadget, grenade, armor, pickaxe, passive_perks, active_perks)

def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

ARMOR_MODS_PATTERN = [3, 2, 1, 3]
PICKAXE_MODS_PATTERN = [1, 3]
ARMOR_IMAGE = resource_path("./resources/images/armor.png")
PICKAXE_IMAGE = resource_path("./resources/images/pickaxe.png")
DWARF_CLASSES = ["gunner", "scout", "engineer", "driller"]

def main():
    fp = open(resource_path("./resources/data.json"))
    data = json.load(fp)

    root = Tk()
    app = Main_Application(root, data)
    root.mainloop()

    fp.close()

if __name__ == "__main__":
    main()