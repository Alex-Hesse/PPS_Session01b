from streetFitting import StreetFitting
from streetFittingIter import StreetFittingIter
from convertStrings2Integers import ConvertStrings2Integers
import os
import json
from enum import Enum
from multiprocessing import Pool
import itertools
import math
from copy import deepcopy
import time


def prettyPrint2D(array2D: list[list]):
    """pretty print of a 2D array (nested list)

    Args:
        array2D (list[list]): array to be printed
    """
    text = ""
    for row in array2D:
        for column in row:
            text += "\t%s" % str(column)
        text += "\n"

    print(text, end="")


class JsonKeys(str, Enum):
    startStreet = "startStreet"
    houseRules = "houseRules"
    neighborRules = "neighborRules"
    ruleOrder = "ruleOrder"
    emptyVal = "emptyVal"


def useSolver(path: str, useConverter: bool = True):
    """opens json file, runs the solver

    Args:
        path (str): file path to the config file
        useConverter (bool, optional): convert strings to integer. Defaults to True.

    Raises:
        KeyError: json is missing a key
        FileNotFoundError: json cant be found/opened
    """
    if os.path.isfile(path):

        with open(path, 'r') as file:
            data = json.load(file)

        try:
            startStreet = data[JsonKeys.startStreet]
            houseRules = data[JsonKeys.houseRules]
            neighborRules = data[JsonKeys.neighborRules]
            emptyVal = data[JsonKeys.emptyVal]
            ruleOrder = data[JsonKeys.ruleOrder]
        except KeyError as e:
            print(e)
            raise KeyError("useSolver: Json config file is missing a key")

        if useConverter:
            conv = ConvertStrings2Integers()
            startStreet = conv.obj2int(startStreet)
            houseRules = conv.obj2int(houseRules)
            neighborRules = conv.obj2int(neighborRules)
            emptyVal = conv.str2int(emptyVal)

        fitting = StreetFitting(startStreet, houseRules,
                                neighborRules, emptyVal, ruleOrder)
        results = fitting.calculate()

        for solution in results:
            if useConverter:
                arr = conv.obj2str(solution)
            else:
                arr = solution
            prettyPrint2D(arr)

    else:
        raise FileNotFoundError(f"{path}")


def calcSpeedWrapper(conf: tuple) -> list:
    """_summary_

    Args:
        conf (tuple): (startStreet (list): nested list with the layouts of the houses
            houseRules (list): rules for a house, needs 2 constrains
            neighborRules (list): rules for neighbors
            emptyVal (int, optional): the value a empty slot has. Defaults to -1.
            basicOrder (list): order the rules should be applied (first house, then neighbor).
            start (int): start point of ther permutations
            end (int): end point of the perutations
            id (int): id)

    Returns:
        list: [solvetime, order]
    """
    return calcSpeed(conf[0], conf[1], conf[2], conf[3], conf[4], conf[5], conf[6], conf[7])


def calcSpeed(startStreet: list, houseRules: list, neighborRules: list, emptyVal, basicOrder: list, start: int, end: int, id: int) -> list:
    """goes permutations from start to end and returns the fastest order to solve the riddle

    Args:
        startStreet (list): nested list with the layouts of the houses
        houseRules (list): rules for a house, needs 2 constrains
        neighborRules (list): rules for neighbors
        emptyVal (int, optional): the value a empty slot has. Defaults to -1.
        basicOrder (list): order the rules should be applied (first house, then neighbor).
        start (int): start point of ther permutations
        end (int): end point of the perutations
        id (int): id

    Returns:
        list: [solvetime, order]
    """
    minIter = 100  # 1e254
    minOrder = []
    orders = itertools.islice(itertools.permutations(basicOrder), start, end)

    iterations = end-start
    i = 0
    iCount = 40000  # number of % prints
    iMod = iterations // iCount
    fitting = StreetFittingIter(
        startStreet, houseRules, neighborRules, emptyVal, minIter)
    for order in orders:
        fitting.ruleOrder = order
        fitting.calculate()
        if fitting.iteration < minIter:
            minIter = fitting.iteration
            fitting.minIter = minIter
            minOrder = order
            print(f"Process {id}: \t{minIter} \t\tOrder: {minOrder}")

        if i % iMod == 0:
            print(f"Process {id}: \t{100*i/iterations} %")
        i += 1

    return [minIter, minOrder]

#77 (0, 1, 2, 3, 8, 6, 4, 5, 10, 7, 9, 11)
def rulesIterator(path: str, cores: int = 0):
    """prints #cores fastest iterations (ordered)

    Args:
        path (str): file path to the config file
        cores (int, optional): how many proceses will be used. 0 == auto. Defaults to 0.

    Raises:
        KeyError: json is missing a key
        FileNotFoundError: json cant be found/opened
    """

    if os.path.isfile(path):

        with open(path, 'r') as file:
            data = json.load(file)

        conv = ConvertStrings2Integers()

        try:
            startStreet = conv.obj2int(data[JsonKeys.startStreet])
            houseRules = conv.obj2int(data[JsonKeys.houseRules])
            neighborRules = conv.obj2int(data[JsonKeys.neighborRules])
            emptyVal = conv.str2int(data[JsonKeys.emptyVal])
            ruleOrder = data[JsonKeys.ruleOrder]
        except KeyError as e:
            print(e)
            raise KeyError("rulesIterator: Json config file is missing a key")

        fitting = StreetFitting(startStreet, houseRules,
                                neighborRules, emptyVal, ruleOrder)

        if cores < 1:
            cores = os.cpu_count()
        chunkSize = math.factorial(len(fitting.ruleOrder)) // cores

        args = []
        # Calculate the start and end index for each core
        for i in range(cores):
            start = i * chunkSize
            end = (i + 1) * chunkSize

            # Give the remainder to the last core
            if i == cores - 1:
                end = math.factorial(len(fitting.ruleOrder))

            args.append((startStreet, houseRules, neighborRules,
                        emptyVal, fitting.ruleOrder, start, end, i+1))

        results = [calcSpeedWrapper(args[0])]
        # pool = Pool(cores)
        # try:
        #     results = pool.map(calcSpeedWrapper, args)
        # except Exception as e:
        #     print(e)
        #     os._exit(-1)

        results.sort(key=lambda x: x[0])
        prettyPrint2D(results)

    else:
        raise FileNotFoundError(f"{path}")
