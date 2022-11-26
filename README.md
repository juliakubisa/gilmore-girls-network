# Gilmore Girls Network 
<img width="994" alt="image" src="https://user-images.githubusercontent.com/79585810/204050458-c819b4e1-7b95-4399-be10-816f4fe3a737.png">

### Data Scraping 

### Data cleaning and EDA 

### Creating Relationships Network 

### Centrality 
There are multiple measures of centrality used in the network anlaysis. Four of them were tested and visually represented in this project:
- **Degree Centrality**: It's the first and the simplest way of decribing centrality. It's the number of edges (links) that are connected to each node. To achieve standarized scores, each score was divided by n-1 (where n = the number of nodes in the network) In the Gilmore Girls series, only the three characters (Lorelai, Rory, Luke) have significantly higher number of links, while the other characters stay at around the same level 

- **Betweenness Centrality**: This is the measure of how important the node is to the flow of information through a network. It's measured as the number of shortest paths (between any couple of nodes in the graphs) that pass through each node. For example, Zach or Sookie (who didn't appear in the degree centrality plot) turned out to be important characters who link others. 

- **Closeness Centrality**: Closeness centrality shows how close a node is to other nodes in the network. It is calculated as the average of the shortest path length from the node to every other node in the network. Basically, the more 'central' position of the node, the higher its score. This time, there is no significant difference between three main characters and the rest of them. The centrality score remains at the similiar level.

- **Eigenvector Centrality**: It's the most complex measure out of the above. It measure's the nodes importance while taking under consideration its neighbours' importance. That is why, for example Dean who scored lower in the terms of edges number, by his connection to the most important characters in the series, rised to the fourth place.


![centrality](https://user-images.githubusercontent.com/79585810/204105959-64b0e040-4607-4ba7-88b5-1a1ea09b2f59.jpg)

