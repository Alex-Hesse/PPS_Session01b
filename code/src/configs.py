
from enum import IntEnum


class Nationalität(IntEnum):
    Brite = 0
    Schwede = 1
    Däne = 2
    Deutsche = 3
    Norweger = 4


class Farbe(IntEnum):
    Rot = 0
    Grün = 1
    Gelb = 2
    Blau = 3
    Weiß = 4


class Getränk(IntEnum):
    Tee = 0
    Kaffee = 1
    Bier = 2
    Milch = 3
    Wasser = 4


class Zigarettenmarke(IntEnum):
    Rothmanns = 0
    Winfield = 1
    Dunhill = 2
    Pall_Mall = 3
    Marlboro = 4


class Hausttier(IntEnum):
    Hund = 0
    Vogel = 1
    Katze = 2
    Pferd = 3
    Fisch = 4


class Idx(IntEnum):
    Nationalität = 0
    Farbe = 1
    Getränk = 2
    Zigarettenmarke = 3
    Hausttier = 4


class Position(IntEnum):
    Links = -1
    Erste = 4
    Rechts = 1
    Mitte = 2
    Letzte = 0


class StraßenConfig():
    pass
    


def convert(rules=[]):
    a = [0, 2, 3, 5, 6]
    n = 2
    b = [i for i in a if i % n == 0]
    print(b)

convert()