from copy import deepcopy


class StreetFitting():

    def __init__(self, startStreet: list, houseRules: list, neighborRules: list, emptyVal=-1, ruleOrder = []):
        self.startStreet = deepcopy(startStreet)
        self.houseRules = deepcopy(houseRules)
        self.neighborRules = deepcopy(neighborRules)
        self.emptyVal = emptyVal
        self.__fittingStreets = []
        if ruleOrder == []:
            self.ruleOrder = [x for x in range(len(self.houseRules) + len(self.neighborRules))]
        else:
            self.ruleOrder = ruleOrder
        print()

    @staticmethod
    def houseFit(street: list, houseRule: list, emptyVal=-1) -> list:
        """wendet houserules f an auf street und gibt alle möglichen 
        sich aus street + rule resultingn streets zurück (keine wenn unmöglich)
        """

        resultingStreets = []
        idx = []
        i = 0
        for slot in houseRule:
            if slot != emptyVal:
                idx.append(i)
            i += 1
        i = 0
        for house in street:
            if house[idx[0]] == emptyVal and house[idx[1]] == emptyVal:
                resultingStreets.append(deepcopy(street))
                resultingStreets[-1][i][idx[0]] = houseRule[idx[0]]
                resultingStreets[-1][i][idx[1]] = houseRule[idx[1]]
            elif house[idx[0]] == emptyVal and house[idx[1]] == houseRule[idx[1]]:
                resultingStreets.append(deepcopy(street))
                resultingStreets[-1][i][idx[0]] = houseRule[idx[0]]
            elif house[idx[1]] == emptyVal and house[idx[0]] == houseRule[idx[0]]:
                resultingStreets.append(deepcopy(street))
                resultingStreets[-1][i][idx[1]] = houseRule[idx[1]]
            elif house[idx[0]] == houseRule[idx[0]] and house[idx[1]] == houseRule[idx[1]]:
                resultingStreets.append(deepcopy(street))
            i += 1
        return resultingStreets

    @staticmethod
    def neighborFit(street: list, neighborRule: list, emptyVal=-1) -> list:
        """wendet neighborrules f an auf street und gibt alle möglichen 
        sich aus street + rule resultingn streets zurück (keine wenn unmöglich)
        """
        resultingStreets = []

        for rule in neighborRule:
            idx = []
            for x in range(2):
                for y in range(len(rule[x])):
                    if rule[x][y] != emptyVal:
                        idx.append(y)
                        break

            for x in range(4):
                if street[x][idx[0]] == emptyVal and street[x+1][idx[1]] == emptyVal:
                    resultingStreets.append(deepcopy(street))
                    resultingStreets[-1][x][idx[0]] = rule[0][idx[0]]
                    resultingStreets[-1][x+1][idx[1]] = rule[1][idx[1]]
                elif street[x][idx[0]] == rule[0][idx[0]] and street[x+1][idx[1]] == emptyVal:
                    resultingStreets.append(deepcopy(street))
                    resultingStreets[-1][x][idx[0]] = rule[0][idx[0]]
                    resultingStreets[-1][x+1][idx[1]] = rule[1][idx[1]]
                elif street[x][idx[0]] == emptyVal and street[x+1][idx[1]] == rule[1][idx[1]]:
                    resultingStreets.append(deepcopy(street))
                    resultingStreets[-1][x][idx[0]] = rule[0][idx[0]]
                    resultingStreets[-1][x+1][idx[1]] = rule[1][idx[1]]
                elif street[x][idx[0]] == rule[0][idx[0]] and street[x+1][idx[1]] == rule[1][idx[1]]:
                    resultingStreets.append(deepcopy(street))

        return resultingStreets

    def __recursiveFitting(self, streets: list, iteration: int = 0):
        """wendet alle house und neighborrules rekursiv an
        """
        if iteration < len(self.houseRules):
            # zuerst die streets rules
            for street in streets:
                newStreets = self.houseFit(
                    street, self.houseRules[iteration], self.emptyVal)
                self.__recursiveFitting(newStreets, iteration+1)
        elif iteration < len(self.houseRules) + len(self.neighborRules):
            # danach die neighborrules
            for street in streets:
                newStreets = self.neighborFit(
                    street, self.neighborRules[iteration-len(self.houseRules)], self.emptyVal)
                self.__recursiveFitting(newStreets, iteration+1)
        else:
            for street in streets:
                self.__fittingStreets.append(street)
                
    def __recursiveFittingMixed(self, streets: list, iteration: int = 0):
        """wendet alle house und neighborrules rekursiv an
        """
        if iteration < len(self.houseRules):
            # zuerst die streets rules
            ruleIndex = self.ruleOrder[iteration]
            for street in streets:
                newStreets = self.houseFit(
                    street, self.houseRules[ruleIndex], self.emptyVal)
                self.__recursiveFittingMixed(newStreets, iteration+1)
        elif iteration < len(self.houseRules) + len(self.neighborRules):
            # danach die neighborrules
            ruleIndex = self.ruleOrder[iteration]
            for street in streets:
                newStreets = self.neighborFit(
                    street, self.neighborRules[ruleIndex-len(self.houseRules)], self.emptyVal)
                self.__recursiveFittingMixed(newStreets, iteration+1)
        else:
            for street in streets:
                self.__fittingStreets.append(street)

    def recursiveFitting(self, street: list) -> list:
        self.__recursiveFittingMixed([street])
        return self.fittingStreets

    def calculate(self) -> list:
        return self.recursiveFitting(self.startStreet)

    @property
    def fittingStreets(self):
        return deepcopy(self.__fittingStreets)
