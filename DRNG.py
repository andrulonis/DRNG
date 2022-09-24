from random import randint, randrange, sample
from tkinter import *
from typing import List
from PIL import ImageTk
import json
import sys
import os

DWARF_CLASSES = ["gunner", "scout", "engineer", "driller"]


class Weapon:
    def __init__(self, data):
        """Chooses random mods_pattern and overclock for the Weapon"""
        self.name = data["name"]
        self.overclock = data["overclocks"][randrange(len(data["overclocks"]))]
        self.mods_pattern = [randint(1, mod) for mod in data["mods_pattern"]]
        self.image = data["image"]


class Gadget:
    def __init__(self, data):
        """Chooses random mods_pattern for the Gadget"""
        self.name = data["name"]
        self.mods_pattern = [randint(1, mod) for mod in data["mods_pattern"]]
        self.image = data["image"]


class Grenade:
    def __init__(self, name, image):
        self.name = name
        self.image = image


class Loadout:
    def __init__(
        self,
        primary: Weapon,
        secondary: Weapon,
        first_gadget: Gadget,
        second_gadget: Gadget,
        grenade: Grenade,
        armor,
        pickaxe,
        passive_perks,
        active_perks,
    ):
        self.primary = primary
        self.secondary = secondary
        self.first_gadget = first_gadget
        self.second_gadget = second_gadget
        self.grenade = grenade
        self.armor = armor
        self.pickaxe = pickaxe
        self.passive_perks = passive_perks
        self.active_perks = active_perks


class Main_Application:
    def __init__(self, root, data):
        self.data = data
        self.root = root
        self.root.title("DRNG")
        icon = ImageTk.PhotoImage(file=resource_path("./resources/icons/icon.ico"))
        self.root.iconphoto(False, icon)
        self.root.resizable(False, False)
        self.root.geometry("1000x700")
        self.root.grid()
        self.root.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.selected_class = StringVar(self.root)
        buttons_frame = Frame(self.root)
        buttons_frame.grid(column=0, row=0, columnspan=4)
        self.gunner_icon = PhotoImage(
            file=resource_path("./resources/icons/gunner_icon.png")
        )
        self.scout_icon = PhotoImage(
            file=resource_path("./resources/icons/scout_icon.png")
        )
        self.engineer_icon = PhotoImage(
            file=resource_path("./resources/icons/engineer_icon.png")
        )
        self.driller_icon = PhotoImage(
            file=resource_path("./resources/icons/driller_icon.png")
        )
        Radiobutton(
            buttons_frame,
            bg="green",
            value="gunner",
            image=self.gunner_icon,
            indicatoron=0,
            variable=self.selected_class,
        ).grid(column=0, row=0, padx=50, pady=20)
        Radiobutton(
            buttons_frame,
            bg="blue",
            value="scout",
            image=self.scout_icon,
            indicatoron=0,
            variable=self.selected_class,
        ).grid(column=1, row=0, padx=50, pady=20)
        Radiobutton(
            buttons_frame,
            bg="red",
            value="engineer",
            image=self.engineer_icon,
            indicatoron=0,
            variable=self.selected_class,
        ).grid(column=2, row=0, padx=50, pady=20)
        Radiobutton(
            buttons_frame,
            bg="yellow",
            value="driller",
            image=self.driller_icon,
            indicatoron=0,
            variable=self.selected_class,
        ).grid(column=3, row=0, padx=50, pady=20)

        loadout_labels = []
        Button(
            root,
            text="Randomise loadout for selected class",
            command=lambda: self.display_loadout(loadout_labels),
        ).grid(column=1, row=1, padx=40, pady=10)
        Button(
            root,
            text="Randomise class and loadout",
            command=lambda: [
                self.selected_class.set(DWARF_CLASSES[randrange(len(DWARF_CLASSES))]),
                self.display_loadout(loadout_labels),
            ],
        ).grid(column=2, row=1, padx=40, pady=10)

    def display_loadout(self, loadout_labels):
        if not self.selected_class.get():
            return

        loadout = randomise_loadout(self.selected_class.get(), self.data)

        for label in loadout_labels:
            label.grid_forget()
        loadout_labels.clear()

        loadout_frame = Frame(self.root)
        loadout_frame.grid(column=0, row=2, columnspan=4)
        loadout_frame.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="uniform")

        def make_list(mods: List) -> str:
            return " ".join(map(str, mods))

        def make_label(weapon: Weapon) -> Label:
            """Creates a label for the weapon in the loadout_frame"""
            return Label(
                loadout_frame,
                text=f"{weapon.name}\n{weapon.overclock}\n{make_list(weapon.mods_pattern)}",
            )

        loadout_labels.append(primary_label := make_label(loadout.primary))
        primary_label.grid(column=0, row=2, padx=10, pady=10)

        self.primary_image = ImageTk.PhotoImage(
            file=resource_path(loadout.primary.image)
        )
        loadout_labels.append(
            primary_image_label := Label(loadout_frame, image=self.primary_image)
        )
        primary_image_label.grid(column=1, row=2, padx=10, pady=10)

        loadout_labels.append(
            secondary_label := make_label(loadout.secondary),
        )
        secondary_label.grid(column=2, row=2, padx=10, pady=10)

        self.secondary_image = ImageTk.PhotoImage(
            file=resource_path(loadout.secondary.image)
        )
        loadout_labels.append(
            secondary_image_label := Label(loadout_frame, image=self.secondary_image)
        )
        secondary_image_label.grid(column=3, row=2, padx=10, pady=10)

        def make_gadget_label(gadget: Gadget) -> Label:
            """Creates a label for the gadget in the loadout_frame"""
            return Label(
                loadout_frame,
                text=f"{gadget.name}\n{make_list(gadget.mods_pattern)}",
            )

        loadout_labels.append(
            first_gadget_label := make_gadget_label(loadout.first_gadget)
        )
        first_gadget_label.grid(column=0, row=3, padx=10, pady=10)

        self.first_gadget_image = ImageTk.PhotoImage(
            file=resource_path(loadout.first_gadget.image)
        )
        loadout_labels.append(
            first_gadget_image_label := Label(
                loadout_frame, image=self.first_gadget_image
            )
        )
        first_gadget_image_label.grid(column=1, row=3, padx=10, pady=10)

        loadout_labels.append(
            second_gadget_label := make_gadget_label(loadout.second_gadget)
        )
        second_gadget_label.grid(column=2, row=3, padx=10, pady=10)

        self.second_gadget_image = ImageTk.PhotoImage(
            file=resource_path(loadout.second_gadget.image)
        )
        loadout_labels.append(
            second_gadget_image_label := Label(
                loadout_frame, image=self.second_gadget_image
            )
        )
        second_gadget_image_label.grid(column=3, row=3, padx=10, pady=10)

        loadout_labels.append(
            grenade_label := Label(loadout_frame, text=loadout.grenade.name)
        )
        grenade_label.grid(column=0, row=4, padx=10, pady=10)

        self.grenade_image = ImageTk.PhotoImage(
            file=resource_path(loadout.grenade.image)
        )
        loadout_labels.append(
            grenade_image_label := Label(loadout_frame, image=self.grenade_image)
        )
        grenade_image_label.grid(column=1, row=4, padx=10, pady=10)

        loadout_labels.append(
            pickaxe_label := Label(
                loadout_frame, text="Armor Rig\n" + " ".join(map(str, loadout.armor))
            )
        )
        pickaxe_label.grid(column=2, row=4, padx=10, pady=10)

        self.armor_image = ImageTk.PhotoImage(
            file=resource_path(self.data["armor"]["image"])
        )
        loadout_labels.append(
            armor_image_label := Label(loadout_frame, image=self.armor_image)
        )
        armor_image_label.grid(column=3, row=4, padx=10, pady=10)

        loadout_labels.append(
            pickaxe_label := Label(
                loadout_frame, text="Pickaxe\n" + " ".join(map(str, loadout.pickaxe))
            )
        )
        pickaxe_label.grid(column=0, row=5, padx=10, pady=10)

        self.pickaxe_image = ImageTk.PhotoImage(
            file=resource_path(self.data["pickaxe"]["image"])
        )
        loadout_labels.append(
            pickaxe_image_label := Label(loadout_frame, image=self.pickaxe_image)
        )
        pickaxe_image_label.grid(column=1, row=5, padx=10, pady=10)

        loadout_labels.append(
            passive_perks_label := Label(
                loadout_frame,
                text="Passive perks:\n" + "\n".join(map(str, loadout.passive_perks)),
            )
        )
        passive_perks_label.grid(column=2, row=5, padx=10, pady=10)

        loadout_labels.append(
            active_perks_label := Label(
                loadout_frame,
                text="\n".join(["Active perks:", *map(str, loadout.active_perks)]),
            )
        )
        active_perks_label.grid(column=3, row=5, padx=10, pady=10)


