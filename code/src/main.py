from cmdLineOptions import CmdLineOptions
import configs
import bruteForce
import os

from plotDistribution import plotDistribution

def main():
    """main function
    """

    cmd = CmdLineOptions()

    args = cmd.parse_args()

    # choose what mode
    if args.bruteForce or args.parallelBruteForce or args.improveOrder or args.plot or args.iterPermutations:
        if args.bruteForce:
            bruteForce.evaluateBruteForce()
        if args.parallelBruteForce:
            bruteForce.parallelBruteForce(os.cpu_count())
        if args.improveOrder:
            configs.rulesIterator(args.rulesFile, True, percentage=0)
        if args.iterPermutations:
             configs.rulesIterator(args.rulesFile, False, percentage=0)
        if args.plot:
            plotDistribution()
    else:
        configs.useSolver(args.rulesFile, args.solverImplementation)


if __name__ == "__main__":
    import time
    t0 = time.perf_counter()
    main()
    print(f"Runtime main: {time.perf_counter() - t0}s")
