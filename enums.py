from enum import Enum

class BattleType(str, Enum):
    NONE = 'NONE'
    NORMAL = 'NORMAL'
    FIRE = 'FIRE'
    WATER = 'WATER'
    GRASS = 'GRASS'
    ELECTRIC = 'ELECTRIC'
    BUG = 'BUG'
    DRAGON = 'DRAGON'
    FAIRY = 'FAIRY'
    DARK = 'DARK'
    POISON = 'POISON'
    PSYCHIC = 'PSYCHIC'
    GHOST = 'GHOST'
    GROUND = 'GROUND'
    STEEL = 'STEEL'
    ROCK = 'ROCK'
    ICE = 'ICE'
    FIGHTING = 'FIGHTING'
    FLYING = 'FLYING'

class Status(Enum):
    NONE = 0
    ASLEEP = 1
    CONFUSED = 2
    POISONED = 3
    PARALYZED = 4
    BURNED = 5
    FROZEN = 6
    KNOCKED_OUT = 7

class PokemonStat(Enum):
    ATTACK = 1
    SPECIAL_ATTACK = 2
    DEFENSE = 3
    SPECIAL_DEFENSE = 4
    HP = 5
    SPEED = 6

class Item(str, Enum):
    POTION = 'POTION'
    SUPER_POTION = 'SUPER_POTION'
    POKEBALL = 'POKEBALL'
    GREATBALL = 'GREATBALL'