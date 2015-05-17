## Ethan Robison, Edward Hu
## EECS 349 Spring 2015

import sys##, os
from collections import defaultdict
from data_collection import *

## command line inputs
spam_dir = sys.argv[1]
ham_dir = sys.argv[2]


if __name__ == '__main__':
    ham_emails = dir_process(ham_dir)
    ##    spam_emails = dir_process(spam_dir)

    split_header(ham_emails[0])
    ##    processed_ham = []
