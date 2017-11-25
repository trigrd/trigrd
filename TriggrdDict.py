import numpy as np
import math
import csv
import re

BUCKET_SIZE = 5
transactionPattern = re.compile("\d+.\d+|\d+")

class TriggrdDict():

    """Build the main dictionary used for analysing the expenses"""

    def __init__(self):
        self.triggernary = {}

    def convertToDateKey(self,date):
        return date[8:10] + date[3:5]

    def getBucketNumber(self, amount):
        return str(int(float(amount) // BUCKET_SIZE))

    def loadData(self,inputFile):
        result = []
        with open(inputFile) as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in spamreader:
                # print(row)
                if row[3] and row[5]:
                    result.append((row[3],row[5]))
        self.data = result

    def makeBuckets(self):
        for t in self.data:
            if len(t[0]) == 10 and transactionPattern.match(t[1]):
                dateKey = self.convertToDateKey(t[0])
                bucketNum = self.getBucketNumber(t[1])
                if dateKey in self.triggernary:
                    if bucketNum in self.triggernary[dateKey]:
                        self.triggernary[dateKey][bucketNum]+=1
                    else:
                        self.triggernary[dateKey][bucketNum] = 1
                else:
                    self.triggernary[dateKey] = {
                        bucketNum: 1
                    }

    def createTriggerArray(self,inputFile,outputFile):
        self.loadData(inputFile)
        self.makeBuckets()
        file = open(outputFile,"w")
        file.write(str(self.triggernary))
        file.close()


corporateTrigger = TriggrdDict()
corporateTrigger.createTriggerArray('dataset.csv', 'outputData.json')

def fitting(x):
    return 1.154595 - 0.3480303*x + 0.1586106*math.pow(x,2) - 0.0149023*math.pow(x,3) + 0.0005504595*math.pow(x,4) - 0.000007036462*math.pow(x,5)
    # return 1.352011 + 0.08025676*x - 0.00000681859*math.pow(x,2)

def updateDelta(arr):
    # Compute std dev
    for i in range(1,len(arr)):
        sum = 0
        for item in arr[0:i]:
            sum += fitting(item)
        avg = sum / i
        #delta = avg + np.std(arr[0:i])
        print(math.ceil(avg))
