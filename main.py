'''
Ethan Robison, Edward Hu
EECS 349 final project
'''

import sys
from data_collection import  SpamFilterClassifier, SpamTrainer, MetaSpamTest



if __name__ == '__main__':
    ## command line inputs
    CASE = sys.argv[1]
    if CASE == "train":
        SPAM_DIR = sys.argv[2]
        HAM_DIR = sys.argv[3]
        RES_CSV = sys.argv[4]

        TRAINER = SpamTrainer(SPAM_DIR, HAM_DIR)
        TRAINER.put_to_csv(RES_CSV)

    elif CASE == "test":
        TRAIN_CSV = sys.argv[2]
        CLASS_SPAM = sys.argv[3]
        CLASS_HAM = sys.argv[4]

        META = MetaSpamTest(TRAIN_CSV, CLASS_SPAM, CLASS_HAM)
        META.run_all_classify()

#        CLASSIFIER = SpamFilterClassifier(TRAIN_CSV, CLASS_SPAM, CLASS_HAM)

#        print CLASSIFIER.run_classify()

    else:
        print "not so good, chief..."

