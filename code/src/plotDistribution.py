import matplotlib.pyplot as plt
import json
import os

def plotDistribution():
    with open(os.path.join(".","resources","distribution.json"), "r") as file:
        data = json.load(file)

    x = data.keys()
    x = [int(i) for i in x]
    y = list(data.values())

    y = [i[0] for i in y]

    #
    plt.plot(x, y)


    # Add labels and a legend for clarity
    plt.xlabel('Number of Recursive Calls')
    plt.ylabel('Total Occurrences')
    plt.title('Distribution of Recursion Depth Across All 12! Permutations')
    plt.grid(True)
    plt.tight_layout()
    print("Sadly I cut off at 10,000 recursive calls...\nBut it run 14.25h so I'm not doing it again for the ~1000 cut of results.")
    plt.show()

if __name__ == "__main__":
    plotDistribution()