import argparse
import pandas as pd
from sklearn.utils import shuffle

def shuffle_csv(filename):
    df = pd.read_csv(filename)
    df = shuffle(df)    
    return df

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Combine .csv files that are contained in some parent/root directory.')
    parser.add_argument('--i', type=str, action='store', dest='input_filename', help='Filename of inputfile')
    parser.add_argument('--o', type=str, action='store', dest='output_filename', help='Filename of resulting HTML-cleaned outputfile')
    args = parser.parse_args()

    if args.input_filename != None and args.output_filename != None:
        shuffled = shuffle_csv(args.input_filename)
        shuffled.to_csv(args.output_filename, index=False)
    else:
        print('Not enough arguments')
    