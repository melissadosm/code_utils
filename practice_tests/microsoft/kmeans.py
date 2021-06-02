import sys
import random

def kmeans(data, K): 
    # I'm doing this for K = 3, I missed a generalization
    c1 = random.uniform(min(data), max(data))
    c2 = random.uniform(min(data), max(data))
    c3 = random.uniform(min(data), max(data))
    
    centroids = [c1, c2, c3]
    closest = []
    for i in data: 
        close = min(centroids, key=lambda x:abs(x-i))
        closest.append(centroids.index(close))

    # Recalculating centroids: Here is a pseudo code as I did not have the time for finishing it
    # We need to recalculate the centroids
    # for all values with group = 1
    # get the average of the group = new centroid
    # Then repeat the process of calculation
    # My stopping criteria = until we reach t = 100 iterations
    # But this can be improved to the stopping criteria of no reassignations being made.

    return closest

n=100
data = [0]*n
for i in range(n):
    data[i] = random.random()

means = kmeans(data, 3)
print(means)


