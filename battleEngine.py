from PIL import Image
import random
import time
from common.enums import BattleType, ItemType, PokemonStat, Status
from common.formatting import Formatting
from models.item import Item
from models.pokemon import Pokemon
from typing import List, Tuple

continueBattling = False

class BattleEngine:

    def DoWildBattle(player_pokemon: List[Pokemon], wildPokemon: Pokemon, items: List[ItemType]):
        global continueBattling

        continueBattling = True
        while (continueBattling):
            Formatting.clearScreen()
            if BattleEngine.CheckIfOpponentPokemonFainted(wildPokemon, player_pokemon):
                continueBattling = False
                continue

            if (player_pokemon[0].currentHP <= 0):
                swapped = False
                while not swapped:
                    swapped = BattleEngine.SwapPokemon(player_pokemon)

            player_active_pokemon = player_pokemon[0]
            BattleEngine.AssessPokemonHealth(wildPokemon)
            print("Your %s" % (player_active_pokemon.GetHPString()))
            print()
            options = ["ATTACK", "ITEM", "SWAP POKEMON", "RUN", "POKEDEX"]
            userChoice = Formatting.GetUserChoice(options, noBack=True)
            if userChoice < 0 or userChoice > len(options) - 1:
                continue

            userAction = options[userChoice]
                
            tookAction = BattleEngine.PerformPlayerInputChoice(userAction, player_pokemon, wildPokemon, items)
            if not tookAction:
                continue

            BattleEngine.ProcessEndOfRoundStatuses(wildPokemon, player_active_pokemon)
            Formatting.PressEnterToContinue()

        # End of battle
        for pokemon in player_pokemon:
            pokemon.combatModifiers.clear()


    def DoTrainerBattle(player_pokemon: List[Pokemon], opponent_pokemon: List[Pokemon], items: List[ItemType], opponent_name: str, winningMoney: int, startLine: str, endLine: str):
        global continueBattling

        continueBattling = True
        print("%s wants to battle!" % (opponent_name))
        print("%s: %s" % (opponent_name, startLine))
        Formatting.PressEnterToContinue()
        print("%s: Go %s!" % (opponent_name, opponent_pokemon[0].name))
        print("You: %s, I choose you!" % (player_pokemon[0].name))
        print()
        while (continueBattling):
            Formatting.clearScreen()
            if BattleEngine.CheckIfOpponentPokemonFainted(opponent_pokemon[0], player_pokemon):
                nextPokemonIndex = -1
                countingIndex = 0
                for nextPokemon in opponent_pokemon:
                    if nextPokemon.currentHP > 0:
                        nextPokemonIndex = countingIndex
                        break
                    countingIndex += 1

                if nextPokemonIndex == -1:
                    print("%s has no remaining Pokemon to battle with! You win!" % (opponent_name))
                    print()
                    print("You gain %s Pokecoins." % (winningMoney))
                    input("*Press ENTER to continue....*")
                    continueBattling = False
                    continue
                else:
                    print("The opposing %s has fainted. It's trainer sends out %s in its place!" % (opponent_pokemon[0].name, opponent_pokemon[nextPokemonIndex].name))
                    opponent_pokemon[0], opponent_pokemon[nextPokemonIndex] = opponent_pokemon[nextPokemonIndex], opponent_pokemon[0]

            if (player_pokemon[0].currentHP <= 0):
                swapped = False
                while not swapped:
                    swapped = BattleEngine.SwapPokemon(player_pokemon)

            opponent_active_pokemon = opponent_pokemon[0]
            player_active_pokemon = player_pokemon[0]
            BattleEngine.AssessPokemonHealth(opponent_active_pokemon)
            print("Your %s" % (player_active_pokemon.GetHPString()))
            print()
            options = ["ATTACK", "ITEM", "SWAP POKEMON", "POKEDEX"]
            userChoice = Formatting.GetUserChoice(options, noBack=True)
            if userChoice < 0 or userChoice > len(options) - 1:
                continue

            userAction = options[userChoice]
            tookAction = BattleEngine.PerformPlayerInputChoice(userAction, player_pokemon, opponent_active_pokemon, items)
            if not tookAction:
                continue

            BattleEngine.ProcessEndOfRoundStatuses(opponent_active_pokemon, player_active_pokemon)
            Formatting.PressEnterToContinue()

        # End of battle
        for pokemon in player_pokemon:
            pokemon.ClearCombatModifiers()

        print("%s: %s" % (opponent_name, endLine))


    def PerformPlayerInputChoice(userAction: str, player_pokemon: List[Pokemon], wildPokemon: Pokemon, items: List[str]) -> bool:
        global continueBattling

        tookAction = True
        player_active_pokemon = player_pokemon[0]
        if (userAction == "ATTACK"):
            tookAction = BattleEngine.DoAttackMenu(player_active_pokemon, wildPokemon)

        elif (userAction == "ITEM"):
            if not BattleEngine.DoItemMenu(items, player_pokemon, wildPokemon, allow_pokeball=True):
                tookAction = False
            else:
                wildPokemon.RandomAttack(player_active_pokemon)

        elif (userAction == "SWAP POKEMON"):
            swapped = BattleEngine.SwapPokemon(player_pokemon)
            if not swapped:
                tookAction = False
            else:
                wildPokemon.RandomAttack(player_pokemon[0])

        elif (userAction == "RUN"):
            continueBattling = BattleEngine.TryToRun(player_active_pokemon, wildPokemon)

            # Get hit if they don't escape
            if continueBattling:
                wildPokemon.RandomAttack(player_active_pokemon)

        elif (userAction == "POKEDEX"):
            BattleEngine.UsePokedex(wildPokemon)
        
        else:
            tookAction = False

        return tookAction


    def CheckIfOpponentPokemonFainted(opponent: Pokemon, playerPokemon: List[Pokemon]) -> bool:
        if (opponent.currentHP <= 0):
            xpGain = opponent.GetExperienceValue()
            print("%s has fainted." % (opponent.name))
            print()
            print("%s XP has been split among your Pokemon!" % (xpGain))

            consciousPokemon = []
            for p in playerPokemon:
                if p.statusCondition != Status.KNOCKED_OUT:
                    consciousPokemon.append(p)

            xpShare = (int)(xpGain / len(consciousPokemon))
            for p in consciousPokemon:
                p.GainExperience(xpShare)
            input("*Press ENTER to continue*")
            Formatting.clearScreen()
            return True

        return False


    def AssessPokemonHealth(poke: Pokemon):
        opponentHealthiness = "completely untouched"
        healthPercentage = poke.currentHP / poke.CalculateMaxHp()
        if (healthPercentage < 0.95):
            opponentHealthiness = "a little scratched up"
        if (healthPercentage < 0.7):
            opponentHealthiness = "like it has a lot of energy left"
        if (healthPercentage < 0.5):
            opponentHealthiness = "like it is starting to get tired"
        if (healthPercentage < 0.3):
            opponentHealthiness = "pretty beat up"
        if (healthPercentage < 0.1):
            opponentHealthiness = "like it is about to faint"
        print("The opposing %s looks %s." % (poke.name, opponentHealthiness))


    def DoAttackMenu(player_pokemon: Pokemon, opponent: Pokemon) -> bool:
        Formatting.clearScreen()
        print("Choose attack:")
        attacks = player_pokemon.GetBattleAttacks()
        attackNames = []
        for attack in attacks:
            attackNames.append("[%s] %s (%s/%s)" % (attack.type, attack.name, attack.currentPP, attack.maxPP))

        attackIndex = Formatting.GetUserChoice(attackNames)
        if attackIndex == -2:
            # User chose BACK
            return False
        if attackIndex == -1 or attackIndex > len(attacks) - 1:
            input("Input not recognized. Press ENTER to try again.")
            return False

        attackChoice = attacks[attackIndex]

        if (attackChoice.currentPP <= 0):
            input("No more PP available for that attack, choose something else. Press ENTER to try again.")
            return False

        Formatting.clearScreen()
        print("You: %s, use %s!" % (player_pokemon.name, attackChoice.name))
        print()
        if (opponent.GetStatValue(PokemonStat.SPEED) > player_pokemon.GetStatValue(PokemonStat.SPEED)):
            print("The opposing %s is faster!" % (opponent.name))
            opponent.RandomAttack(player_pokemon)
            if not BattleEngine.CheckForKnockout(player_pokemon):
                player_pokemon.DoAttack(attackIndex, opponent)
        else:
            player_pokemon.DoAttack(attackIndex, opponent)
            if not BattleEngine.CheckForKnockout(opponent):
                opponent.RandomAttack(player_pokemon)

        return True


    def DoItemMenu(items: List[ItemType], player_pokemon: List[Pokemon], opponent: Pokemon, allow_pokeball: bool = True) -> bool:
        global continueBattling

        if len(items) == 0:
            print("You have no items.")
            input("*Press ENTER to continue*")
            return False

        Formatting.clearScreen()
        chosenItemIndex = Item.ChooseItem(items)

        if chosenItemIndex is None:
            return False

        chosenItem = items[chosenItemIndex]
        match chosenItem:
            case ItemType.POTION:
                # The Item.UsePotion(int) function returns false if the player fails to select a target.
                # If that happens, we should skip the rest of execution and go back to getting player input.
                if not Item.UsePotion(30, player_pokemon):
                    return False
                else:
                    items.pop(chosenItemIndex)

            case ItemType.SUPER_POTION:
                # The Item.UsePotion(int) function returns false if the player fails to select a target.
                # If that happens, we should skip the rest of execution and go back to getting player input.
                if not Item.UsePotion(60, player_pokemon):
                    return False
                else:
                    items.pop(chosenItemIndex)

            case ItemType.POKEBALL:
                if allow_pokeball:
                    caught = Item.UsePokeball(opponent, player_pokemon, ItemType.POKEBALL)
                    items.pop(chosenItemIndex)
                    if caught:
                        continueBattling = False
                        xpGain = opponent.GetExperienceValue()
                        print()
                        print("%s XP has been split among your Pokemon!" % (xpGain))
                        xpShare = (int)(xpGain / len(player_pokemon) - 1)
                        for p in player_pokemon:
                            p.GainExperience(xpShare)
                        input("*Press ENTER to continue*")
                        Formatting.clearScreen()
                        return False
                else:
                    print("You can't use this item on that Pokemon!")
                    input("*Press ENTER to continue...*")
                    Formatting.clearScreen()

            case ItemType.GREATBALL:
                if allow_pokeball:
                    caught = Item.UsePokeball(opponent, player_pokemon, ItemType.GREATBALL)
                    items.pop(chosenItemIndex)
                    if caught:
                        continueBattling = False
                        xpGain = opponent.GetExperienceValue()
                        print()
                        print("%s XP has been split among your Pokemon!" % (xpGain))
                        xpShare = (int)(xpGain / len(player_pokemon) - 1)
                        for p in player_pokemon:
                            p.GainExperience(xpShare)
                        input("*Press ENTER to continue*")
                        Formatting.clearScreen()
                        return False
                else:
                    print("You can't use this item on that Pokemon!")
                    input("*Press ENTER to continue...*")
                    Formatting.clearScreen()

            case ItemType.CAMPING_KIT:
                print("You can't use this in battle!")
                input("*Press ENTER to continue...*")
                Formatting.clearScreen()

        return True


    def UsePokedex(opponent: Pokemon):
        print("You pull out your Pokedex and point it at the %s..." % (opponent.name))
        print("*Analyzing...*")
        time.sleep(1)
        print("...")
        time.sleep(1)
        print("*BEEP*")
        time.sleep(1)
        print("...")
        typePhrase = "%s" % (opponent.battleType1)
        if opponent.battleType2 != BattleType.NONE:
            typePhrase += " and %s" % (opponent.battleType2)

        print("%s, a %s type. This one appears to be level %s." % (opponent.name, typePhrase, opponent.level))
        print()
        try:
            pokemonimg = "data/images/%s.jpg" % (opponent.name)
            img = Image.open(pokemonimg)
            img.show()
        except:
            print("No visual data found for this Pokemon.")

    
    def TryToRun(trainerPokemon: Pokemon, wildPokemon: Pokemon) -> bool:
        print("You try to run...")
        escapeFailed = False
        odds = (int)(trainerPokemon.GetStatValue(PokemonStat.SPEED) / wildPokemon.GetStatValue(PokemonStat.SPEED) * 50)
        escapeFailed = random.randint(1,100) > odds

        if escapeFailed:
            print("the wild %s blocks your path!" % (wildPokemon.name))
        else:
            print("SUCCESS!")
            print()

        return escapeFailed

    
    def CheckForKnockout(pokemon: Pokemon) -> bool:
        if pokemon.currentHP <= 0:
            pokemon.currentHP = 0
            pokemon.statusCondition = Status.KNOCKED_OUT
            print("%s is no longer able to battle!" % (pokemon.name))
            return True
        else:
            return False


    def SwapPokemon(pokemonList: List[Pokemon]) -> bool:
        allDefeated = True
        for p in pokemonList:
            if p.currentHP > 0:
                allDefeated = False
                break

        if allDefeated:
            print("All of your Pokemon have fainted. GAME OVER.")
            input("*Press ENTER to quit*")
            quit()

        Formatting.clearScreen()
        print("Choose which Pokemon to send out next:")
        options = []
        optionCounter = 0
        for p in pokemonList:
            status = p.statusCondition
            statusString = "%s" % (status) if status != Status.NONE else ""
            options.append("%s - Level: %s, HP: %s/%s %s" % (p.name, p.level, p.currentHP, p.CalculateMaxHp(), statusString))
            optionCounter += 1

        chosenIndex = Formatting.GetUserChoice(options)
        if chosenIndex == -2:
            # User chose BACK
            return False

        elif chosenIndex == -1 or chosenIndex > len(options) - 1:
            print("Input %s is not understood. Try again.")
            input("*Press ENTER to continue*")
            BattleEngine.SwapPokemon(pokemonList)

        else:
            if chosenIndex == 0:
                print("That Pokemon is already active!")
                input("*Press ENTER to continue*")
                return False

            elif pokemonList[chosenIndex].currentHP <= 0:
                print("%s is knocked out! Choose another Pokemon!" % (pokemonList[chosenIndex].name))
                input("*Press ENTER to continue*")
                BattleEngine.SwapPokemon(pokemonList)

            else:
                print("You: %s, return! I choose you, %s!" % (pokemonList[0].name, pokemonList[chosenIndex].name))
                pokemonList[0], pokemonList[chosenIndex] = pokemonList[chosenIndex], pokemonList[0]
                return True


    def ProcessEndOfRoundStatuses(opponent: Pokemon, player_pokemon: Pokemon):
        for p in (opponent, player_pokemon):
            roll = random.randint(1,100)
            match p.statusCondition:
                case Status.NONE:
                    # Nothing happens intentionally
                    continue

                case Status.ASLEEP:
                    if roll > 50:
                        print("%s suddenly woke up!" % (p.name))
                        p.statusCondition = Status.NONE
                    else:
                        print("%s is asleep." % (p.name))

                case Status.POISONED:
                    dmg = 1 + (int)(p.CalculateMaxHp()/7)
                    print("The poison causes %s to wince." % (p.name))
                    p.TakeDamage(dmg)

                case Status.PARALYZED:
                    if roll > 60:
                        print("%s shook off the paralysis!" % (p.name))
                        p.statusCondition = Status.NONE
                    else:
                        print("%s is paralyzed." % (p.name))

                case Status.CONFUSED:
                    if roll > 40:
                        print("%s took a deep breath and closed it's eyes for a moment, then snapped to attention. It is no longer confused!" % (p.name))
                        p.statusCondition = Status.NONE
                    else:
                        print("%s is confused!" % (p.name))

                case Status.FROZEN:
                    if roll + p.attackStat / 5 > 100:
                        print("%s used it's overwhelming strength to shatter the ice and break out! Incredible!" % (p.name))
                        p.statusCondition = Status.NONE
                    else:
                        print("%s is frozen in a solid block of ice." % (p.name))

                case Status.BURNED:
                    if roll + p.spAttackStat / 2 > 100:
                        print("%s overcame the burn with sheer will power!" % (p.name))
                        p.statusCondition = Status.NONE
                    else:
                        damage = 2 + (int)(p.CalculateMaxHp() / 10)
                        print("%s winces as it's burned skin throbs." % (p.name))
                        p.TakeDamage(damage)

                case Status.CURSED:
                    if roll + p.HPStat / 4 > 100:
                        print("%s overcame the curse with sheer will power!" % (p.name))
                        p.statusCondition = Status.NONE
                    else:
                        print("%s is trembling in fear, it can't focus!" % (p.name, damage))