from enum import IntEnum
import itertools
import numpy as np


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
def checkStraße(straße: list) -> bool:
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


def bruteForce() -> list:
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
                        if checkStraße(straße):
                            richtigeStraßen.append(list(straße))
                            print(straße)
    return richtigeStraßen


def prettyPrint(straße: list):
    """Pretty print für straße
    """
    text = ""
    for haus in straße:
        for fact in haus:
            text += "%11s" % fact.name
        text += "\n"

    print(text, end="")


def evaluateBruteForce():
    richtigeStraßen = bruteForce()  # ~ 48h (ungetested)
    for straße in richtigeStraßen:
        prettyPrint(straße)
        print()
    print("Keine Weiteren lösungen")


if __name__ == "__main__":
    evaluateBruteForce()