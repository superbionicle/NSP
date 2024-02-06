import networkx as nx
import matplotlib.pyplot as plt
import igraph as ig
import itertools
import sys
import os

currentDir = os.path.dirname(os.path.abspath(__file__))

import manipulations

def createNodesEdges(iDataFrame,iStorageFile):
    # TODO: tester si iStorageFile est bien un nom de dossier et tester si le dossier existe

    items = manipulations.getListItems(iDataFrame)
    tickets = manipulations.getListTickets(iDataFrame)

    manipulations.createArticlesNodesFile(items,iStorageFile)
    manipulations.createTicketsNodesFile(tickets,iStorageFile)
    manipulations.createEdgesFile(iDataFrame,iStorageFile)