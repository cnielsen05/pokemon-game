from battleAttack import BattleAttack
from enums import BattleType, Status, PokemonStat
import json
import random

class Pokemon:
    def __init__(self, pokemon = None):
        self.name = "Pidgey"
        self.attackStat = 20
        self.defenseStat = 28
        self.spAttackStat = 19
        self.spDefenseStat = 28
        self.speedStat = 31
        self.HPStat = 19

        self.battleType1 = BattleType.FLYING
        self.battleType2 = BattleType.NORMAL

        self.battleAttacks = [BattleAttack("peck"), BattleAttack("tackle")]

        if pokemon:
            pokemonFileName = "pokemon/%s.json" % (pokemon)

            with open(pokemonFileName, 'r') as pokemonFile:
                data = json.load(pokemonFile)
                self.name = data["name"]
                self.attackStat = data["attackStat"]
                self.defenseStat = data["defenseStat"]
                self.spAttackStat = data["spAttackStat"]
                self.spDefenseStat = data["spDefenseStat"]
                self.speedStat = data["speedStat"]
                self.HPStat = data["HPStat"]
                self.battleType1 = data["battleType1"]
                self.battleType2 = data["battleType2"]
                self.battleAttacks.clear()
                for atk in data["battleAttacks"]:
                    self.battleAttacks.append(BattleAttack(atk))

        self.level = 1
        self.XP = 0
        self.statusCondition = Status.NONE

        self.currentHP = self.calculateMaxHp()


    def exportJson(self) -> str:
        data = {
            "name": self.name,
            "attackStat": self.attackStat,
            "defenseStat": self.defenseStat,
            "spAttackStat": self.spAttackStat,
            "spDefenseStat": self.spDefenseStat,
            "speedStat": self.speedStat,
            "HPStat": self.HPStat,
            "battleType1": self.battleType1,
            "battleType2": self.battleType2,
            "battleAttacks": []
        }
        for attack in self.battleAttacks:
            data["battleAttacks"].append(attack.name.lower())

        return json.dumps(data)


    def GetStatValue(self, stat: PokemonStat) -> int:
        if stat == PokemonStat.ATTACK:
            return 1 + (int)(1/5*self.attackStat*self.level)
        elif stat == PokemonStat.SPECIAL_ATTACK:
            return 1 + (int)(1/5*self.spAttackStat*self.level)
        elif stat == PokemonStat.DEFENSE:
            return 1 + (int)(1/5*self.defenseStat*self.level)
        elif stat == PokemonStat.SPECIAL_DEFENSE:
            return 1 + (int)(1/5*self.spDefenseStat*self.level)
        elif stat == PokemonStat.HP:
            return self.calculateMaxHp()
        elif stat == PokemonStat.SPEED:
            return 1 + (int)(1/5*self.speedStat*self.level)


    def calculateMaxHp(self) -> int:
        return 10 + (int)(self.HPStat * self.level * 3/5)


    def GetExperienceValue(self) -> int:
        return ( self.attackStat + self.defenseStat + self.spAttackStat + self.spDefenseStat + self.speedStat + self.HPStat ) * self.level


    def GainExperience(self, xp: int):
        self.XP += xp
        while self.XP >= (int)((1 + self.level / 5) * 450):
            self.LevelUp()
            self.XP -= (int)((1 + self.level / 5) * 450)


    def LevelUp(self):
        oldStats = {
            "HP": self.calculateMaxHp(),
            "Attack": self.GetStatValue(PokemonStat.ATTACK),
            "Special_Attack": self.GetStatValue(PokemonStat.SPECIAL_ATTACK),
            "Defense": self.GetStatValue(PokemonStat.DEFENSE),
            "Special_Defense": self.GetStatValue(PokemonStat.SPECIAL_DEFENSE),
            "Speed": self.GetStatValue(PokemonStat.SPEED),
        }

        self.level += 1

        newStats = {
            "HP": self.calculateMaxHp(),
            "Attack": self.GetStatValue(PokemonStat.ATTACK),
            "Special_Attack": self.GetStatValue(PokemonStat.SPECIAL_ATTACK),
            "Defense": self.GetStatValue(PokemonStat.DEFENSE),
            "Special_Defense": self.GetStatValue(PokemonStat.SPECIAL_DEFENSE),
            "Speed": self.GetStatValue(PokemonStat.SPEED),
        }
        print("%s has grown to level %s!" % (self.name, self.level))
        self.FullHealHP()
        for key in oldStats:
            if newStats[key] > oldStats[key]:
                print("%s has gained %s %s!" % (self.name, newStats[key] - oldStats[key], key))
        input("*Press ENTER to continue*")


    def FullHealHP(self):
        self.currentHP = self.calculateMaxHp()


    def RandomAttack(self, defender: any):
        # Defender is a Pokemon object
        randomNumber = random.randint(0, len(self.battleAttacks) - 1)
        randomAttack = self.battleAttacks[randomNumber]

        if (randomAttack.currentPP <= 0):
            print("%s struggles to choose an attack!")
            exit
        else:
            self.DoAttack(randomNumber, defender)


    def DoAttack(self, attackIndex: int, defender: any):
        attack = self.battleAttacks[attackIndex]

        attack.currentPP -= 1
        miss = random.randint(1, 100) > attack.accuracy
        if (miss):
            print("%s tries to use %s, but misses!" % (self.name, attack.name))
        else:
            print("%s uses %s!" % (self.name, attack.name))
            attackStatValue = self.GetStatValue(PokemonStat.ATTACK) if attack.isPhysical else self.GetStatValue(PokemonStat.SPECIAL_ATTACK)

            result = defender.ReceiveAttack(attack.type, attack.baseDmg, attackStatValue, attack.isPhysical)
            print(result)


    def ReceiveAttack(self, type: BattleType, attackBaseDmg: int, attackerOffensiveStatValue: int, isPhysical: bool) -> str:
        effectivenessMultiplier = Pokemon.CalculateDamageTypeMultiplier(self.battleType1, self.battleType2, type)
        if effectivenessMultiplier >= 2.0:
            print("It's super effective!")
        elif effectivenessMultiplier == 0:
            print("%s is completely unaffected!" % (self.name))
        elif effectivenessMultiplier < 1.0:
            print("It's not very effective!")
            
        defenseValue = self.GetStatValue(PokemonStat.DEFENSE) if isPhysical else self.GetStatValue(PokemonStat.SPECIAL_DEFENSE)
        damage = 2 + (int)((((attackBaseDmg * effectivenessMultiplier) / 5.0 + 2 ) * (attackerOffensiveStatValue / defenseValue) / 3.0) + random.randint(0,3))
        crit = random.randint(0,9) > 8
        critString = ""
        if crit:
            damage = (int)(damage * 1.75)
            critString = "CRITICAL HIT!"
        self.currentHP -= damage
        return "%s received %s damage. %s" % (self.name, damage, critString)


    # This function calls the other function, and multiplies the two multipliers together to get a final product
    def CalculateDamageTypeMultiplier(defType1: BattleType, defType2: BattleType, attackType: BattleType) -> int:
        multiplierOne = Pokemon.CalculateDamageTypeMultiplierInner(defType1, attackType)
        multiplierTwo = Pokemon.CalculateDamageTypeMultiplierInner(defType2, attackType)
        return multiplierOne * multiplierTwo


    # This function returns the multiplier for one attack type on one defense type
    def CalculateDamageTypeMultiplierInner(defType: BattleType, attackType: BattleType) -> int:
        multiplier = 1.0

        # Damage type advantages
        if (defType == BattleType.BUG):
            if (attackType == BattleType.FIGHTING):
                multiplier = 0.5
            elif (attackType == BattleType.GROUND):
                multiplier = 0.5
            elif (attackType == BattleType.GRASS):
                multiplier = 0.5
            elif (attackType == BattleType.FLYING):
                multiplier = 2
            elif (attackType == BattleType.ROCK):
                multiplier = 2
            elif (attackType == BattleType.FIRE):
                multiplier = 2
        elif (defType == BattleType.DARK):
            if (attackType == BattleType.PSYCHIC):
                multiplier = 0
            elif (attackType == BattleType.DARK):
                multiplier = 0.5
            elif (attackType == BattleType.GHOST):
                multiplier = 0.5
            elif (attackType == BattleType.FIGHTING):
                multiplier = 2
            elif (attackType == BattleType.BUG):
                multiplier = 2
            elif (attackType == BattleType.FAIRY):
                multiplier = 2
        elif (defType == BattleType.NORMAL):
            if (attackType == BattleType.GHOST):
                multiplier = 0
            elif (attackType == BattleType.FIGHTING):
                multiplier = 2
        elif (defType == BattleType.FIGHTING):
            if (attackType == BattleType.ROCK):
                multiplier = 0.5
            elif (attackType == BattleType.DARK):
                multiplier = 0.5
            elif (attackType == BattleType.BUG):
                multiplier = 0.5
            elif (attackType == BattleType.FLYING):
                multiplier = 2
            elif (attackType == BattleType.PSYCHIC):
                multiplier = 2
            elif (attackType == BattleType.FAIRY):
                multiplier = 2
        elif (defType == BattleType.FLYING):
            if (attackType == BattleType.FIGHTING):
                multiplier = 0.5
            elif (attackType == BattleType.GRASS):
                multiplier = 0.5
            elif (attackType == BattleType.BUG):
                multiplier = 0.5
            elif (attackType == BattleType.ROCK):
                multiplier = 2
            elif (attackType == BattleType.ELECTRIC):
                multiplier = 2
            elif (attackType == BattleType.ICE):
                multiplier = 2
        elif (defType == BattleType.POISON):
            if (attackType == BattleType.FIGHTING):
                multiplier = 0.5
            elif (attackType == BattleType.POISON):
                multiplier = 0.5
            elif (attackType == BattleType.BUG):
                multiplier = 0.5
            elif (attackType == BattleType.GRASS):
                multiplier = 0.5
            elif (attackType == BattleType.FAIRY):
                multiplier = 0.5
            elif (attackType == BattleType.GROUND):
                multiplier = 2
            elif (attackType == BattleType.PSYCHIC):
                multiplier = 2
        elif (defType == BattleType.GROUND):
            if (attackType == BattleType.ELECTRIC):
                multiplier = 0
            elif (attackType == BattleType.POISON):
                multiplier = 0.5
            elif (attackType == BattleType.ROCK):
                multiplier = 0.5
            elif (attackType == BattleType.WATER):
                multiplier = 2
            elif (attackType == BattleType.GRASS):
                multiplier = 2
            elif (attackType == BattleType.ICE):
                multiplier = 2
        elif (defType == BattleType.ROCK):
            if (attackType == BattleType.NORMAL):
                multiplier = 0.5
            elif (attackType == BattleType.FLYING):
                multiplier = 0.5
            elif (attackType == BattleType.POISON):
                multiplier = 0.5
            elif (attackType == BattleType.FIRE):
                multiplier = 0.5
            elif (attackType == BattleType.FIGHTING):
                multiplier = 2
            elif (attackType == BattleType.GROUND):
                multiplier = 2
            elif (attackType == BattleType.STEEL):
                multiplier = 2
            elif (attackType == BattleType.WATER):
                multiplier = 2
            elif (attackType == BattleType.GRASS):
                multiplier = 2
        elif (defType == BattleType.GHOST):
            if (attackType == BattleType.NORMAL):
                multiplier = 0
            elif (attackType == BattleType.FIGHTING):
                multiplier = 0
            elif (attackType == BattleType.POISON):
                multiplier = 0.5
            elif (attackType == BattleType.BUG):
                multiplier = 0.5
            elif (attackType == BattleType.GHOST):
                multiplier = 2
            elif (attackType == BattleType.DARK):
                multiplier = 2
        elif (defType == BattleType.STEEL):
            if (attackType == BattleType.POISON):
                multiplier = 0
            elif (attackType == BattleType.NORMAL):
                multiplier = 0.5
            elif (attackType == BattleType.FLYING):
                multiplier = 0.5
            elif (attackType == BattleType.ROCK):
                multiplier = 0.5
            elif (attackType == BattleType.BUG):
                multiplier = 0.5
            elif (attackType == BattleType.STEEL):
                multiplier = 0.5
            if (attackType == BattleType.GRASS):
                multiplier = 0.5
            elif (attackType == BattleType.PSYCHIC):
                multiplier = 0.5
            elif (attackType == BattleType.ICE):
                multiplier = 0.5
            elif (attackType == BattleType.DRAGON):
                multiplier = 0.5
            elif (attackType == BattleType.FAIRY):
                multiplier = 0.5
            elif (attackType == BattleType.FIGHTING):
                multiplier = 2
            elif (attackType == BattleType.GROUND):
                multiplier = 2
            elif (attackType == BattleType.FIRE):
                multiplier = 2
        elif (defType == BattleType.FIRE):
            if (attackType == BattleType.BUG):
                multiplier = 0.5
            elif (attackType == BattleType.STEEL):
                multiplier = 0.5
            elif (attackType == BattleType.FIRE):
                multiplier = 0.5
            elif (attackType == BattleType.GRASS):
                multiplier = 0.5
            elif (attackType == BattleType.ICE):
                multiplier = 0.5
            elif (attackType == BattleType.FAIRY):
                multiplier = 0.5
            elif (attackType == BattleType.GROUND):
                multiplier = 2
            elif (attackType == BattleType.ROCK):
                multiplier = 2
            elif (attackType == BattleType.WATER):
                multiplier = 2
        elif (defType == BattleType.WATER):
            if (attackType == BattleType.STEEL):
                multiplier = 0.5
            elif (attackType == BattleType.FIRE):
                multiplier = 0.5
            elif (attackType == BattleType.WATER):
                multiplier = 0.5
            elif (attackType == BattleType.ICE):
                multiplier = 0.5
            elif (attackType == BattleType.GRASS):
                multiplier = 2
            elif (attackType == BattleType.ELECTRIC):
                multiplier = 2
        elif (defType == BattleType.GRASS):
            if (attackType == BattleType.GROUND):
                multiplier = 0.5
            elif (attackType == BattleType.WATER):
                multiplier = 0.5
            elif (attackType == BattleType.GRASS):
                multiplier = 0.5
            elif (attackType == BattleType.ELECTRIC):
                multiplier = 0.5
            elif (attackType == BattleType.FLYING):
                multiplier = 2
            elif (attackType == BattleType.POISON):
                multiplier = 2
            elif (attackType == BattleType.BUG):
                multiplier = 2
            elif (attackType == BattleType.FIRE):
                multiplier = 2
            elif (attackType == BattleType.ICE):
                multiplier = 2
        elif (defType == BattleType.ELECTRIC):
            if (attackType == BattleType.FLYING):
                multiplier = 0.5
            elif (attackType == BattleType.STEEL):
                multiplier = 0.5
            elif (attackType == BattleType.ELECTRIC):
                multiplier = 0.5
            elif (attackType == BattleType.GROUND):
                multiplier = 2
        elif (defType == BattleType.PSYCHIC):
            if (attackType == BattleType.FIGHTING):
                multiplier = 0.5
            elif (attackType == BattleType.PSYCHIC):
                multiplier = 0.5
            elif (attackType == BattleType.BUG):
                multiplier = 2
            elif (attackType == BattleType.GHOST):
                multiplier = 2
            elif (attackType == BattleType.DARK):
                multiplier = 2
        elif (defType == BattleType.ICE):
            if (attackType == BattleType.ICE):
                multiplier = 0.5
            elif (attackType == BattleType.FIRE):
                multiplier = 0.5
            elif (attackType == BattleType.FIRE):
                multiplier = 2
            elif (attackType == BattleType.STEEL):
                multiplier = 2
            elif (attackType == BattleType.ROCK):
                multiplier = 2
            elif (attackType == BattleType.FIGHTING):
                multiplier = 2
        elif (defType == BattleType.DRAGON):
            if (attackType == BattleType.FIRE):
                multiplier = 0.5
            elif (attackType == BattleType.WATER):
                multiplier = 0.5
            elif (attackType == BattleType.GRASS):
                multiplier = 0.5
            elif (attackType == BattleType.ELECTRIC):
                multiplier = 0.5
            elif (attackType == BattleType.ICE):
                multiplier = 2
            elif (attackType == BattleType.DRAGON):
                multiplier = 2
            elif (attackType == BattleType.FAIRY):
                multiplier = 2
        elif (defType == BattleType.FAIRY):
            if (attackType == BattleType.DRAGON):
                multiplier = 0
            elif (attackType == BattleType.FIGHTING):
                multiplier = 0.5
            elif (attackType == BattleType.BUG):
                multiplier = 0.5
            elif (attackType == BattleType.DARK):
                multiplier = 0.5
            elif (attackType == BattleType.STEEL):
                multiplier = 2
            elif (attackType == BattleType.POISON):
                multiplier = 2

        return multiplier


if __name__ == "__main__":
    pokemon = Pokemon()
    with open("pokemon/%s.json" % (pokemon.name.lower()), 'w') as outfile:
        outfile.write(pokemon.exportJson())