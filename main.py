import sys
import os

currentDir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(currentDir + "/functions")

import figures
import manipulations
import intels
import graphes

## Variables de fichiers
FILE = "data/Bakery Sales.csv"
LARGE_CAT = "data/large categories.csv"
NORMAL_CAT = "data/normal categories.csv"

## Variables de chemin data
NORMAL_DATA = "data/normal group/"
LARGE_DATA = "data/large group/"

## Variables de chemin images
IMAGES = "images/"
LARGE_GROUP = "images/categories/large/"
NORMAL_GROUP = "images/categories/normal/"

## Variables
THRESHOLDS = [0, 0.5, 1, 2]

if __name__ == "__main__":
    ## Création de la dataframe principale
    dataFrame = manipulations.createDataFrame(FILE)
    # print(dataFrame)

    ## Création des dataframes de période
    dataFrame2021 = dataFrame[dataFrame["date"].dt.year == 2021]
    dataFrame2022 = dataFrame[dataFrame["date"].dt.year == 2022]

    ## Créations des différentes dataframes
    menu = manipulations.getItemsAndPrice(dataFrame)

    ## Création du fichier .csv pour récupérer tous les objets (utile pour Gephi)
    ## Remarque : à modifier à la main pour créer ses catégories
    # items = manipulations.getListItems(dataFrame)
    # items = pd.DataFrame(items)
    # items.to_csv("data/items.csv") # À décommenter si on veut (re)créer le fichier

    # transactions = manipulations.getTransactionsPerClient(dataFrame)
    itemsSold = manipulations.getTotalItemsSold(dataFrame)
    itemsSold2021 = manipulations.getTotalItemsSold(dataFrame2021)
    itemsSold2022 = manipulations.getTotalItemsSold(dataFrame2022)

    ## Création des dataframes selon le groupement des catégories
    largeGroupedDataFrame = manipulations.groupedCategories(dataFrame, LARGE_CAT)
    normalGroupedDataFrame = manipulations.groupedCategories(dataFrame, NORMAL_CAT)

    # ## Illustrations groupement
    # figures.compareAnnualeSalesCategories(
    #     [["normal", normalGroupedDataFrame], ["large", largeGroupedDataFrame]],
    #     1,
    #     "Grouped",
    #     IMAGES,
    # )
    # # getAnnualSales(normalGroupedDataFrame,[1],"Annual sales, grouped")
    # # createHistogram(normalGroupedDataFrame,"article","Quantity","Proportion of articles sold, grouped")

    # ## Illustrations période globale
    figures.getIllustrations(dataFrame, "Global", IMAGES)
    # figures.createHistogram(
    #     menu,
    #     "article",
    #     "unit_price",
    #     "Visual of articles and their prices",
    #     "Articles_Prices",
    #     IMAGES,
    # )
    # figures.createHistogram(
    #     itemsSold,
    #     "article",
    #     "Quantity",
    #     "Proportion of articles sold",
    #     "Quantity_Sold",
    #     IMAGES,
    # )
    # figures.getAnnualSales(dataFrame, [0], "", IMAGES)
    # figures.getAnnualSales(dataFrame, THRESHOLDS[1:], "", IMAGES)

    # ## Illustrations pour 2021
    # figures.getIllustrations(dataFrame2021, "2021", IMAGES)
    # figures.createHistogram(
    #     itemsSold2021,
    #     "article",
    #     "Quantity",
    #     "Proportion of articles sold in 2021",
    #     "Quantity_Sold_2021",
    #     IMAGES,
    # )
    # figures.getAnnualSales(dataFrame2021, [0], "2021", IMAGES)
    # figures.getAnnualSales(dataFrame2021, THRESHOLDS[1:], "2021", IMAGES)

    # ## Illustrations pour 2022
    # figures.getIllustrations(dataFrame2022, "2022", IMAGES)
    # figures.createHistogram(
    #     itemsSold2022,
    #     "article",
    #     "Quantity",
    #     "Proportion of articles sold in 2022",
    #     "Quantity_Sold_2022",
    #     IMAGES,
    # )
    # figures.getAnnualSales(dataFrame2022, [0], "2022", IMAGES)
    # figures.getAnnualSales(dataFrame2022, THRESHOLDS[1:], "2022", IMAGES)

    # ## Création des fichiers nodes et edges
    # graphes.createNodesEdges(dataFrame, "data/global/")

    ## Création des dataframes selon les catégories
    # largeGroupedDataFrame = manipulations.changeReference(dataFrame, LARGE_CAT)
    # normalGroupedDataFrame = manipulations.changeReference(dataFrame, NORMAL_CAT)

    ## Génération des diagrammes circulaires et fichiers nodes et edges pour chaque catégorie et groupement
    # figures.getAnnualSales(normalGroupedDataFrame,[0],"",NORMAL_GROUP)
    # figures.getAnnualSales(largeGroupedDataFrame,[0],"",LARGE_GROUP)

    # graphes.createNodesEdges(normalGroupedDataFrame,NORMAL_DATA)
    # graphes.createNodesEdges(largeGroupedDataFrame,LARGE_DATA)

    # pageRankList = intels.pageRankScore(dataFrame,"BAGUETTE")
    # pageRankList = intels.pageRankScore(normalGroupedDataFrame,"BAGUETTE")
    # pageRankList = intels.pageRankScore(largeGroupedDataFrame,"BAGUETTE")
    # graphes.graphe(dataFrame)

    # figures.getAnnualSales(normalGroupedDataFrame, THRESHOLDS[1:], "", NORMAL_GROUP)
    # figures.getAnnualSales(normalGroupedDataFrame, [0.5], "0,5", NORMAL_GROUP)

    normalGroupedThresholdDataFrame = manipulations.groupWithTreshold(
        normalGroupedDataFrame, 0.5
    )
    normalGroupedThresholdDataFrameAS = manipulations.calculateProportions(
        normalGroupedThresholdDataFrame
    )
    # normalGroupedThresholdDataFrameAS = normalGroupedThresholdDataFrameAS.sort_values(
    #     by="proportion of annual sales", ascending=False
    # ).reset_index()
    # listNormal = list(normalGroupedThresholdDataFrameAS["article"])
    # print(listNormal)
    # for i in range(len(listNormal)):
    #     print(str(listNormal[i]))
    #     pageRankList = intels.pageRankScore(
    #         normalGroupedThresholdDataFrame, str(listNormal[i])
    #     )
    #     print("\n")

    ## Illustration Powerpoint
    intels.pageRankDataFrame(normalGroupedThresholdDataFrame,"BOISSON").to_csv("data/BOISSON.csv")
    intels.pageRankDataFrame(normalGroupedThresholdDataFrame,"CROISSANT").to_csv("data/CROISSANT.csv")
    intels.pageRankDataFrame(normalGroupedThresholdDataFrame,"ECLAIR").to_csv("data/ECLAIR.csv")
    
