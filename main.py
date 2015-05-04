## Ethan Robison, Edward Hu
## EECS 349 Spring 2015

import sys, os
from collections import defaultdict
# from blah import *
spam_directory = sys.argv[1]
#clean_directory = sys.argv[2]
#test_directory = sys.argv[3]


# check to see that each directory has no subdirectories
#root_S = [root for root, _, _ in os.walk(spam_directory)]
#root_C = [root for root, _, _ in os.walk(spam_directory)]
#root_T = [root for root, _, _ in os.walk(spam_directory)]


for root, dirs, files in os.walk(spam_directory):
    path = root.split('/')
    print(len(path) - 1)*'---', os.path.basename(root)
    for f in files:
        print(len(path))*'---', f
    
