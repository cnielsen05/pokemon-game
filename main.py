# main.py
from ast import For
import time
import random
from typing import List
from battleEngine import BattleEngine
from enums import ItemType
from formatting import Formatting
from item import Item
from pokemon import Pokemon
from threading import Thread

# Globals for asynchronous code to share information
isWalking = True
isBattling = False
steps_taken = 0

class Game:
    def __init__(self):
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
        self.player_options = []


    def intro(self):
        answered_mom = False
        while (not answered_mom):
            Formatting.clearScreen()
            print("*You sit alone in your room, quiet save the rumbling from an old television set in the corner.*")
            print()
            print("Professor: Hello, and welcome to the world of Pokemon. I am Professor Mulberry and you are in the great Jarea region.")
            print("Professor: I am hiring trainers in this region for...RESEARCH! I am getting too old to do it myself, so now... LET'S START YOUR JOURNEY!")
            print("")
            print("*Your mom walks into the room.*")
            print("")

            self.player_options.clear()
            self.player_options.append("A) NO! I DO WAT I WANNA!")
            self.player_options.append("B) Yes, mom.")

            player_input = self.getPlayerInput("Mom: Stop watching TV, it's late. NOW RUN OFF TO BED!")

            if player_input == "B":
                print("Mom: Thank you for being such a responsible child, I'm so proud of you!")
                self.items.append(ItemType.POKEBALL)
                self.items.append(ItemType.POKEBALL)
                self.items.append(ItemType.POKEBALL)
                print("Mom: That reminds me, you should take these to help you on your journey!")
                print("*You have gained 3x pokeballs*")
                print("Mom: NOW, GO TO BED!")
                print("*You scamper quickly to your bed and fall fast asleep.*")
                answered_mom = True
            elif player_input == "A":
                print("Enraged Mom: YOU DO NOT TALK TO ME LIKE THAT NOW GO TO BED! TOMORROW IS YOUR BIRTHDAY AND YOU WILL NEED ALL YOUR ENERGY FOR YOUR POKEMON ADVENTURE!!!")
                print("*You walk sadly to your room and cry yourself to sleep.*")
                answered_mom = True
            else:
                print("'%s' not recognized. Please try again." % (player_input))
                Formatting.PressEnterToContinue()
            

        Formatting.PressEnterToContinue()
        time.sleep(1)
        print("*As you drift off to sleep, you have an uneasy feeling...*")
        time.sleep(1)
        print("*You toss and turn with nightmares all night long.*")
        Formatting.PressEnterToContinue()
        
        print("*The sun breaks through your curtains and dances over your eyelids. You wake up.*")
        Formatting.PressEnterToContinue()

        print("*Before you become fully aware of your surroundings, your Mom is in your doorway again.*")
        print()
        print("Mom: Finally, you woke up.")
        print("You: What time is it?")
        print("Mom: Just after 10.")
        print("You: WHAT! I'm late!")
        Formatting.PressEnterToContinue()

        print("Mom: Late for what?")
        print("You: Professor Mulberry is giving out starters for the trainers he is hiring!")
        print("Mom: Oh yeah, I almost forgot that was happening today.")
        print("Mom: You'll need to go qui-")
        print()
        print("*You fall down the stairs*")
        time.sleep(1)
        Formatting.PressEnterToContinue()

        print("You: I'm okay!")
        print("*You quickly pull on clothes and run out the door before your mom can finish her sentence...*")
        print("Mom: ... quickly. The event is supposed to start in an hour. He could have at least grabbed something to eat.")
        print("Mom: What's he going to do now, sit around longer with an empty stomach? That kid really needs to think before he acts.")
        Formatting.PressEnterToContinue()

        print("At the door of Professor Mulberrys lab. 10:29 AM")
        print("")
        print("*You bump into a garbage can with a loud CLANG! as you arrive*")
        print("You: Nice, I made it! I think I made good time too...")
        Formatting.PressEnterToContinue()

        print("*A door opens...*")
        time.sleep(1)
        print("Rival: What is all that racket!")
        print("Rival: Of course, it's the loser!")
        print("Rival: What are you doing here, loser?")
        print("You: You don't need to call me names. Better hurry up and come out or you won't get a Pokemon until next year.")
        Formatting.PressEnterToContinue()

        print("Rival: Wait... hurry? You idiot, do you even know what time it is? Gramps isn't giving out any Pokemon until 11:30, that's not for another hour you idiot!")
        print("You: What do you mean?!")
        print("Rival: Exactly like I said! You, the idiotic dumb loser, are ONE HOUR EARLY. You are truly a pea-brained moron.")
        print()
        self.player_options.clear()
        self.player_options.append("A) You're no genius yourself. I should fight you here and now for talking to me that way.")
        self.player_options.append("B) Oh man, is it really not starting for another hour? I guess this one is my mistake.")

        player_input = self.getPlayerInput("")
        if player_input == "A":
            print("You: You're no genius yourself. I should fight you here and now for talking to me that way.")
            print("Rival: WHAT! You are choosing the wrong enemy, fool. You WILL regret this.")
        if player_input == "B":
            print("You: Oh man, is it really not starting for another hour? I guess this one is my mistake.")
            print("Rival: ...")
            time.sleep(1)
            print("Rival: Wait, you aren't going to insult me back?")
            print("Rival: That makes me feel weird for being mean to you. Here, take this I guess...")
            print("You have acquired Greatball x 5")
            for i in range(1,6):
                self.items.append(ItemType.GREATBALL)

            print("*Your rival slams the door shut*")

        Formatting.PressEnterToContinue()
        print("*You wait around idly for an hour until Professor Mulberry starts giving out the Pokemon...*")
        print("*You enter the Lab promptly at 11:30.*")
        Formatting.PressEnterToContinue()

        while (not self.state["choose_starter_complete"]):
            Formatting.clearScreen()
            self.player_options.clear()
            self.player_options.append("A) Atsebi (Fire Type)")
            self.player_options.append("B) Nardent (Water Type)")
            self.player_options.append("C) Leafox (Grass Type)")

            player_input = self.getPlayerInput("Choose your starter:")
            starter = None
            rival_starter = None

            if (player_input == "A"):
                starter = Pokemon("atsebi")
                rival_starter = Pokemon("nardent")

            elif (player_input == "B"):
                starter = Pokemon("nardent")
                rival_starter = Pokemon("leafox")

            elif (player_input == "C"):
                starter = Pokemon("leafox")
                rival_starter = Pokemon("atsebi")

            if not starter:
                print("'%s' not recognized. Please try again." % (player_input))
                Formatting.PressEnterToContinue()
                continue
            else:
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

        print("Rival Gary: Ugh, I would never give you the time of the day if it were up to me... but Gramps says I have to battle you.")
        print("Rival Gary: Prepare to get creamed, sucker!")
        Formatting.PressEnterToContinue()

        # Example new list of pokemon to battle against
        # not_rival_pokemon = []
        # for name in ("clovney", "sleepoud", "pidgey"):
        #   newPokemon = Pokemon(name)
        #   newPokemon.level = 2
        #   not_rival_pokemon.append(newPokemon)
        #   BattleEngine.DoTrainerBattle(self.player_pokemon, self.not_rival_pokemon, self.items, "Trainer Fakeguy", 300)
        BattleEngine.DoTrainerBattle(self.player_pokemon, self.rival_pokemon, self.items, "Rival Gary", 1000)

        print("Professor: You should take some basic supplies with you. I'll give you a pokeball and a potion so you can learn how they work.")
        print("Professor: You will need to learn the tools of your trade well, if you are ever to become a Pokemon Master.")
        print()
        time.sleep(1)
        print("*You receive Potion x 5*")
        print("*You receive Pokeball x 10*")
        for i in range(0,5):
            self.items.append(ItemType.POTION)
        for i in range(0,10):
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

            for i in range(0,5):
                self.items.append(ItemType.GREATBALL)

            print()
            print("*You gain 5x Greatball!")
            Formatting.PressEnterToContinue()

    
    def route_one(self):
        Formatting.clearScreen()
        print("Starting the journey along Route 1.")
        print()

        global isWalking
        global steps_taken
        route_length = 30
        # Define which pokemon can show up. Make more common pokemon show up more often.
        wildPokemonList = [
            "flokefish", 
            "flokefish", 
            "flokefish", 
            "sleepoud", 
            "sleepoud", 
            "scorpoint", 
            "flokefish",
            "stackuri",
            "jareanpidgey", 
            "jareanpidgey", 
            "jareanpidgey",
            "hebike",
            "hebike",
            "hebike",
            "hebike",
            "hebike",
            "clovney",
            "clovney",
            "stackuri",
            "stackuri",
            "stackuri"]
        wildPokemonLevelRange = [1,2]

        hiddenItemList = [ItemType.POTION, ItemType.POKEFEAST, ItemType.POKEBALL]

        steps_taken = 0
        while (steps_taken < route_length):
            self.doWalk(route_length, wildPokemonList, self.player_pokemon, self.items, hiddenItemList, wildPokemonLevelRange)
            Formatting.clearScreen()

        isWalking = False
        print("You have reached the end of Route 1!")
        self.state["route_one_complete"] = True
        

    def route_two(self):
        global isWalking
        global steps_taken

        print("Starting route two!")
        self.state["route_two_complete"] = False
        route_length = 50
        # Define which pokemon can show up. Make more common pokemon show up more often.
        wildPokemonList = ["geodude", "rocketgon", "geodude", "geodude", "geodude", "rockegon", "pidgey", "jareanpidgey", "jareanpidgey","jareanpidgey", "jareanpidgey", "implien", "implien"]
        wildPokemonLevelRange = [1, 2, 3]
        hiddenItemList = [ItemType.POTION, ItemType.POKEFEAST, ItemType.POKEFEAST, ItemType.POKEBALL]

        steps_taken = 0
        while (steps_taken < route_length):
            self.doWalk(route_length, wildPokemonList, self.player_pokemon, self.items, hiddenItemList, wildPokemonLevelRange)
            Formatting.clearScreen()
                
        isWalking = False
        print("You have reached the end of Route 2!")
        self.state["route_two_complete"] = True

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

    def run(self):
        while (self.keepPlaying):
            # Our game code goes in here
            if (not self.state["choose_starter_complete"]):
                self.intro()
            elif (not self.state["route_one_complete"]):
                self.route_one()
            elif (not self.state["route_two_complete"]):
                self.route_two()
            else:
                print("Congratulations, you've reached the end of the game! You WIN!")
                self.keepPlaying = False
            

    def doWalk(self, 
        route_length: int, 
        wildPokemonList: List[str], 
        trainerPokemon: List[Pokemon], 
        trainerItems: List[ItemType], 
        hiddenItems: List[ItemType], 
        wildPokemonLevelRange: List[int]):

        global isWalking
        global steps_taken
        isWalking = True

        start_time = time.time()
        userInterrupt = Thread(target=self.handleUserInput)
        userInterrupt.start()

        while isWalking and steps_taken < route_length:
            time.sleep(0.1)
            if time.time() - start_time >= 1:
                start_time = time.time()
                steps_taken += 1
                print("*You are traveling along the route... press ENTER to pause (step %s of %s)" % (steps_taken, route_length))
                hadEncounter = Game.DoWildPokemonEncounterChance(wildPokemonList, trainerPokemon, trainerItems, wildPokemonLevelRange)
                if not hadEncounter:
                    self.FindHiddenItemChance(hiddenItems)

        userInterrupt.join()


    def handleUserInput(self):
        global isWalking
        global isBattling

        user_input = input()

        if not isBattling and isWalking:
            isWalking = False
            awaitingChoice = True

            while (awaitingChoice):
                Formatting.clearScreen()
                commands = ['ITEM', 'CAMP', 'RESUME JOURNEY']
                command_counter = 0
                for command in commands:
                    print("%s) %s" % (chr(ord('A') + command_counter), command))
                    command_counter += 1

                user_input = input()
                chosen_index = ord(user_input[0]) - ord('A')
                if chosen_index < 0 or chosen_index > len(commands) - 1:
                    input("Input %s was not recognized. Press ENTER to try again." % user_input)
                    continue

                match commands[chosen_index]:
                    case 'ITEM':
                        if len(self.items) == 0:
                            print("You have no items.")
                            input("*Press ENTER to continue*")
                            continue

                        Formatting.clearScreen()
                        counter = 0
                        for item in self.items:
                            identifier = chr(ord("A") + counter)
                            counter += 1
                            print("%s) %s" % (identifier, item))

                        player_input = input()
                        index = ord(player_input[0]) - ord("A")
                        if (index < 0 or index > len(self.items) - 1):
                            input("Input %s not recognized. Press ENTER to try again.")
                            continue

                        itemToUse = self.items[index]
                        match itemToUse:
                            case ItemType.POTION:
                                # The Item.UsePotion(int) function returns false if the player fails to select a target.
                                # If that happens, we should skip the rest of execution and go back to getting player input.
                                if not Item.UsePotion(30, self.player_pokemon):
                                    continue
                                else:
                                    self.items.pop(index)

                            case ItemType.POKEBALL:
                                print("*You roll the pokeball back and forth in your palm, imagining your next throw...*")

                        awaitingChoice = False

                    case 'CAMP':
                        print("Camping!")
                        for pokemon in self.player_pokemon:
                            for move in pokemon.GetBattleAttacks():
                                move.currentPP = move.maxPP

                        print("All of your pokemon have had their PP restored!")
                        Formatting.PressEnterToContinue()
                        awaitingChoice = False

                    case 'RESUME JOURNEY':
                        Formatting.clearScreen()
                        print("Resuming the journey!")
                        print()
                        awaitingChoice = False


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
            print("A wild %s has appeared!" % (wildPokemon.name))
            Formatting.PressEnterToContinue()
            BattleEngine.DoWildBattle(trainerPokemon, wildPokemon, trainerItems)
            isBattling = False

        return encounterWildPokemon

    
    def getPlayerInput(self, prompt: str) -> str:
        print(prompt)
        for option in self.player_options:
            print(option)

        player_input = input()
        if (player_input == "Quit"):
            self.keepPlaying = False
            print("Thank you for playing! Exiting now...")
            quit()
        else:
            return player_input

if __name__ == "__main__":
    myGame = Game()
    myGame.run()