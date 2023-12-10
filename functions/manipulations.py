import pandas as pd
import numpy as np


def convertColumnStrToFloat(ioDataFrame, iColumnName):
    ioDataFrame[iColumnName] = ioDataFrame[iColumnName].astype("str")
    ioDataFrame[iColumnName] = ioDataFrame[iColumnName].str.replace(",", ".")
    ioDataFrame[iColumnName] = ioDataFrame[iColumnName].astype("float")

    return ioDataFrame[iColumnName]


def createDataFrame(iCSV):
    oDataFrame = pd.read_csv(iCSV)

    del oDataFrame["Unnamed: 0"]

    oDataFrame["unit_price"] = oDataFrame["unit_price"].str.replace(" €", "")
    oDataFrame["unit_price"] = convertColumnStrToFloat(oDataFrame, "unit_price")
    oDataFrame["date"] = pd.to_datetime(oDataFrame["date"])

    totalAmount = oDataFrame["unit_price"] * oDataFrame["Quantity"]
    oDataFrame["total"] = totalAmount

    return oDataFrame


def getItemsAndPrice(iDataFrame):
    articles = iDataFrame[["article", "unit_price"]]
    oMenu = articles.drop_duplicates().sort_values(by=["article"], ascending=True)

    return oMenu


def getTotalItemsSold(iDataFrame):
    dataFrameSelected = iDataFrame[["article", "Quantity"]]
    oItemsSold = dataFrameSelected.groupby("article", as_index=False).sum("Quantity")

    return oItemsSold


def getListItems(iDataFrame):
    oArticlesSold = iDataFrame.article.unique()
    oArticlesSold.sort()

    return oArticlesSold


def getTransactionsPerClient(iDataFrame):
    oDataFrameTransactions = iDataFrame.groupby("ticket_number").sum("total")

    return oDataFrameTransactions


def groupedCategories(iDataFrame, iRefFile):
    dataFrameRef = pd.read_csv(iRefFile)
    del dataFrameRef["Unnamed: 0"]

    dataFrame = iDataFrame

    commonDataFrame = pd.merge(dataFrame, dataFrameRef, on="article")

    grouped = pd.DataFrame(
        commonDataFrame.dropna(subset=["categorie"])
        .groupby("categorie", as_index=False)[["Quantity", "total"]]
        .sum()
    )
    grouped = grouped.rename(columns={"categorie": "article"})

    noCategories = commonDataFrame[commonDataFrame["categorie"].isna()][
        ["article", "Quantity", "total"]
    ]
    noCategories = pd.DataFrame(
        noCategories.groupby("article", as_index=False).sum("total")
    )

    oDataFrame = pd.concat([grouped, noCategories], ignore_index=True)

    return oDataFrame


def calculateProportions(iDataFrame):
    oDataFrame = iDataFrame

    totalAnnualSales = sum(oDataFrame["total"])
    oDataFrame = oDataFrame.groupby("article", as_index=False).sum("total")
    oDataFrame["proportion of annual sales"] = (
        oDataFrame["total"] / totalAnnualSales * 100
    )

    return oDataFrame


def groupedArticles(iDataFrame, iThreshHold):
    dataFrame = iDataFrame

    oDataFrameGrouped = dataFrame[
        dataFrame["proportion of annual sales"] >= iThreshHold
    ]
    othersArticlesNumber = len(
        dataFrame[dataFrame["proportion of annual sales"] < iThreshHold].index
    )
    articlesGrouped = dataFrame[
        dataFrame["proportion of annual sales"] < iThreshHold
    ].sum()
    articlesGrouped[0] = "Others (" + str(othersArticlesNumber) + " articles)"
    oDataFrameGrouped = oDataFrameGrouped._append(articlesGrouped, ignore_index=True)

    return oDataFrameGrouped
