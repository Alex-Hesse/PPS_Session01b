import argparse
from os.path import join, abspath
from pathlib import Path
from configs import SolverImplementations

SCRIPT_DIR = Path(__file__).resolve().parent


class CmdLineOptions(argparse.ArgumentParser):
    def __init__(self):
        """initializes command line arguments
        """
        super().__init__(prog='PPS_Session01b',
                         description='Solves the riddle of Albert Einstein.',
                         epilog='Responsible: Alexander Hesse\nVersion: 0.1')

        self.add_argument("-r", "--rulesFile", help="path to rule config File for solver",
                          default=abspath(join(SCRIPT_DIR, "..", "..", "resources", "optimalRules.json")), required=False)
        solverKeyList = list(SolverImplementations.__members__.values())
        solverKeyList = [str(s.value) for s in solverKeyList]
        self.add_argument("-s", "--solverImplementation", help=f"Solver implementation choose: {solverKeyList}. Defaults to {solverKeyList[0]}",
                          default=solverKeyList[0], required=False)
        self.add_argument("-b", "--bruteForce", help="flag to use brute force",
                          action='store_true', default=False)
        self.add_argument("-pb", "--parallelBruteForce",
                          help="flag to use parallel brute force", action='store_true', default=False)
        self.add_argument("-i", "--iterPermutations", help="iterPermutations and count recursive calls",
                          action='store_true', default=False)
        self.add_argument("-io", "--improveOrder", help="flag to search for best rule order",
                          action='store_true', default=False)
        self.add_argument("-plt", "--plot", help="plots distribution",
                          action='store_true', default=False)
        self.add_argument("-d", "--debug", help="runs streetFitting using strings",
                          action='store_true', default=False)


if __name__ == "__main__":
    """Test"""
    cmd = CmdLineOptions()
    print(cmd.parse_args())
