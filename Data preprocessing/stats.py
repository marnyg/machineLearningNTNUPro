import matplotlib.pyplot as plt; plt.rcdefaults()
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt

dataset = pd.read_csv('../dataset.csv')

#lengths = dataset['text'].str.len()
lengths = dataset['text'].str.split().str.len() # count number of words in each row (split by space)
values = lengths.values # returns values in lengths as numpy array
maximum = max(values)
minimum = min(values)

bins = 20
stepsize = math.floor((maximum - minimum) / bins)
xs = np.arange(minimum, maximum, stepsize)
ys = np.zeros(len(xs))

for i in np.nditer(values):
    for j in range(len(xs)):
        if j == len(xs) - 1:
            # last bin
            ys[j] += 1
            break
        else:
            current_bin_min_val = xs[j]
            next_bin_min_val = xs[j+1]

            if i >= current_bin_min_val and i < next_bin_min_val:
                ys[j] += 1
                break
        

ys = [i/len(values) for i in ys]

x = np.arange(len(xs))

num_less_than_three_hundred = 0
for i in np.nditer(values):
    if i <= 300:
        num_less_than_three_hundred += 1

indices = np.where(np.logical_not(np.isnan(values)))[0]
average = np.average(values[indices])
median = np.median(values[indices])
print('Maximum question length (words):', maximum)
print('Minimum question length (words):', minimum)
print('Average question length:', average)
print('Median question length: ', median)
print('Percentage of questions with less than 300 words:', str(num_less_than_three_hundred / len(values)))
print('Number of questions with less than 300 words:', str(num_less_than_three_hundred))
ax = plt.gca()
plt.xlabel('Words in question')
plt.ylabel('Number of questions with given number of words')
xstics = []
for i in range(len(xs)):
    #xstics.append(str(i * stepsize) + ' <= q < ' + str((i + 1) * stepsize))
    if i == len(xs) - 1:
        xstics.append(str(int(i * stepsize)) + ' <= q ')
    else:
        xstics.append(str(int(i * stepsize)) + ' <= q < ' + str(int((i + 1) * stepsize)))
plt.bar(x, ys, tick_label=xstics, width=0.2)
plt.setp(ax.get_xticklabels(), rotation=30, horizontalalignment='right')
plt.show()

total = len(values)
bad = len(dataset.loc[dataset['label'] == 'b'].values) / total
good = len(dataset.loc[dataset['label'] == 'g'].values) / total 

ax = plt.gca()
plt.xlabel('Distribution of good/bad publications')
plt.ylabel('Percentage')
xstics = ['good', 'bad']
xs = [0, 1]
ys = [good, bad]
plt.bar(xs, ys, tick_label=xstics, width=0.4)
plt.setp(ax.get_xticklabels())
plt.show()
