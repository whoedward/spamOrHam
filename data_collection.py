## Ethan Robison, Edward Hu

def readFile(file_name, offset=0):
    with open(file_name) as f:
        output = [line.strip() for line in f.readlines()][offset:]

    return output
