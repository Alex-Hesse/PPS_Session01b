import numpy as np
import numba
from numba import njit, types
from numba.typed import List
import time


STREET_TYPE = numba.typeof(np.zeros((5, 5), dtype=np.int64))

# this is just for the dimensions, the values will be integer and not strings
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

@njit
def houseFitNumba(street: np.ndarray, houseRule: np.ndarray, emptyVal:int) -> List:
    """Applies houseRule to the street and returns all valid 
    configurations of the street with the applied value

    Args:
        street (np.ndarray): the street the house rule should be applied with
        houseRule (np.ndarray): rule for a house, needs 2 constrains
        emptyVal (int): the value a empty slot has

    Returns:
        np.ndarray: array of possible streets
    """
    resultingStreets = List.empty_list(STREET_TYPE)
    
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

    return resultingStreets

@njit
def neighborFitNumba(street: np.ndarray, neighborRule: np.ndarray, emptyVal:int) -> List:
    """Applies neighborRules to the street and returns all valid 
    configurations of the street with the applied value

    Args:
        street (np.ndarray): the street the house rule should be applied with
        neighborRule (np.ndarray): rule for neighbor first part is right neighbor seconde one is the left
        emptyVal (int): the value a empty slot has

    Returns:
        np.ndarray: array of possible streets
    """
    resultingStreets = List.empty_list(STREET_TYPE)


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

    return resultingStreets

@njit
def _recursiveFittingCounterNumba(streets: List, houseRules: np.ndarray, neighborRules: np.ndarray, emptyVal:int, ruleOrder:np.ndarray, 
                      iteration: int, counter = List) -> List:
    """"Applies house and neighbor rules in ruleOrder to the street

    Args:
        streets (np.ndarray): array of streets that should be checked
        houseRules (np.ndarray): array of rules for a house, needs 2 constrains
        neighborRules (np.ndarray): array rules for neighbors
        emptyVal (int): the value a empty slot has
        ruleOrder (np.ndarray): order the rules should be applied in (first house, then neighbor)
        iteration (int): iteration counter
        counter (int): call counter
        minCounter (int): call counter cutoff

    Returns:
        int: total calls
    """
    # using list to attempt to speed up to the original function code
    counter[0] += 1
    if counter[0] > counter[1]:
        pass
    else:
        if iteration < len(ruleOrder):
            ruleIndex = ruleOrder[iteration]
        else:
            ruleIndex = iteration

        if ruleIndex < len(houseRules):
            # zuerst die streets rules
            for street in streets:
                newStreets = houseFitNumba(street, houseRules[ruleIndex], emptyVal)
                counter =_recursiveFittingCounterNumba(newStreets, houseRules, neighborRules, emptyVal, ruleOrder, iteration+1, counter)
        elif ruleIndex < len(houseRules) + len(neighborRules):
            # danach die neighbor rules
            for street in streets:
                newStreets = neighborFitNumba(street, neighborRules[ruleIndex-len(houseRules)], emptyVal)
                counter =_recursiveFittingCounterNumba(newStreets, houseRules, neighborRules, emptyVal, ruleOrder, iteration+1, counter)
        # else:
        #     for street in streets:
        #         print(street)
            
    return counter


def recursiveFittingCounterNumba(streets: np.ndarray, houseRules: np.ndarray, neighborRules: np.ndarray, emptyVal:int, ruleOrder:np.ndarray, minCounter: int) -> int:
    """"Applies house and neighbor rules in ruleOrder to the street

    Args:
        streets (np.ndarray): array of streets that should be checked
        houseRules (np.ndarray): array of rules for a house, needs 2 constrains
        neighborRules (np.ndarray): array rules for neighbors
        emptyVal (int): the value a empty slot has
        ruleOrder (np.ndarray): order the rules should be applied in (first house, then neighbor)
        counter (int): call counter
        minCounter (int): call counter cutoff

    Returns:
        int: total calls
    """
    result = _recursiveFittingCounterNumba(List(streets), houseRules, neighborRules, emptyVal, ruleOrder, 0, List(np.array([0, int(minCounter)])))[0]
    return result

