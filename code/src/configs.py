from streetFitting import StreetFitting
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
            text += "%11s" % column
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


def calcSpeed(startStreet: list, houseRules : list, neighborRules: list, emptyVal, basicOrder: list, start:int, end:int) -> list:
    """goes permutations from start to end and returns the fastest order to solve the riddle

    Args:
        startStreet (list): nested list with the layouts of the houses
        houseRules (list): rules for a house, needs 2 constrains
        neighborRules (list): rules for neighbors
        emptyVal (int, optional): the value a empty slot has. Defaults to -1.
        basicOrder (list): order the rules should be applied (first house, then neighbor).
        start (int): start point of ther permutations
        end (int): end point of the perutations

    Returns:
        list: [solvetime, order]
    """
    minTime = 10
    minOrder = []
    orders = itertools.islice(itertools.permutations(basicOrder), start, end)
    for order in orders:
        fitting = StreetFitting(startStreet, houseRules,
                                neighborRules, emptyVal)
        fitting.ruleOrder = order
        t0 = time.time()
        fitting.calculate()
        t1 = time.time()
        delta = t1 - t0
        if delta < minTime:
            minTime = delta
            minOrder = order
    return [minTime, minOrder]


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
                        emptyVal, fitting.ruleOrder, start, end))

        pool = Pool(cores)
        try:
            results = pool.map(calcSpeed, args)
        except:
            os._exit()

        results.sort(key=lambda x: x[0])
        prettyPrint2D(results)

    else:
        raise FileNotFoundError(f"{path}")
