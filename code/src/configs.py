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


def prettyPrint2D(array2D):
    """Pretty print für straße
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
    emptyKey = "emptyKey"


def useSolver(path: str, useConverter: bool = True):
    if os.path.isfile(path):

        with open(path, 'r') as file:
            data = json.load(file)

        if useConverter:
            conv = ConvertStrings2Integers()

            startStreet = conv.obj2int(data[JsonKeys.startStreet])
            houseRules = conv.obj2int(data[JsonKeys.houseRules])
            neighborRules = conv.obj2int(data[JsonKeys.neighborRules])
            emptyVal = conv.str2int(data[JsonKeys.emptyKey])
            ruleOrder = data[JsonKeys.ruleOrder]
        else:
            startStreet = data[JsonKeys.startStreet]
            houseRules = data[JsonKeys.houseRules]
            neighborRules = data[JsonKeys.neighborRules]
            emptyVal = data[JsonKeys.emptyKey]
            ruleOrder = data[JsonKeys.ruleOrder]

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


def calcSpeed(startStreet, houseRules, neighborRules, emptyVal, basicOrder, start, end):
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
    if os.path.isfile(path):

        with open(path, 'r') as file:
            data = json.load(file)

            conv = ConvertStrings2Integers()

            startStreet = conv.obj2int(data[JsonKeys.startStreet])
            houseRules = conv.obj2int(data[JsonKeys.houseRules])
            neighborRules = conv.obj2int(data[JsonKeys.neighborRules])
            emptyVal = conv.str2int(data[JsonKeys.emptyKey])
            ruleOrder = data[JsonKeys.ruleOrder]

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
