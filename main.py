# main.py
import time
import os
import random
from typing import List
from battleEngine import BattleEngine
from enums import Item
from pokemon import Pokemon, BattleAttack
from threading import Thread


thread_running = True
steps_taken = 0

class Game:
    def __init__(self):
        self.keepPlaying = True
        self.current_pokemon = []
        self.items = []
        self.state = {
            "choose_starter_complete": False,
            "route_one_complete": False,
            "route_two_complete": False,
        }
        self.player_options = []

    def intro(self):
        answered_mom = False
        while (not answered_mom):
            os.system('cls')
            print("Professor: Hello, and welcome to the world of Pokemon. I am Professor Mulberry and you are in the great Jarea region.")
            print("Professor: I am hiring trainers in this region for...RESEARCH! I am getting too old to do it myself, so now... LET'S START YOUR JOURNEY!")
            print("")
            print("*your mom walks into the room*")
            print("")

            self.player_options.clear()
            self.player_options.append("A) NO!")
            self.player_options.append("B) Yes, mom.")

            player_input = self.getPlayerInput("Mom: Stop watching TV, it's late. NOW RUN OFF TO BED!")

            if player_input == "B":
                print("Mom: Thank you for being such a responsible child, I'm so proud of you!")
                print("*You scamper quickly to your bed and fall fast asleep.*")
                answered_mom = True
            elif player_input == "A":
                print("Enraged Mom: YOU DO NOT TALK TO ME LIKE THAT NOW GO TO BED! TOMORROW IS YOUR BIRTHDAY AND YOU WILL NEED ALL YOUR ENERGY FOR YOUR POKEMON ADVENTURE!!!")
                print("*You walk sadly to your room and cry yourself to sleep.*")
                answered_mom = True
            else:
                print("'%s' not recognized. Please try again." % (player_input))
                input("*Press ENTER to continue...*")
            

        input("\n*Press ENTER to continue...*")
        os.system('cls')
        print("In the morning...")
        print("")
        print("*You wake up*")

        input("\n*Press ENTER to continue...*")
        os.system('cls')
        print("Mom: Finally you woke up")
        print("You: What time is it")
        print("Mom: 10:00")
        print("You: WHAT!")
        print("You: I'm late!")

        input("\n*Press ENTER to continue...*")
        os.system('cls')
        print("Mom: For what?")
        print("You: Professor Mulberry is giving out starters for the trainers he is hiring!")
        print("Mom: OHHHHH that.")
        print("Mom: Wait bu-")
        print("*You fall down the stairs*")

        input("\n*Press ENTER to continue...*")
        os.system('cls')
        print("You: I'm okay")
        print("*You quickly get ready and run out the door before your mom can finish her sentance*")
        print("Mom: -t that starts in an hour")
        print("Mom: Oh he's already gone!")

        input("\n*Press ENTER to continue...*")
        os.system('cls')
        print("")
        print("*At the door of Professor Mulberrys lab*")
        print("")
        print("You: Finally I got here")
        print("*A door opens*")
        print("Rival: what is all that racket!")
        print("Rival: Ohhhh its the loser!")
        print("Rival: Ha what are you doing here ya loser")
        print("You: hey come out or you will not get a pokemon until next year")
        print("Rival: HA HA HA HA HA your so pathetic you even forgot the time it starts!")
        print("You: what do you mean?!")
        print("Rival it happens in a hour loser oh and I can't forget the title DUMBY")

        

        self.player_options.clear()
        self.player_options.append("A) Your no smarter")
        self.player_options.append("B) Okay I guess I did forget the time it starts")

        player_input = self.getPlayerInput("")
        if player_input == "A":
            print("You: Your no smarter")
            print("Rival: WHAT! Than I'm just gonna stand here until it starts while I insult you")
        if player_input == "B":
            print("You: Okay I guess I did forget the time it starts")
            print("Rival: Good you know your place")
            print("*your rival slams the door shut")

        input("\n*Press ENTER to continue...*")
        os.system("cls")

        print("When Professor Mulberry starts giving out the Pokemon")
        print("*You enter the Lab*")
        input("\n*Press ENTER to continue...*")
        while (not self.state["choose_starter_complete"]):
            os.system('cls')
            self.player_options.clear()
            self.player_options.append("A) Atsebi (Fire Type)")
            self.player_options.append("B) Nardent (Water Type)")
            self.player_options.append("C) Leafox (Grass Type)")

            player_input = self.getPlayerInput("Choose your starter:")
            starter = None

            if (player_input == "A"):
                starter = Pokemon("atsebi")

            elif (player_input == "B"):
                starter = Pokemon("nardent")

            elif (player_input == "C"):
                starter = Pokemon("leafox")

            if not starter:
                print("'%s' not recognized. Please try again." % (player_input))
                input("*Press ENTER to continue...*")
            else:
                starter.level = 3
                starter.FullHealHP()
                self.current_pokemon.append(starter)

            if (len(self.current_pokemon) > 0):
                print("Professor: Good choice, I'm sure %s will be an excellent companion on your journey!" % (self.current_pokemon[0].name))
                self.state["choose_starter_complete"] = True

    def doWalk(self, route_length: int, wildPokemonList: List[str], trainerPokemon: List[Pokemon], trainerItems: List[Item]):
        global thread_running
        global steps_taken
        start_time = time.time()

        while thread_running:
            time.sleep(0.1)
            if time.time() - start_time >= 1:
                start_time = time.time()
                steps_taken += 1
                print("*You are walking along the path, nothing interesting happening...* (step %s of %s)" % (steps_taken, route_length))
                Game.DoWildPokemonEncounterChance(wildPokemonList, trainerPokemon, trainerItems)


    def handleUserInput(self):
        global thread_running

        user_input = input()
        print("User typed: %s" % (user_input))


    def DoWildPokemonEncounterChance(wildPokemonList: List[str], trainerPokemon: List[Pokemon], trainerItems: List[Item]):
        global thread_running

        encounterWildPokemon = random.randint(0,9) > 7
        if (encounterWildPokemon):
            thread_running = False
            whichPokemon = random.randint(0, len(wildPokemonList) - 1)
            wildPokemon = Pokemon(wildPokemonList[whichPokemon])
            print("A wild %s has appeared!" % (wildPokemon.name))
            print()
            input("*Press ENTER to continue...*")
            BattleEngine.DoWildBattle(trainerPokemon, wildPokemon, trainerItems)

    
    def route_one(self):
        print("Starting the journey along Route 1.")
        print()
        input("*Press ENTER to continue...*")

        global thread_running
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

        hiddenItemList = [Item.POTION, Item.POTION, Item.POKEBALL]

        steps_taken = 0
        while (steps_taken < route_length):
            thread_running = True
            walkThread = Thread(target=self.doWalk(route_length, wildPokemonList, self.current_pokemon, self.items))
            userInterrupt = Thread(target=self.handleUserInput)

            walkThread.start()
            userInterrupt.start()
            userInterrupt.join()
            thread_running = False
            
            # if random.randint(0,19) > 18:
            #     print("You found a hidden item!")
            #     whichItem = random.randint(0,len(hiddenItemList) - 1)
            #     found_item = hiddenItemList[whichItem]
            #     print("You have acquired... %s!" % (found_item))
            #     self.items.append(found_item)
            #     input("*Press ENTER to continue...*")
                
        
        print("You have reached the end of Route 1!")
        self.state["route_one_complete"] = True

    def route_two(self):
        print("Starting route two!")
        self.state["route_two_complete"] = False
        route_length = 50
        # Define which pokemon can show up. Make more common pokemon show up more often.
        wildPokemonList = ["geodude", "rockegon", "geodude", "geodude", "geodude", "rockegon", "pidgey", "jareanpidgey", "jareanpidgey","jareanpidgey", "jareanpidgey", "implien", "implien"]

        hiddenItemList = [Item.POTION, Item.POTION, Item.POKEBALL]

        steps_taken = 0
        while (steps_taken < route_length):
            steps_taken += 1
            print("*You are walking along the path, nothing interesting happening...* (step %s of %s)" % (steps_taken, route_length))

            encounterWildPokemon = random.randint(0,9) > 7
            if (encounterWildPokemon):
                whichPokemon = random.randint(0, len(wildPokemonList) - 1)
                wildPokemon = Pokemon(wildPokemonList[whichPokemon])
                print("A wild %s has appeared!" % (wildPokemon.name))
                print()
                input("*Press ENTER to continue...*")
                BattleEngine.DoWildBattle(self.current_pokemon, wildPokemon, self.items)
            else:
                time.sleep(1)
                if random.randint(0,19) > 18:
                    print("You found a hidden item!")

                    whichItem = random.randint(0,len(hiddenItemList) - 1)
                    found_item = hiddenItemList[whichItem]
                    print("You have acquired... %s!" % (found_item))
                    self.items.append(found_item)
                    input("*Press ENTER to continue...*")
                
        
        print("You have reached the end of Route 2!")
        self.state["route_two_complete"] = True
        print("You: Now time to the first Gym the Grass Gym")

        input("\n*Press ENTER to continue...*")
        os.system('cls')

        print("*BOOOOOM*")
        print("*An explosion comes from the Grass Gym")
        print("You: What is happening?")
        print("*You start running towards the explosion*")

        input("\n*Press ENTER to continue...*")
        os.system('cls')

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