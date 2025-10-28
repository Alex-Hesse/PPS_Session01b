
import os
import itertools
import time
from streetFittingProcedureNumba import recursiveFittingCounterNumba
import numpy as np
import math

def calcIterWrapper(conf: tuple) -> dict:
    """wrapper for calcIter

    Args:
    conf (tuple): (startStreet (list): nested list with the layouts of the houses
                    houseRules (list): rules for a house, needs 2 constrains
                    neighborRules (list): rules for neighbors
                    emptyVal (int, optional): the value a empty slot has. Defaults to -1.
                    basicOrder (list): order the rules should be applied (first house, then neighbor).
                    start (int): start point of the permutations
                    end (int): end point of the permutations
                    id (int): id
                    percentage (float): percentage to start from)

    Returns:
        dict: {"num rec calls": [int(how often), [example of permutation for this result]]}
    """
    return calcIter(conf[0], conf[1], conf[2], conf[3], conf[4], conf[5], conf[6], conf[7], conf[8])


def calcIter(startStreet: list, houseRules: list, neighborRules: list, emptyVal, basicOrder: list, start: int, end: int, id: int, percentage: float) -> dict:
    """goes permutations from start to end and returns dict of total recursive calls and how often they happen with one example value

    Args:
        startStreet (list): nested list with the layouts of the houses
        houseRules (list): rules for a house, needs 2 constrains
        neighborRules (list): rules for neighbors
        emptyVal (int, optional): the value a empty slot has
        basicOrder (list): order the rules should be applied (first house, then neighbor).
        start (int): start point of the permutations
        end (int): end point of the permutations
        id (int): id
        percentage (float): percentage to start from

    Returns:
        dict: {"num rec calls": [int(how often), [example of permutation for this result]]}
    """
    iterations = end-start
    alreadyCompleted = math.ceil((iterations  * percentage) / 100)
    start +=  alreadyCompleted
    i = alreadyCompleted
    iCount = 400  # number of % prints
    iMod = iterations // iCount
    startStreet =  np.array([startStreet])
    houseRules = np.array(houseRules)
    neighborRules = np.array(neighborRules)
    orders = itertools.islice(itertools.permutations(basicOrder), start, end)
    counterDict = {}
    try:
        for order in orders:
            counter = recursiveFittingCounterNumba(startStreet, houseRules, neighborRules, emptyVal, np.array(order), 10000000)
            try:
                counterDict[counter][0] += 1
            except KeyError:
                counterDict[counter] = [1, order]

            i += 1
            if i % iMod == 0:
                print(f"Process {id}: \t{100*i/iterations} %")  # {time.process_time()-t0}")
    except KeyboardInterrupt:
        print(f"Process {id} stopped at: \t{100*i/iterations} %")
    print(f"Process {id}: Done!")
    return counterDict


def calcMinIterWrapper(conf: tuple) -> list:
    """wrapper for calcMinIter

    Args:
        conf (tuple):   (startStreet (list): nested list with the layouts of the houses
                        houseRules (list): rules for a house, needs 2 constrains
                        neighborRules (list): rules for neighbors
                        emptyVal (int, optional): the value a empty slot has
                        basicOrder (list): order the rules should be applied (first house, then neighbor).
                        start (int): start point of the permutations
                        end (int): end point of the permutations
                        id (int): id
                        percentage (float): percentage to start from)

    Returns:
        list: [solve time, order]
    """
    return calcMinIter(conf[0], conf[1], conf[2], conf[3], conf[4], conf[5], conf[6], conf[7], conf[8])


def calcMinIter(startStreet: list, houseRules: list, neighborRules: list, emptyVal, basicOrder: list, start: int, end: int, id: int, percentage: float) -> list:
    """goes permutations from start to end and returns the fastest order to solve the riddle

    Args:
        startStreet (list): nested list with the layouts of the houses
        houseRules (list): rules for a house, needs 2 constrains
        neighborRules (list): rules for neighbors
        emptyVal (int, optional): the value a empty slot has.
        basicOrder (list): order the rules should be applied (first house, then neighbor).
        start (int): start point of there permutations
        end (int): end point of the permutations
        id (int): id
        percentage (float): percentage to start from

    Returns:
        list: [solve time, order]
    """
    minOrder = []
    minIter = 27
    iterations = end-start
    alreadyCompleted = math.ceil((iterations  * percentage) // 100)
    start +=  alreadyCompleted
    i = alreadyCompleted
    iCount = 400  # number of % prints
    iMod = iterations // iCount
    startStreet =  np.array([startStreet])
    houseRules = np.array(houseRules)
    neighborRules = np.array(neighborRules)
    orders = itertools.islice(itertools.permutations(basicOrder), start, end)
    t0 = time.process_time()
    for order in orders:
        counter = recursiveFittingCounterNumba(startStreet, houseRules, neighborRules, emptyVal, np.array(order), minIter)
        if counter < minIter:
            minIter = counter
            minOrder = order
            print(f"Process {id}: \t{minIter} \t\tOrder: {minOrder}")
            try:
                with open(os.path.join(".temp", str(minIter)+str(minOrder)), "w", encoding='utf-8') as file:
                    file.write(str(minIter)+str(minOrder))
            except:
                print("error"+ str(minIter)+str(minOrder))

        i += 1
        if i % iMod == 0:
            print(f"Process {id}: \t{100*i/iterations} %")  # {time.process_time()-t0}")
    print(f"Process {id}: Done!")
    return [minIter, minOrder]