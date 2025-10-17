import argparse
from os.path import join, abspath
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent


class CmdLineOptions(argparse.ArgumentParser):
    def __init__(self):
        super().__init__(prog='PPS_Session01b',
                         description='Solves the riddle of Albert Einstein.',
                         epilog='Responsible: Alexander Hesse\nVersion: 0.1')

        self.add_argument("-r", "--rulesFile", help="path to rule config File",
                          default=abspath(join(SCRIPT_DIR, "..", "..", "resources", "rules.json")), required=False)
        self.add_argument("-b", "--bruteForce", help="flag to use brute force",
                          action='store_true', default=False)
        self.add_argument("-p", "--parallelBruteForce",
                          help="flag to use parallel brute force", action='store_true', default=False)
        self.add_argument("-i", "--improveOrder", help="flag to search for best rule order",
                          action='store_true', default=False)


if __name__ == "__main__":
    """Test"""
    cmd = CmdLineOptions()
    print(cmd.parse_args())