def randomise_loadout(dwarf_class, data):
    random_primary = data[dwarf_class]["primaries"][
        randrange(len(data[dwarf_class]["primaries"]))
    ]
    primary_weapon = Weapon(
        random_primary,
    )

    random_secondary = data[dwarf_class]["secondaries"][
        randrange(len(data[dwarf_class]["secondaries"]))
    ]
    secondary_weapon = Weapon(
        random_secondary,
    )

    first_gadget = Gadget(data[dwarf_class]["first_gadget"])

    second_gadget = Gadget(data[dwarf_class]["second_gadget"])

    random_grenade = randrange(len(data[dwarf_class]["grenades"]["names"]))
    grenade = Grenade(
        data[dwarf_class]["grenades"]["names"][random_grenade],
        data[dwarf_class]["grenades"]["images"][random_grenade],
    )

    armor = [randint(1, mod) for mod in data["armor"]["mods_pattern"]]

    pickaxe = [randint(1, mod) for mod in data["pickaxe"]["mods_pattern"]]

    passive_perks = sample(data["passive_perks"], 3)

    active_perks = sample(data["active_perks"], 2)

    return Loadout(
        primary_weapon,
        secondary_weapon,
        first_gadget,
        second_gadget,
        grenade,
        armor,
        pickaxe,
        passive_perks,
        active_perks,
    )


def resource_path(relative_path):
    """
    Function needed for pyinstaller to bundle everything into one
    standalone .exe
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def main():
    fp = open(resource_path("./resources/data.json"))
    data = json.load(fp)

    root = Tk()
    app = Main_Application(root, data)
    root.mainloop()

    fp.close()


if __name__ == "__main__":
    main()
