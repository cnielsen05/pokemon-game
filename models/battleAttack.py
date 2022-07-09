from common.enums import BattleType, CombatModifiers, EffectType, Targeting
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
        self.effects = [MoveEffect()]
        
        if attackname:
            attackFileName = "data/attacks/%s.json" % (attackname.lower())

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
                self.effects = []
                for effect in data["effects"]:
                    self.effects.append(MoveEffect(effect["target"], effect["effectType"], effect["effectDetail"], effect["chance"]))

        self.currentPP = self.maxPP


    def exportJson(self) -> str:
        data = {
            "name": self.name,
            "baseDmg": self.baseDmg,
            "type": self.type,
            "isPhysical": self.isPhysical,
            "maxPP": self.maxPP,
            "accuracy": self.accuracy,
            "effects": []
        }
        for effect in self.effects:
            data["effects"].append({"target": effect.target, "effectType": effect.effectType, "effectDetail": effect.effectDetail, "chance": effect.chance})
        
        return json.dumps(data)

        

class MoveEffect():
    def __init__(self, t: Targeting = None, eType: EffectType = None, eDetail: any = None, c: int = None):
        self.target = Targeting.SELF
        self.effectType = EffectType.ADD_COMBAT_MODIFIER
        self.effectDetail = CombatModifiers.ACCURACY_UP
        self.chance = 100

        if t:
            self.target = t
        if eType:
            self.effectType = eType
        if eDetail:
            self.effectDetail = eDetail
        if c:
            self.chance = c


if __name__ == "__main__":
    tackle = BattleAttack()
    with open("data/attacks/tackle.json", 'w') as outfile:
        outfile.write(tackle.exportJson())
