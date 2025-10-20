from cmdLineOptions import CmdLineOptions
import configs
import bruteForce
import os


def main():
    """main fuction
    """

    cmd = CmdLineOptions()

    args = cmd.parse_args()

    if args.bruteForce or args.parallelBruteForce or args.improveOrder:
        if args.bruteForce:
            bruteForce.evaluateBruteForce()
        if args.parallelBruteForce:
            bruteForce.parallelBruteForce(os.cpu_count())
        if args.improveOrder:
            configs.rulesIterator(args.rulesFile, 12, 54)
    else:
        configs.useSolver(args.rulesFile)


if __name__ == "__main__":
    import time
    t0 = time.time()
    main()
    print(f"Runtime main: {time.time() - t0}s")
