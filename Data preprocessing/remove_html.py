import argparse
import pandas as pd

def clean_html(filname):
    df = pd.read_csv(filname)
    print('Berfore cleaning:')
    print(df)
    df['Title'].replace(to_replace='<[^<]+?>', value='', regex=True, inplace=True)
    df['Body'].replace(to_replace='<[^<]+?>', value='', regex=True, inplace=True)
    print('After cleaning:')
    print(df)
    return df
  
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Combine .csv files that are contained in some parent/root directory.')
    parser.add_argument('--i', type=str, action='store', dest='input_filename', help='Filename of inputfile')
    parser.add_argument('--o', type=str, action='store', dest='output_filename', help='Filename of resulting HTML-cleaned outputfile')
    args = parser.parse_args()

    if args.input_filename != None and args.output_filename != None:
        cleaned = clean_html(args.input_filename)
        cleaned.to_csv(args.output_filename, index=False)
    else:
        print('Not enough arguments')
    