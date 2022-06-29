import random
from time import sleep
from typing import List
from enums import ItemType
from formatting import Formatting
from pokemon import Pokemon

class Item:
    def UsePotion(healAmount: int, player_pokemon: List[Pokemon]) -> bool:
        print("Which Pokemon will you use the potion on?")
        counter = 0
        for pokemon in player_pokemon:
            identifier = chr(ord("A") + counter)
            counter += 1
            print("%s) %s" % (identifier, pokemon.name))

        player_input = input()
        index = ord(player_input[0]) - ord("A")
        if (index < 0 or index > len(player_pokemon) - 1):
            input("Input %s not recognized. Press ENTER to try again.")
            return False

        chosen_pokemon = player_pokemon[index]
        print("You use POTION on %s!" % (chosen_pokemon.name))
        chosen_pokemon.HealHP(healAmount)
        return True


    def UsePokeball(target: Pokemon, player_pokemon: List[Pokemon], ball: ItemType) -> bool:
        ballFactor = 0.0
        match ball:
            case ItemType.POKEBALL:
                ballFactor = 1.0

            case ItemType.GREATBALL:
                ballFactor = 1.5

        odds = target.catchFactor * ballFactor + 0.25*(1 - (target.currentHP/target.calculateMaxHp()))
        roll = random.randint(1,100)
        if roll < 5:
            print("*Your fingers glow for a moment as the ball leaves your hand...*")
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
        if odds * 100 > roll:
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