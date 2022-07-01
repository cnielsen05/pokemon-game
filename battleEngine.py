from PIL import Image
from sys import platform
import random
from time import sleep
from battleAttack import BattleAttack
from enums import BattleType, ItemType, PokemonStat, Status
from formatting import Formatting
from item import Item
from pokemon import Pokemon
from typing import List

continueBattling = False

class BattleEngine:
    # def __init__(self):

    def DoWildBattle(player_pokemon: List[Pokemon], wildPokemon: Pokemon, items: List[ItemType]):
        global continueBattling

        continueBattling = True
        while (continueBattling):
            Formatting.clearScreen()
            if BattleEngine.OpponentFaintIfDead(wildPokemon, player_pokemon[0]):
                continueBattling = False
                continue

            if (player_pokemon[0].currentHP <= 0):
                BattleEngine.SwapPokemon(player_pokemon)

            BattleEngine.AssessOpponentHealthiness(wildPokemon)
            print("Your %s has %s/%s HP remaining." % (player_pokemon[0].name, player_pokemon[0].currentHP, player_pokemon[0].calculateMaxHp()))
            print()
            options = ["ATTACK", "ITEM", "SWAP POKEMON", "RUN", "POKEDEX"]
            userChoice = Formatting.GetUserChoice(options)
            if userChoice < 0 or userChoice > len(options) - 1:
                input("Input %s unrecognized. Press ENTER to try again." % (userAction))
                continue

            userAction = options[userChoice]
                
            if (userAction == "ATTACK"):
                if not BattleEngine.DoAttackMenu(player_pokemon[0], wildPokemon):
                    continue

            elif (userAction == "ITEM"):
                if not BattleEngine.DoItemMenu(items, player_pokemon, wildPokemon, allow_pokeball=True):
                    continue
                else:
                    wildPokemon.RandomAttack(player_pokemon[0])

            elif (userAction == "SWAP POKEMON"):
                BattleEngine.SwapPokemon(player_pokemon)
                wildPokemon.RandomAttack(player_pokemon[0])

            elif (userAction == "RUN"):
                continueBattling = BattleEngine.TryToRun(player_pokemon[0], wildPokemon)

                # Get hit if they don't escape
                if continueBattling:
                    wildPokemon.RandomAttack(player_pokemon[0])

            elif (userAction == "POKEDEX"):
                BattleEngine.UsePokedex(wildPokemon)
                roll = random.randint(1,100)
                if roll < 20 and wildPokemon.GetStatValue(PokemonStat.SPEED) > player_pokemon[0].GetStatValue(PokemonStat.SPEED):
                    print("The wild %s attacks suddenly!")
                    wildPokemon.RandomAttack(player_pokemon[0])

            BattleEngine.ProcessEndOfRoundStatuses(wildPokemon, player_pokemon[0])

        # End of battle
        for pokemon in player_pokemon:
            pokemon.combatModifiers.clear()


    def DoTrainerBattle(player_pokemon: List[Pokemon], opponent_pokemon: List[Pokemon], items: List[ItemType], opponent_name: str, winningMoney: int):
        global continueBattling

        continueBattling = True
        while (continueBattling):
            Formatting.clearScreen()
            if BattleEngine.OpponentFaintIfDead(opponent_pokemon[0], player_pokemon[0]):
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
                BattleEngine.SwapPokemon(player_pokemon)

            opponent_active_pokemon = opponent_pokemon[0]
            player_active_pokemon = player_pokemon[0]
            BattleEngine.AssessOpponentHealthiness(opponent_active_pokemon)
            print("Your %s has %s/%s HP remaining." % (player_active_pokemon.name, player_active_pokemon.currentHP, player_active_pokemon.calculateMaxHp()))
            print()
            options = ["ATTACK", "ITEM", "SWAP POKEMON", "POKEDEX"]
            userChoice = Formatting.GetUserChoice(options)
            if userChoice < 0 or userChoice > len(options) - 1:
                continue

            userAction = options[userChoice]
                
            if (userAction == "ATTACK"):
                if not BattleEngine.DoAttackMenu(player_active_pokemon, opponent_active_pokemon):
                    continue

            elif (userAction == "ITEM"):
                if not BattleEngine.DoItemMenu(items, player_pokemon, allow_pokeball = False):
                    continue
                else:
                    opponent_active_pokemon.RandomAttack(player_pokemon)

            elif (userAction == "SWAP POKEMON"):
                BattleEngine.SwapPokemon(player_pokemon)
                opponent_active_pokemon.RandomAttack(player_pokemon)

            elif (userAction == "POKEDEX"):
                print("%s: It seems like you've never seen a %s before? I'll give you a moment to prepare yourself." % (opponent_name, opponent_active_pokemon.name))
                BattleEngine.UsePokedex(opponent_active_pokemon)

            BattleEngine.ProcessEndOfRoundStatuses(opponent_active_pokemon, player_pokemon[0])

        # End of battle
        for pokemon in player_pokemon:
            pokemon.combatModifiers.clear()


    def OpponentFaintIfDead(opponent: Pokemon, playerPokemon: Pokemon) -> bool:
        if (opponent.currentHP <= 0):
            xpGain = opponent.GetExperienceValue()
            print("%s has fainted." % (opponent.name))
            print()
            print("%s has gained %s XP!" % (playerPokemon.name, xpGain))
            playerPokemon.GainExperience(xpGain)
            input("*Press ENTER to continue*")
            Formatting.clearScreen()
            return True
        return False


    def AssessOpponentHealthiness(wildPokemon: Pokemon):
        opponentHealthiness = "completely untouched"
        healthPercentage = wildPokemon.currentHP / wildPokemon.calculateMaxHp()
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
        print("The opposing %s looks %s." % (wildPokemon.name, opponentHealthiness))


    def DoAttackMenu(player_pokemon: Pokemon, opponent: Pokemon) -> bool:
        Formatting.clearScreen()
        print("Choose attack:")
        attacks = player_pokemon.GetBattleAttacks()
        attackNames = []
        for attack in attacks:
            attackNames.append("[%s] %s (%s/%s)" % (attack.type, attack.name, attack.currentPP, attack.maxPP))

        attackIndex = Formatting.GetUserChoice(attackNames)
        if attackIndex < 0 or attackIndex > len(attacks) - 1:
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
        counter = 0
        for item in items:
            identifier = chr(ord("A") + counter)
            counter += 1
            print("%s) %s" % (identifier, item))

        player_input = input()
        index = ord(player_input[0]) - ord("A")
        if (index < 0 or index > len(items) - 1):
            input("Input %s not recognized. Press ENTER to try again.")
            return False

        itemUse = items[index]
        match itemUse:
            case ItemType.POTION:
                # The Item.UsePotion(int) function returns false if the player fails to select a target.
                # If that happens, we should skip the rest of execution and go back to getting player input.
                if not Item.UsePotion(30, player_pokemon):
                    return False
                else:
                    items.pop(index)

            case ItemType.POKEBALL:
                if allow_pokeball:
                    caught = Item.UsePokeball(opponent, player_pokemon, ItemType.POKEBALL)
                    items.pop(index)
                    if caught:
                        continueBattling = False
                        xpGain = opponent.GetExperienceValue()
                        print()
                        print("%s has gained %s XP!" % (player_pokemon[0].name, xpGain))
                        player_pokemon[0].GainExperience(xpGain)
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
                    items.pop(index)
                    if caught:
                        continueBattling = False
                        xpGain = opponent.GetExperienceValue()
                        print()
                        print("%s has gained %s XP!" % (player_pokemon[0].name, xpGain))
                        player_pokemon[0].GainExperience(xpGain)
                        input("*Press ENTER to continue*")
                        Formatting.clearScreen()
                        return False
                else:
                    print("You can't use this item on that Pokemon!")
                    input("*Press ENTER to continue...*")
                    Formatting.clearScreen()

        return True


    def UsePokedex(opponent: Pokemon):
        print("You pull out your Pokedex and point it at the %s..." % (opponent.name))
        print("*Analyzing...*")
        sleep(1)
        print("...")
        sleep(1)
        print("*BEEP*")
        sleep(1)
        print("...")
        typePhrase = "%s" % (opponent.battleType1)
        if opponent.battleType2 != BattleType.NONE:
            typePhrase += " and %s" % (opponent.battleType2)

        print("%s, a %s type. This one appears to be level %s." % (opponent.name, typePhrase, opponent.level))
        print()
        try:
            pokemonimg = "images/%s.jpg" % (opponent.name)
            img = Image.open(pokemonimg)
            img.show()
        except:
            print("No visual data found for this Pokemon.")

    
    def TryToRun(trainerPokemon: Pokemon, wildPokemon: Pokemon) -> bool:
        print("You try to run...")
        escapeFailed = False
        odds = (int)((trainerPokemon.GetStatValue(PokemonStat.SPEED) * 2) / (wildPokemon.GetStatValue(PokemonStat.SPEED) / 2)) * 15
        escapeFailed = random.randint(1,100) > odds

        if escapeFailed:
            print("the wild %s blocks your path!" % (wildPokemon.name))
        else:
            print("SUCCESS!")
            input("*Press ENTER to continue*")

        return escapeFailed

    
    def CheckForKnockout(pokemon: Pokemon) -> bool:
        if pokemon.currentHP <= 0:
            pokemon.currentHP = 0
            pokemon.statusCondition = Status.KNOCKED_OUT
            print("%s is no longer able to battle!" % (pokemon.name))
            return True
        else:
            return False


    def SwapPokemon(pokemonList: List[Pokemon]):
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
        optionCounter = 0
        for p in pokemonList:
            status = p.statusCondition
            optionLetter = chr((ord("A") + optionCounter))
            statusString = "%s" % (status) if status != Status.NONE else ""
            print("%s) %s - Level: %s, HP: %s/%s %s" % (optionLetter, p.name, p.level, p.currentHP, p.calculateMaxHp(), statusString))
            optionCounter += 1

        player_input = input()
        if len(player_input) > 1:
            print("Input %s is not understood. Try again.")
            input("*Press ENTER to continue*")
            BattleEngine.SwapPokemon(pokemonList)

        else:
            chosen_index = ord(player_input[0]) - ord("A")
            if chosen_index == 0:
                print("That Pokemon is already active! Please try again.")
                input("*Press ENTER to continue*")
                BattleEngine.SwapPokemon(pokemonList)

            elif chosen_index < 0 or chosen_index > 5:
                print("Input %s is not understood. Try again.")
                input("*Press ENTER to continue*")
                BattleEngine.SwapPokemon(pokemonList)

            elif pokemonList[chosen_index].currentHP <= 0:
                print("%s is knocked out! Choose another Pokemon!" % (pokemonList[chosen_index].name))
                input("*Press ENTER to continue*")
                BattleEngine.SwapPokemon(pokemonList)

            else:
                print("You: %s, return! I choose you, %s!" % (pokemonList[0].name, pokemonList[chosen_index].name))
                pokemonList[0], pokemonList[chosen_index] = pokemonList[chosen_index], pokemonList[0]


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
                    dmg = 1 + (int)(p.calculateMaxHp()/20)
                    print("The poison causes %s to wince. It takes %s damage." % (p.name, dmg))
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
                        damage = 2 + (int)(p.calculateMaxHp() / 10)
                        print("%s winces as it's burned skin throbs. It takes %s damage!" % (p.name, damage))

                case Status.CURSED:
                    if roll + p.HPStat / 4 > 100:
                        print("%s overcame the curse with sheer will power!" % (p.name))
                        p.statusCondition = Status.NONE
                    else:
                        print("%s is trembling in fear, it can't focus!" % (p.name, damage))

        input("*Press ENTER to continue...*")


    def DoBurnChance(target: Pokemon, odds: float):
        roll = random.randint(1,100)
        if roll < odds * 100:
            print("%s got burned!" % (target.name))
            target.statusCondition = Status.BURNED
            input("*Press ENTER to continue...*")


    def DoSleepChance(target: Pokemon, odds: float):
        roll = random.randint(1,100)
        if roll < odds * 100:
            print("%s fell asleep!" % (target.name))
            target.statusCondition = Status.ASLEEP
            input("*Press ENTER to continue...*")


    def DoPoisonChance(target: Pokemon, odds: float):
        roll = random.randint(1,100)
        if roll < odds * 100:
            print("%s got poisoned!" % (target.name))
            target.statusCondition = Status.POISONED
            input("*Press ENTER to continue...*")


    def DoFreezeChance(target: Pokemon, odds: float):
        roll = random.randint(1,100)
        if roll < odds * 100:
            print("%s is frozen solid in a block of ice!" % (target.name))
            target.statusCondition = Status.FROZEN
            input("*Press ENTER to continue...*")


    def DoParalyzeChance(target: Pokemon, odds: float):
        roll = random.randint(1,100)
        if roll < odds * 100:
            print("%s is moving stiffly, it's been paralyzed!" % (target.name))
            target.statusCondition = Status.PARALYZED
            input("*Press ENTER to continue...*")


    def DoConfuseChance(target: Pokemon, odds: float):
        roll = random.randint(1,100)
        if roll < odds * 100:
            print("%s is acting strangely, it's confused!" % (target.name))
            target.statusCondition = Status.CONFUSED
            input("*Press ENTER to continue...*")


    def DoAbsorb(target: Pokemon, caster: Pokemon, amount: int):
        actualHealed = amount
        damage = caster.calculateMaxHp() - caster.currentHP
        if damage < amount:
            actualHealed = damage

        print("%s drains energy from %s! %s is healed for %s HP." % (caster.name, target.name, caster.name, actualHealed))
        caster.HealHP(actualHealed)
        input("*Press ENTER to continue...*")