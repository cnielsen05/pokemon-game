import time
from typing import List
from battleAttack import BattleAttack
from engineUtilities import EngineUtilities
from enums import BattleType, CombatModifiers, Status, PokemonStat, Targeting, EffectType
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
        self.catchFactor = 0.25
        self.evolveLevel = 0
        self.evolutionName = ""

        self.accuracyModifierLevel = 0
        self.attackModifierLevel = 0
        self.specialAttackModifierLevel = 0
        self.defenseModifierLevel = 0
        self.specialDefenseModifierLevel = 0
        self.speedModifierLevel = 0
        self.isFlinched = False

        self.battleType1 = BattleType.FLYING
        self.battleType2 = BattleType.NORMAL

        self.battleAttacks = [BattleAttack("peck", 2), BattleAttack("tackle", 1)]

        if pokemon:
            pokemonFileName = "data/pokemon/%s.json" % (pokemon.replace(" ", ""))

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
                self.catchFactor = data["catchFactor"]
                self.evolveLevel = data["evolveLevel"]
                self.evolutionName = data["evolutionName"]
                self.battleAttacks.clear()
                for atk in data["battleAttacks"]:
                    self.battleAttacks.append(BattleAttack(atk["Move"], atk["UnlockLevel"]))

        self.level = 1
        self.XP = 0
        self.statusCondition = Status.NONE
        self.combatModifiers = []

        self.currentHP = self.CalculateMaxHp()


    def ExportJson(self) -> str:
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
            "evolveLevel": self.evolveLevel,
            "evolutionName": self.evolutionName,
            "battleAttacks": []
        }
        for attack in self.battleAttacks:
            data["battleAttacks"].append({"Move": attack.name.lower(), "UnlockLevel": attack.unlockLevel})

        return json.dumps(data)


    def GetBattleAttacks(self) -> List[BattleAttack]:
        unlockedAttacks = []
        for attack in self.battleAttacks:
            if attack.unlockLevel <= self.level:
                unlockedAttacks.append(attack)

        return unlockedAttacks


    def AddStatusEffect(self, status: Status):
        self.statusCondition = status


    def AddCombatModifier(self, effect: CombatModifiers):
        # Accuracy Modifier
        if effect == CombatModifiers.ACCURACY_DOWN:
            self.accuracyModifierLevel -= 1
            print("%s's ACCURACY fell!" % (self.name))
        elif effect == CombatModifiers.ACCURACY_DOWN_DOWN:
            self.accuracyModifierLevel -= 2
            print("%s's ACCURACY fell sharply!" % (self.name))
        elif effect == CombatModifiers.ACCURACY_UP:
            self.accuracyModifierLevel += 1
            print("%s's ACCURACY rose!" % (self.name))
        elif effect == CombatModifiers.ACCURACY_UP_UP:
            self.accuracyModifierLevel += 2
            print("%s's ACCURACY rose sharply!" % (self.name))

        # Attack Modifier
        elif effect == CombatModifiers.ATK_DOWN:
            self.attackModifierLevel -= 1
            print("%s's ATTACK fell!" % (self.name))
        elif effect == CombatModifiers.ATK_DOWN_DOWN:
            self.attackModifierLevel -= 2
            print("%s's ATTACK fell sharply!" % (self.name))
        elif effect == CombatModifiers.ATK_UP:
            self.attackModifierLevel += 1
            print("%s's ATTACK rose!" % (self.name))
        elif effect == CombatModifiers.ATK_UP_UP:
            self.attackModifierLevel += 2
            print("%s's ATTACK rose sharply!" % (self.name))

        # SpAttack Modifier
        elif effect == CombatModifiers.SPATK_DOWN:
            self.specialAttackModifierLevel -= 1
            print("%s's SPECIAL ATTACK fell!" % (self.name))
        elif effect == CombatModifiers.SPATK_DOWN_DOWN:
            self.specialAttackModifierLevel -= 2
            print("%s's SPECIAL ATTACK fell sharply!" % (self.name))
        elif effect == CombatModifiers.SPATK_UP:
            self.specialAttackModifierLevel += 1
            print("%s's SPECIAL ATTACK rose!" % (self.name))
        elif effect == CombatModifiers.SPATK_UP_UP:
            self.specialAttackModifierLevel += 2
            print("%s's SPECIAL ATTACK rose sharply!" % (self.name))

        # Defense Modifier
        elif effect == CombatModifiers.DEF_DOWN:
            self.defenseModifierLevel -= 1
            print("%s's DEFENSE fell!" % (self.name))
        elif effect == CombatModifiers.DEF_DOWN_DOWN:
            self.defenseModifierLevel -= 2
            print("%s's DEFENSE fell sharply!" % (self.name))
        elif effect == CombatModifiers.DEF_UP:
            self.defenseModifierLevel += 1
            print("%s's DEFENSE rose!" % (self.name))
        elif effect == CombatModifiers.DEF_UP_UP:
            self.defenseModifierLevel += 2
            print("%s's DEFENSE rose sharply!" % (self.name))

        # SpDef Modifier
        elif effect == CombatModifiers.SPDEF_DOWN:
            self.specialAttackModifierLevel -= 1
            print("%s's SPECIAL DEFENSE fell!" % (self.name))
        elif effect == CombatModifiers.SPDEF_DOWN_DOWN:
            self.specialAttackModifierLevel -= 2
            print("%s's SPECIAL DEFENSE fell sharply!" % (self.name))
        elif effect == CombatModifiers.SPDEF_UP:
            self.specialAttackModifierLevel += 1
            print("%s's SPECIAL DEFENSE rose!" % (self.name))
        elif effect == CombatModifiers.SPDEF_UP_UP:
            self.specialAttackModifierLevel += 2
            print("%s's SPECIAL DEFENSE rose sharply!" % (self.name))

        # Speed Modifier
        elif effect == CombatModifiers.SPEED_DOWN:
            self.speedModifierLevel -= 1
            print("%s's SPECIAL ATTACK fell!" % (self.name))
        elif effect == CombatModifiers.SPEED_DOWN_DOWN:
            self.speedModifierLevel -= 2
            print("%s's SPECIAL ATTACK fell sharply!" % (self.name))
        elif effect == CombatModifiers.SPEED_UP:
            self.speedModifierLevel += 1
            print("%s's SPECIAL ATTACK rose!" % (self.name))
        elif effect == CombatModifiers.SPEED_UP_UP:
            self.speedModifierLevel += 2
            print("%s's SPECIAL ATTACK rose sharply!" % (self.name))

        elif (effect == CombatModifiers.CHARGED_UP):
            alreadyCharged = False
            for mod in self.combatModifiers:
                if mod == CombatModifiers.CHARGED_UP:
                    alreadyCharged = True

            if not alreadyCharged:
                self.combatModifiers.append(effect)

        elif (effect == CombatModifiers.BIND):
            alreadyBound = False
            for mod in self.combatModifiers:
                if mod == CombatModifiers.BIND:
                    alreadyBound = True

            if not alreadyBound:
                self.combatModifiers.append(effect)

        # Ensure combat modifiers all remain in the -4 to +4 range
        # Accuracy
        if self.accuracyModifierLevel < -4:
            self.accuracyModifierLevel = -4
            print("%s's ACCURACY cannot fall any lower!" % (self.name))
        elif self.accuracyModifierLevel > 4:
            self.accuracyModifierLevel = 4
            print("%s's ACCURACY cannot raise any higher!" % (self.name))

        # Attack
        if self.attackModifierLevel < -4:
            self.attackModifierLevel = -4
            print("%s's SPECIAL ATTACK cannot fall any lower!" % (self.name))
        elif self.attackModifierLevel > 4:
            self.attackModifierLevel = 4
            print("%s's SPECIAL ATTACK cannot raise any higher!" % (self.name))

        # Special Attack
        if self.specialAttackModifierLevel < -4:
            self.specialAttackModifierLevel = -4
            print("%s's SPECIAL ATTACK cannot fall any lower!" % (self.name))
        elif self.specialAttackModifierLevel > 4:
            self.specialAttackModifierLevel = 4
            print("%s's SPECIAL ATTACK cannot raise any higher!" % (self.name))

        # Defense
        if self.defenseModifierLevel < -4:
            self.defenseModifierLevel = -4
            print("%s's DEFENSE cannot fall any lower!" % (self.name))
        elif self.defenseModifierLevel > 4:
            self.defenseModifierLevel = 4
            print("%s's DEFENSE cannot raise any higher!" % (self.name))

        # Special Defense
        if self.specialDefenseModifierLevel < -4:
            self.specialDefenseModifierLevel = -4
            print("%s's SPECIAL DEFENSE cannot fall any lower!" % (self.name))
        elif self.specialDefenseModifierLevel > 4:
            self.specialDefenseModifierLevel = 4
            print("%s's SPECIAL DEFENSE cannot raise any higher!" % (self.name))

        # Speed
        if self.speedModifierLevel < -4:
            self.speedModifierLevel = -4
            print("%s's SPEED cannot fall any lower!" % (self.name))
        elif self.speedModifierLevel > 4:
            self.speedModifierLevel = 4
            print("%s's SPEED cannot raise any higher!" % (self.name))


    def GetStatValue(self, stat: PokemonStat) -> int:
        modFactor = 1.0
        
        if stat == PokemonStat.ATTACK:
            if self.attackModifierLevel > 0:
                modFactor += (0.75 * self.attackModifierLevel)
            elif self.attackModifierLevel < 0:
                modFactor += (0.2 * self.attackModifierLevel)

            if self.statusCondition == Status.BURNED:
                modFactor *= 0.5

            return 1 + (int)(1.0/5*self.attackStat*self.level*modFactor)

        elif stat == PokemonStat.SPECIAL_ATTACK:
            if self.specialAttackModifierLevel > 0:
                modFactor += (0.75 * self.specialAttackModifierLevel)
            elif self.specialAttackModifierLevel < 0:
                modFactor += (0.2 * self.specialAttackModifierLevel)

            if self.statusCondition == Status.CURSED:
                modFactor *= 0.5

            return 1 + (int)(1.0/5*self.spAttackStat*self.level*modFactor)

        elif stat == PokemonStat.DEFENSE:
            if self.defenseModifierLevel > 0:
                modFactor += (0.75 * self.defenseModifierLevel)
            elif self.defenseModifierLevel < 0:
                modFactor += (0.2 * self.defenseModifierLevel)

            return 1 + (int)(1.0/5*self.defenseStat*self.level*modFactor)

        elif stat == PokemonStat.SPECIAL_DEFENSE:
            if self.specialDefenseModifierLevel > 0:
                modFactor += (0.75 * self.specialDefenseModifierLevel)
            elif self.specialDefenseModifierLevel < 0:
                modFactor += (0.2 * self.specialDefenseModifierLevel)

            return 1 + (int)(1.0/5*self.spDefenseStat*self.level*modFactor)

        elif stat == PokemonStat.HP:
            return self.CalculateMaxHp()

        elif stat == PokemonStat.SPEED:
            if self.speedModifierLevel > 0:
                modFactor += (0.75 * self.speedModifierLevel)
            elif self.speedModifierLevel < 0:
                modFactor += (0.2 * self.speedModifierLevel)

            if self.statusCondition == Status.PARALYZED:
                modFactor *= 0.5

            return 1 + (int)(1.0/5*self.speedStat*self.level*modFactor)


    def CalculateMaxHp(self) -> int:
        return 10 + (int)(self.HPStat * self.level * 3/5)


    def GetExperienceValue(self) -> int:
        return ( self.attackStat + self.defenseStat + self.spAttackStat + self.spDefenseStat + self.speedStat + self.HPStat ) * self.level


    def GainExperience(self, xp: int):
        self.XP += xp
        nextLevelXP = self.CalculateNextLevelExperience()
        while self.XP >= nextLevelXP:
            self.LevelUp()
            self.XP -= nextLevelXP
            nextLevelXP = self.CalculateNextLevelExperience()


    def CalculateNextLevelExperience(self):
        return (int)((1 + self.level / 5) * 300 + (int)(self.level/3) * self.GetExperienceValue())


    def LevelUp(self):
        oldStats = {
            "HP": self.CalculateMaxHp(),
            "Attack": self.GetStatValue(PokemonStat.ATTACK),
            "Special_Attack": self.GetStatValue(PokemonStat.SPECIAL_ATTACK),
            "Defense": self.GetStatValue(PokemonStat.DEFENSE),
            "Special_Defense": self.GetStatValue(PokemonStat.SPECIAL_DEFENSE),
            "Speed": self.GetStatValue(PokemonStat.SPEED),
        }

        oldMoves = self.GetBattleAttacks()

        self.level += 1

        if self.evolveLevel > 0 and self.level >= self.evolveLevel:
            self.Evolve(self.evolutionName)

        newStats = {
            "HP": self.CalculateMaxHp(),
            "Attack": self.GetStatValue(PokemonStat.ATTACK),
            "Special_Attack": self.GetStatValue(PokemonStat.SPECIAL_ATTACK),
            "Defense": self.GetStatValue(PokemonStat.DEFENSE),
            "Special_Defense": self.GetStatValue(PokemonStat.SPECIAL_DEFENSE),
            "Speed": self.GetStatValue(PokemonStat.SPEED),
        }

        newMoves = self.GetBattleAttacks()

        print("%s has grown to level %s!" % (self.name, self.level))
        self.FullHealHP()
        for key in oldStats:
            if newStats[key] > oldStats[key]:
                print("%s has gained %s %s!" % (self.name, newStats[key] - oldStats[key], key))

        if len(newMoves) > len(oldMoves):
            i = len(oldMoves)
            while i < len(newMoves):
                print()
                print("%s has learned %s!" % (self.name, newMoves[i].name))
                i += 1


    def Evolve(self, newPokemon: str):
        print("%s is evolving!" % (self.name))
        time.sleep(2)
        print("...")
        time.sleep(2)
        pokemonFileName = "data/pokemon/%s.json" % (newPokemon)
        oldName = self.name

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
            self.catchFactor = data["catchFactor"]
            self.evolutionName = data["evolutionName"]
            self.evolveLevel = data["evolveLevel"]
            self.battleAttacks.clear()
            for atk in data["battleAttacks"]:
                self.battleAttacks.append(BattleAttack(atk["Move"], atk["UnlockLevel"]))

        newName = self.name
        print("%s has evolved into %s!" % (oldName, newName))
    
    
    def FullHealHP(self):
        self.currentHP = self.CalculateMaxHp()
        if self.statusCondition == Status.KNOCKED_OUT:
            self.statusCondition = Status.NONE


    def HealHP(self, healAmount: int):
        damage = self.CalculateMaxHp() - self.currentHP
        if self.statusCondition == Status.KNOCKED_OUT:
            self.statusCondition = Status.NONE

        if damage <= healAmount:
            self.FullHealHP()
            print("%s healed for %s HP!" % (self.name, damage))
        else:
            self.currentHP += healAmount
            print("%s healed for %s HP!" % (self.name, healAmount))


    def RandomAttack(self, defender: any):
        # Defender is a Pokemon object
        attackList = self.GetBattleAttacks()
        randomNumber = random.randint(0, len(attackList) - 1)
        randomAttack = attackList[randomNumber]

        if (randomAttack.currentPP <= 0):
            print("%s struggles to choose an attack!")
            exit
        else:
            self.DoAttack(randomNumber, defender)


    def DoAttack(self, attackIndex: int, defender: any):
        # Skip a turn if flinched
        if self.isFlinched:
            print("%s flinched!" % (self.name))
            self.isFlinched = False
            return

        # Skip action if bound
        try:
            bound_index = self.combatModifiers.index(CombatModifiers.BIND)
            roll = random.randint(1,100)
            if roll < 66:
                print("%s is bound and cannot move!" % (self.name))
                return
            else:
                print("%s breaks out of the bind!" % (self.name))
                self.combatModifiers.pop(bound_index)
                self.combatModifiers.append(CombatModifiers.FREED)
        except:
            pass

        attack = self.GetBattleAttacks()[attackIndex]
        attack.currentPP -= 1

        if self.statusCondition == Status.FROZEN and attack.type == BattleType.FIRE:
            self.statusCondition = Status.NONE
            print("The heat melts the ice around %s, it is no longer frozen!" % (self.name))

        # Some status effects impact attacking
        if self.statusCondition == Status.CONFUSED:
            roll = random.randint(1,100)
            if roll < 50:
                print("%s hurts itself in its confusion!" % (self.name))
                damage = (int)(self.MaxHp() / 7)
                self.TakeDamage(damage)
                return

        elif self.statusCondition == Status.ASLEEP:
            print("%s snores." % (self.name))
            return

        elif self.statusCondition == Status.PARALYZED:
            roll = random.randint(1,100)
            if roll < 50:
                print("%s is stuck in place due to paralysis!" % (self.name))
                return

        elif self.statusCondition == Status.FROZEN:
            return

        effectiveAccuracy = (int)(attack.accuracy + attack.accuracy / 4.0 * (self.accuracyModifierLevel))
        miss = random.randint(1, 100) > effectiveAccuracy
        if (miss):
            print("%s tries to use %s, but misses!" % (self.name, attack.name))
        else:
            print("%s uses %s!" % (self.name, attack.name))
            
            defender.ReceiveAttack(attack, self)
            self.HandleOnAttackEffects(attack)


    def ReceiveAttack(self, attack: BattleAttack, attacker: object) -> str:
        if attack.type == BattleType.FIRE and self.statusCondition == Status.FROZEN:
            self.statusCondition = Status.NONE
            print("The heat melts the flames around %s! It is no longer frozen!" % (self.name))

        attackerOffensiveStatValue = attacker.GetStatValue(PokemonStat.ATTACK) if attack.isPhysical else attacker.GetStatValue(PokemonStat.SPECIAL_ATTACK)

        effectivenessMultiplier = EngineUtilities.GetTypeAdvantageMultiplier(self.battleType1, self.battleType2, attack.type)
        if effectivenessMultiplier >= 2.0:
            print("It's super effective!")
        elif effectivenessMultiplier == 0:
            print("%s is completely unaffected!" % (self.name))
        elif effectivenessMultiplier < 1.0:
            print("It's not very effective!")
            
        defenseValue = self.GetStatValue(PokemonStat.DEFENSE) if attack.isPhysical else self.GetStatValue(PokemonStat.SPECIAL_DEFENSE)
        damage = 0
        if attack.baseDmg > 0:
            damage = 2 + (int)((((attack.baseDmg * effectivenessMultiplier) + 2 ) * (attackerOffensiveStatValue * 0.75 / (5 * defenseValue))) + random.randint(0,3))
            crit = random.randint(1,20) > 19
            if crit:
                damage = (int)(damage * 1.75)
                print("CRITICAL HIT!")
        self.TakeDamage(damage)
        self.HandleAttackReceivedEffects(attack, attacker, damage)


    def HandleAttackReceivedEffects(self, attack: BattleAttack, attacker: object, damage: int):
        for effect in attack.effects:
            if effect.target == Targeting.OPPONENT:
                if effect.effectType == EffectType.ADD_COMBAT_MODIFIER:
                    roll = random.randint(1,100)
                    if effect.effectDetail == CombatModifiers.BIND:
                        freed_index = -1
                        try:
                            freed_index = self.combatModifiers.index(CombatModifiers.FREED)
                            roll += 25
                        except:
                            pass
                        if roll < effect.chance * 100:
                            print("%s has been bound!" % (self.name))
                            self.AddCombatModifier(CombatModifiers.BIND)
                        
                        if freed_index >= 0:
                            self.combatModifiers.pop(freed_index)
                    else:
                        if roll < effect.chance:
                            self.AddCombatModifier(effect.effectDetail)

                elif effect.effectType == EffectType.ADD_STATUS_EFFECT:
                    roll = random.randint(1,100)
                    if roll < effect.chance:
                        self.AddStatusEffect(effect.effectDetail)
                        print("%s becomes %s!" % (self.name, effect.effectDetail))
                elif effect.effectType == EffectType.CLEANSE_COMBAT_MODIFIERS:
                    print("%s stumbles and resets it's position, it seems to have lost it's rhythm!" % (self.name))
                    self.combatModifiers.clear()
                elif effect.effectType == EffectType.CLEANSE_STATUS_EFFECTS:
                    print("%s moves freely, as all status effects are cleared!" % (self.name))
                    self.statusCondition = Status.NONE
                elif effect.effectType == EffectType.DRAIN:
                    drainFactor = effect.effectDetail
                    drainAmount = (int)(damage * drainFactor)
                    print("%s drains energy from it's opponent!" % (attacker.name))
                    attacker.HealHP(drainAmount)
                elif effect.effectType == EffectType.FLINCH:
                    roll = random.randint(1,100)
                    if roll < effect.chance:
                        self.isFlinched = True


    def HandleOnAttackEffects(self, attack: BattleAttack):
        for effect in attack.effects:
            if effect.target == Targeting.SELF:
                roll = random.randint(1,100)
                # We need to skip effects that don't trigger because we roll outside of their range
                if roll > effect.chance:
                    continue

                if effect.effectType == EffectType.ADD_COMBAT_MODIFIER:
                        self.AddCombatModifier(effect.effectDetail)
                elif effect.effectType == EffectType.ADD_STATUS_EFFECT:
                        self.AddStatusEffect(effect.effectDetail)
                elif effect.effectType == EffectType.CLEANSE_COMBAT_MODIFIERS:
                    print("%s stumbles and resets it's position, it seems to have lost it's rhythm!" % (self.name))
                    self.combatModifiers.clear()
                elif effect.effectType == EffectType.CLEANSE_STATUS_EFFECTS:
                    print("%s moves freely, as all status effects are cleared!" % (self.name))
                    self.statusCondition = Status.NONE
                elif effect.effectType == EffectType.HEAL:
                    healAmount = (int)(self.CalculateMaxHp() * effect.effectDetail)
                    print("%s is healed for %s HP!" % (self.name, healAmount))

    
    def TakeDamage(self, damage: int):
        if damage > self.currentHP:
            self.currentHP = 0
            self.statusCondition = Status.KNOCKED_OUT
            print("%s took %s damage and got knocked out. It is no longer able to battle!" % (self.name, damage))
        else:
            self.currentHP -= damage
            print("%s took %s damage!" % (self.name, damage))


    def ClearCombatModifiers(self):
        self.combatModifiers.clear()
        self.accuracyModifierLevel = 0
        self.attackModifierLevel = 0
        self.specialAttackModifierLevel = 0
        self.defenseModifierLevel = 0
        self.specialDefenseModifierLevel = 0
        self.speedModifierLevel = 0


if __name__ == "__main__":
    pokemon = Pokemon()
    with open("data/pokemon/%s.json" % (pokemon.name.lower()), 'w') as outfile:
        outfile.write(pokemon.ExportJson())