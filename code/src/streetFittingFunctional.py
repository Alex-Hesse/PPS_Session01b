from copy import deepcopy
import numpy as np

# this is just for the dimesions, the values will be integer and not strings
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
    "neighborRules": [[[["", "Gruen", "", "", ""], ["", "Weiss", "", "", ""]]],
                 [[["", "", "", "Marlboro", ""], ["", "", "", "", "Katze"]],
                  [["", "", "", "", "Katze"], ["", "", "", "Marlboro", ""]]],
                 [[["", "", "", "Marlboro", ""], ["", "", "Wasser", "", ""]],
                  [["", "", "Wasser", "", ""], ["", "", "", "Marlboro", ""]]],
                 [[["", "", "", "Dunhill", ""], ["", "", "", "", "Pferd"]],
                  [["", "", "", "", "Pferd"], ["", "", "", "Dunhill", ""]]]],
    "ruleOrder": [],
    "emptyVal": ""
}

def houseFit(street: np.ndarray, houseRule: np.ndarray, emptyVal:int) -> np.ndarray:
    """Apllies houseRule to the street and returns all valid 
    configurations of the street with the applied value

    Args:
        street (np.ndarray): the street the houserule should be apllied with
        houseRule (np.ndarray): rule for a house, needs 2 constrains
        emptyVal (int, optional): the value a empty slot has. Defaults to -1.

    Returns:
        np.ndarray: np.ndarray of possible streets
    """
    resultingStreets = [] #np.array([street for _ in range(4)])
    
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


def neighborFit(street: np.ndarray, neighborRule: np.ndarray, emptyVal:int) -> np.ndarray:
    """Apllies neighborRules to the street and returns all valid 
    configurations of the street with the applied value

    Args:
        street (np.ndarray): the street the houserule should be apllied with
        neighborRule (np.ndarray): rule for neighbor first part is right neigbor seconde one is the left
        emptyVal (int): the value a empty slot has

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


def _recursiveFitting(streets: np.ndarray, houseRules: np.ndarray, neighborRules: np.ndarray, emptyVal:int, ruleOrder:np.ndarray, 
                      iteration: int, counter:int, minCounter: int) -> int:
    counter += 1
    if counter > minCounter:
        return counter
    
    if iteration < len(ruleOrder):
        ruleIndex = ruleOrder[iteration]
    else:
        ruleIndex = iteration

    if ruleIndex < len(houseRules):
        # zuerst die streets rules
        for street in streets:
            newStreets = houseFit(street, houseRules[ruleIndex], emptyVal)
            counter =_recursiveFitting(newStreets, houseRules, neighborRules, emptyVal, ruleOrder, iteration+1, counter, minCounter)
    elif ruleIndex < len(houseRules) + len(neighborRules):
        # danach die neighborrules
        for street in streets:
            newStreets = neighborFit(street, neighborRules[ruleIndex-len(houseRules)], emptyVal)
            counter =_recursiveFitting(newStreets, houseRules, neighborRules, emptyVal, ruleOrder, iteration+1, counter, minCounter)
    else:
        # print("r", end="")
        # for street in streets:
        #     print(street)
        pass
    return counter


def recursiveFitting(streets: np.ndarray, houseRules: np.ndarray, neighborRules: np.ndarray, emptyVal:int, ruleOrder:np.ndarray, minCounter: int) -> int:
    return _recursiveFitting(streets, houseRules, neighborRules, emptyVal, ruleOrder, 0, 0, minCounter)


def houseFitOld(street: np.ndarray, houseRule: np.ndarray, emptyVal:int) -> np.ndarray:
    """Apllies houseRule to the street and returns all valid 
    configurations of the street with the applied value

    Args:
        street (np.ndarray): the street the houserule should be apllied with
        houseRule (np.ndarray): rule for a house, needs 2 constrains
        emptyVal (int, optional): the value a empty slot has. Defaults to -1.

    Returns:
        np.ndarray: np.ndarray of possible streets
    """

    resultingStreets = [] #np.array([street for _ in range(4)])
    idx0 = -1
    idx1 = -1 
    i = 0
    for slot in houseRule:
        if slot != emptyVal:
            if idx0 == -1:
                idx0 = i
            else:
                idx1 = i
        i += 1
        
    constrained_indices = np.where(houseRule != emptyVal)[0]
    
    # Guard against rules that don't have exactly two constraints
    if len(constrained_indices) != 2:
        # Depending on the expected behavior, you might raise an error or return an empty array
        return np.empty((0,) + street.shape, dtype=street.dtype)

    idx0, idx1 = constrained_indices
    rule0, rule1 = houseRule[idx0], houseRule[idx1]

    i = 0
    for house in street:
        if house[idx0] == emptyVal and house[idx1] == emptyVal:
            resultingStreets.append(deepcopy(street))
            resultingStreets[-1][i][idx0] = houseRule[idx0]
            resultingStreets[-1][i][idx1] = houseRule[idx1]
        elif house[idx0] == emptyVal and house[idx1] == houseRule[idx1]:
            resultingStreets.append(deepcopy(street))
            resultingStreets[-1][i][idx0] = houseRule[idx0]
        elif house[idx0] == houseRule[idx0] and house[idx1] == emptyVal:
            resultingStreets.append(deepcopy(street))
            resultingStreets[-1][i][idx1] = houseRule[idx1]
        elif house[idx0] == houseRule[idx0] and house[idx1] == houseRule[idx1]:
            resultingStreets.append(deepcopy(street))
        i += 1
    return np.array(resultingStreets)

def neighborFit0ld(street: np.ndarray, neighborRule: np.ndarray, emptyVal:int) -> np.ndarray:
    """Apllies neighborRules to the street and returns all valid 
    configurations of the street with the applied value

    Args:
        street (np.ndarray): the street the houserule should be apllied with
        neighborRule (np.ndarray): rule for neighbor first part is right neigbor seconde one is the left
        emptyVal (int): the value a empty slot has

    Returns:
        np.ndarray: np.ndarray of possible streets
    """
    resultingStreets = []

    for rule in neighborRule:
        idx0 = -1
        idx1 = -1 
        for x in range(2):
            for y in range(len(rule[x])):
                if rule[x][y] != emptyVal:
                    if idx0 == -1:
                        idx0 = y
                    else:
                        idx1 = y
                    break
        if idx0 == -1 and idx1 == -1:
            continue
        
        for x in range(4):
            if street[x][idx0] == emptyVal and street[x+1][idx1] == emptyVal:
                resultingStreets.append(deepcopy(street))
                resultingStreets[-1][x][idx0] = rule[0][idx0]
                resultingStreets[-1][x+1][idx1] = rule[1][idx1]
            elif street[x][idx0] == rule[0][idx0] and street[x+1][idx1] == emptyVal:
                resultingStreets.append(deepcopy(street))
                resultingStreets[-1][x][idx0] = rule[0][idx0]
                resultingStreets[-1][x+1][idx1] = rule[1][idx1]
            elif street[x][idx0] == emptyVal and street[x+1][idx1] == rule[1][idx1]:
                resultingStreets.append(deepcopy(street))
                resultingStreets[-1][x][idx0] = rule[0][idx0]
                resultingStreets[-1][x+1][idx1] = rule[1][idx1]
            elif street[x][idx0] == rule[0][idx0] and street[x+1][idx1] == rule[1][idx1]:
                resultingStreets.append(deepcopy(street))

    return np.array(resultingStreets)




if __name__ == "__main__":
    pass    