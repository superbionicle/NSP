import sys
import os
import numpy as np
import pandas as pd

currentDir = os.path.dirname(os.path.abspath(__file__))

import manipulations


def getNerdStats(iDataFrame):
    dataFrame = manipulations.getTransactionsPerClient(iDataFrame)

    oMean = dataFrame["total"].mean()
    oMedian = dataFrame["total"].median()
    oStandardDeviation = dataFrame["total"].std()

    print("Mean by client :", oMean)
    print("Median by client :", oMedian)
    print("Standard deviation by client :", oStandardDeviation)

    return [oMean, oMedian, oStandardDeviation]


def getQuantity(iRow, iArticleReference):
    index = iRow["article"].index(iArticleReference) if iArticleReference in iRow["article"] else -1

    if index != -1:
        return iRow["Quantity"][index]
    else:
        return 0


def pageRankDataFrame(iDataFrame, iArticleReference):
    articles = iDataFrame.article.unique()
    if not (iArticleReference in articles):
        return False

    dataFrame = iDataFrame[["ticket_number", "article", "Quantity"]]
    dataFrame = (
        dataFrame.groupby("ticket_number")
        .agg({"article": list, "Quantity": list})
        .reset_index()
    )
    dataFrame = dataFrame[
        dataFrame["article"].apply(lambda article: iArticleReference in article)
    ]
    # print(dataFrame)

    index = np.where(articles == iArticleReference)[0][0]
    articles = np.delete(articles, index)

    onlyArticlePresence = (
        dataFrame["article"].apply(lambda article: article == [iArticleReference]).sum()
    )
    onlyArticle = dataFrame[
        dataFrame["article"].apply(lambda article: article == [iArticleReference])
    ]
    onlyArticleQuantities = sum(onlyArticle["Quantity"].sum())
    presence = [onlyArticlePresence]
    quantityInPresence = [onlyArticleQuantities]

    for item in articles:
        numberOfTransactions = (
            dataFrame["article"].apply(lambda article: item in article).sum()
        )
        presence.append(numberOfTransactions)
        tempDataFrame = dataFrame[
            dataFrame["article"].apply(lambda article: item in article)
        ]
        tempQuantity = tempDataFrame.apply(lambda row: getQuantity(row, item), axis=1)
        if tempQuantity.empty:
            quantityPerArticle = 0
        else:
            tempDataFrameQuantity = pd.Series.to_frame(tempQuantity, name="quantity")
            quantityPerArticle = tempDataFrameQuantity["quantity"].sum()
        quantityInPresence.append(quantityPerArticle)

    articles = np.insert(articles, 0, iArticleReference)
    oDataFrame = pd.DataFrame(
        {"article": articles, "presence": presence, "quantity": quantityInPresence}
    )

    oDataFrame["average bought"] = oDataFrame["quantity"]/oDataFrame["presence"]
    oDataFrame["mult"] = oDataFrame["average bought"]*oDataFrame["presence"]
    totalAverage = oDataFrame["mult"].sum()
    totalPresence = oDataFrame["presence"].sum()

    oDataFrame["weighted"] = oDataFrame["mult"]/totalAverage
    oDataFrame["not weighted"] = oDataFrame["presence"]/totalPresence
    del oDataFrame["mult"]

    oDataFrame = oDataFrame[oDataFrame["presence"] > 0]
    oDataFrame = oDataFrame[oDataFrame["quantity"] > 0]
    return oDataFrame


def pageRankScore(iDataFrame, iArticleReference):
    dataFrame = pageRankDataFrame(iDataFrame, iArticleReference)
    # print(dataFrame)
    # print(dataFrame.sort_values(by=["presence"], ascending=False))
    # print(dataFrame.sort_values(by=["quantity"], ascending=False))
    print(dataFrame[["article","weighted"]].sort_values(by=["weighted"], ascending=False))
    # print("\n")
    # print(dataFrame.sort_values(by=["not weighted"], ascending=False))
    # print("\n")
