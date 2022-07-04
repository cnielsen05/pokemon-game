

from enums import BattleType


class EngineUtilities:
    # This function calls the other function, and multiplies the two multipliers together to get a final product
    def GetTypeAdvantageMultiplier(defType1: BattleType, defType2: BattleType, attackType: BattleType) -> int:
        multiplierOne = EngineUtilities.GetSingleTypeAdvantageMultiplier(defType1, attackType)
        multiplierTwo = EngineUtilities.GetSingleTypeAdvantageMultiplier(defType2, attackType)
        return multiplierOne * multiplierTwo


    # This function returns the multiplier for one attack type on one defense type
    def GetSingleTypeAdvantageMultiplier(defType: BattleType, attackType: BattleType) -> int:
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