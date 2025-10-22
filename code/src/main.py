from cmdLineOptions import CmdLineOptions
import configs
import bruteForce
import os


def main():
    """main function
    """

    cmd = CmdLineOptions()

    args = cmd.parse_args()

    if args.bruteForce or args.parallelBruteForce or args.improveOrder:
        if args.bruteForce:
            bruteForce.evaluateBruteForce()
        if args.parallelBruteForce:
            bruteForce.parallelBruteForce(os.cpu_count())
        if args.improveOrder:
            configs.rulesIterator(args.rulesFile, 12, 0)
    else:
        configs.useSolver(args.rulesFile, args.solverImplementation)


if __name__ == "__main__":
    import time
    t0 = time.perf_counter()
    main()
    print(f"Runtime main: {time.perf_counter() - t0}s")
