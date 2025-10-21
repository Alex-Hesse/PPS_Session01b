from streetFitting import StreetFitting
from streetFittingNumpy import StreetFittingNumpy
from convertStrings2Integers import ConvertStrings2Integers
import os
import json
from enum import Enum
import multiprocessing
import itertools
import math
from copy import deepcopy
import time
from streetFittingFunctionalNumpy import recursiveFittingNumpy
from streetFittingFunctionalNumba import recursiveFittingNumba
import numpy as np
from calcIter import calcMinIterWrapper
from collections import OrderedDict



def prettyPrint2D(array2D: list[list]):
    """pretty print of a 2D array (nested list)

    Args:
        array2D (list[list]): array to be printed
    """
    text = ""
    try:
        for row in array2D:
            for column in row:
                text += "\t%8s" % str(column)
            text += "\n"
    except:
        text = str(array2D)

    print(text, end="")


class JsonKeys(str, Enum):
    startStreet = "startStreet"
    houseRules = "houseRules"
    neighborRules = "neighborRules"
    ruleOrder = "ruleOrder"
    emptyVal = "emptyVal"


class SolverImplementations(str, Enum):
    classSolver = "class"
    classNumpySolver = "classNumpy"
    functionalSolver = "functional"
    numbaSolver = "numba"


def useSolver(path: str, whichSolver: SolverImplementations = SolverImplementations.classSolver):
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
            if len(ruleOrder) == 0:
                ruleOrder = np.arange(len(houseRules)+len(neighborRules))
        except KeyError as e:
            print(e)
            raise KeyError("useSolver: Json config file is missing a key")

        conv = ConvertStrings2Integers()
        startStreet = conv.obj2int(startStreet)
        houseRules = conv.obj2int(houseRules)
        neighborRules = conv.obj2int(neighborRules)
        emptyVal = conv.str2int(emptyVal)
        
        match SolverImplementations(whichSolver):
            case SolverImplementations.classSolver:
                t0 = time.perf_counter()
                fitting = StreetFitting(startStreet, houseRules,
                                neighborRules, emptyVal, ruleOrder)
                results = fitting.calculate()
                
            case SolverImplementations.classNumpySolver:
                t0 = time.perf_counter()
                fitting = StreetFittingNumpy(startStreet, houseRules,
                                neighborRules, emptyVal, ruleOrder)
                results = fitting.calculate()
                
            case SolverImplementations.functionalSolver:
                
                startStreet = np.array([startStreet])
                houseRules = np.array(houseRules)
                neighborRules = np.array(neighborRules)
                emptyVal = np.array(emptyVal)
                ruleOrder = np.array(ruleOrder)
                t0 = time.perf_counter()
                results = recursiveFittingNumpy(startStreet, houseRules, neighborRules, emptyVal, ruleOrder)
                
            case SolverImplementations.numbaSolver:
                
                startStreet = np.array([startStreet])
                houseRules = np.array(houseRules)
                neighborRules = np.array(neighborRules)
                emptyVal = np.array(emptyVal)
                ruleOrder = np.array(ruleOrder)
                print("Compile numba")
                t0 = time.perf_counter()
                recursiveFittingNumba(startStreet, houseRules, neighborRules, emptyVal, np.arange(len(houseRules) + len(neighborRules)))
                t1 = time.perf_counter()
                print(f"Compile numba time: {t1-t0}")
                t0 = time.perf_counter()
                results = recursiveFittingNumba(startStreet, houseRules, neighborRules, emptyVal, ruleOrder)
            case _:
                raise TypeError(f"Invalid SolverImplenation: {whichSolver}")
        t1 = time.perf_counter()
        
        for solution in results:
            arr = conv.obj2str([[int(i) for i in r] for r in solution])
            prettyPrint2D(arr)
        print(f"{whichSolver} calculation time: {t1-t0}s")
    else:
        raise FileNotFoundError(f"{path}")




def rulesIterator(path: str, function, cores: int = 0, percentage: float = 0):
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
        
        with multiprocessing.Manager() as manager:
            # minIter = manager.Value('i', 1e10)
            # lock = manager.Lock()

            args = []
            # Calculate the start and end index for each core
            for i in range(cores):
                start = i * chunkSize
                end = (i + 1) * chunkSize

                # Give the remainder to the last core
                if i == cores - 1:
                    end = math.factorial(len(fitting.ruleOrder))

                args.append((startStreet, houseRules, neighborRules,
                            emptyVal, fitting.ruleOrder, start, end, i+1, percentage))#, minIter, lock))

            # results = [function(args[8])]
            # return
            pool = manager.Pool(cores)
            try:
                results = pool.map(function, args)
            except KeyboardInterrupt:
                pool.join()

        # results.sort(key=lambda x: x[0])
        # prettyPrint2D(results)
        finalResult = {}
        for res in results:
            for counterKey, (count, order) in res.items():
                try:
                    finalResult[counterKey][0] += count
                except KeyError:
                    finalResult[counterKey] = [count, order]
        
        sortedItems = sorted(finalResult.items())
        finalResult = dict(sortedItems)
        try:
            with open(os.path.join(".temp", "distribution.json"), "w", encoding='utf-8') as file:
                file.write(json.dumps(finalResult ,indent=4))
        except:
            print(finalResult)

    else:
        raise FileNotFoundError(f"{path}")
