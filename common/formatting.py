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


    def GetUserChoice(options: List[str], noBack: bool = False) -> int:
        if len(options) == 0:
            return -2
            
        counter = 0
        if not noBack and not options[len(options) - 1] == "BACK":
            options.append("BACK")
        for option in options:
            identifier = chr(ord("A") + counter)
            counter += 1
            print("%s) %s" % (identifier, option))

        userAction = input()
        Formatting.clearScreen()

        try:
            userChoice = ord(userAction[0]) - ord("A")
            if userChoice == len(options) - 1 and not noBack:
                # Return -2 when the user chooses BACK so the caller doesn't try to dereference something from the options list passed in
                return -2
            else:
                return userChoice
        except:
            input("Input %s unrecognized. Press ENTER to try again." % (userAction))
            return -1