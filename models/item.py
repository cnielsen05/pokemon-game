import random
from time import sleep
from typing import List
from common.enums import ItemType, Status
from common.formatting import Formatting
from models.pokemon import Pokemon

class Item:
    def ChooseItem(items: List[ItemType]) -> ItemType:
        notChosen = True
        while (notChosen):
            unique_items = []
            counts = {}
            player_options = []
            for item in items:
                try:
                    unique_items.index(item)
                    counts[item] += 1
                except:
                    unique_items.append(item)
                    counts[item] = 1

            counter = 0
            for item in unique_items:
                identifier = chr(ord("A") + counter)
                counter += 1
                player_options.append("%s) %s (Owned: %s)" % (identifier, item, counts[item]))

            index = Formatting.GetUserChoice(player_options)

            if (index == -1 or index > len(unique_items)):
                input("Input %s not recognized. Press ENTER to try again.")
                continue

            if index == -2 :
                # Player chose BACK
                return None

            chosenItem = unique_items[index]
            originalIndex = 0
            while originalIndex < len(items):
                if items[originalIndex] == chosenItem:
                    break
                else:
                    originalIndex += 1

            notChosen = False
            return originalIndex


    def UsePotion(healAmount: int, player_pokemon: List[Pokemon]) -> bool:
        print("Which Pokemon will you use the potion on?")
        counter = 0
        options = []
        for pokemon in player_pokemon:
            identifier = chr(ord("A") + counter)
            counter += 1
            options.append("%s) %s" % (identifier, pokemon.name))

        index = Formatting.GetUserChoice(options)
        if (index < 0 or index > len(player_pokemon) - 1):
            return False

        chosen_pokemon = player_pokemon[index]
        print("You use POTION on %s!" % (chosen_pokemon.name))
        chosen_pokemon.HealHP(healAmount)
        input("*Press ENTER to continue...*")
        return True


    def UsePokeball(target: Pokemon, player_pokemon: List[Pokemon], ball: ItemType) -> bool:
        ballFactor = 0.0
        match ball:
            case ItemType.POKEBALL:
                ballFactor = 1.0

            case ItemType.GREATBALL:
                ballFactor = 1.5

        odds = target.catchFactor + (target.catchFactor * ballFactor)*(1 - (target.currentHP/target.CalculateMaxHp()))
        if target.statusCondition != Status.NONE:
            odds *= 1.2

        roll = random.randint(1,100)
        if roll < 5:
            print("*Your fingers glow for a moment as the ball leaves your hand...*")
            odds *= 0.65
        elif roll < 15:
            print("*You throw the ball expertly, like you were made for this! Amazing!*")
        elif roll < 30:
            print("*You throw the ball deftly, making it look easy! Excellent!*")
        elif roll < 60:
            print("*You throw the ball accurately! Nice one!*")
        elif roll < 90:
            print("*You throw the ball and barely hit your target!*")
        else:
            print("*You trip while you throw the ball!*")
            odds *= 1.5

        if odds * 100 < roll:
            sleep(1)
            print("*Shake* ...")
            sleep(1)
            print("*Shake* ...")
            sleep(1)
            print("*%s breaks out of the ball!*" % (target.name))
            print()
            input("*Press ENTER to continue...*")
            return False
        else:
            print("*You throw the ball!*")
            sleep(1)
            print("*Shake* ...")
            sleep(1)
            print("*Shake* ...")
            sleep(1)
            print("*You caught %s! Congratulations!*" % (target.name))
            print()
            input("*Press ENTER to continue...*")
            player_pokemon.append(target)

            while len(player_pokemon) >= 7:
                Formatting.clearScreen()
                print("You have too many Pokemon! You will have to let one go... who will you say goodbye to?")
                counter = 0
                for pokemon in player_pokemon:
                    identifier = chr(ord("A") + counter)
                    counter += 1

                    print("%s) %s" % (identifier, pokemon.name))

                player_choice = input()
                index = ord(player_choice[0]) - ord("A")
                if index < 0 or index > len(player_pokemon) - 1:
                    input("Input %s unrecognized. Press ENTER to try again..." % (player_choice))
                    continue

                print()
                print("You: Goodbye %s! Thank you for everything!" % (player_pokemon[index].name))
                player_pokemon.pop(index)

            return True