import os
import argparse
import pandas as pd

def combine_files(root_dir):
    combined_good = pd.DataFrame(columns=['Title', 'Body', 'Score', 'ViewCount', 'Tags'])
    combined_bad = pd.DataFrame(columns=['Title', 'Body', 'Score', 'ViewCount', 'Tags'])
    for dirName, subdirList, fileList in os.walk(root_dir):
        for fname in fileList:
            if fname != None and not str(fname).startswith('.'):
                filepath = str(dirName) + '/' + str(fname)
                extension = os.path.splitext(fname)[1]
                if extension == '.csv':
                    print(filepath)
                    file_content = pd.read_csv(filepath)
                    
                    if os.path.splitext(fname)[0] == "Good":
                        combined_good = combined_good.append(file_content)
                    elif os.path.splitext(fname)[0] == "Bad":
                        combined_bad = combined_bad.append(file_content)
                    else:
                        print('Nothing to do')
    print(combined_good)
    print(combined_bad)
    return combined_good, combined_bad

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Combine .csv files that are contained in some parent/root directory.')
    parser.add_argument('--root_dir', type=str, action='store', dest='root_dir', default='.', help='Parent directory of all .csv files you want to combine.')
    parser.add_argument('--output_dir', type=str, action='store', dest='output_dir', default='./', help='Parent directory of all .csv files you want to combine.')

    args = parser.parse_args()

    if args.root_dir != None and args.output_dir != None:
        good, bad = combine_files(args.root_dir)
        good.to_csv(args.output_dir + '/combined_good.csv', index=False)
        bad.to_csv(args.output_dir + '/combined_bad.csv', index=False)
    else:
        print('Not enogh arguments')

