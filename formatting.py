import os
from sys import platform

class Formatting:
    def clearScreen():
        if platform == 'win32':
            os.system('cls')
        else:
            os.system('clear')