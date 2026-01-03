import numpy as np
inport sys
 
 def main()
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
    if(len(args)<6):
        has_iter=0
    else:
        has_iter=1
        try:
            max_iter=int(args[2])
        except ValueError:
            print("Incorrect number of iterations!")
            sys.exit(1)
    try:
        eps=float(args[-3])
    except ValueError:
        print("Incorrect epsilon!")
        sys.exit(1)
    # we can assume validity of input files.
    input_file1=args[-2]
    input_file2=args[-1]
#input merging


if __name__ == "__main__":
    main()