import json

from MainApplication import *
from Loadout import *

def main():
    fp = open(resource_path("./resources/data.json"))
    data = json.load(fp)

    root = Tk()
    app = MainApplication(root, data)
    root.mainloop()

    fp.close()

if __name__ == "__main__":
    main()