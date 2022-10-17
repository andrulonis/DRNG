from tkinter import *
from PIL import ImageTk
import sys
import os

from Loadout import *

GRID_PAD_VAL = 10

# Function needed for pyinstaller to bundle everything into one standalone .exe
def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class MainApplication:
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

        self.gunner_icon = PhotoImage(file=resource_path("./resources/icons/gunner_icon.png"))
        self.scout_icon = PhotoImage(file=resource_path("./resources/icons/scout_icon.png"))
        self.engineer_icon = PhotoImage(file=resource_path("./resources/icons/engineer_icon.png"))
        self.driller_icon = PhotoImage(file=resource_path("./resources/icons/driller_icon.png"))

        Radiobutton(
            buttons_frame, bg="green", 
            value="gunner", 
            image=self.gunner_icon, 
            indicatoron=0, 
            variable=self.selected_class
        ).grid(column=0, row=0, padx=50, pady=20)

        Radiobutton(
            buttons_frame, 
            bg="blue", 
            value="scout", 
            image=self.scout_icon, 
            indicatoron=0, 
            variable=self.selected_class
        ).grid(column=1, row=0, padx=50, pady=20)

        Radiobutton(
            buttons_frame, 
            bg="red", 
            value="engineer", 
            image=self.engineer_icon, 
            indicatoron=0, 
            variable=self.selected_class
        ).grid(column=2, row=0, padx=50, pady=20)

        Radiobutton(
            buttons_frame, 
            bg="yellow", 
            value="driller", 
            image=self.driller_icon, 
            indicatoron=0, 
            variable=self.selected_class
        ).grid(column=3, row=0, padx=50, pady=20)

        loadout_labels = []
        
        Button(
            root, 
            text="Randomise loadout for selected class", 
            command=lambda : self.display_random_loadout(loadout_labels)
        ).grid(column=1, row=1, padx=40, pady=10)

        Button(
            root,
            text="Randomise class and loadout",
            command=lambda : [self.selected_class.set(DWARF_CLASSES[randrange(len(DWARF_CLASSES))]), 
            self.display_random_loadout(loadout_labels)]
        ).grid(column=2, row=1, padx=40, pady=10)
    
    def display_random_loadout(self, loadout_labels):
        if (not self.selected_class.get()):
            return
        
        loadout = randomise_loadout(self.selected_class.get(), self.data)
        
        for label in loadout_labels:
            label.grid_forget()
        loadout_labels.clear()

        loadout_frame = Frame(self.root)
        loadout_frame.grid(column=0, row=2, columnspan=4)
        loadout_frame.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="uniform")

        def make_list(mods):
            return " ".join(map(str, mods))

        def make_weapon_label(weapon):
            return Label(
                loadout_frame,
                text=f"{weapon.name}\n{weapon.overclock}\n{make_list(weapon.mods_pattern)}"
            )

        def make_image_label(image):
            return Label(
                loadout_frame,
                image=image
            )
        
        def make_gadget_label(gadget):
            return Label(
                loadout_frame,
                text=f"{gadget.name}\n{make_list(gadget.mods_pattern)}"
            )
        
        def put_item_labels(text_label, image_label, col, row):
            loadout_labels.append(text_label)
            text_label.grid(column=col, row=row, padx=GRID_PAD_VAL, pady=GRID_PAD_VAL)

            loadout_labels.append(image_label)
            image_label.grid(column=col+1, row=row, padx=GRID_PAD_VAL, pady=GRID_PAD_VAL)

        self.primary_image = ImageTk.PhotoImage(file=resource_path(loadout.primary.image))
        put_item_labels(make_weapon_label(loadout.primary), make_image_label(self.primary_image), 0, 2)

        self.secondary_image = ImageTk.PhotoImage(file=resource_path(loadout.secondary.image))
        put_item_labels(make_weapon_label(loadout.secondary), make_image_label(self.secondary_image), 2, 2)

        self.first_gadget_image = ImageTk.PhotoImage(file=resource_path(loadout.first_gadget.image))
        put_item_labels(make_gadget_label(loadout.first_gadget), make_image_label(self.first_gadget_image), 0, 3)

        self.second_gadget_image = ImageTk.PhotoImage(file=resource_path(loadout.second_gadget.image))
        put_item_labels(make_gadget_label(loadout.second_gadget), make_image_label(self.second_gadget_image), 2, 3)

        self.grenade_image = ImageTk.PhotoImage(file=resource_path(loadout.grenade.image))
        put_item_labels(Label(loadout_frame, text=loadout.grenade.name), make_image_label(self.grenade_image), 0, 4)

        self.armor_image = ImageTk.PhotoImage(file=resource_path(self.data["armor"]["image"]))
        put_item_labels(Label(loadout_frame, text= f"Armor Rig\n{make_list(loadout.armor)}"), make_image_label(self.armor_image), 2, 4)

        self.pickaxe_image = ImageTk.PhotoImage(file=resource_path(self.data["pickaxe"]["image"]))
        put_item_labels(Label(loadout_frame, text=f"Pickaxe\n{make_list(loadout.pickaxe)}"), make_image_label(self.pickaxe_image), 0, 5)

        loadout_labels.append(passive_perks_label := Label(loadout_frame, text="Passive perks:\n" + "\n".join(map(str, loadout.passive_perks))))
        passive_perks_label.grid(column=2, row=5, padx=GRID_PAD_VAL, pady=GRID_PAD_VAL)

        loadout_labels.append(active_perks_label := Label(loadout_frame, text= "Active perks:\n" + "\n".join(map(str, loadout.active_perks))))
        active_perks_label.grid(column=3, row=5, padx=GRID_PAD_VAL, pady=GRID_PAD_VAL)