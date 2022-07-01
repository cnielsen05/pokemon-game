import os
from sys import platform
import time
from typing import List

class Formatting:
    def clearScreen():
        if platform == 'win32':
            os.system('cls')
        else:
            os.system('clear')


    def PressEnterToContinue():
        time.sleep(1)
        print()
        input("Press ENTER to continue...")    
        Formatting.clearScreen()    


    def GetUserChoice(options: List[str]) -> int:
        counter = 0
        for option in options:
            identifier = chr(ord("A") + counter)
            counter += 1
            print("%s) %s" % (identifier, option))

        userAction = input()
        Formatting.clearScreen()

        try:
            userChoice = ord(userAction[0]) - ord("A")
            return userChoice
        except:
            input("Input %s unrecognized. Press ENTER to try again." % (userAction))
            return -1