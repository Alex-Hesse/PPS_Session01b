from enum import Enum, IntEnum
import itertools
import numpy as np
from copy import deepcopy


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
    Letzte = 1


def checkStatement(straße: tuple[tuple[int]]) -> bool:
    """straße : (( nat, farbe, getränk, zig, tier),(),(),(),())
    """
    for hausnummer in range(len(straße)):
        haus = straße[hausnummer]

        if hausnummer == Position.Erste:
            if haus[Idx.Nationalität] != Nationalität.Norweger:
                return False
            if straße[hausnummer+Position.Links][Idx.Farbe] != Farbe.Blau:
                return False

            if haus[Idx.Zigarettenmarke] == Zigarettenmarke.Marlboro:
                if straße[hausnummer+Position.Links][Idx.Hausttier] != Hausttier.Katze:
                    return False
                if straße[hausnummer+Position.Links][Idx.Getränk] != Getränk.Wasser:
                    return False
            elif haus[Idx.Zigarettenmarke] == Zigarettenmarke.Dunhill:
                if straße[hausnummer+Position.Links][Idx.Hausttier] != Hausttier.Pferd:
                    return False

        elif hausnummer == Position.Letzte:

            if haus[Idx.Farbe] == Farbe.Grün:
                if straße[hausnummer-Position.Rechts][Idx.Farbe] != Farbe.Weiß:
                    return False

            if haus[Idx.Zigarettenmarke] == Zigarettenmarke.Marlboro:
                if straße[hausnummer+Position.Rechts][Idx.Hausttier] != Hausttier.Katze:
                    return False
                if straße[hausnummer+Position.Rechts][Idx.Getränk] != Getränk.Wasser:
                    return False
            elif haus[Idx.Zigarettenmarke] == Zigarettenmarke.Dunhill:
                if straße[hausnummer+Position.Rechts][Idx.Hausttier] != Hausttier.Pferd:
                    return False
        else:
            if hausnummer == Position.Mitte:
                if haus[Idx.Getränk] != Getränk.Milch:
                    return False
            if haus[Idx.Farbe] == Farbe.Grün:
                if straße[hausnummer-Position.Links][Idx.Farbe] != Farbe.Weiß:
                    return False

            if haus[Idx.Zigarettenmarke] == Zigarettenmarke.Marlboro:
                if straße[hausnummer+Position.Rechts][Idx.Hausttier] != Hausttier.Katze and straße[hausnummer+Position.Links][Idx.Hausttier] != Hausttier.Katze:
                    return False
                if straße[hausnummer+Position.Rechts][Idx.Getränk] != Getränk.Wasser and straße[hausnummer+Position.Links][Idx.Getränk] != Getränk.Wasser:
                    return False
            elif haus[Idx.Zigarettenmarke] == Zigarettenmarke.Dunhill:
                if straße[hausnummer+Position.Rechts][Idx.Hausttier] != Hausttier.Pferd and straße[hausnummer+Position.Links][Idx.Hausttier] != Hausttier.Pferd:
                    return False

        if haus[Idx.Nationalität] == Nationalität.Brite:
            if haus[Idx.Farbe] != Farbe.Rot:
                return False
        elif haus[Idx.Nationalität] == Nationalität.Schwede:
            if haus[Idx.Hausttier] != Hausttier.Hund:
                return False
        elif haus[Idx.Nationalität] == Nationalität.Däne:
            if haus[Idx.Getränk] != Getränk.Tee:
                return False
        elif haus[Idx.Nationalität] == Nationalität.Deutsche:
            if haus[Idx.Zigarettenmarke] != Zigarettenmarke.Rothmanns:
                return False

        if haus[Idx.Farbe] == Farbe.Grün:
            if haus[Idx.Getränk] != Getränk.Kaffee:
                return False

        elif haus[Idx.Farbe] == Farbe.Gelb:
            if haus[Idx.Zigarettenmarke] != Zigarettenmarke.Dunhill:
                return False

        if haus[Idx.Zigarettenmarke] == Zigarettenmarke.Winfield:
            if haus[Idx.Getränk] != Getränk.Bier:
                return False
        elif haus[Idx.Zigarettenmarke] == Zigarettenmarke.Pall_Mall:
            if haus[Idx.Hausttier] != Hausttier.Vogel:
                return False

    return True


