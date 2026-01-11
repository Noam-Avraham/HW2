import numpy as np
import pandas as pd
import sys
 
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
            print("Incorrect number of iterations!")
            sys.exit(1)
        if max_iter<=0 or max_iter>=800:
            print("Incorrect number of iterations!")
            sys.exit(1)
    try:
        eps=float(args[-3])
    except ValueError:
        print("Incorrect epsilon!")
        sys.exit(1)
    if eps<0:
        print("Incorrect epsilon!")
        sys.exit(1)
    # we can assume validity of input files.
    input_file1=args[-2]
    input_file2=args[-1]

    data1 = pd.read_csv(input_file1, header=None)
    data2 = pd.read_csv(input_file2, header=None)

    data = pd.merge(data1, data2, on=0, how='inner')
    data = data.sort_values(by=0)
    data = data.drop(columns=[0])




def distance(vector1, vector2):
	distance =0.0
	for i in range(len(vector1)):
		distance += (vector1[i]-vector2[i])**2
	return math.sqrt(distance)

# returns new distances.
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
def get_new_cluster(points, clusters, probabilities):
    # chooses a random point based on probabilities.
    new_cluster = np.choice(points, p=probabilities)
    clusters.append(new_cluster)


# returns porpability for all points
def calc_prob_all_points(distances):
    # calculate probability for all points
    sum_dis = sum(distances)
    probabilities = [distances[i] / sum_dis for i in range(len(distances))]
    return probabilities
    
    
    

if __name__ == "__main__":
    main()