import numpy as np
import pandas as pd
import sys
def distance(vector1, vector2):
	distance =0.0
	for i in range(len(vector1)):
		distance += (vector1[i]-vector2[i])**2
	return math.sqrt(distance)

def read_points(merged_data):
	points = []
	all_input = merged_data.read().strip()
	lines=all_input.splitlines()

	for line in lines:
		if not line.strip():
			continue
		coards_string=line.split(',')
		current_point=[]
		
		for coard in coards_string:
			try:
				coard_float = float(coard)
			except ValueError:
				print("An Error Has Occurred")
				sys.exit(1)
			coard_float=float(coard)
			current_point.append(coard_float)
		points.append(current_point)

	return points

def main():
    #input parsing
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
    #input merging
    
    data1 = pd.read_csv(input_file1, header=None)
    data2 = pd.read_csv(input_file2, header=None)

    data = pd.merge(data1, data2, on=0, how='inner')
    data = data.sort_values(by=0)
    data = data.drop(columns=[0])

    pd.to_csv(data, 'merged_data.csv', header=False, index=False)
    #clusters initialization
    

    points = read_points()
	if not points:
		print("An Error Has Occurred")
		sys.exit(1)
	points_num = len(points)
	#point in i place in order is assign to cluster points_to_clusters[i]
	points_to_clusters = [-1 for x in range(points_num)]

	# all points must have same dimension
	dim = len(points[0])
	
	for p in points:
		if len(p) != dim:
			print("An Error Has Occurred")
			sys.exit(1)
	
	if(k<=1 or k>=len(points)):
		print("Incorrect number of clusters!")
		sys.exit(1)


if __name__ == "__main__":
    main()