def bruteForce():
    richtigeStraßen = []
    for nationalitäten in itertools.permutations(Nationalität):
        print(120)
        for farben in itertools.permutations(Farbe):
            print(14.400)
            for getränke in itertools.permutations(Getränk):
                for zigarettenmarken in itertools.permutations(Zigarettenmarke):
                    for haustiere in itertools.permutations(Hausttier):
                        straße = list(np.transpose(
                            np.array([nationalitäten, farben, getränke, zigarettenmarken, haustiere])))
                        if checkStatement(straße):
                            richtigeStraßen.append(list(straße))
                            print(straße)
    return richtigeStraßen


# f11_12_15a = ((Nationalität.Norweger, -1, -1, -1, -1),
#              (-1, Farbe.Blau, -1, -1, -1),
#              (-1, -1, Getränk.Milch, -1, -1),
#              (-1, -1, -1, -1, -1),
#              (-1, -1, -1, -1, -1))*+

startStraße = [[-1, -1, -1, -1, -1],
               [-1, -1, -1, -1, -1],
               [-1, -1, Getränk.Milch, -1, -1],
               [-1, Farbe.Blau, -1, -1, -1],
               [Nationalität.Norweger, -1, -1, -1, -1]]


hausRegeln = [[Nationalität.Brite, Farbe.Rot, -1, -1, -1],
              [Nationalität.Schwede, -1, -1, -1, Hausttier.Hund],
              [Nationalität.Däne, -1, Getränk.Tee, -1, -1],
              [Nationalität.Deutsche, -1, -1, Zigarettenmarke.Rothmanns],
              [-1, Farbe.Grün, Getränk.Kaffee, -1, -1],
              [-1, -1, Getränk.Bier, Zigarettenmarke.Winfield, -1],
              [-1, Farbe.Gelb, -1, Zigarettenmarke.Dunhill, -1],
              [-1, -1, -1, Zigarettenmarke.Pall_Mall, Hausttier.Vogel]]

nachbarRegeln = [[[[-1, Farbe.Grün, -1, -1, -1], [-1, Farbe.Weiß, -1, -1, -1]]],
                 [[[-1, -1, -1, Zigarettenmarke.Marlboro, -1], [-1, -1, -1, -1, Hausttier.Katze]],
                  [[-1, -1, -1, -1, Hausttier.Katze], [-1, -1, -1, Zigarettenmarke.Marlboro, -1]]],
                 [[[-1, -1, -1, Zigarettenmarke.Marlboro, -1], [-1, -1, Getränk.Wasser, -1, -1]],
                  [[-1, -1, Getränk.Wasser, -1, -1], [-1, -1, -1, Zigarettenmarke.Marlboro, -1]]],
                 [[[-1, -1, -1, Zigarettenmarke.Dunhill, -1], [-1, -1, -1, -1, Hausttier.Pferd]],
                  [[-1, -1, -1, -1, Hausttier.Pferd], [-1, -1, -1, Zigarettenmarke.Dunhill, -1]]],]


f11_12_15 = ((-1, -1, -1, -1, -1),
             (-1, -1, -1, -1, -1),
             (-1, -1, Getränk.Milch, -1, -1),
             (-1, Farbe.Blau, -1, -1, -1),
             (Nationalität.Norweger, -1, -1, -1, -1))
f5 = (Nationalität.Brite, Farbe.Rot, -1, -1, -1)
f6 = (Nationalität.Schwede, -1, -1, -1, Hausttier.Hund)
f7 = (Nationalität.Däne, -1, Getränk.Tee, -1, -1)
f8 = (Nationalität.Deutsche, -1, -1, Zigarettenmarke.Rothmanns)
f9 = (-1, Farbe.Grün, Getränk.Kaffee, -1, -1)
f10 = (-1, -1, Getränk.Bier, Zigarettenmarke.Winfield, -1)
f13 = (-1, Farbe.Gelb, -1, Zigarettenmarke.Dunhill, -1)
f14 = (-1, -1, -1, Zigarettenmarke.Pall_Mall, Hausttier.Vogel)

f16 = ((-1, Farbe.Grün, -1, -1, -1),
       (-1, Farbe.Weiß, -1, -1, -1))

f17a = ((-1, -1, -1, Zigarettenmarke.Marlboro, -1),
        (-1, -1, -1, -1, Hausttier.Katze))
f17b = ((-1, -1, -1, -1, Hausttier.Katze),
        (-1, -1, -1, Zigarettenmarke.Marlboro, -1))

f18a = ((-1, -1, -1, Zigarettenmarke.Marlboro, -1),
        (-1, -1, Getränk.Wasser, -1, -1))
f18b = ((-1, -1, Getränk.Wasser, -1, -1),
        (-1, -1, -1, Zigarettenmarke.Marlboro, -1))

