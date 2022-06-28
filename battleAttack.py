from enums import BattleType
import json

class BattleAttack:

    def __init__(self, attackname = None, unlockLevel = None):
        self.name = "Tackle"
        self.baseDmg = 20
        self.type = BattleType.NORMAL
        self.isPhysical = True
        self.maxPP = 20
        self.accuracy = 90
        self.unlockLevel = 1
        
        if attackname:
            attackFileName = "attacks/%s.json" % (attackname.lower())

            with open(attackFileName, 'r') as attackFile:
                data = json.load(attackFile)
                self.name = data["name"]
                self.baseDmg = data["baseDmg"]
                self.type = data["type"]
                self.isPhysical = data["isPhysical"]
                self.maxPP = data["maxPP"]
                self.accuracy = data["accuracy"]
                if unlockLevel:
                    self.unlockLevel = unlockLevel

        self.currentPP = self.maxPP


    def exportJson(self) -> str:
        data = {
            "name": self.name,
            "baseDmg": self.baseDmg,
            "type": self.type,
            "isPhysical": self.isPhysical,
            "maxPP": self.maxPP,
            "accuracy": self.accuracy
        }
        return json.dumps(data)


class MoveData():
    def __init__(self):
        self.Move = "Tackle"
        self.UnlockLevel = 1


if __name__ == "__main__":
    tackle = BattleAttack()
    with open("attacks/tackle.json", 'w') as outfile:
        outfile.write(tackle.exportJson())
