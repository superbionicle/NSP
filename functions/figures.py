import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import sys
import os

currentDir = os.path.dirname(os.path.abspath(__file__))

import manipulations

def createHistogram(iDataFrame, iXValues, iYValues, iTitleCommentary):
    plt.figure()
    plt.figure(figsize=(40, 15))

    plt.bar(iDataFrame[iXValues], iDataFrame[iYValues])

    plt.xlabel(iXValues)
    plt.xticks(rotation=90)

    plt.ylabel(iYValues)

    plt.title(iTitleCommentary)
    plt.show()


def createHistogramByMonth(iDataFrame, iTitleCommentary):
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

    plt.figure()
    plt.figure(figsize=(30, 10))

    plt.hist(
        dataFrame["Month"],
        weights=dataFrame["Quantity"],
        bins=len(period),
        edgecolor="black",
    )

    plt.xlabel("Months")
    plt.xticks(period, months[:monthsNumber])

    plt.ylabel("Quantities sold")

    plt.title("Proportion of items sold per month in a work year " + iTitleCommentary)
    plt.tight_layout()
    plt.show()


def createHistogramByDayWeek(iDataFrame, iTitleCommentary):
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

    plt.figure()
    plt.figure(figsize=(30, 10))

    plt.hist(
        dataFrame["Day of week"],
        weights=dataFrame["Quantity"],
        bins=len(days),
        edgecolor="black",
    )

    plt.xlabel("Days")
    plt.xticks(days, daysWeek)

    plt.ylabel("Quantities sold")

    plt.title("Proportion of items sold per day in a work week " + iTitleCommentary)
    plt.tight_layout()
    plt.show()


def createHistogramByHoursOfDay(iDataFrame, iTitleCommentary):
    dataFrame = iDataFrame

    minHour = (pd.Timestamp(min(dataFrame["time"])).floor(freq="H")).time().hour
    maxHour = (pd.Timestamp(max(dataFrame["time"])).ceil(freq="H")).time().hour

    hours = np.linspace(minHour, maxHour, maxHour - minHour + 1)
    period = [str(int(hour)) + ":00" for hour in hours]

    dataFrame["Time period"] = pd.to_datetime(dataFrame["time"]).dt.hour
    dataFrame = dataFrame.groupby("Time period", as_index=False).sum("Quantity")

    plt.figure()
    plt.figure(figsize=(30, 10))

    plt.hist(
        dataFrame["Time period"],
        weights=dataFrame["Quantity"],
        bins=len(hours),
        edgecolor="black",
    )

    plt.xlabel("Hours")
    plt.xticks(hours, period)

    plt.ylabel("Quantities sold")

    plt.title("Proportion of items sold per hour in a work day " + iTitleCommentary)
    plt.show()


def getAnnualSales(iDataFrame, iThreshold, iTitleCommentary,isLabelRotating=False):
    dataFrame = manipulations.calculateProportions(iDataFrame)

    plt.figure()
    plt.figure(figsize=(30, 5))

    for index, threshold in enumerate(iThreshold):
        plt.subplot(1, len(iThreshold), index + 1)

        tempDataFrame = manipulations.groupedArticles(dataFrame,threshold)
        tempDataFrame = tempDataFrame.sort_values(by=["proportion of annual sales"], ascending=False)

        plt.pie(
            tempDataFrame["proportion of annual sales"],
            labels=tempDataFrame["article"],
            rotatelabels=isLabelRotating,
            labeldistance=0.5,
        )

    plt.title("ratio of items sold "+iTitleCommentary)
    plt.show()


def compareAnnualeSalesCategories(iDataFrames, iThreshold, iTitleCommentary,isLabelRotating=False):
    plt.figure()
    plt.figure(figsize=(30, 5))

    for index, dataFrame in enumerate(iDataFrames):
        plt.subplot(1, len(iDataFrames), index + 1)

        tempDataFrame = manipulations.calculateProportions(dataFrame)
        tempDataFrame = manipulations.groupedArticles(tempDataFrame,iThreshold)

        plt.pie(
            tempDataFrame["proportion of annual sales"],
            labels=tempDataFrame["article"],
            rotatelabels=isLabelRotating,
            labeldistance=0.5,
        )

    plt.title("Comparaison of different grouping choices "+iTitleCommentary)
    plt.show()


def getIllustrations(iDataFrame,iTitleCommentary,iThreshold=[0],isLabelRotating=False):
    createHistogram(iDataFrame,"article","Quantity",iTitleCommentary)
    createHistogramByHoursOfDay(iDataFrame,iTitleCommentary)
    createHistogramByDayWeek(iDataFrame,iTitleCommentary)
    createHistogramByMonth(iDataFrame,iTitleCommentary)
    getAnnualSales(iDataFrame,iThreshold,iTitleCommentary,isLabelRotating)

