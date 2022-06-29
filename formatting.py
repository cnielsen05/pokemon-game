import os
from sys import platform
from typing import List

class Formatting:
    def clearScreen():
        if platform == 'win32':
            os.system('cls')
        else:
            os.system('clear')


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