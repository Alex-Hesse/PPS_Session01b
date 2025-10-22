import numpy as np

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


class StreetFittingNumpy():

    def __init__(self, startStreet: np.ndarray, houseRules: np.ndarray, neighborRules: np.ndarray, emptyVal: int=-1, ruleOrder=np.empty((0))):
        """Recursive fitting of rules into the street

        Args:
            startStreet (np.ndarray): nested np.ndarray with the layouts of the houses
            houseRules (np.ndarray): rules for a house, needs 2 constrains
            neighborRules (np.ndarray): rules for neighbors
            emptyVal (int, optional): the value a empty slot has. Defaults to -1.
            ruleOrder (np.ndarray, optional): order the rules should be applied (first house, then neighbor). Defaults to np.empty((0)).
        """
        self.startStreet = np.array(startStreet)
        self.houseRules = np.array(houseRules)
        self.neighborRules = np.array(neighborRules)
        self.emptyVal = emptyVal
        self._fittingStreets = []
        if len(ruleOrder) == 0:
            self.ruleOrder = np.arange(len(self.houseRules) + len(self.neighborRules))
        else:
            self.ruleOrder = np.array(ruleOrder)

    @staticmethod
    def houseFit(street: np.ndarray, houseRule: np.ndarray, emptyVal=-1) -> np.ndarray:
        """Apllies houseRule to the street and returns all valid 
        configurations of the street with the applied value

        Args:
            street (np.ndarray): the street the houserule should be apllied with
            houseRule (np.ndarray): rule for a house, needs 2 constrains
            emptyVal (int, optional): the value a empty slot has. Defaults to -1.

        Returns:
            np.ndarray: np.ndarray of possible streets
        """

        resultingStreets = []
    
        idx0, idx1 = np.where(houseRule != emptyVal)[0]
        rule0, rule1 = houseRule[idx0], houseRule[idx1]

        for i, house in enumerate(street):
            
            slot0, slot1 = house[idx0], house[idx1]

            if slot0 == emptyVal:
                if slot1 == emptyVal:
                    resultingStreets.append(street.copy())
                    resultingStreets[-1][i][idx0] = rule0
                    resultingStreets[-1][i][idx1] = rule1
                elif slot1 == rule1:
                    resultingStreets.append(street.copy())
                    resultingStreets[-1][i][idx0] = rule0
            elif slot0 == rule0:
                if slot1 == emptyVal:
                    resultingStreets.append(street.copy())
                    resultingStreets[-1][i][idx1] = rule1
                elif slot1 == rule1:
                    resultingStreets.append(street.copy())
        
        return np.array(resultingStreets)

    @staticmethod
    def neighborFit(street: np.ndarray, neighborRule: np.ndarray, emptyVal=-1) -> np.ndarray:
        """Apllies neighborRules to the street and returns all valid 
        configurations of the street with the applied value

        Args:
            street (np.ndarray): the street the houserule should be apllied with
            neighborRule (np.ndarray): rule for neighbor first part is right neigbor seconde one is the left
            emptyVal (int, optional): the value a empty slot has. Defaults to -1.

        Returns:
            np.ndarray: np.ndarray of possible streets
        """
        resultingStreets = []

        for rule in neighborRule:

            idx0 = np.where(rule[0] != emptyVal)[0]
            idx1 = np.where(rule[1] != emptyVal)[0]
            
            if idx0.size == 0 and idx1.size == 0:
                continue
                
            idx0 = idx0[0]
            idx1 = idx1[0]
            
            rule0, rule1 = rule[0][idx0], rule[1][idx1]

            for x in range(4):
                
                slot0 = street[x][idx0]
                slot1 = street[x+1][idx1]
                
                if slot0 == emptyVal:
                    if slot1 == emptyVal:
                        resultingStreets.append(street.copy())
                        resultingStreets[-1][x][idx0] = rule0
                        resultingStreets[-1][x+1][idx1] = rule1
                    elif slot1 == rule1:
                        resultingStreets.append(street.copy())
                        resultingStreets[-1][x][idx0] = rule0
                if slot0 == rule0:
                    if slot1 == emptyVal:
                        resultingStreets.append(street.copy())
                        resultingStreets[-1][x+1][idx1] = rule1
                    elif slot1 == rule1:
                        resultingStreets.append(street.copy())

        return np.array(resultingStreets)

    def _recursiveFitting(self, streets: np.ndarray, iteration: int = 0):
        """Applies house and Neighbor rules in ruleOrder to the street

        Args:
            streets (np.ndarray): np.ndarray of streets that should be checked
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
            # danach die neighborrules
            for street in streets:
                newStreets = self.neighborFit(
                    street, self.neighborRules[ruleIndex-len(self.houseRules)], self.emptyVal)
                self._recursiveFitting(newStreets, iteration+1)
        else:
            if len(self._fittingStreets) == 0:
                self._fittingStreets = streets
            elif len(streets) != 0:
                self._fittingStreets = np.concatenate((self._fittingStreets, streets))

    def recursiveFitting(self, streets: np.ndarray) -> np.ndarray:
        """starts the fitting algorithm with the given streets

        Args:
            street (np.ndarray): np.ndarray of allowed start configurations 

        Returns:
            np.ndarray: final streets with all rules applied
        """
        self._recursiveFitting(streets)
        return self.fittingStreets

    def calculate(self) -> np.ndarray:
        """calculates results of startstreet and returns solutions

        Returns:
            np.ndarray: solutions
        """
        return self.recursiveFitting(np.array([self.startStreet]))

    @property
    def fittingStreets(self):
        """all the resulting streets of last Fitting call
        """
        return self._fittingStreets.copy()
