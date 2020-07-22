#!/usr/local/bin/python
import argparse
import pandas as pd
import sys

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] != None and sys.argv[1] != "":
        input_filename = sys.argv[1]
        df = pd.read_csv(input_filename)
        print(df)
    else:
        print('Missing file argument')