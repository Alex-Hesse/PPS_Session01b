from cmdLineOptions import CmdLineOptions
import configs
import bruteForce
import os

MSG_CAN_NOT_BE_INTERRUPTED = "WARNING process cant be Keybord Interrupted"


def main():
    """main fuction
    """

    cmd = CmdLineOptions()

    args = cmd.parse_args()

    if args.bruteForce or args.parallelBruteForce or args.improveOrder:
        if args.bruteForce:
            bruteForce.evaluateBruteForce()
        if args.parallelBruteForce:
            print(MSG_CAN_NOT_BE_INTERRUPTED)
            bruteForce.parallelBruteForce(os.cpu_count())
        if args.improveOrder:
            print(MSG_CAN_NOT_BE_INTERRUPTED)
            configs.rulesIterator(args.rulesFile, 8)
    else:
        configs.useSolver(args.rulesFile)


if __name__ == "__main__":
    import time
    t0 = time.time()
    main()
    print(f"Runtime main: {time.time() - t0}s")
