from cmdLineOptions import CmdLineOptions
import configs
import bruteForce
import os
import calcIter
from plotDistribution import plotDistribution

def main():
    """main fuction
    """

    cmd = CmdLineOptions()

    args = cmd.parse_args()

    if args.bruteForce or args.parallelBruteForce or args.improveOrder or args.plot:
        if args.bruteForce:
            bruteForce.evaluateBruteForce()
        if args.parallelBruteForce:
            bruteForce.parallelBruteForce(os.cpu_count())
        if args.improveOrder:
            configs.rulesIterator(args.rulesFile, calcIter.calcIterWrapper, 12, 0)
        if args.plot:
            plotDistribution()
    else:
        configs.useSolver(args.rulesFile, args.solverImplementation)


if __name__ == "__main__":
    import time
    t0 = time.perf_counter()
    main()
    print(f"Runtime main: {time.perf_counter() - t0}s")
