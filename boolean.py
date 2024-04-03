import math
import random

truth_table = {
    "000": random.choice([0, 1]),
    "001": random.choice([0, 1]),
    "010": random.choice([0, 1]),
    "011": random.choice([0, 1]),
    "100": random.choice([0, 1]),
    "101": random.choice([0, 1]),
    "110": random.choice([0, 1]),
    "111": random.choice([0, 1]),
}

K = 20

# nodes can be either 0 or 1
nodes = [random.choice([0, 1]) for _ in range(K)]

connections = {
    k: [random.randint(0, K - 1) for k in range(3)] for k in range(K)
}

iterations = 1000

for _ in range(iterations):
    new_nodes = nodes.copy()

    for i in range(K):
        inputs = "".join([str(nodes[k]) for k in connections[i]])
        new_nodes[i] = truth_table[inputs]

    nodes = new_nodes

    # break if all nodes are the same
    if len(set(nodes)) == 1:
        print("Converged in", _ + 1, "iterations")
        break

print(nodes)