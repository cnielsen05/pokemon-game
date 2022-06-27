import os
import random
from enums import Item, PokemonStat, Status
from pokemon import Pokemon
from typing import List

class BattleEngine:
    # def __init__(self):

    def DoWildBattle(trainerPokemon: List[Pokemon], wildPokemon: Pokemon, items: List[Item]):
        continueBattling = True
        while (continueBattling):
            os.system("cls")
            if (wildPokemon.currentHP <= 0):
                continueBattling = False
                xpGain = wildPokemon.GetExperienceValue()
                print("%s has fainted." % (wildPokemon.name))
                print()
                print("%s has gained %s XP!" % (trainerPokemon[0].name, xpGain))
                trainerPokemon[0].GainExperience(xpGain)
                input("*Press ENTER to continue*")
                os.system("cls")
                continue

            if (trainerPokemon[0].currentHP <= 0):
                BattleEngine.SwapPokemon(trainerPokemon)

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
            print("Your %s has %s/%s HP remaining." % (trainerPokemon[0].name, trainerPokemon[0].currentHP, trainerPokemon[0].calculateMaxHp()))

            print()
            for action in ("A) ATTACK", "B) ITEM", "C) SWAP POKEMON", "D) RUN"):
                print(action)

            userAction = input()
            os.system("cls")

            if (userAction != "A" and userAction != "B" and userAction != "C" and userAction != "D"):
                input("Input %s unrecognized. Press ENTER to try again." % (userAction))
                continue
            elif (userAction == "A"):
                os.system("cls")
                print("Choose attack:")
                for i in range(0, len(trainerPokemon[0].battleAttacks)):
                    letterChoice = chr(ord("A") + i)
                    attack = trainerPokemon[0].battleAttacks[i]
                    print("%s) %s (%s/%s)" % (letterChoice, attack.name, attack.currentPP, attack.maxPP))

                player_input = input()
                attackIndex = ord(player_input[0]) - ord("A")
                if attackIndex < 0 or attackIndex > 3:
                    input("Input %s unrecognized. Press ENTER to try again." % (player_input))
                    continue

                attackChoice = trainerPokemon[0].battleAttacks[attackIndex]

                if (attackChoice.currentPP <= 0):
                    input("No more PP available for that attack, choose something else. Press ENTER to try again.")
                    continue

                os.system("cls")
                print("You: %s, use %s!" % (trainerPokemon[0].name, attackChoice.name))
                print()
                if (wildPokemon.GetStatValue(PokemonStat.SPEED) > trainerPokemon[0].GetStatValue(PokemonStat.SPEED)):
                    print("The wild %s is faster!" % (wildPokemon.name))
                    wildPokemon.RandomAttack(trainerPokemon[0])
                    if not BattleEngine.CheckForKnockout(trainerPokemon[0]):
                        trainerPokemon[0].DoAttack(attackIndex, wildPokemon)
                else:
                    trainerPokemon[0].DoAttack(attackIndex, wildPokemon)
                    if not BattleEngine.CheckForKnockout(wildPokemon):
                        wildPokemon.RandomAttack(trainerPokemon[0])

                input("*Press ENTER to continue...*")
            elif (userAction == "B"):
                if len(items) == 0:
                    print("You have no items.")
                    input("*Press ENTER to continue*")
                    continue

                os.system("cls")
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
                    case Item.POTION:
                        print("You use POTION on %s!" % (trainerPokemon[0].name))
                        missingHP = trainerPokemon[0].calculateMaxHp() - trainerPokemon[0].currentHP
                        if missingHP >= 30:
                            trainerPokemon[0].currentHP += 30
                            print("%s heals for 30 HP!" % (trainerPokemon[0].name))
                        else:
                            trainerPokemon[0].currentHP += missingHP
                            print("%s heals for %s HP!" % (trainerPokemon[0].name, missingHP))

                    case Item.POKEBALL:
                        print("Not yet implemented, sorry!")

                wildPokemon.RandomAttack(trainerPokemon[0])
                input("*Press ENTER to continue...*")


            elif (userAction == "C"):
                BattleEngine.SwapPokemon(trainerPokemon)
            elif (userAction == "D"):
                continueBattling = BattleEngine.TryToRun(trainerPokemon[0], wildPokemon)

                # Get hit if they don't escape
                if continueBattling:
                    wildPokemon.RandomAttack(trainerPokemon[0])


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

        os.system('cls')
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
