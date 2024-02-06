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

def getListTickets(iDataFrame):
    oTickets = iDataFrame.ticket_number.unique()
    oTickets.sort()

    return oTickets


def getTransactionsPerClient(iDataFrame):
    oDataFrameTransactions = iDataFrame.groupby("ticket_number").sum("total")

    return oDataFrameTransactions


def groupedCategories(iDataFrame, iRefFile):
    dataFrameRef = pd.read_csv(iRefFile)
    del dataFrameRef["Unnamed: 0"]

    dataFrame = iDataFrame

    oDataFrame = pd.merge(dataFrame, dataFrameRef, on="article")
    oDataFrame["article"] = oDataFrame.apply(lambda row: row["article"] if pd.isnull(row["categorie"]) else row["categorie"],axis=1)
    del oDataFrame["categorie"]

    return oDataFrame

def changeReference(iDataFrame,iRefFile):
    dataFrameRef = pd.read_csv(iRefFile)
    del dataFrameRef["Unnamed: 0"]

    dataFrame = iDataFrame

    oDataFrame = pd.merge(dataFrame, dataFrameRef, on="article")
    oDataFrame["categorie"] = oDataFrame.apply(lambda row: row["article"] if pd.isnull(row["categorie"]) else row["categorie"],axis=1)
    del oDataFrame["article"]
    oDataFrame = oDataFrame.rename(columns={"categorie": "article"})
    oDataFrame["article"] = oDataFrame["article"].astype("str")

    return oDataFrame


def calculateProportions(iDataFrame):
    oDataFrame = iDataFrame

    totalAnnualSales = sum(oDataFrame["total"])
    oDataFrame = oDataFrame.groupby("article", as_index=False).sum("total")
    oDataFrame["proportion of annual sales"] = (
        oDataFrame["total"] / totalAnnualSales * 100
    )

    return oDataFrame

def groupWithTreshold(iDataFrame,iThreshHold):
    oDataFrame = iDataFrame
    dataFrameRef = calculateProportions(iDataFrame)
    dataFrameGrouped, otherLabel = groupedArticles(dataFrameRef,iThreshHold)
    list = getListItems(dataFrameGrouped)
    oDataFrame["article"] = oDataFrame.apply(lambda row: row["article"] if row["article"] in list else otherLabel,axis=1)

    return(oDataFrame)

def groupedArticles(iDataFrame, iThreshHold):
    dataFrame = iDataFrame

    oDataFrameGrouped = dataFrame[
        dataFrame["proportion of annual sales"] >= iThreshHold
    ]
    othersArticlesNumber = len(
        dataFrame[dataFrame["proportion of annual sales"] < iThreshHold].index
    )
    if(othersArticlesNumber > 0):
        articlesGrouped = dataFrame[
            dataFrame["proportion of annual sales"] < iThreshHold
        ].sum()
        oOthers = "Others (" + str(othersArticlesNumber) + " articles)"
        articlesGrouped[0] = "Others (" + str(othersArticlesNumber) + " articles)"
        oDataFrameGrouped = oDataFrameGrouped._append(articlesGrouped, ignore_index=True)
        return (oDataFrameGrouped,oOthers)
    else:
        return(dataFrame,"")

def createArticlesNodesFile(iListArticles,iStorageFile="data/"):
    dataFrame = pd.DataFrame({"id":iListArticles,"label":iListArticles})
    fileName = iStorageFile+"articles-nodes.csv"

    dataFrame.to_csv(fileName,sep='\t', index=False)

def createTicketsNodesFile(iListTickets,iStorageFile="data/"):
    dataFrame = pd.DataFrame({"id":iListTickets,"label":iListTickets})
    fileName = iStorageFile+"tickets-nodes.csv"

    dataFrame.to_csv(fileName,sep='\t', index=False)
    
def createEdgesFile(iDataFrame,iStorageFile="data/"):
    dataFrame = iDataFrame[["ticket_number","article","Quantity"]]
    filename = iStorageFile+"edges.csv"

    dataFrame = dataFrame.rename(columns={"ticket_number": "Target"})
    dataFrame = dataFrame.rename(columns={"article": "Source"})
    dataFrame = dataFrame.rename(columns={"Quantity": "Weight"})

    dataFrame.to_csv(filename,sep='\t', index=False)
