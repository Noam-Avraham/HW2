import numpy as np
import pandas as pd
import sys
import mykmeanssp


def distance(vector1, vector2):
	return np.linalg.norm(vector1 - vector2)


def main():
    #input parsing
    np.random.seed(1234)
    args = sys.argv
    if len(args)>6 or len(args)<5:
        print("An Error Has Occurred")
        sys.exit(1)
    try:
        k=int(args[1])
    except ValueError:
        print("Incorrect number of clusters!")
        sys.exit(1)
    if k<=0:
        print("Incorrect number of clusters!")
        sys.exit(1)

    if(len(args)<6):
        max_iter=300
    else:
        try:
            max_iter=int(args[2])
        except ValueError:
            print("Incorrect maximum iteration!")
            sys.exit(1)
        if max_iter<=0 or max_iter>=800:
            print("Incorrect maximum iteration!")
            sys.exit(1)
    try:
        eps=float(args[-3])
    except ValueError:
        print("Incorrect epsilon!")
        sys.exit(1)
    if eps<0:
        print("Incorrect epsilon!")
        sys.exit(1)
    # we can assume validity of name of input files.
    input_file1=args[-2]
    input_file2=args[-1]

    # get input data:
    data1 = pd.read_csv(input_file1, header=None)
    data2 = pd.read_csv(input_file2, header=None)

    data = pd.merge(data1, data2, on=0, how='inner')
    data = data.sort_values(by=0)
    observed_ids = data.iloc[:, 0].values
    data = data.drop(columns=[0])

    if data.isnull().values.any():
        print("An Error Has Occurred")
        sys.exit(1)

    try:
        data = data.astype(float)
    except ValueError:
        print("An Error Has Occurred")
        sys.exit(1)

    points = data.to_numpy()
    
    if k >=len(points):
        print("Incorrect number of clusters!")
        sys.exit(1)
    # create clusters array:
    clusters_keys=[]
    clusters = []
    points_indecies = [i for i in range(len(points))]
    first_index=np.random.choice(points_indecies)
    clusters_keys.append(first_index)
    clusters.append(points[first_index])
    points_to_cluster = [0 for _ in range(len(points))]
    points_distances = [distance(points[i], clusters[0]) for i in range(len(points))]

    while len(clusters) < k:
        # calculate probabilities for all points
        probabilities = calc_prob_all_points(points_distances)
        # get new cluster
        get_new_cluster(points, clusters, probabilities, points_indecies,clusters_keys)
        # calculate new distances
        calculate_new_distances(points, clusters, points_distances, points_to_cluster)
         
    print(clusters)


# updates the points_to_cluster and points_distances arrays.
def calculate_new_distances(points, clusters, points_distances, points_to_cluster):
    # Checks for each point if closer to new point.
    # if so, updates distance, and points_to_cluster.
    for i in range(len(points)):
        point = points[i]
        maybe_new_distance = distance(point, clusters[-1])
        if points_distances[i] > maybe_new_distance:
            points_distances[i] = maybe_new_distance
            points_to_cluster[i] = len(clusters) - 1


# appends new cluster to the array
def get_new_cluster(points, clusters, probabilities, points_indecies,clusters_keys):
    # chooses a random point based on probabilities.
    new_cluster = np.random.choice(points_indecies, p=probabilities)
    clusters.append(points[new_cluster])
    clusters_keys.append(new_cluster)

# returns porpability for all points
def calc_prob_all_points(distances):
    # calculate probability for all points
    sum_dis = sum(distances)
    probabilities = [distances[i] / sum_dis for i in range(len(distances))]
    return probabilities
C_points=points.tolist()
dim=len(points[0])
n=len(points)
try :
    result=mykmeanssp.fit(C_points,clusters,points_to_cluster, k,  max_iter,dim, eps)
except Exception:
    print("An Error Has Occurred")
    sys.exit(1)


    

if __name__ == "__main__":
    main()


