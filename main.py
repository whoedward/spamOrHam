## Ethan Robison, Edward Hu
## EECS 349 Spring 2015

import sys, os
from collections import defaultdict
from data_collection import *
spam_directory = sys.argv[1]
#clean_directory = sys.argv[2]
#test_directory = sys.argv[3]


# check to see that each directory has no subdirectories
#root_S = [root for root, _, _ in os.walk(spam_directory)]
#root_C = [root for root, _, _ in os.walk(spam_directory)]
#root_T = [root for root, _, _ in os.walk(spam_directory)]

spam_counts = defaultdict(int)

for root, dirs, files in os.walk(spam_directory):
    path = root.split('/')
    for f in files:
        p = readFile(path[0] + '/' + f,4) # offset of 4 to remove headers
        for line in p:
            for word in line.split(' '):
                spam_counts[word] += 1

clean_spam = [(key, spam_counts[key]) for key in spam_counts.keys()]
clean_spam.sort()
for item in clean_spam[0:100]:
    print(item)
