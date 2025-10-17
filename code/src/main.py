from cmdLineOptions import CmdLineOptions
import configs


def main():

    cmd = CmdLineOptions()

    args = cmd.parse_args()

    if args.bruteForce or args.parallelBruteForce or args.improveOrder:
        if args.bruteForce:
            print("b")
        if args.parallelBruteForce:
            print("pb")
        if args.improveOrder:
            print("i")
        raise NotImplementedError
    else:
        configs.useSolver(args.rulesFile)


if __name__ == "__main__":
    import time
    t0 = time.time()
    main()
    print(f"Runtime Main: {time.time() - t0}")
