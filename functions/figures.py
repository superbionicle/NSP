import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import os

currentDir = os.path.dirname(os.path.abspath(__file__))

import manipulations

HIST_SIZE = (30, 10)
DIAG_SIZE_1 = 15
DIAG_SIZE_2 = 10


def createHistogram(iDataFrame, iXValues, iYValues, iTitle, iFileName, iStorageFile):
    fileName = iStorageFile + iFileName
    plt.figure(figsize=(40, 15))
    plt.bar(iDataFrame[iXValues], iDataFrame[iYValues])

    plt.xlabel(iXValues)
    plt.xticks(rotation=90)
    plt.ylabel(iYValues)

    plt.title(iTitle)
    plt.savefig(fileName)


def extension(iTitleCommentary, ioFileName, ioTitle):
    if iTitleCommentary != "":
        ioFileName += "_" + iTitleCommentary
        ioTitle += ", " + iTitleCommentary
    return (ioFileName, ioTitle)


def createHistogramByMonth(iDataFrame, iTitleCommentary, iStorageFile):
    fileName = iStorageFile + "Sells_Months"
    title = "Proportion of items sold per month in a work year"
    fileName, title = extension(iTitleCommentary, fileName, title)

    months = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ]

    dataFrame = iDataFrame
    dataFrame["Month"] = dataFrame["date"].dt.month
    dataFrame = dataFrame.groupby("Month", as_index=False).sum("Quantity")

    monthsNumber = dataFrame["Month"].max()
    period = np.linspace(1, monthsNumber, monthsNumber)

    plt.figure(figsize=HIST_SIZE)
    plt.hist(
        dataFrame["Month"],
        weights=dataFrame["Quantity"],
        bins=len(period),
        edgecolor="black",
    )

    plt.xlabel("Months")
    plt.xticks(period, months[:monthsNumber])
    plt.ylabel("Quantities sold")

    plt.title(title)
    plt.tight_layout()
    plt.savefig(fileName)


def createHistogramByDayWeek(iDataFrame, iTitleCommentary, iStorageFile):
    fileName = iStorageFile + "Sells_Days"
    title = "Proportion of items sold per day in a work week"
    fileName, title = extension(iTitleCommentary, fileName, title)

    daysOfWeek = {
        0: "Monday",
        1: "Tuesday",
        2: "Wednesday",
        3: "Thursday",
        4: "Friday",
        5: "Saturday",
        6: "Sunday",
    }
    days = np.linspace(0, 6, 7)
    daysWeek = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]

    dataFrame = iDataFrame

    dataFrame["Day of week"] = dataFrame["date"].dt.dayofweek
    dataFrame["Day of week"] = dataFrame["Day of week"].map(daysOfWeek)
    dataFrame = dataFrame.groupby("Day of week", as_index=False).sum("Quantity")

    plt.figure(figsize=HIST_SIZE)
    plt.hist(
        dataFrame["Day of week"],
        weights=dataFrame["Quantity"],
        bins=len(days),
        edgecolor="black",
    )

    plt.xlabel("Days")
    plt.xticks(days, daysWeek)
    plt.ylabel("Quantities sold")

    plt.title(title)
    plt.tight_layout()
    plt.savefig(fileName)


def createHistogramByHoursOfDay(iDataFrame, iTitleCommentary, iStorageFile):
    fileName = iStorageFile + "Sells_Hours"
    title = "Proportion of items sold per hour in a work day"
    fileName, title = extension(iTitleCommentary, fileName, title)

    dataFrame = iDataFrame

    minHour = (pd.Timestamp(min(dataFrame["time"])).floor(freq="H")).time().hour
    maxHour = (pd.Timestamp(max(dataFrame["time"])).ceil(freq="H")).time().hour

    hours = np.linspace(minHour, maxHour, maxHour - minHour + 1)
    period = [str(int(hour)) + ":00" for hour in hours]

    dataFrame["Time period"] = pd.to_datetime(dataFrame["time"]).dt.hour
    dataFrame = dataFrame.groupby("Time period", as_index=False).sum("Quantity")

    plt.figure(figsize=HIST_SIZE)
    plt.hist(
        dataFrame["Time period"],
        weights=dataFrame["Quantity"],
        bins=len(hours),
        edgecolor="black",
    )

    plt.xlabel("Hours")
    plt.xticks(hours, period)
    plt.ylabel("Quantities sold")

    plt.title(title)
    plt.savefig(fileName)


def getAnnualSales(iDataFrame, iThreshold, iTitleCommentary, iStorageFile):
    fileName = iStorageFile + "AS"
    if len(iThreshold) > 1:
        fileName += "_Thresholds"
    title = "Ratio of items sold"
    fileName, title = extension(iTitleCommentary, fileName, title)

    dataFrame = manipulations.calculateProportions(iDataFrame)

    plt.figure(figsize=(DIAG_SIZE_1 * len(iThreshold), DIAG_SIZE_2))

    for index, threshold in enumerate(iThreshold):
        plt.subplot(1, len(iThreshold), index + 1)
        plt.title("Threshold : " + str(threshold) + "%")
        tempDataFrame,temp = manipulations.groupedArticles(dataFrame, threshold)
        tempDataFrame = tempDataFrame.sort_values(
            by=["proportion of annual sales"], ascending=False
        )

        plt.pie(
            tempDataFrame["proportion of annual sales"],
            labels=tempDataFrame["article"],
            rotatelabels=True,
            labeldistance=0.5,
        )

    plt.suptitle(title)
    plt.savefig(fileName)


def compareAnnualeSalesCategories(
    iDataFrames, iThreshold, iTitleCommentary, iStorageFile
):
    fileName = iStorageFile + "AS_Compare"
    title = "Comparaison of different grouping choices"
    fileName, title = extension(iTitleCommentary, fileName, title)

    plt.figure(figsize=(DIAG_SIZE_1, DIAG_SIZE_2))

    for index, dataFrame in enumerate(iDataFrames):
        plt.subplot(1, len(iDataFrames), index + 1)
        plt.title("Category " + dataFrame[0])
        tempDataFrame = manipulations.calculateProportions(dataFrame[1])
        tempDataFrame,temp = manipulations.groupedArticles(tempDataFrame, iThreshold)

        plt.pie(
            tempDataFrame["proportion of annual sales"],
            labels=tempDataFrame["article"],
            rotatelabels=True,
            labeldistance=0.5,
        )

    plt.suptitle(title)
    plt.savefig(fileName)


def getIllustrations(iDataFrame, iTitleCommentary, iStorageFile):
    createHistogramByHoursOfDay(iDataFrame, iTitleCommentary, iStorageFile)
    createHistogramByDayWeek(iDataFrame, iTitleCommentary, iStorageFile)
    createHistogramByMonth(iDataFrame, iTitleCommentary, iStorageFile)
