from streetFitting import StreetFitting
from convertStrings2Integers import ConvertStrings2Integers
import os
import json
from enum import Enum


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


def useSolver(path: str):
    if os.path.isfile(path):

        with open(path, 'r') as file:
            data = json.load(file)

        conv = ConvertStrings2Integers()

        startStreet = conv.obj2int(data[JsonKeys.startStreet])
        houseRules = conv.obj2int(data[JsonKeys.houseRules])
        neighborRules = conv.obj2int(data[JsonKeys.neighborRules])
        emptyVal = conv.str2int("")

        fitting = StreetFitting(startStreet, houseRules,
                                neighborRules, emptyVal)
        results = fitting.calculate()

        for solution in results:
            prettyPrint2D(conv.obj2str(solution))

    else:
        raise FileNotFoundError(f"{path}")
