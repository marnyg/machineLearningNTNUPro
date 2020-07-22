import argparse
import pandas as pd

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Combine .csv files that are contained in some parent/root directory.')
    parser.add_argument('--i1', type=str, action='store', dest='input_filename1', help='Filename of first inputfile')
    parser.add_argument('--i2', type=str, action='store', dest='input_filename2', help='Filename of second inputfile')
    parser.add_argument('--o', type=str, action='store', dest='output_filename', help='Filename of resulting HTML-cleaned outputfile')
    args = parser.parse_args()

    if args.input_filename1 != None and args.output_filename != None and args.input_filename2 != None:
        first = pd.read_csv(args.input_filename1)
        second = pd.read_csv(args.input_filename2)
        output = first.append(second)
        output.to_csv(args.output_filename, index=False)
    else:
        print('Not enough arguments')