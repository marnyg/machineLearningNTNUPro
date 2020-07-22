import argparse
import pandas as pd

def mark_bad(filename, label):
    df = pd.read_csv(filename)
    df['label'] = label
    return df

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Combine .csv files that are contained in some parent/root directory.')
    parser.add_argument('--i', type=str, action='store', dest='input_filename', help='Filename of inputfile')
    parser.add_argument('--o', type=str, action='store', dest='output_filename', help='Filename of resulting HTML-cleaned outputfile')
    parser.add_argument('--l', type=str, action='store', dest='label', help='Label to give all the rows in the new [label] column')
    args = parser.parse_args()

    if args.input_filename != None and args.output_filename != None and args.label != None:
        labeled = mark_bad(args.input_filename, args.label)
        labeled.to_csv(args.output_filename, index=False)
    else:
        print('Not enough arguments')
    