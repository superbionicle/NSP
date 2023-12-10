import sys
import os

currentDir = os.path.dirname(os.path.abspath(__file__))

import manipulations

def getNerdStats(iDataFrame):
    dataFrame = manipulations.getTransactionsPerClient(iDataFrame)

    print("Mean by client :", dataFrame["total"].mean())
    print("Median by client :", dataFrame["total"].median())
    print("Standard deviation by client :", dataFrame["total"].std())