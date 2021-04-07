import os
import pandas as pd
import simpleBDB as db
import shutil
import time
import matplotlib.pyplot as plt
from random import choice
from string import ascii_letters

problemsPath = os.path.join('data', 'problems.bed')
ThingToStore = pd.read_csv(problemsPath, sep='\t', header=None)


def addTest(TestDB, keyLength=5, numLabels=100, sampleSize=100, testGet=False):
    byKeys = []
    allFuncs = []
    addTime = []

    keysList = generateKeyList(keyLength, numLabels, 2)

    for keys in keysList:

        sample = ThingToStore.sample(sampleSize)

        startAdd = time.time()
        txn = db.getEnvTxn()
        TestDB.TestResource(*keys).put(sample, txn=txn)
        txn.commit()

        endAdd = time.time()

        addTime.append(endAdd - startAdd)

        if testGet:
            byKey, AllFunc = getAllValuesTime(TestDB)

            byKeys.append(byKey)
            allFuncs.append(AllFunc)

    return addTime, byKeys, allFuncs


def getAllValuesTime(TestDB):
    start = time.time()
    for keys in TestDB.TestResource.db_key_tuples():
        TestDB.TestResource(*keys).get()

    end = time.time()

    byKey = end - start

    start = time.time()

    things = TestDB.TestResource.all()

    end = time.time()

    allFunc = end - start
    return byKey, allFunc


def generateKeyList(keyLength, numLabels, numKeysForLabel):
    keysList = []

    for i in range(numLabels):

        keys = []

        for j in range(numKeysForLabel):
            keys.append(''.join(choice(ascii_letters) for i in range(keyLength)))

        keysList.append(keys)

    return keysList


def runSizeTests():
    numLabels = 10 ** 3

    if os.path.exists('db'):
        shutil.rmtree('db')

    import TestDB

    timeToAdd, getAllByKey, getAllWithFunc = addTest(TestDB, numLabels=numLabels, testGet=True)

    print(timeToAdd, '\n', getAllByKey, '\n', getAllWithFunc)

    plt.subplot(3, 1, 1)
    plt.plot(timeToAdd, label=str(numLabels))

    plt.xlabel('num values')
    plt.ylabel('time taken for value')

    plt.title('Speed of add as number of labels increases')

    plt.subplot(3, 1, 2)
    plt.plot(getAllByKey, label=str(numLabels))

    plt.xlabel('num values')
    plt.ylabel('time taken for label')

    plt.title('Speed of get all using db_key_tuples() as number of labels increases')

    plt.subplot(3, 1, 3)
    plt.plot(getAllWithFunc, label=str(numLabels))

    plt.xlabel('num values')
    plt.ylabel('time taken for label')

    plt.title('Speed of get all using db_key_tuples() as number of labels increases')

    plt.legend()

    plt.tight_layout()

    plt.savefig('figures/byKey.png')

def runTests():
    runSizeTests()



if __name__ == '__main__':
    runTests()
