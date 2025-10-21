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


def houseFitNumpy(street: np.ndarray, houseRule: np.ndarray, emptyVal:int) -> np.ndarray:
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


def neighborFitNumpy(street: np.ndarray, neighborRule: np.ndarray, emptyVal:int) -> np.ndarray:
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


def _recursiveFittingCounterNumpy(streets: np.ndarray, houseRules: np.ndarray, neighborRules: np.ndarray, emptyVal:int, ruleOrder:np.ndarray, 
                      iteration: int, counter:int, minCounter: int) -> int:
    """"Applies house and Neigbore rules in ruleOrder to the street recursively

    Args:
        streets (np.ndarray): _description_
        houseRules (np.ndarray): rules for a house, needs 2 constrains
        neighborRules (np.ndarray): _description_
        emptyVal (int): _description_
        ruleOrder (np.ndarray): _description_
        iteration (int): _description_
        counter (int): _description_
        minCounter (int): _description_

    Returns:
        int: _description_
    """
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
            newStreets = houseFitNumpy(street, houseRules[ruleIndex], emptyVal)
            counter =_recursiveFittingCounterNumpy(newStreets, houseRules, neighborRules, emptyVal, ruleOrder, iteration+1, counter, minCounter)
    elif ruleIndex < len(houseRules) + len(neighborRules):
        # danach die neighborrules
        for street in streets:
            newStreets = neighborFitNumpy(street, neighborRules[ruleIndex-len(houseRules)], emptyVal)
            counter =_recursiveFittingCounterNumpy(newStreets, houseRules, neighborRules, emptyVal, ruleOrder, iteration+1, counter, minCounter)
    # else:
    #     for street in streets:
    #         print(street)
        
    return counter


def recursiveFittingCounterNumpy(streets: np.ndarray, houseRules: np.ndarray, neighborRules: np.ndarray, emptyVal:int, ruleOrder:np.ndarray, minCounter: int) -> int:
    return _recursiveFittingCounterNumpy(streets, houseRules, neighborRules, emptyVal, ruleOrder, 0, 0, minCounter)


def _recursiveFittingNumpy(streets: np.ndarray, houseRules: np.ndarray, neighborRules: np.ndarray, emptyVal:int, ruleOrder:np.ndarray, iteration: int, result: np.ndarray) -> np.ndarray:
    
    if iteration < len(ruleOrder):
        ruleIndex = ruleOrder[iteration]
    else:
        ruleIndex = iteration

    if ruleIndex < len(houseRules):
        # zuerst die streets rules
        for street in streets:
            newStreets = houseFitNumpy(street, houseRules[ruleIndex], emptyVal)
            result =_recursiveFittingNumpy(newStreets, houseRules, neighborRules, emptyVal, ruleOrder, iteration+1, result)
    elif ruleIndex < len(houseRules) + len(neighborRules):
        # danach die neighborrules
        for street in streets:
            newStreets = neighborFitNumpy(street, neighborRules[ruleIndex-len(houseRules)], emptyVal)
            result =_recursiveFittingNumpy(newStreets, houseRules, neighborRules, emptyVal, ruleOrder, iteration+1, result)
    else:
        if len(result) == 0:
            result = streets
        elif len(streets) != 0:
            result = np.concatenate((result,streets))
        # for street in streets:
        #     print(street)
        
    return result


def recursiveFittingNumpy(streets: np.ndarray, houseRules: np.ndarray, neighborRules: np.ndarray, emptyVal:int, ruleOrder:np.ndarray) -> np.ndarray:
    result = _recursiveFittingNumpy(streets, houseRules, neighborRules, emptyVal, ruleOrder, 0, np.empty((0)))
    return result


if __name__ == "__main__":
    import time
    import  convertStrings2Integers
    from configs import prettyPrint2D, JsonKeys

    conv = convertStrings2Integers.ConvertStrings2Integers()
    try:
        startStreet = np.array([conv.obj2int(exampleVals[JsonKeys.startStreet])])
        houseRules =  np.array(conv.obj2int(exampleVals[JsonKeys.houseRules]))
        neighborRules = np.array(conv.obj2int(exampleVals[JsonKeys.neighborRules]))
        emptyVal =  np.array(conv.str2int(exampleVals[JsonKeys.emptyVal]))
        ruleOrder =  exampleVals[JsonKeys.ruleOrder]
    except KeyError as e:
        print(e)
        raise KeyError("rulesIterator: Json config file is missing a key")
    
    t0 = time.perf_counter()
    result = recursiveFittingNumpy(startStreet, houseRules,neighborRules, emptyVal, ruleOrder)
    t1 = time.perf_counter()
    print(f"Runtime Function: {t1 - t0}s")
    
    for res in result:
        prettyPrint2D(conv.obj2str([[int(i) for i in r] for r in res]))
    
    
        