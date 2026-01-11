import numpy as np
import pandas as pd
import sys
 
def main():
 #input parsing k is clusters number, max_iter is maximum iterations, eps is epsilon for convergence, input_file1 and input_file2 are input files.
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

if __name__ == "__main__":
    main()