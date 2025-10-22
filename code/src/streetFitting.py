from copy import deepcopy


exampleVals = {
    "startStreet": [["", "", "", "", ""],
                    ["", "", "", "", ""],
                    ["", "", "Milch", "", ""],
                    ["", "Blau", "", "", ""],
                    ["Norweger", "", "", "", ""]],
    "houseRules": [["Brite", "Rot", "", "", ""],
              ["Schwede", "", "", "", "Hund"],
              ["Daene", "", "Tee", "", ""],
              ["Deutsche", "", "", "Rothmanns", ""],
              ["", "Gruen", "Kaffee", "", ""],
              ["", "", "Bier", "Winfield", ""],
              ["", "Gelb", "", "Dunhill", ""],
              ["", "", "", "Pall Mall", "Vogel"]],
    "neighborRules": [[[["", "Gruen", "", "", ""], ["", "Weiss", "", "", ""]],
                    [["", "", "", "", ""], ["", "", "", "", ""]]],
                 [[["", "", "", "Marlboro", ""], ["", "", "", "", "Katze"]],
                  [["", "", "", "", "Katze"], ["", "", "", "Marlboro", ""]]],
                 [[["", "", "", "Marlboro", ""], ["", "", "Wasser", "", ""]],
                  [["", "", "Wasser", "", ""], ["", "", "", "Marlboro", ""]]],
                 [[["", "", "", "Dunhill", ""], ["", "", "", "", "Pferd"]],
                  [["", "", "", "", "Pferd"], ["", "", "", "Dunhill", ""]]]],
    "ruleOrder": [8, 0, 6, 4, 2, 5, 10, 3, 1, 7, 9, 11],
    "iters": 26,
    "emptyVal": ""
}


class StreetFitting():

    def __init__(self, startStreet: list, houseRules: list, neighborRules: list, emptyVal=-1, ruleOrder=[]):
        """Recursive fitting of rules into the street

        Args:
            startStreet (list): nested list with the layouts of the houses
            houseRules (list): rules for a house, needs 2 constrains
            neighborRules (list): rules for neighbors
            emptyVal (int, optional): the value a empty slot has. Defaults to -1.
            ruleOrder (list, optional): order the rules should be applied (first house, then neighbor). Defaults to [].
        """
        self.startStreet = deepcopy(startStreet)
        self.houseRules = deepcopy(houseRules)
        self.neighborRules = deepcopy(neighborRules) 
        self.emptyVal = emptyVal
        self._fittingStreets = []
        if len(ruleOrder) == 0:
            self.ruleOrder = [x for x in range(
                len(self.houseRules) + len(self.neighborRules))]
        else:
            self.ruleOrder = ruleOrder

    @staticmethod
    def houseFit(street: list, houseRule: list, emptyVal=-1) -> list:
        """Applies houseRule to the street and returns all valid 
        configurations of the street with the applied value

        Args:
            street (list): the street the house rule should be applied with
            houseRule (list): rule for a house, needs 2 constrains
            emptyVal (int, optional): the value a empty slot has. Defaults to -1.

        Returns:
            list: list of possible streets
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
        """Applies neighborRules to the street and returns all valid 
        configurations of the street with the applied value

        Args:
            street (list): the street the house rule should be applied with
            neighborRule (list): rule for neighbor first part is right neighbor seconde one is the left
            emptyVal (int, optional): the value a empty slot has. Defaults to -1.

        Returns:
            list: list of possible streets
        """
        resultingStreets = []

        for rule in neighborRule:
            idx = []
            for x in range(2):
                for y in range(len(rule[x])):
                    if rule[x][y] != emptyVal:
                        idx.append(y)
                        break
            if len(idx) == 0:
                continue

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

    def _recursiveFitting(self, streets: list, iteration: int = 0):
        """Applies house and Neighbor rules in ruleOrder to the street

        Args:
            streets (list): list of streets that should be checked
            iteration (int, optional): iteration counter. Defaults to 0.
        """
        if iteration < len(self.ruleOrder):
            ruleIndex = self.ruleOrder[iteration]
        else:
            ruleIndex = iteration

        if ruleIndex < len(self.houseRules):
            # zuerst die streets rules
            for street in streets:
                newStreets = self.houseFit(
                    street, self.houseRules[ruleIndex], self.emptyVal)
                self._recursiveFitting(newStreets, iteration+1)
        elif ruleIndex < len(self.houseRules) + len(self.neighborRules):
            # danach die neighbor rules
            for street in streets:
                newStreets = self.neighborFit(
                    street, self.neighborRules[ruleIndex-len(self.houseRules)], self.emptyVal)
                self._recursiveFitting(newStreets, iteration+1)
        else:
            # print("r", end="")
            for street in streets:
                self._fittingStreets.append(street)

    def recursiveFitting(self, streets: list) -> list:
        """starts the fitting algorithm with the given streets

        Args:
            street (list): list of allowed start configurations 

        Returns:
            list: final streets with all rules applied
        """
        self._recursiveFitting(streets)
        return self.fittingStreets

    def calculate(self) -> list:
        """calculates results of start street and returns solutions

        Returns:
            list: solutions
        """
        return self.recursiveFitting([self.startStreet])

    @property
    def fittingStreets(self):
        """all the resulting streets of last Fitting call
        """
        return deepcopy(self._fittingStreets)
