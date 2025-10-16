from enum import IntEnum
import itertools
import numpy as np
from copy import deepcopy
import time
import sys


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

# erster anastz
def checkStatement(straße):
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
                if straße[hausnummer+Position.Rechts][Idx.Farbe] != Farbe.Weiß:
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
    """brute force methode, nicht zu gebrauchen dauert vermutlich 48h
    """
    richtigeStraßen = []
    for nationalitäten in itertools.permutations(Nationalität):
        print(f"Muss 120 mal geprinted werden")
        for farben in itertools.permutations(Farbe):
            print("Muss 14400 mal geprinted werden")
            for getränke in itertools.permutations(Getränk):
                for zigarettenmarken in itertools.permutations(Zigarettenmarke):
                    for haustiere in itertools.permutations(Hausttier):
                        straße = list(np.transpose(
                            np.array([nationalitäten, farben, getränke, zigarettenmarken, haustiere])))
                        if checkStatement(straße):
                            richtigeStraßen.append(list(straße))
                            print(straße)
    return richtigeStraßen


# regeln 1, 2, 3, 4, 11, 12, 15 ergeben startposition
startStraße = [[-1, -1, -1, -1, -1],
               [-1, -1, -1, -1, -1],
               [-1, -1, Getränk.Milch, -1, -1],
               [-1, Farbe.Blau, -1, -1, -1],
               [Nationalität.Norweger, -1, -1, -1, -1]]

# hausregeln beziehn sich nur auf ein haus
# regeln 5, 6, 7, 8, 9, 10, 13, 14
hausRegeln = [[Nationalität.Brite, Farbe.Rot, -1, -1, -1],
              [Nationalität.Schwede, -1, -1, -1, Hausttier.Hund],
              [Nationalität.Däne, -1, Getränk.Tee, -1, -1],
              [Nationalität.Deutsche, -1, -1, Zigarettenmarke.Rothmanns],
              [-1, Farbe.Grün, Getränk.Kaffee, -1, -1],
              [-1, -1, Getränk.Bier, Zigarettenmarke.Winfield, -1],
              [-1, Farbe.Gelb, -1, Zigarettenmarke.Dunhill, -1],
              [-1, -1, -1, Zigarettenmarke.Pall_Mall, Hausttier.Vogel]]

# nachbarregeln sind für nachbarn, doppelt jeweils nach links und rechts
# regeln 16, 17, 18, 19
nachbarRegeln = [[[[-1, Farbe.Grün, -1, -1, -1], [-1, Farbe.Weiß, -1, -1, -1]]],
                 [[[-1, -1, -1, Zigarettenmarke.Marlboro, -1], [-1, -1, -1, -1, Hausttier.Katze]],
                  [[-1, -1, -1, -1, Hausttier.Katze], [-1, -1, -1, Zigarettenmarke.Marlboro, -1]]],
                 [[[-1, -1, -1, Zigarettenmarke.Marlboro, -1], [-1, -1, Getränk.Wasser, -1, -1]],
                  [[-1, -1, Getränk.Wasser, -1, -1], [-1, -1, -1, Zigarettenmarke.Marlboro, -1]]],
                 [[[-1, -1, -1, Zigarettenmarke.Dunhill, -1], [-1, -1, -1, -1, Hausttier.Pferd]],
                  [[-1, -1, -1, -1, Hausttier.Pferd], [-1, -1, -1, Zigarettenmarke.Dunhill, -1]]],]

# zweiter ansatz


def hausFit(straße, hausRegel):
    """wendet hausregeln f an auf straße und gibt alle möglichen 
    sich aus straße + regel ergebenden straßen zurück (keine wenn unmöglich)
    """
    ergebendeStraßen = []
    idx = []
    i = 0
    for slot in hausRegel:
        if slot != -1:
            idx.append(i)
        i += 1
    i = 0
    for haus in straße:
        if haus[idx[0]] == -1 and haus[idx[1]] == -1:
            ergebendeStraßen.append(deepcopy(straße))
            ergebendeStraßen[-1][i][idx[0]] = hausRegel[idx[0]]
            ergebendeStraßen[-1][i][idx[1]] = hausRegel[idx[1]]
        i += 1
    return ergebendeStraßen


def nachbarFit(straße, nachbarRegel):  # two houses
    """wendet nachbarregeln f an auf straße und gibt alle möglichen 
    sich aus straße + regel ergebenden straßen zurück (keine wenn unmöglich)
    """
    ergebendeStraßen = []

    for regel in nachbarRegel:
        idx = []
        for x in range(2):
            for y in range(len(regel[x])):
                if regel[x][y] != -1:
                    idx.append(y)
                    break

        for x in range(4):
            if straße[x][idx[0]] == -1 and straße[x+1][idx[1]] == -1:
                ergebendeStraßen.append(deepcopy(straße))
                ergebendeStraßen[-1][x][idx[0]] = regel[0][idx[0]]
                ergebendeStraßen[-1][x+1][idx[1]] = regel[1][idx[1]]
            elif straße[x][idx[0]] == regel[0][idx[0]] and straße[x+1][idx[1]] == -1:
                ergebendeStraßen.append(deepcopy(straße))
                ergebendeStraßen[-1][x][idx[0]] = regel[0][idx[0]]
                ergebendeStraßen[-1][x+1][idx[1]] = regel[1][idx[1]]
            elif straße[x][idx[0]] == -1 and straße[x+1][idx[1]] == regel[1][idx[1]]:
                ergebendeStraßen.append(deepcopy(straße))
                ergebendeStraßen[-1][x][idx[0]] = regel[0][idx[0]]
                ergebendeStraßen[-1][x+1][idx[1]] = regel[1][idx[1]]

    return ergebendeStraßen


def prettyPrint(i):
    """Pretty print für straße
    """
    text = ""
    for x in i:
        for y in x:
            text += "%11s" % y.name
        text += "\n"

    print(text, end="")


def recursiveFitting(straßen, iteration=0):
    """wendet alle haus und nachbarregeln rekursiv an
    """

    if iteration < len(hausRegeln):
        # zuerst die straßen regeln
        for straße in straßen:
            neueStraßen = hausFit(straße, hausRegeln[iteration])
            recursiveFitting(neueStraßen, iteration+1)
    elif iteration < len(hausRegeln) + len(nachbarRegeln):
        # danach die nachbarregeln
        for straße in straßen:
            neueStraßen = nachbarFit(
                straße, nachbarRegeln[iteration-len(hausRegeln)])
            recursiveFitting(neueStraßen, iteration+1)
    else:
        for straße in straßen:
            print(f"Ein Ergebnis ist {checkStatement(straße)}")
            prettyPrint(straße)


def fitting():
    # fisch platziern an mögliche positionen
    for fischHausnummer in range(len(startStraße)):
        # startstraße ist die einzige festgelegten sachen von den annahmen  11, 12, 15
        straße = deepcopy(startStraße)
        straße[fischHausnummer][4] = Hausttier.Fisch
        recursiveFitting([straße])
    print("Keine weiteren Lösungen.")


if __name__ == "__main__":
    t0 = time.time()

    if sys.argv[-1].lower() == "b":
        # ! brute force
        richtigeStraßen = bruteForce()  # ~ 48h (ungetested)
        for straße in richtigeStraßen:
            prettyPrint(straße)
    else:
        # ! recursive fitting
        fitting()  # ~ 0.03s

    print(f"runtime: {time.time()-t0}s")
