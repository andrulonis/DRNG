from random import randint, randrange, sample

DWARF_CLASSES = ["gunner", "scout", "engineer", "driller"]

class Weapon:
    def __init__(self, data):
        self.name = data["name"]
        self.overclock = data["overclocks"][randrange(len(data["overclocks"]))]
        self.mods_pattern = [randint(1, mod) for mod in data["mods_pattern"]]
        self.image = data["image"]

class Gadget:
    def __init__(self, data):
        self.name = data["name"]
        self.mods_pattern = [randint(1, mod) for mod in data["mods_pattern"]]
        self.image = data["image"]

class Grenade:
    def __init__(self, data, grenade_index):
        self.name = data["names"][grenade_index]
        self.image = data["images"][grenade_index]

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
    primary_weapon = Weapon(data[dwarf_class]["primaries"][randrange(len(data[dwarf_class]["primaries"]))])

    secondary_weapon = Weapon(data[dwarf_class]["secondaries"][randrange(len(data[dwarf_class]["secondaries"]))])

    first_gadget = Gadget(data[dwarf_class]["first_gadget"])

    second_gadget = Gadget(data[dwarf_class]["second_gadget"])

    grenade = Grenade(data[dwarf_class]["grenades"], randrange(len(data[dwarf_class]["grenades"]["names"])))

    armor = [randint(1,mod) for mod in data["armor"]["mods_pattern"]]

    pickaxe = [randint(1,mod) for mod in data["pickaxe"]["mods_pattern"]]

    passive_perks = sample(data["passive_perks"], 3)

    active_perks = sample(data["active_perks"], 2)

    return Loadout(primary_weapon, secondary_weapon, first_gadget, second_gadget, grenade, armor, pickaxe, passive_perks, active_perks)