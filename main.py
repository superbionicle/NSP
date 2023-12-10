import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import os

currentDir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(currentDir + "/functions")

import figures
import manipulations
import intels

FILE = "data/Bakery Sales.csv"
LARGE_CAT = "data/categories larges.csv"
NORMAL_CAT = "data/categories normales.csv"

if __name__ == "__main__":
    dataFrame = manipulations.createDataFrame(FILE)
    # print(dataFrame)

    # Création des dataframes de période
    dataFrame2021 = dataFrame[dataFrame["date"].dt.year == 2021]
    # dataFrame2022 = dataFrame[dataFrame["date"].dt.year == 2022]

    # Créations des différentes dataframes
    # menu = manipulations.getItemsAndPrice(dataFrame)
    # items = manipulations.getListItems(dataFrame)
    # items = pd.DataFrame(items)
    # # items.to_csv("data/items.csv") # À décommenter si on veut (re)créer le fichier
    # transactions = manipulations.getTransactionsPerClient(dataFrame)
    # itemsSold = manipulations.getTotalItemsSold(dataFrame)
    # itemsSold2021 = manipulations.getTotalItemsSold(dataFrame2021)
    # itemsSold2022 = manipulations.getTotalItemsSold(dataFrame2022)

    largeGroupedDataFrame = manipulations.groupedCategories(dataFrame, LARGE_CAT)
    normalGroupedDataFrame = manipulations.groupedCategories(dataFrame, NORMAL_CAT)
    # figures.compareAnnualeSalesCategories([normalGroupedDataFrame,largeGroupedDataFrame],1,"Grouped categorized",True)

    # getAnnualSales(normalGroupedDataFrame,[1],"Annual sales, grouped")
    # createHistogram(normalGroupedDataFrame,"article","Quantity","Proportion of articles sold, grouped")

    ## Illustrations période globale
    # createHistogram(menu,"article","unit_price","Visual of articles and their prices")
    # createHistogram(itemsSold,"article","Quantity","Proportion of articles sold")
    # createHistogramByHoursOfDay(dataFrame,"Items sold, by hours of day")
    # createHistogramByDayWeek(dataFrame,"Items sold, by days of the week")
    # figures.createHistogramByMonth(dataFrame"Items sold, by months of the year")
    # getAnnualSales(dataFrame2021,0,"Annual sales")
    # getAnnualSales(dataFrame2021,[0.5,1,2],"Annual sales in 2021 with thresholds")
    figures.getIllustrations(dataFrame2021,"in 2021",[0],True)

    ## Illustrations pour 2021
    # figures.createHistogramByHoursOfDay(dataFrame2021,"Items sold in 2021, by hours of day")
    # figures.createHistogramByDayWeek(dataFrame2021,"Items sold in 2021, by days of the week")
    # figures.createHistogramByMonth(
    #     dataFrame2021, "Items sold in 2021, by months of the year"
    # )
    # figures. createHistogram(itemsSold2021,"article","Quantity","Proportion of articles sold in 2021")
    # figures.getAnnualSales(dataFrame2021,[0],"Annual sales in 2021")
    # figures.getAnnualSales(dataFrame2021,[0.5,1,2],"Annual sales in 2021 with thresholds")

    ## Illustrations pour 2022
    # createHistogramByHoursOfDay(dataFrame2022,"Items sold in 2022, by hours of day")
    # createHistogramByDayWeek(dataFrame2022,"Items sold in 2022, by days of the week")
    # figures.createHistogramByMonth(
    #     dataFrame2022, "Items sold in 2022, by months of the year"
    # )
    # createHistogram(itemsSold2022,"article","Quantity","Proportion of articles sold in 2022")
    # getAnnualSales(dataFrame2022,0,"Annual sales in 2022")
    # getAnnualSales(dataFrame2022,[0.5,1,2],"Annual sales in 2022 with thresholds")

    # print("items",len(items))
    # print("transaction",len(transactions))
    # print("itemsSold",len(itemsSold.index))
    # getAnnualSales(dataFrame2021,1)
    # getAnnualSales(dataFrame2021,2)
    # print("general")
    # getNerdStats(dataFrame)
    # print("2021")
    # getNerdStats(dataFrame2021)
    # print("2022")
    # getNerdStats(dataFrame2022)
