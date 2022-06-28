import random
from time import sleep
from battleAttack import BattleAttack
from enums import BattleType, ItemType, PokemonStat, Status
from formatting import Formatting
from item import Item
from pokemon import Pokemon
from typing import List

class BattleEngine:
    # def __init__(self):

    def DoWildBattle(player_pokemon: List[Pokemon], wildPokemon: Pokemon, items: List[ItemType]):
        continueBattling = True
        while (continueBattling):
            Formatting.clearScreen()
            if (wildPokemon.currentHP <= 0):
                continueBattling = False
                xpGain = wildPokemon.GetExperienceValue()
                print("%s has fainted." % (wildPokemon.name))
                print()
                print("%s has gained %s XP!" % (player_pokemon[0].name, xpGain))
                player_pokemon[0].GainExperience(xpGain)
                input("*Press ENTER to continue*")
                Formatting.clearScreen()
                continue

            if (player_pokemon[0].currentHP <= 0):
                BattleEngine.SwapPokemon(player_pokemon)

            wildPokemonHealthiness = "completely untouched"
            healthPercentage = wildPokemon.currentHP / wildPokemon.calculateMaxHp()
            if (healthPercentage < 0.95):
                wildPokemonHealthiness = "a little scratched up"
            if (healthPercentage < 0.7):
                wildPokemonHealthiness = "like it's taken a few hits"
            if (healthPercentage < 0.5):
                wildPokemonHealthiness = "tired"
            if (healthPercentage < 0.3):
                wildPokemonHealthiness = "pretty beat up"
            if (healthPercentage < 0.1):
                wildPokemonHealthiness = "like it is about to faint"
            print("The wild %s looks %s." % (wildPokemon.name, wildPokemonHealthiness))
            print("Your %s has %s/%s HP remaining." % (player_pokemon[0].name, player_pokemon[0].currentHP, player_pokemon[0].calculateMaxHp()))

            print()
            for action in ("A) ATTACK", "B) ITEM", "C) SWAP POKEMON", "D) RUN", "E) POKEDEX"):
                print(action)

            userAction = input()
            Formatting.clearScreen()

            if (userAction != "A" and userAction != "B" and userAction != "C" and userAction != "D" and userAction != "E"):
                input("Input %s unrecognized. Press ENTER to try again." % (userAction))
                continue
            elif (userAction == "A"):
                Formatting.clearScreen()
                print("Choose attack:")
                for i in range(0, len(player_pokemon[0].GetBattleAttacks())):
                    letterChoice = chr(ord("A") + i)
                    attack = player_pokemon[0].GetBattleAttacks()[i]
                    print("%s) %s (%s/%s)" % (letterChoice, attack.name, attack.currentPP, attack.maxPP))

                player_input = input()
                attackIndex = ord(player_input[0]) - ord("A")
                if attackIndex < 0 or attackIndex > 3:
                    input("Input %s unrecognized. Press ENTER to try again." % (player_input))
                    continue

                attackChoice = player_pokemon[0].GetBattleAttacks()[attackIndex]

                if (attackChoice.currentPP <= 0):
                    input("No more PP available for that attack, choose something else. Press ENTER to try again.")
                    continue

                Formatting.clearScreen()
                print("You: %s, use %s!" % (player_pokemon[0].name, attackChoice.name))
                print()
                if (wildPokemon.GetStatValue(PokemonStat.SPEED) > player_pokemon[0].GetStatValue(PokemonStat.SPEED)):
                    print("The wild %s is faster!" % (wildPokemon.name))
                    wildPokemon.RandomAttack(player_pokemon[0])
                    if not BattleEngine.CheckForKnockout(player_pokemon[0]):
                        player_pokemon[0].DoAttack(attackIndex, wildPokemon)
                else:
                    player_pokemon[0].DoAttack(attackIndex, wildPokemon)
                    if not BattleEngine.CheckForKnockout(wildPokemon):
                        wildPokemon.RandomAttack(player_pokemon[0])

                input("*Press ENTER to continue...*")
            elif (userAction == "B"):
                if len(items) == 0:
                    print("You have no items.")
                    input("*Press ENTER to continue*")
                    continue

                Formatting.clearScreen()
                itemCounter = 0
                for item in items:
                    optionIdentifier = chr(ord("A") + itemCounter)
                    print("%s) %s" % (optionIdentifier, item))

                player_input = input()
                index = ord(player_input[0]) - ord("A")
                if (index < 0 or index > len(items) - 1):
                    input("Input %s not recognized. Press ENTER to try again.")
                    continue

                itemUse = items[index]
                match itemUse:
                    case ItemType.POTION:
                        # The Item.UsePotion(int) function returns false if the player fails to select a target.
                        # If that happens, we should skip the rest of execution and go back to getting player input.
                        if not Item.UsePotion(30, player_pokemon):
                            continue
                        else:
                            items.pop(index)

                    case ItemType.POKEBALL:
                        caught = Item.UsePokeball(wildPokemon, player_pokemon, ItemType.POKEBALL)
                        items.pop(index)
                        if caught:
                            continueBattling = False
                            continue

                wildPokemon.RandomAttack(player_pokemon[0])
                input("*Press ENTER to continue...*")


            elif (userAction == "C"):
                BattleEngine.SwapPokemon(player_pokemon)
            elif (userAction == "D"):
                continueBattling = BattleEngine.TryToRun(player_pokemon[0], wildPokemon)

                # Get hit if they don't escape
                if continueBattling:
                    wildPokemon.RandomAttack(player_pokemon[0])
            elif (userAction == "E"):
                print("You pull out your Pokedex and point it at the %s..." % (wildPokemon.name))
                print("*Analyzing...*")
                sleep(3)
                typePhrase = "%s" % (wildPokemon.battleType1)
                if wildPokemon.battleType2 != BattleType.NONE:
                    typePhrase += " and %s" % (wildPokemon.battleType2)

                print("%s, a %s type. This one appears to be level %s." % (wildPokemon.name, typePhrase, wildPokemon.level))
                print()
                input("*Press ENTER to continue...*")


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
            statusString = "(Knocked Out)" if status == Status.KNOCKED_OUT else ""
            print("%s) %s %s" % (optionLetter, p.name, statusString))
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
