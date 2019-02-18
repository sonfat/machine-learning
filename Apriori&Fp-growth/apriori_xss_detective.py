import data_path

from apriori import apriori
from apriori import generateRules
import re

if __name__ == "__main__":
    myDat = []
    with open(data_path.xss_2000) as f:
        for line in f:
            # print line
            index = line.find("?")
            if index > 0:
                line = line[index+1:len(line)]
                token = re.split('\=|&|\?|\%3e|\%3c|\%3E|\%3C|\%20|\%22|<|>|\\n|\(|\)|\'|\"|;|:|,|\%28|\%29',line)
                myDat.append(token)
        f.close()

        L, suppData = apriori(myDat, 0.01)
        rules = generateRules(L, suppData, minConf=0.99)
