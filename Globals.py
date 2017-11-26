import re

inputFilePath = "dataset.csv"
outputFilePath = "output2.json"
BUCKET_SIZE = 5
transactionPattern = re.compile("\d+.\d+|\d+")
