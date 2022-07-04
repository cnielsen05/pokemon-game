import json
from enums import ItemType


class Route:
    def __init__(self, id: str = None):
        self.Name = "Route 1"
        self.id = "routeone"
        self.Length = 30

        self.WildPokemonList = [
            "flokefish", 
            "flokefish", 
            "flokefish", 
            "sleepoud", 
            "sleepoud", 
            "scorpoint", 
            "flokefish",
            "stackuri",
            "jareanpidgey", 
            "jareanpidgey", 
            "jareanpidgey",
            "hebike",
            "hebike",
            "hebike",
            "hebike",
            "hebike",
            "clovney",
            "clovney",
            "stackuri",
            "stackuri",
            "stackuri"]

        self.WildPokemonLevelRange = [1,2]

        self.HiddenItemList = [ItemType.POTION, ItemType.POKEFEAST, ItemType.POKEBALL]

        self.TrainerBattles = [None] * self.Length
        self.TrainerBattles[9] = {
            "Name": "Newbie Bobby",
            "Money": 200,
            "StartLine": "Check out my awesome first Pokemon!",
            "EndLine": "Aww man, it stopped moving. What do I do now?",
            "Pokemon": [
                {
                    "name": "flokefish",
                    "level": 1
                }
            ]
        }
        self.TrainerBattles[19] = {
            "Name": "Enthusiastic Noob Steven",
            "Money": 300,
            "StartLine": "I've been preparing for this day my whole life! I'll show you some tips.",
            "EndLine": "Maybe I got a little full of myself, I'll focus on the basics and become a great trainer one day!",
            "Pokemon": [
                {
                    "name": "clovney",
                    "level": 2
                },
                {
                    "name": "hebike",
                    "level": 1
                }
            ]
        }

        self.TrainerBattles[29] = {
            "Name": "Rich Kid David",
            "Money": 1000,
            "StartLine": "My parents got me all the items I could ever need! Nobody can keep up with me!",
            "EndLine": "Wow, I guess being rich isn't enough by itself. I'll try harder next time!",
            "Pokemon": [
                {
                    "name": "atsebi",
                    "level": 1
                },
                {
                    "name": "leafox",
                    "level": 1
                },
                {
                    "name": "nardent",
                    "level": 1
                },
                {
                    "name": "jareanpidgey",
                    "level": 1
                },
                {
                    "name": "clovney",
                    "level": 1
                },
                {
                    "name": "implien",
                    "level": 1
                }
            ]
        }

        if id is not None:
            routeFileName = "routes/%s.json" % (id)

            with open(routeFileName, 'r') as routeFile:
                data = json.load(routeFile)
                self.Name = data["Name"]
                self.id = data["id"]
                self.WildPokemonList = data["WildPokemonList"]
                self.WildPokemonLevelRange = data["WildPokemonLevelRange"]
                self.HiddenItemList = data["HiddenItemList"]
                self.TrainerBattles = data["TrainerBattles"]


    def ExportJson(self) -> str:
        data = {
            "Name": self.Name,
            "id": self.id,
            "Length": self.Length,
            "WildPokemonList": self.WildPokemonList,
            "WildPokemonLevelRange": self.WildPokemonLevelRange,
            "HiddenItemList": self.HiddenItemList,
            "TrainerBattles": self.TrainerBattles
        }

        return json.dumps(data)


if __name__ == "__main__":
    route = Route()
    with open("routes/%s.json" % (route.id), 'w') as outfile:
        outfile.write(route.ExportJson())