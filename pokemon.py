from typing import List
from battleAttack import BattleAttack
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

        self.battleType1 = BattleType.FLYING
        self.battleType2 = BattleType.NORMAL

        self.battleAttacks = [BattleAttack("peck", 2), BattleAttack("tackle", 1)]

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
        if (effect == CombatModifiers.ACCURACY_DOWN or 
            effect == CombatModifiers.ACCURACY_DOWN_DOWN or
            effect == CombatModifiers.ACCURACY_UP or 
            effect == CombatModifiers.ACCURACY_UP_UP):

            # Clear all existing accuracy modifiers
            index = 0
            while index < len(self.combatModifiers):
                if (self.combatModifiers[index] == CombatModifiers.ACCURACY_DOWN or 
                    self.combatModifiers[index] == CombatModifiers.ACCURACY_DOWN_DOWN or
                    self.combatModifiers[index] == CombatModifiers.ACCURACY_UP or
                    self.combatModifiers[index] == CombatModifiers.ACCURACY_UP_UP):

                    self.combatModifiers.pop(index)
                else:
                    index += 1
            self.combatModifiers.append(effect)
            print("%s's ACCURACY has changed!" % (self.name))

        # Attack Modifier
        elif (effect == CombatModifiers.ATK_DOWN or 
            effect == CombatModifiers.ATK_DOWN_DOWN or
            effect == CombatModifiers.ATK_UP or 
            effect == CombatModifiers.ATK_UP_UP):

            # Clear all existing accuracy modifiers
            index = 0
            while index < len(self.combatModifiers):
                if (self.combatModifiers[index] == CombatModifiers.ATK_UP_UP or 
                    self.combatModifiers[index] == CombatModifiers.ATK_UP or
                    self.combatModifiers[index] == CombatModifiers.ATK_DOWN or
                    self.combatModifiers[index] == CombatModifiers.ATK_DOWN_DOWN):

                    self.combatModifiers.pop(index)
                else:
                    index += 1
            self.combatModifiers.append(effect)
            print("%s's ATTACK has changed!" % (self.name))

        # SpAttack Modifier
        elif (effect == CombatModifiers.SPATK_DOWN or 
            effect == CombatModifiers.SPATK_DOWN_DOWN or
            effect == CombatModifiers.SPATK_UP or 
            effect == CombatModifiers.SPATK_UP_UP):

            # Clear all existing accuracy modifiers
            index = 0
            while index < len(self.combatModifiers):
                if (self.combatModifiers[index] == CombatModifiers.SPATK_UP_UP or 
                    self.combatModifiers[index] == CombatModifiers.SPATK_UP or
                    self.combatModifiers[index] == CombatModifiers.SPATK_DOWN or
                    self.combatModifiers[index] == CombatModifiers.SPATK_DOWN_DOWN):

                    self.combatModifiers.pop(index)
                else:
                    index += 1
            self.combatModifiers.append(effect)
            print("%s's SPECIAL ATTACK has changed!" % (self.name))

        # Defense Modifier
        elif (effect == CombatModifiers.DEF_DOWN or 
            effect == CombatModifiers.DEF_DOWN_DOWN or
            effect == CombatModifiers.DEF_UP or 
            effect == CombatModifiers.DEF_UP_UP):

            # Clear all existing accuracy modifiers
            index = 0
            while index < len(self.combatModifiers):
                if (self.combatModifiers[index] == CombatModifiers.DEF_UP_UP or 
                    self.combatModifiers[index] == CombatModifiers.DEF_UP or
                    self.combatModifiers[index] == CombatModifiers.DEF_DOWN or
                    self.combatModifiers[index] == CombatModifiers.DEF_DOWN_DOWN):

                    self.combatModifiers.pop(index)
                else:
                    index += 1
            self.combatModifiers.append(effect)
            print("%s's DEFENSE has changed!" % (self.name))

        # SpDef Modifier
        elif (effect == CombatModifiers.SPDEF_DOWN or 
            effect == CombatModifiers.SPDEF_DOWN_DOWN or
            effect == CombatModifiers.SPDEF_UP or 
            effect == CombatModifiers.SPDEF_UP_UP):

            # Clear all existing accuracy modifiers
            index = 0
            while index < len(self.combatModifiers):
                if (self.combatModifiers[index] == CombatModifiers.SPDEF_UP_UP or 
                    self.combatModifiers[index] == CombatModifiers.SPDEF_UP or
                    self.combatModifiers[index] == CombatModifiers.SPDEF_DOWN or
                    self.combatModifiers[index] == CombatModifiers.SPDEF_DOWN_DOWN):

                    self.combatModifiers.pop(index)
                else:
                    index += 1
            self.combatModifiers.append(effect)
            print("%s's SPECIAL DEFENSE has changed!" % (self.name))

        # Speed Modifier
        elif (effect == CombatModifiers.SPEED_DOWN or 
            effect == CombatModifiers.SPEED_DOWN_DOWN or
            effect == CombatModifiers.SPEED_UP or 
            effect == CombatModifiers.SPEED_DOWN):

            # Clear all existing accuracy modifiers
            index = 0
            while index < len(self.combatModifiers):
                if (self.combatModifiers[index] == CombatModifiers.SPEED_DOWN or 
                    self.combatModifiers[index] == CombatModifiers.SPEED_DOWN_DOWN or
                    self.combatModifiers[index] == CombatModifiers.SPEED_UP or
                    self.combatModifiers[index] == CombatModifiers.SPEED_UP_UP):

                    self.combatModifiers.pop(index)
                else:
                    index += 1
            self.combatModifiers.append(effect)
            print("%s's SPEED has changed!" % (self.name))

        elif (effect == CombatModifiers.CHARGED_UP):
            alreadyCharged = False
            for mod in self.combatModifiers:
                if mod == CombatModifiers.CHARGED_UP:
                    alreadyCharged = True

            if not alreadyCharged:
                self.combatModifiers.append(effect)


    def GetStatValue(self, stat: PokemonStat) -> int:
        modFactor = 1.0
        
        if stat == PokemonStat.ATTACK:
            for modifier in self.combatModifiers:
                if modifier == CombatModifiers.ATK_UP_UP:
                    modFactor = 4.0
                    break
                elif modifier == CombatModifiers.ATK_UP:
                    modFactor = 2.0
                    break
                elif modifier == CombatModifiers.ATK_DOWN:
                    modFactor = 0.5
                    break
                elif modifier == CombatModifiers.ATK_DOWN_DOWN:
                    modFactor = 0.25
                    break

            if self.statusCondition == Status.BURNED:
                modFactor *= 0.5

            return 1 + (int)(1.0/5*self.attackStat*self.level*modFactor)

        elif stat == PokemonStat.SPECIAL_ATTACK:
            for modifier in self.combatModifiers:
                if modifier == CombatModifiers.SPATK_UP_UP:
                    modFactor = 4.0
                    break
                elif modifier == CombatModifiers.SPATK_UP:
                    modFactor = 2.0
                    break
                elif modifier == CombatModifiers.SPATK_DOWN:
                    modFactor = 0.5
                    break
                elif modifier == CombatModifiers.SPATK_DOWN_DOWN:
                    modFactor = 0.25
                    break

            if self.statusCondition == Status.CURSED:
                modFactor *= 0.5

            return 1 + (int)(1.0/5*self.spAttackStat*self.level*modFactor)

        elif stat == PokemonStat.DEFENSE:
            for modifier in self.combatModifiers:
                if modifier == CombatModifiers.DEF_UP_UP:
                    modFactor = 4.0
                    break
                elif modifier == CombatModifiers.DEF_UP:
                    modFactor = 2.0
                    break
                elif modifier == CombatModifiers.DEF_DOWN:
                    modFactor = 0.5
                    break
                elif modifier == CombatModifiers.DEF_DOWN_DOWN:
                    modFactor = 0.25
                    break

            return 1 + (int)(1.0/5*self.defenseStat*self.level*modFactor)

        elif stat == PokemonStat.SPECIAL_DEFENSE:
            for modifier in self.combatModifiers:
                if modifier == CombatModifiers.SPDEF_UP_UP:
                    modFactor = 4.0
                    break
                elif modifier == CombatModifiers.SPDEF_UP:
                    modFactor = 2.0
                    break
                elif modifier == CombatModifiers.SPDEF_DOWN:
                    modFactor = 0.5
                    break
                elif modifier == CombatModifiers.SPDEF_DOWN_DOWN:
                    modFactor = 0.25
                    break

            return 1 + (int)(1.0/5*self.spDefenseStat*self.level*modFactor)

        elif stat == PokemonStat.HP:
            return self.calculateMaxHp()

        elif stat == PokemonStat.SPEED:
            for modifier in self.combatModifiers:
                if modifier == CombatModifiers.SPEED_UP_UP:
                    modFactor = 4.0
                    break
                elif modifier == CombatModifiers.SPEED_UP:
                    modFactor = 2.0
                    break
                elif modifier == CombatModifiers.SPEED_DOWN:
                    modFactor = 0.5
                    break
                elif modifier == CombatModifiers.SPEED_DOWN_DOWN:
                    modFactor = 0.25
                    break

            if self.statusCondition == Status.PARALYZED:
                modFactor *= 0.5

            return 1 + (int)(1.0/5*self.speedStat*self.level*modFactor)


    def calculateMaxHp(self) -> int:
        return 10 + (int)(self.HPStat * self.level * 3/5)


    def GetExperienceValue(self) -> int:
        return ( self.attackStat + self.defenseStat + self.spAttackStat + self.spDefenseStat + self.speedStat + self.HPStat ) * self.level


    def GainExperience(self, xp: int):
        self.XP += xp
        while self.XP >= (int)((1 + self.level / 5) * 450 + 2 * self.level):
            self.LevelUp()
            self.XP -= (int)((1 + self.level / 5) * 450 + 2 * self.level)


    def LevelUp(self):
        oldStats = {
            "HP": self.calculateMaxHp(),
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
            "HP": self.calculateMaxHp(),
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
        pokemonFileName = "pokemon/%s.json" % (newPokemon)

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
            self.battleAttacks.clear()
            for atk in data["battleAttacks"]:
                self.battleAttacks.append(BattleAttack(atk["Move"], atk["UnlockLevel"]))
    
    
    def FullHealHP(self):
        self.currentHP = self.calculateMaxHp()
        if self.statusCondition == Status.KNOCKED_OUT:
            self.statusCondition = Status.NONE


    def HealHP(self, healAmount: int):
        damage = self.calculateMaxHp() - self.currentHP
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
        # Some status effects impact attacking
        if self.statusCondition == Status.CONFUSED:
            roll = random.randint(1,100)
            if roll < 50:
                print("%s hurts itself in its confusion!" % (self.name))
                damage = (int)(self.calculateMaxHp() / 7)
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

        attack = self.GetBattleAttacks()[attackIndex]
        attack.currentPP -= 1

        effectiveAccuracy = attack.accuracy
        for mod in self.combatModifiers:
            if mod == CombatModifiers.ACCURACY_DOWN:
                effectiveAccuracy -= 20
            elif mod == CombatModifiers.ACCURACY_DOWN_DOWN:
                effectiveAccuracy -= 40
            elif mod == CombatModifiers.ACCURACY_UP:
                effectiveAccuracy += 15
            elif mod == CombatModifiers.ACCURACY_UP_UP:
                effectiveAccuracy += 50

        miss = random.randint(1, 100) > effectiveAccuracy
        if (miss):
            print("%s tries to use %s, but misses!" % (self.name, attack.name))
        else:
            print("%s uses %s!" % (self.name, attack.name))
            
            defender.ReceiveAttack(attack, self)
            self.HandleOnAttackEffects(attack)


    def ReceiveAttack(self, attack: BattleAttack, attacker: object) -> str:
        attackerOffensiveStatValue = attacker.GetStatValue(PokemonStat.ATTACK) if attack.isPhysical else attacker.GetStatValue(PokemonStat.SPECIAL_ATTACK)

        effectivenessMultiplier = Pokemon.CalculateDamageTypeMultiplier(self.battleType1, self.battleType2, attack.type)
        if effectivenessMultiplier >= 2.0:
            print("It's super effective!")
        elif effectivenessMultiplier == 0:
            print("%s is completely unaffected!" % (self.name))
        elif effectivenessMultiplier < 1.0:
            print("It's not very effective!")
            
        defenseValue = self.GetStatValue(PokemonStat.DEFENSE) if attack.isPhysical else self.GetStatValue(PokemonStat.SPECIAL_DEFENSE)
        damage = 2 + (int)((((attack.baseDmg * effectivenessMultiplier) + 2 ) * (attackerOffensiveStatValue * 0.75 / (5 * defenseValue))) + random.randint(0,3))
        crit = random.randint(0,9) > 8
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


    def HandleOnAttackEffects(self, attack: BattleAttack):
        for effect in attack.effects:
            if effect.target == Targeting.SELF:
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
                    healAmount = (int)(self.calculateMaxHp() * effect.effectDetail)
                    print("%s is healed for %s HP!" % (self.name, healAmount))

    
    
    def TakeDamage(self, damage: int):
        if damage > self.currentHP:
            self.currentHP = 0
            self.statusCondition = Status.KNOCKED_OUT
            print("%s took %s damage and got knocked out. It is no longer able to battle!" % (self.name, damage))
        else:
            self.currentHP -= damage
            print("%s took %s damage!" % (self.name, damage))


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