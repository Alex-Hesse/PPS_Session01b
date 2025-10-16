from copy import deepcopy


class StraßenFitting():

    def __init__(self, startStraße: list, hausRegeln:list , nachbarRegeln:list, emptyVal = -1):
        self.startStraße = deepcopy(startStraße)
        self.hausRegeln = deepcopy(hausRegeln)
        self.nachbarRegeln = deepcopy(nachbarRegeln)
        self.emptyVal = emptyVal
        self.__passendeStraßen = []

    @staticmethod
    def hausFit(straße:list, hausRegel:list, emptyVal = -1):
        """wendet hausregeln f an auf straße und gibt alle möglichen 
        sich aus straße + regel ergebenden straßen zurück (keine wenn unmöglich)
        """
        ergebendeStraßen = []
        idx = []
        i = 0
        for slot in hausRegel:
            if slot != emptyVal:
                idx.append(i)
            i += 1
        i = 0
        for haus in straße:
            if haus[idx[0]] == emptyVal and haus[idx[1]] == emptyVal:
                ergebendeStraßen.append(deepcopy(straße))
                ergebendeStraßen[-1][i][idx[0]] = hausRegel[idx[0]]
                ergebendeStraßen[-1][i][idx[1]] = hausRegel[idx[1]]
            elif haus[idx[0]] == emptyVal and haus[idx[1]] == hausRegel[idx[1]]:
                print("h1")
                ergebendeStraßen.append(deepcopy(straße))
                ergebendeStraßen[-1][i][idx[0]] = hausRegel[idx[0]]
            elif haus[idx[1]] == emptyVal and haus[idx[0]] == hausRegel[idx[0]]:
                print("h2")
                ergebendeStraßen.append(deepcopy(straße))
                ergebendeStraßen[-1][i][idx[1]] = hausRegel[idx[1]]
            elif haus[idx[0]] == hausRegel[idx[0]] and haus[idx[1]] == hausRegel[idx[1]]:
                print("h3")
                ergebendeStraßen.append(deepcopy(straße))
            i += 1
        return ergebendeStraßen

    @staticmethod
    def nachbarFit(straße:list, nachbarRegel:list, emptyVal = -1):
        """wendet nachbarregeln f an auf straße und gibt alle möglichen 
        sich aus straße + regel ergebenden straßen zurück (keine wenn unmöglich)
        """
        ergebendeStraßen = []

        for regel in nachbarRegel:
            idx = []
            for x in range(2):
                for y in range(len(regel[x])):
                    if regel[x][y] != emptyVal:
                        idx.append(y)
                        break

            for x in range(4):
                if straße[x][idx[0]] == emptyVal and straße[x+1][idx[1]] == emptyVal:
                    ergebendeStraßen.append(deepcopy(straße))
                    ergebendeStraßen[-1][x][idx[0]] = regel[0][idx[0]]
                    ergebendeStraßen[-1][x+1][idx[1]] = regel[1][idx[1]]
                elif straße[x][idx[0]] == regel[0][idx[0]] and straße[x+1][idx[1]] == emptyVal:
                    ergebendeStraßen.append(deepcopy(straße))
                    ergebendeStraßen[-1][x][idx[0]] = regel[0][idx[0]]
                    ergebendeStraßen[-1][x+1][idx[1]] = regel[1][idx[1]]
                elif straße[x][idx[0]] == emptyVal and straße[x+1][idx[1]] == regel[1][idx[1]]:
                    ergebendeStraßen.append(deepcopy(straße))
                    ergebendeStraßen[-1][x][idx[0]] = regel[0][idx[0]]
                    ergebendeStraßen[-1][x+1][idx[1]] = regel[1][idx[1]]
                elif straße[x][idx[0]] == regel[0][idx[0]] and straße[x+1][idx[1]] == regel[1][idx[1]]:
                    print("n")
                    ergebendeStraßen.append(deepcopy(straße))

        return ergebendeStraßen

    def recursiveFitting(self, straßen:list, iteration: int = 0):
        """wendet alle haus und nachbarregeln rekursiv an
        """
        if iteration < len(self.hausRegeln):
            # zuerst die straßen regeln
            for straße in straßen:
                neueStraßen = self.hausFit(straße, self.hausRegeln[iteration], self.emptyVal)
                self.recursiveFitting(neueStraßen, iteration+1)
        elif iteration < len(self.hausRegeln) + len(self.nachbarRegeln):
            # danach die nachbarregeln
            for straße in straßen:
                neueStraßen = self.nachbarFit(straße, self.nachbarRegeln[iteration-len(self.hausRegeln)], self.emptyVal)
                self.recursiveFitting(neueStraßen, iteration+1)
        else:
            for straße in straßen:
                self.__passendeStraßen.append(straße)
    
    @property
    def passendeStraßen(self):
        return deepcopy(self.__passendeStraßen)

