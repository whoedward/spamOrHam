'''
Ethan Robison, Edward Hu
EECS 349 final project
processing module
'''

import os, re

class MetaSpamTest:
    '''creates a number of spam classifiers for testing'''
    def __init__(self, train_csv, spam_dir, ham_dir):
        self.thresh_options = [(x+0.0)/100 for x in range(90,100)]
        self.not_found_options = [(x+0.0)/100 for x in range(40,60,5)]

        self.classifiers = []

        for thresh in self.thresh_options:
            for nfo in self.not_found_options:
                self.classifiers.append(SpamFilterClassifier(train_csv, spam_dir, ham_dir, thresh, nfo))

    def run_all_classify(self):
        '''have each classifier run, printing the results'''
        for classifier in self.classifiers:
            (spam_a, ham_a) = classifier.run_classify()
            print "Spam Accuracy: " + str(spam_a)
            print "Ham Accuracy: " + str(ham_a)
            print classifier.thresh, classifier.not_found_chance
            print


class SpamFilterClassifier:
    '''takes training results and classifies using them'''
    def __init__(self, train_csv, spam_dir, ham_dir, thresh=0.95, not_found_chance=0.4):
        with open(train_csv) as t_csv:
            self.all_lines = [l.strip().split(",") for l in t_csv.readlines()][1:]

        self.ham_words = {}
        self.spam_words = {}
        for line in self.all_lines:
            if line[2] == "ham":
                self.ham_words[line[0]] = int(line[1])
            else:
                self.spam_words[line[0]] = int(line[1])

        self.ham_total = sum(self.ham_words.values())
        self.spam_total = sum(self.spam_words.values())

        self.class_spam_dir = spam_dir
        self.class_ham_dir = ham_dir

        self.min_count = 5
        self.filt = re.compile(r"[^a-zA-Z]+", re.IGNORECASE)
        self.thresh = thresh
        self.not_found_chance = not_found_chance


    def run_classify(self):
        '''classifies over both directories'''
        spam_res = self.classify_directory(self.class_spam_dir)
        ham_res = self.classify_directory(self.class_ham_dir)

        spam_correct = sum([1 for res in spam_res if res])
        ham_correct = sum([1 for res in ham_res if not res])

        return ((spam_correct+0.0) / len(spam_res), (ham_correct+0.0) / len(ham_res))


    def classify_directory(self, directory):
        '''classify an entire directory'''
        results = []
        for _, _, files in os.walk('./' + directory):
            for f in files:
                with open('./' + directory + '/' + f) as email:
                    results.append(self.classify_email(email))
        return results


    def classify_email(self, email):
        '''classify one email'''
        probs = []
        for line in email:
            for word in line.split(" "):
                if len(word) < 30:
                    trim = self.filt.sub('', word).lower()
                    probs += [self.probability_spam(trim)]

        probs.sort(key=lambda x: abs(x-0.5), reverse=True) # Paul Graham's method

        return self.likely_spam(probs[:15])


    def probability_spam(self, word):
        '''odds that an email is spam given that it contains this word'''
        ham_count = self.ham_words[word] if word in self.ham_words else 0
        spam_count = self.spam_words[word] if word in self.spam_words else 0

        if ham_count + spam_count > self.min_count:
            spam_prop = (spam_count+0.0) / self.spam_total
            ham_prop = (ham_count+0.0) / self.ham_total
            return  max([0.01, min([0.99, spam_prop / (spam_prop + ham_prop)])])
        else:
            return self.not_found_chance


    def likely_spam(self, probablities):
        '''the likelihood that something is spam given this probability distribution'''
        numer = 1
        comp = 1
        for p in probablities:
            numer *= p
            comp *= (1-p)
        res = (numer) / (numer + comp)
        return res > self.thresh



class SpamTrainer:
    '''takes sample spam/ham and creates training data'''
    def __init__(self, spam_dir, ham_dir):
        self.spam_dir = spam_dir
        self.ham_dir = ham_dir

        self.spam_words = {}
        self.ham_words = {}

        self.filt = re.compile(r"[^a-zA-Z]+", re.IGNORECASE)

        self.get_dir_counts(self.spam_dir, self.spam_words)
        self.get_dir_counts(self.ham_dir, self.ham_words)


    def get_dir_counts(self, directory, counts):
        '''get word counts of the emails in the directory'''
        print "Processing " + directory
        for _, _, files in os.walk('./' + directory):
            for f in files:
                with open('./' + directory + '/' + f) as email:
                    for word in self.filt_file(email):
                        if word in counts:
                            counts[word] += 1
                        else:
                            counts[word] = 1


    def filt_file(self, fil):
        '''filter the words in a given file'''
        words = []
        file_lines = [line.strip() for line in fil.readlines()]
        for line in file_lines:
            for word in line.split(" "):
                if len(word) < 30:
                    trim = self.filt.sub('', word).lower()
                    words.append(trim)
        return words

    def put_to_csv(self, csv_file):
        '''print results in .csv format'''
        print "Writing to " + str(csv_file)
        with open(csv_file, 'w') as c_f:
            c_f.write('Word,Count,SpamHam\n')
            for word, count in self.spam_words.iteritems():
                c_f.write(word+','+str(count)+',spam\n')
            for word, count in self.ham_words.iteritems():
                c_f.write(word+','+str(count)+',ham\n')