f19a = ((-1, -1, -1, Zigarettenmarke.Dunhill, -1),
        (-1, -1, -1, -1, Hausttier.Pferd))
f19b = ((-1, -1, -1, -1, Hausttier.Pferd),
        (-1, -1, -1, Zigarettenmarke.Dunhill, -1))


def tryFits(straße, f):  # single house
    copyStreet = list(straße)
    streetFits = []
    indexes = []
    idx = []
    i = 0
    for slot in f:
        if slot != -1:
            idx.append(i)
        i += 1
    i = 0
    for house in straße:
        if house[idx[0]] == -1 and house[idx[1]] == -1:
            streetFits.append(deepcopy(copyStreet))
            streetFits[-1][i][idx[0]] = f[idx[0]]
            streetFits[-1][i][idx[1]] = f[idx[1]]
        i += 1
    return streetFits


def tryFits2(straße, f):  # two houses
    copyStreet = deepcopy(list(straße))
    streetFits = []

    idx = []
    for x in range(2):
        for y in range(len(f[x])):
            if f[x][y] != -1:
                idx.append(y)
                break

    for x in range(4):
        if copyStreet[x][idx[0]] == -1 and copyStreet[x+1][idx[1]] == -1:
            streetFits.append(deepcopy(copyStreet))
            streetFits[-1][x][idx[0]] = f[0][idx[0]]
            streetFits[-1][x+1][idx[1]] = f[1][idx[1]]
        elif copyStreet[x][idx[0]] == f[0][idx[0]] and copyStreet[x+1][idx[1]] == -1:
            streetFits.append(deepcopy(copyStreet))
            streetFits[-1][x][idx[0]] = f[0][idx[0]]
            streetFits[-1][x+1][idx[1]] = f[1][idx[1]]
        elif copyStreet[x][idx[0]] == -1 and copyStreet[x+1][idx[1]] == f[1][idx[1]]:
            streetFits.append(deepcopy(copyStreet))
            streetFits[-1][x][idx[0]] = f[0][idx[0]]
            streetFits[-1][x+1][idx[1]] = f[1][idx[1]]

    return streetFits


def prettyPrint(i):
    text = ""
    for x in i:
        for y in x:
            text += "%11s" % y.name
        text += "\n"

    print(text, end="")

# todo pretty up  use one arraey instead of f and loop over it


def recTryFit(z, i):
    #exit case
    if i < len(hausRegeln):
        for x in z:
            newZ = tryFits(x, hausRegeln[i])
            recTryFit(newZ, i+1)
    elif i < len(hausRegeln)+ len(nachbarRegeln):
        for x in z:
            newZ = tryFits2(x, nachbarRegeln[i-len(hausRegeln)][0])
            recTryFit(newZ, i+1)
    else:
        if z != []:
            prettyPrint(z[0])


def logic():
    straße = list(f11_12_15)
    for x in range(len(straße)):
        straße[x] = list(straße[x])
    for x in range(5):
        straßeF = straße
        straßeF[x][4] = Hausttier.Fisch

       

        recTryFit([straßeF], 0)

        z5 = tryFits(straßeF, f5) 
        for x5 in z5:
            z6 = tryFits(x5, f6)
            for x6 in z6:
                z7 = tryFits(x6, f7)
                for x7 in z7:
                    z8 = tryFits(x7, f8)
                    for x8 in z8:
                        z9 = tryFits(x8, f9)
                        for x9 in z9:
                            z10 = tryFits(x9, f10)
                            for x10 in z10:
                                z13 = tryFits(x10, f13)
                                for x13 in z13:
                                    z14 = tryFits(x13, f14)


                                    for x14 in z14:
                                        z16 = tryFits2(x14, f16)
                                        for x16 in z16:
                                            z17a = tryFits2(x16, f17a)
                                            z17b = tryFits2(x16, f17b)
                                            z17 = z17a + z17b
                                            for x17 in z17:
                                                z18a = tryFits2(x17, f18a)
                                                z18b = tryFits2(x17, f18b)
                                                z18 = z18a + z18b
                                                for x18 in z18:
                                                    z19a = tryFits2(x18, f19a)
                                                    z19b = tryFits2(x18, f19b)
                                                    z19 = z19a + z19b
                                                    for x19 in z19:
                                                        if len(x19) != 0:
                                                            print(
                                                                checkStatement(x19))
                                                            prettyPrint(x19)


if __name__ == "__main__":
    # richtigeStraßen = bruteForce()  # ~ 48h
    logic()  # <1s
    # print(richtigeStraßen)
