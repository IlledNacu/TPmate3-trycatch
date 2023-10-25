import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

Data = pd.read_csv('Downloads/Titanic.csv')
nombre = "^" + input().capitalize() + ".*"
Data = Data[Data['Name'].str.match(nombre)==True]
print(Data)

fig, ax = plt.subplots(figsize =(12,12))

DG = nx.DiGraph()
for i in range(0, len(Data)):
    
    DG.add_edge(Data.iloc[i]['Name'], Data.iloc[i]['Sex'])
    i = i + 1 
genero = ["male", "female"]
nx.draw(DG, with_labels=True, node_color= ['red' if node in genero else 'lightblue' for node in DG.nodes()])
plt.show()

