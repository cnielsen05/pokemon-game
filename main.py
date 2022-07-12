# main.py
import json
import os
import random
import sys
import time
from typing import List

from battleEngine import BattleEngine
from common.enums import ItemType, MenuState
from common.formatting import Formatting
from models.item import Item
from models.pokemon import Pokemon
from models.route import Route

# Globals for asynchronous code to share information
CurrentMenuState = MenuState.NONE
steps_taken = 0

if sys.platform == 'win32':
    import msvcrt
else:
    from select import select
    import termios

class Game:
    instance = None

    def __init__(self, savedProfile = None):
        if Game.instance != None:
            raise Exception("Singleton class can only be instantiated once!")

        self.keepPlaying = True
        self.player_pokemon = []
        self.rival_pokemon = []
        self.items = []
        self.playerMoney = 0
        self.state = {
            "choose_starter_complete": False,
            "route_one_complete": False,
            "route_two_complete": False,
        }
        self.profile = None

        if savedProfile:
            self.profile = savedProfile
            savedFile = os.path.join(os.getcwd(), "data", "savedgames", savedProfile)
            with open(savedFile, 'r') as playerProfile:
                data = json.load(playerProfile)
                self.player_pokemon = []
                self.rival_pokemon = []
                self.items = data["items"]
                self.playerMoney = data["playerMoney"]
                self.state = data["state"]

                for p in data["player_pokemon"]:
                    pokemon = Pokemon(p["name"])
                    pokemon.level = p["level"]
                    pokemon.currentHP = p["currentHP"]

                    self.player_pokemon.append(pokemon)

                for p in data["rival_pokemon"]:
                    pokemon = Pokemon(p["name"])
                    pokemon.level = p["level"]
                    pokemon.FullHealHP()

                    self.rival_pokemon.append(pokemon)

        Game.instance = self


    def StartGame():
        print("Welcome to the world of Pokemon! What would you like to do:")
        options = ["Continue", "New Game"]
        player_choice_index = Formatting.GetUserChoice(options, noBack=True)
        player_choice = options[player_choice_index]

        if player_choice == "Continue":
            print("Which profile would you like to continue on?")
            profileOptions = []
            directory = os.getcwd() + "/data/savedgames"
            os.makedirs(directory, exist_ok=True)
            for root, dirs, files in os.walk(directory):
                for f in files:
                    profileOptions.append(f)

            profile_choice_index = Formatting.GetUserChoice(profileOptions)
            if profile_choice_index == -2:
                print("Sorry, no saved game files were found!")
                Formatting.PressEnterToContinue()
                Game.StartGame()
                
            profile = profileOptions[profile_choice_index]

            continue_game = Game(profile)
            continue_game.Run()

        elif player_choice == "New Game":
            new_game = Game()
            new_game.profile = input("What would you like your profile to be called? ")
            Formatting.clearScreen()
            new_game.Run()


    def Run(self):
        keepPlaying = True
        while(keepPlaying):
            if (not self.state["choose_starter_complete"]):
                self.PlayIntro()
            self.DoTown()


    def GetInstance():
        if instance == None:
            instance = Game()
        return instance


    def SaveGame(self):
        print("Saving game...")
        data = {
            "player_pokemon": [],
            "rival_pokemon": [],
            "items": self.items,
            "playerMoney": self.playerMoney,
            "state": self.state
        }
        for p in self.player_pokemon:
            data["player_pokemon"].append({"name": p.name, "level": p.level, "currentHP": p.currentHP})

        for p in self.rival_pokemon:
            data["rival_pokemon"].append({"name": p.name, "level": p.level})
        
        saveFilePath = os.path.join(os.getcwd(), "data", "savedgames", self.profile.lower())
        os.makedirs(saveFilePath, exist_ok=True)

        with open(saveFilePath, 'w') as outfile:
            outfile.write(json.dumps(data))
        
        time.sleep(3)
        print("Save complete.")


    def Do_Route(self, routeid):
        global CurrentMenuState

        steps_taken = 0
        route = Route(routeid)
        Formatting.clearScreen()
        print("Beginning your journey on %s." % (route.Name))
        CurrentMenuState = MenuState.IS_WALKING
        
        while (steps_taken < route.Length):
            if CurrentMenuState == MenuState.IS_WALKING:
                steps_taken = self.DoWalk(route.Length, steps_taken, route.WildPokemonList, self.player_pokemon, self.items, route.HiddenItemList, route.WildPokemonLevelRange, route.TrainerBattles)
            elif CurrentMenuState == MenuState.IS_CAMPING:
                self.DoCamping()
            Formatting.clearScreen()

        print("You have reached the end of %s!" % (route.Name))
        CurrentMenuState = MenuState.IS_IN_TOWN
 

    def DoWalk(self, 
        route_length: int, 
        steps_taken: int,
        wildPokemonList: List[str], 
        trainerPokemon: List[Pokemon], 
        trainerItems: List[ItemType], 
        hiddenItems: List[ItemType], 
        wildPokemonLevelRange: List[int],
        trainerBattles: List[object]):

        global CurrentMenuState

        while CurrentMenuState == MenuState.IS_WALKING and steps_taken < route_length:
            self.UserInputInterrupt(1)
            if CurrentMenuState == MenuState.IS_WALKING:
                steps_taken += 1
                trainerBattle = trainerBattles[steps_taken - 1]
                if not trainerBattle is None:
                    print("*You are traveling along the route (step %s of %s)" % (steps_taken, route_length)) 
                    self.EncounterTrainer(trainerBattle)
                else:
                    print("*You are traveling along the route... press ENTER to pause (step %s of %s)" % (steps_taken, route_length))
                    hadEncounter = Game.DoWildPokemonEncounterChance(wildPokemonList, trainerPokemon, trainerItems, wildPokemonLevelRange)
                    if not hadEncounter:
                        self.FindHiddenItemChance(hiddenItems)
                CurrentMenuState = MenuState.IS_WALKING

            else:
                # User interrupted the walking
                return steps_taken

        return steps_taken


    def UserInputInterrupt(self, timeout: int):
        global CurrentMenuState

        if sys.platform == 'win32':
            start_time = time.time()
            while True:
                if msvcrt.kbhit():
                    CurrentMenuState = MenuState.IS_CAMPING
                elif time.time() - start_time > timeout:
                    break

        else:
            rlist, _, _ = select([sys.stdin], [], [], timeout)
            if rlist:
                termios.tcflush(sys.stdin, termios.TCIOFLUSH)
                CurrentMenuState = MenuState.IS_CAMPING


    def DoCamping(self):
        global CurrentMenuState

        print("Setting up camp...")
        print()
        time.sleep(1)
        awaitingChoice = True
        while (awaitingChoice):
            Formatting.clearScreen()
            commands = ['ITEM', 'CAMP', 'SWITCH_LEAD_POKEMON']
            chosen_index = Formatting.GetUserChoice(commands)

            if chosen_index == -2:
                # User chose BACK
                Formatting.clearScreen()
                print("Resuming the journey...")
                print()
                Formatting.PressEnterToContinue()
                CurrentMenuState = MenuState.IS_WALKING
                awaitingChoice = False
                continue

            if chosen_index == -1 or chosen_index > len(commands) - 1:
                continue

            match commands[chosen_index]:
                case 'ITEM':
                    if len(self.items) == 0:
                        print("You have no items.")
                        input("*Press ENTER to continue*")
                        continue

                    Formatting.clearScreen()
                    itemIndex = Item.ChooseItem(self.items)

                    if itemIndex is None:
                        # Player chose BACK
                        continue

                    itemToUse = self.items[itemIndex]
                    match itemToUse:
                        case ItemType.POTION:
                            # The Item.UsePotion(int) function returns false if the player fails to select a target.
                            # If that happens, we should skip the rest of execution and go back to getting player input.
                            if not Item.UsePotion(30, self.player_pokemon):
                                continue
                            else:
                                self.items.pop(itemIndex)

                        case ItemType.POKEBALL:
                            print("*You roll the Pokeball back and forth in your palm, imagining your next throw...*")
                        case ItemType.GREATBALL:
                            print("*You roll the Greatball back and forth in your palm, imagining your next throw...*")
                        case ItemType.CAMPING_KIT:
                            print("You need to CAMP to use this.")

                    Formatting.PressEnterToContinue()
                    awaitingChoice = False

                case 'CAMP':
                    try:
                        index = self.items.index(ItemType.CAMPING_KIT)
                        self.items.pop(index)
                    except:
                        print("You don't have any camping kits! Try buying one in town.")
                        Formatting.PressEnterToContinue()
                        continue

                    print("Camping!")
                    time.sleep(2)
                    print("...")
                    time.sleep(2)
                    for pokemon in self.player_pokemon:
                        for move in pokemon.GetBattleAttacks():
                            move.currentPP = move.maxPP

                        damage = pokemon.CalculateMaxHp() - pokemon.currentHP
                        healedAmount = 50
                        if damage < 50:
                            healedAmount = damage
                        pokemon.currentHP += healedAmount
                        print("%s healed %s HP and had its PP restored!" % (pokemon.name, healedAmount))

                    Formatting.PressEnterToContinue()
                    awaitingChoice = False

                case 'SWITCH_LEAD_POKEMON':
                    BattleEngine.SwapPokemon(self.player_pokemon)


    def DoTown(self):
        print("You are in town. What you you like to do?")
        print()
        options = ["Pokemon Center", "PokeMart", "Continue Journey", "Save and Continue", "Save and Quit"]
        player_choice_index = Formatting.GetUserChoice(options, noBack=True)
        choice = options[player_choice_index]
        if choice == "Pokemon Center":
            if self.playerMoney > 100:
                print("You pay 100 Pokecoins for the services.")
                self.playerMoney -= 100
            else:
                print("You don't have enough money to pay! This time will be on the house, try to do better out there!")

            for p in self.player_pokemon:
                p.FullHealHP()
                p.RestoreAllPP()

            print("All of your Pokemon have had their HP and PP restored!")
            Formatting.PressEnterToContinue()

        elif choice == "PokeMart":
            options = ["POTION - $50", "POKEBALL - $50", "CAMPING_KIT - $150"]
            done = False
            while not done:
                print("You have %s Pokecoins. What would you like to buy?" % (self.playerMoney))
                player_choice_index = Formatting.GetUserChoice(options)

                if player_choice_index == -1 or player_choice_index >= len(options):
                    continue

                elif player_choice_index == 0:
                    if self.playerMoney >= 50:
                        print("You bought a POTION!")
                        self.items.append(ItemType.POTION)
                        self.playerMoney -= 50
                    else:
                        print("You can't afford that!")

                elif player_choice_index == 1:
                    if self.playerMoney >= 50:
                        print("You bought a POKEBALL!")
                        self.items.append(ItemType.POKEBALL)
                        self.playerMoney -= 50
                    else:
                        print("You can't afford that!")

                elif player_choice_index == 2:
                    if self.playerMoney >= 150:
                        print("You bought a CAMPING_KIT!")
                        self.items.append(ItemType.CAMPING_KIT)
                        self.playerMoney -= 150
                    else:
                        print("You can't afford that!")

                elif player_choice_index == -2:
                    done = True

                Formatting.PressEnterToContinue()

        elif choice == "Continue Journey":
            if (not self.state["route_one_complete"]):
                self.Do_Route("routeone")
                self.state["route_one_complete"] = True
            elif (not self.state["route_two_complete"]):
                self.Do_Route("routetwo")
                self.state["route_two_complete"] = True
            else:
                self.GrassGym()
                print("Congratulations, you've reached the end of the game! You WIN!")
                keepPlaying = False

        elif choice == "Save and Continue":
            self.SaveGame()
            Formatting.PressEnterToContinue()

        elif choice == "Save and Quit":
            self.SaveGame()
            quit()


    def FindHiddenItemChance(self, hiddenItemList: List[ItemType]):
        if random.randint(1,100) > 93:
            print("You found a hidden item!")
            whichItem = random.randint(0,len(hiddenItemList) - 1)
            found_item = hiddenItemList[whichItem]

            if found_item == ItemType.POKEFEAST:
                time.sleep(1)
                print()
                print("Lucky you! You've stumbled across a huge feast of wild berries and all of your Pokemon dig in! Delicious and nutritious!")
                print()
                print("Your Pokemon have all had their HP restored!")
                for pokemon in self.player_pokemon:
                    pokemon.HealHP(30)
            else:
                print("You have acquired... %s!" % (found_item))
                self.items.append(found_item)

            Formatting.PressEnterToContinue()


    def DoWildPokemonEncounterChance(wildPokemonList: List[str], trainerPokemon: List[Pokemon], trainerItems: List[ItemType], wildPokemonLevelRange: List[int]) -> bool:
        global isWalking
        global isBattling

        encounterWildPokemon = random.randint(0,9) > 7
        if (encounterWildPokemon):
            isWalking = False
            isBattling = True
            whichPokemon = random.randint(0, len(wildPokemonList) - 1)
            wildPokemon = Pokemon(wildPokemonList[whichPokemon])
            levelIndex = random.randint(0, len(wildPokemonLevelRange) - 1)
            wildPokemon.level = wildPokemonLevelRange[levelIndex]
            wildPokemon.FullHealHP()
            print()
            print("A wild %s has appeared!\n\nPress ENTER to continue..." % (wildPokemon.name))
            input()
            BattleEngine.DoWildBattle(trainerPokemon, wildPokemon, trainerItems)
            isBattling = False

        return encounterWildPokemon


    def EncounterTrainer(self, trainerBattle: object):
        global CurrentMenuState

        CurrentMenuState = MenuState.IS_BATTLING

        opp_pokemon = []
        for p in trainerBattle["Pokemon"]:
            newPoke = Pokemon(p["name"])
            newPoke.level = p["level"]
            newPoke.FullHealHP()
            opp_pokemon.append(newPoke)

        print("%s wants to battle!" % (trainerBattle["Name"]))
        Formatting.PressEnterToContinue()
        BattleEngine.DoTrainerBattle(self.player_pokemon, opp_pokemon, self.items, trainerBattle["Name"], trainerBattle["Money"], trainerBattle["StartLine"], trainerBattle["EndLine"])
        self.playerMoney += trainerBattle["Money"]


    def PlayIntro(self):
        answered_mom = False
        while (not answered_mom):
            Formatting.clearScreen()
            print("*You sit alone in your room, mostly quiet except for the rumbling from an old television set in the corner.*")
            print()
            print("Professor Mulberry: Hello, and welcome to the world of Pokemon. I am Professor Mulberry and you are in the great Jarea region.")
            print("Professor Mulberry: I am hiring trainers in this region for...RESEARCH! I am getting too old to do it myself, so now... LET'S START YOUR JOURNEY!")
            print("")
            print("*Your mom walks into the room.*")
            print("")

            options = [
                "NO! I DO WAT I WANNA!", 
                "Yes, mom."]

            print("Mom: Stop watching TV, it's late. NOW RUN OFF TO BED!")
            player_choice_index = Formatting.GetUserChoice(options, noBack=True)

            if player_choice_index == 0:
                print("Enraged Mom: YOU DO NOT TALK TO ME LIKE THAT! NOW GO TO BED! TOMORROW IS YOUR BIRTHDAY AND YOU WILL NEED ALL YOUR ENERGY FOR YOUR POKEMON ADVENTURE!!!")
                print("*You walk sadly to your room and cry yourself to sleep.*")
                answered_mom = True
            elif player_choice_index == 1:
                for i in range(10):
                    self.items.append(ItemType.POKEBALL)
                print("Mom: Thank you for being such a responsible child, I'm so proud of you!")
                print("Mom: That reminds me, you should take these to help you on your journey!")
                print()
                print("You have gained Pokeball x 10.")
                print()
                print("Mom: NOW, GO TO BED!")
                print("*You scamper quickly to your bed and fall fast asleep.*")
                answered_mom = True
            

        Formatting.PressEnterToContinue()
        time.sleep(1)
        print("*As you drift off to sleep, you have an uneasy feeling...*")
        Formatting.PressEnterToContinue()
        print("*You start dreaming, a nightmare...*")
        time.sleep(2)
        Formatting.clearScreen()
        print("*You feel as if you've woken up, but you can't move.*")
        time.sleep(2)
        print("*Dread begins to set over you. A knot forms in your stomach, and you feel like you can't breathe. Nearby, you hear a mix of crunching and squelching sounds.*")
        time.sleep(2)
        print("*You try to run, but your body is paralyzed. You hear something pacing around you, breathing hungrily.*")
        time.sleep(2)
        print("*In an instant, a demonic apparition is above you; it's red eyes burn into your own and you begin to cry. You feel yourself begin to pee.*")
        time.sleep(2)
        print("*The demon screams at you.*")
        time.sleep(2)
        print("Demon: GiVE mE yOuR SOOooOOuuUUlLLL!!!!!")
        Formatting.PressEnterToContinue()
        
        print("*The sun breaks through your curtains and assaults your eyelids. Groggily, you recall something sinister as reality crispens around you and memories of your dream fade away like morning fog. You are awake now.*")
        Formatting.PressEnterToContinue()

        print("*Before you can move, Mom is in your doorway again.*")
        print()
        print("Mom: Finally, I was starting to wonder if you were ever going to get up today, sleepyhead.")
        print("You: What time is it?")
        print("Mom: Just after 10. Would you like some breakfast?")
        print("You: WHAT! After 10!? I'm late!")
        Formatting.PressEnterToContinue()

        print("Mom: Late? For what? I've never seen you move this fast.")
        print("You: I need to get to Professor Mulberry's lab to get my first Pokemon!")
        print("Mom: Oh that, of course!")
        print("Mom: In that case, you'll need...")
        print()
        print("*You ignore her and bolt out the door, promptly falling down the stairs with your pants half on.*")
        time.sleep(1)
        Formatting.PressEnterToContinue()

        print("You: I'm okay!")
        print("*You quickly pull on the rest of your clothes and run out the door before your mom can finish her sentence...*")
        print("Mom: *Sigh*. And just like that, kids are gone. The Pokemon thing doesn't even start until 11:30, what's the rush?")
        print("Mom: That kid really needs to think before acting.")
        Formatting.PressEnterToContinue()

        print("At the door of Professor Mulberry's lab. 10:29 AM")
        print("")
        print("*You bump into a garbage can with a loud CLANG! as you arrive*")
        print("You: Nice, I made it! I think I made good time too...")
        Formatting.PressEnterToContinue()

        print("*A door opens...*")
        time.sleep(1)
        print("Rival kid: What is all that racket!")
        print("Rival kid: Of course, it's the loser!")
        print("Rival kid: What are you doing here, loser?")
        print("You: You don't need to call me names. Obviously I'm here to get my first Pokemon! Aren't you starting your journey this year too?")
        Formatting.PressEnterToContinue()

        print("Rival kid: Wait... hurry? You idiot, do you even know what time it is? Gramps isn't giving out any Pokemon until 11:30, that's not for another hour you idiot!")
        print("You: What do you mean?!")
        print("Rival kid: Exactly like I said! You, the idiotic dumb loser, are ONE HOUR EARLY. You are truly a pea-brained moron.")
        print()

        options = [
            "You're no genius yourself. I should fight you here and now for talking to me that way.", 
            "Oh man, is it really not starting for another hour? I guess this one is my mistake." ]

        player_choice_index = Formatting.GetUserChoice(options, noBack=True)

        if player_choice_index == 0:
            print("You: You're no genius yourself. I should fight you here and now for talking to me that way.")
            print("Rival kid: WHAT! You are choosing the wrong enemy, fool. You WILL regret this.")
            print("*You jump forward toward the Rival kid, feigning a punch.*")
            print("*Rival kid flinches and falls backward, sprawling awkwardly. He trips and falls off the porch, crashing into the trash cans.*")
            print("You: HAHAHAHAHAHAHAHA!!!! Wait... are you okay?")
            print("Rival kid: I'm fine, no thanks to you. I stand by what I said though, you WILL regret your choice today.")
            print("Rival kid: Maybe not today. Maybe not tomorrow. But I will have my revenge and it will hurt. Prepare yourself, fool.")
        elif player_choice_index == 1:
            print("You: Oh man, is it really not starting for another hour? I guess this one is my mistake.")
            print("Rival kid: ...")
            time.sleep(1)
            print("Rival: Wait, you aren't going to insult me back?")
            print("Rival: That makes me feel weird for being mean to you. No way I'm going to apologize to you, so here, take these I guess...")
            print()
            print("*You have acquired Greatball x 5*")
            print()
            print("Rival kid: I'm Gary, by the way. I've seen you around town before, Professor Mulberry is my grandpa. I can't wait to start my Pokemon journey!")
            print("Rival Gary: I'm determined to become greatest Pokemon master ever! I might end up facing you in the Pokemon League, so that makes us rivals.")
            
            for i in range(5):
                self.items.append(ItemType.GREATBALL)

            print("*Gary slams the door shut.*")

        Formatting.PressEnterToContinue()
        print("*You wait around idly for an hour until Professor Mulberry starts giving out the Pokemon...*")
        print("*You enter the Lab promptly at 11:30.*")
        Formatting.PressEnterToContinue()

        print("Professor Mulberry: Welcome trainers! I'm super excited to be a part of starting your journey today!")
        print("Professor Mulberry: You will all start by choosing a starting Pokemon.")
        print("Professor Mulberry: Let me tell you about each of the starting Pokemon you can choose from today.")
        Formatting.PressEnterToContinue()

        while (not self.state["choose_starter_complete"]):
            print("Professor Mulberry: First up is Atsebi, the Fire Snake Pokemon!")
            print("Professor Mulberry: Atsebi specializes in high speed and special attack damage.")
            print("Professor Mulberry: If you like you to strike first and strike hard, Atsebi may be the Pokemon for you!")
            Formatting.PressEnterToContinue()

            print("Professor Mulberry: Next up is Nardent, the Narwhal Warrior Pokemon.")
            print("Professor Mulberry: Nardent excels at physical offense and defense, and is quite durable.")
            print("Professor Mulberry: If you like a balanced approach that combines offense and defense, Nardent may be for you.")
            Formatting.PressEnterToContinue()

            print("Professor Mulberry: Finally we have Leafox, the Forest Spirit Pokemon.")
            print("Professor Mulberry: Leafox is clever and fast, a master of manipulation and deceit.")
            print("Professor Mulberry: If you like to outwit your opponent, you should give Leafox a try!")
            Formatting.PressEnterToContinue()

            Formatting.clearScreen()
            options = ["Atsebi", "Nardent", "Leafox"]
            print("Choose your starter:")
            starter_index = Formatting.GetUserChoice(options)
            if starter_index == -2:
                # User chose BACK, replay the descriptions
                continue

            starter_choice = options[starter_index]
            rival_choice = None

            if starter_choice == "Atsebi":
                rival_choice = "nardent"

            elif starter_choice == "Nardent":
                rival_choice = "leafox"

            elif starter_choice == "Leafox":
                rival_choice = "atsebi"

            starter = Pokemon(starter_choice.lower())
            rival_starter = Pokemon(rival_choice)

            starter.level = 2
            starter.XP = 500
            starter.FullHealHP()
            self.player_pokemon.append(starter)

            rival_starter.level = 1
            rival_starter.FullHealHP()
            self.rival_pokemon.append(rival_starter)
            self.state["choose_starter_complete"] = True


        if (len(self.player_pokemon) > 0):
            print("Professor: Good choice, I'm sure %s will be an excellent companion on your journey!" % (self.player_pokemon[0].name))

        print("Professor: You should do a practice battle before you go. Let me get my nephew in here...")
        print("Professor: *sucks in breath...*")
        print("Professor: GAAAAAAAAAAAAAAAA---")
        time.sleep(1)
        print("Professor: --AAAAAAAAAAAAAARRRYYYYYYYY!!!!!!!!")
        print()
        Formatting.PressEnterToContinue()
        
        print("Rival Gary: I'm here gramps! I hope you aren't calling me to help that loser over there...")
        print("Professor: Gary! What have I told you about speaking to guests that way?")
        print("Professor: But, yes. Actually, I did want you to have a practice battle with this kid.")
        Formatting.PressEnterToContinue()

        print("Rival Gary: Ugh, I would never disgrace myself like this normally... but Gramps says I have to battle you.")
        Formatting.PressEnterToContinue()

        rivalBattle = {
            "Name": "Rival Gary",
            "Money": 650,
            "StartLine": "Prepare to get creamed, sucker!",
            "EndLine": "Wait, I wasn't ready! No fair, you could never have beaten me if I was ready.",
            "Pokemon": []
        }
        for p in self.rival_pokemon:
            rivalBattle["Pokemon"].append({"name": p.name, "level": p.level})

        self.EncounterTrainer(rivalBattle)

        print("Rival Gary: I refuse to acknowledge this defeat. You picked a better Pokemon is all that happened here.")
        print("Rival Gary: The next time we battle, I won't go down so easily. If you underestimate me, I'll CRUSH you.")
        print()
        print("*Gary storms off.*")
        Formatting.PressEnterToContinue()

        print("Professor: You should take some basic supplies with you. I'll give you a pokeball and a potion so you can learn how they work.")
        print("Professor: You will need to learn the tools of your trade well, if you are ever to become a Pokemon Master.")
        print()
        time.sleep(1)
        print("*You receive Potion x 5*")
        print("*You receive Pokeball x 10*")
        for i in range(5):
            self.items.append(ItemType.POTION)
        for i in range(10):
            self.items.append(ItemType.POKEBALL)

        print()
        Formatting.PressEnterToContinue()

        print("Professor: You can begin your journey on Route 1 now, unless you have more questions for me?")
        player_choice = input("*Ask a question? Or press ENTER to continue...*")
        if player_choice != "":
            print("Professor: ...")
            time.sleep(1)
            print("Professor: Oh! You actually want to know something from me? %s..." % (player_choice))
            print("Professor: Sorry to say, I'm stumped! I wasn't trained to handle this kind of thing!")
            time.sleep(1)
            print("Professor: ...")
            time.sleep(1)
            print("Professor: ...")
            time.sleep(1)
            print("Professor: !!! Wait! I've got it! I'll give you STUFF instead! Let's call it compensation for my inadequacies.")
            print("Professor: Have these Greatballs, they should help you on your journey.")

            for i in range(5):
                self.items.append(ItemType.GREATBALL)

            print()
            print("*You gain 5x Greatball!")
            Formatting.PressEnterToContinue()

        self.SaveGame()

           
    def GrassGym(self):
        print("You: Now time for the first Gym. The Grass Gym!")

        input("\n*Press ENTER to continue...*")
        Formatting.clearScreen()

        print("*BOOOOOM*")
        time.sleep(1)
        print("*An explosion comes from the Grass Gym in the far distance*")
        print("You: What is happening?!")
        print("*You start running towards the explosion*")

        input("\n*Press ENTER to continue...*")
        Formatting.clearScreen()\

        #to do add more here such as Battles and towns
        
        time.sleep(1)
        print("You finally make it to the Grass Gym door. Everyone is screaming.")
        print("*You bravely walk into the Grass Gym*")

        input("\n*Press ENTER to continue...*")
        Formatting.clearScreen()


        print("*You hide behind a pillar and eavesdrop on the conversation*")

        input("\n*Press ENTER to continue...*")
        Formatting.clearScreen()

        print("Grass Gym Leader: MORE")
        time.sleep(1)
        print("Grass Gym Leader: GIVE me MoRE tO KiLl")
        time.sleep(1)
        print("Grass Gym Leader: iT gIvEs ME MorE ENerGy.")
        time.sleep(1)
        print("Grass Gym Leader: GiVE ME MorE oR YoU WiLl bE mY NexT KiLl.")
        print("A Random Person: Yes okay.")
        print("*You hear someone walk out the building.*")

        input("\n*Press ENTER to continue...*")
        Formatting.clearScreen()

        print("Grass Gym Leader: AhHh A ChAlengEr.")
        print("*You get teleported in front of the Grass Gym Leader!*")
        print("*The Grass Gym Leader's eyes are red*")
        print("Grass Gym Leader: HoW AboUt iF yOu LoSE I WilL KiLl YoU!")

        input("\n*Press ENTER to continue...*")
        Formatting.clearScreen()

        print("Grass Gym Leader: YES YoU MuST")
        print("Grass Gym Leader: LeTs StaRt NOW!")

        input("\n*Press ENTER to continue...*")
        Formatting.clearScreen()

        print("You have been engaged for a BATTLE!")
      

if __name__ == "__main__":
    Game.StartGame()