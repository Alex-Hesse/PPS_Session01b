import matplotlib.pyplot as plt
import json
import os

def plotDistribution():
    """plots the distribution of recursive calls
    """
    with open(os.path.join(".","resources","distribution.json"), "r") as file:
        data = json.load(file)

    x = data.keys()
    x = [int(i) for i in x]
    x = [i for i in range(max(x))]
    
    y = [0 for _ in range(max(x)+1)]
    for i in range(max(x)):
        try:
            y[i] = data[str(i)][0]
        except KeyError:
            y[i] = 0

    plt.plot(x, y)

    # Add labels and a legend for clarity
    plt.xlabel('Number of Recursive Calls')
    plt.ylabel('Total Occurrences')
    plt.title('Distribution of Recursion Calls Across All 12! Permutations')
    plt.grid(True)
    plt.tight_layout()
    print("Sadly I cut off at 10,000 recursive calls...\nBut it run 14.25h so I'm not doing it again for the ~1000 cut of results.")
    plt.show()

if __name__ == "__main__":
    plotDistribution()