@njit
def _recursiveFittingNumba(streets: List, houseRules: np.ndarray, neighborRules: np.ndarray, emptyVal:int, ruleOrder:np.ndarray, 
                      iteration: int, result = List) -> List:
    """"Applies house and neighbor rules in ruleOrder to the street

    Args:
        streets (np.ndarray): array of streets that should be checked
        houseRules (np.ndarray): array of rules for a house, needs 2 constrains
        neighborRules (np.ndarray): array rules for neighbors
        emptyVal (int): the value a empty slot has
        ruleOrder (np.ndarray): order the rules should be applied in (first house, then neighbor)
        iteration (int): iteration counter
        result (np.ndarray): array of solutions

    Returns:
        np.ndarray: array of solutions
    """
    if iteration < len(ruleOrder):
        ruleIndex = ruleOrder[iteration]
    else:
        ruleIndex = iteration

    if ruleIndex < len(houseRules):
        # zuerst die streets rules
        for street in streets:
            newStreets = houseFitNumba(street, houseRules[ruleIndex], emptyVal)
            result =_recursiveFittingNumba(newStreets, houseRules, neighborRules, emptyVal, ruleOrder, iteration+1, result)
    elif ruleIndex < len(houseRules) + len(neighborRules):
        # danach die neighbor rules
        for street in streets:
            newStreets = neighborFitNumba(street, neighborRules[ruleIndex-len(houseRules)], emptyVal)
            result =_recursiveFittingNumba(newStreets, houseRules, neighborRules, emptyVal, ruleOrder, iteration+1, result)
    else:
        for street in streets:
            result.append(street)
        
    return result


def recursiveFittingNumba(streets: np.ndarray, houseRules: np.ndarray, neighborRules: np.ndarray, emptyVal:int, ruleOrder:np.ndarray) -> List:
    """"Applies house and neighbor rules in ruleOrder to the street

    Args:
        streets (np.ndarray): array of streets that should be checked
        houseRules (np.ndarray): array of rules for a house, needs 2 constrains
        neighborRules (np.ndarray): array rules for neighbors
        emptyVal (int): the value a empty slot has
        ruleOrder (np.ndarray): order the rules should be applied in (first house, then neighbor)
        result (np.ndarray): array of solutions

    Returns:
        np.ndarray: array of solutions
    """
    result = _recursiveFittingNumba(List(streets), houseRules, neighborRules, emptyVal, ruleOrder, 0, List.empty_list(STREET_TYPE))
    return result

def compileNumba():
    """doesn't work"""
    street = np.full((5,5), 0)
    streets = List(np.array([street for _ in range(7)]))
    houseRule = np.array([1,1,0,0,0])
    houseRules = np.array([houseRule for _ in range(4)])
    neighborRule = np.array([[[0,0,2,0,0], [0,0,3,0,0]], [[0,0,0,0,0], [0,0,0,0,0]]])
    neighborRules = np.array([neighborRule])
    ruleOrder = np.arange(len(houseRules) + len(neighborRules))
    
    #houseFitNumba(street, houseRule, 0)
    #neighborFitNumba(street, neighborRule, 0)
    recursiveFittingCounterNumba(streets, houseRules, neighborRules, 0, ruleOrder, 5)
    recursiveFittingNumba(streets, houseRules, neighborRules, 0, ruleOrder)

if __name__ == "__main__":
    from convertStrings2Integers import ConvertStrings2Integers
    from configs import prettyPrint2D, JsonKeys

    conv = ConvertStrings2Integers()
    try:
        startStreet = np.array([conv.obj2int(exampleVals[JsonKeys.startStreet])])
        houseRules =  np.array(conv.obj2int(exampleVals[JsonKeys.houseRules]))
        neighborRules = np.array(conv.obj2int(exampleVals[JsonKeys.neighborRules]))
        emptyVal =  np.array(conv.str2int(exampleVals[JsonKeys.emptyVal]))
        ruleOrder =  exampleVals[JsonKeys.ruleOrder]
    except KeyError as e:
        print(e)
        raise KeyError("rulesIterator: Json config file is missing a key")

    print("Compiling Numba")
    t0 = time.perf_counter()
    recursiveFittingCounterNumba(startStreet, houseRules,neighborRules, emptyVal, ruleOrder, 1000)
    recursiveFittingNumba(startStreet, houseRules,neighborRules, emptyVal, ruleOrder)
    t1 = time.perf_counter()
    print(f"Numba compilation time: {t1 -t0}s")

    iters = 10000
    print(f"Running {iters} times to measure average...")
    t0 = time.perf_counter()
    for x in range(iters):
        recursiveFittingCounterNumba(startStreet, houseRules,neighborRules, emptyVal, ruleOrder, 1000)
    t1 = time.perf_counter()
    print(f"Runtime recursiveFittingCounter numba: {(t1 - t0)/iters}s")
    
    t0 = time.perf_counter()
    for x in range(iters):
        result = recursiveFittingNumba(startStreet, houseRules,neighborRules, emptyVal, ruleOrder)
    t1 = time.perf_counter()
    print(f"Runtime recursiveFitting numba: {(t1 - t0)/iters}s")

    for res in result:
        prettyPrint2D(conv.obj2str([[int(i) for i in r] for r in res]))
