## Ethan Robison, Edward Hu
import os
def dir_process(directory):
    '''walks over a directory and returns the '''
    emails = []
    for _, _, files in os.walk('./' + directory):
        for f in files:
            with open('./' + directory + '/' + f) as email:
                emails.append([line.strip() for line in email.readlines()])

    return emails

def split_header(email):
    '''split an email into header and body'''
    for w in email:
        print w.split(" ")
    return

def email_process(email):
    '''process the lines in an email according to filter restrictions'''
    return
