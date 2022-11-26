# Gilmore Girls Network 
<img width="994" alt="image" src="https://user-images.githubusercontent.com/79585810/204050458-c819b4e1-7b95-4399-be10-816f4fe3a737.png">

### Data Scraping
First, the list of all characters (that appeared in the show) was acquired from [Gilmore Girls fandom wiki](https://gilmoregirls.fandom.com) using Selenium-Webdriver. Then, also using Seleninum, the scripts from each episodes were scraped from [this website](https://transcripts.foreverdreaming.org/viewforum.php?f=22). The script dataset contains: 
- character
- line
- season

### Data cleaning and EDA 
Because the data didn't have any missing values, only small spelling mistakes (such as Loreai -> Lorelai) were manually corrected. Then using visualitaion tools (seaborn, matplotlib_ and NLP libraries (NLTK, re), the simple analysis of the Gilmore Girls script was conducted. For example, Lorelai Gilmore said the most lines in the whole show (almost 10k more than second place Rory Gilmore) while season 6 contained the highest number of characeters. Moreover, wordclouds for main characters were created.

### Creating Relationships Network
To create relationships network, it was important to divide lines into smaller scenes, to find out which characters interacted with each other. For the analysis purposes, the assumed number of lines in the scene was 5. Then, the interactions were counted. Only the interactions with characters from "characters" dataset were left. 
The network was created using NetworkX and the more visually pleasing graph was possible with Pyvis Network.

### Centrality 
There are multiple measures of centrality used in the network anlaysis. Four of them were tested and visually represented in this project:
- **Degree Centrality**: It's the first and the simplest way of decribing centrality. It's the number of edges (links) that are connected to each node. To achieve standarized scores, each score was divided by n-1 (where n = the number of nodes in the network) In the Gilmore Girls series, only the three characters (Lorelai, Rory, Luke) have significantly higher number of links, while the other characters stay at around the same level 

- **Betweenness Centrality**: This is the measure of how important the node is to the flow of information through a network. It's measured as the number of shortest paths (between any couple of nodes in the graphs) that pass through each node. For example, Zach or Sookie (who didn't appear in the degree centrality plot) turned out to be important characters who link others. 

- **Closeness Centrality**: Closeness centrality shows how close a node is to other nodes in the network. It is calculated as the average of the shortest path length from the node to every other node in the network. Basically, the more 'central' position of the node, the higher its score. This time, there is no significant difference between three main characters and the rest of them. The centrality score remains at the similiar level.

- **Eigenvector Centrality**: It's the most complex measure out of the above. It measure's the nodes importance while taking under consideration its neighbours' importance. That is why, for example Dean who scored lower in the terms of edges number, by his connection to the most important characters in the series, rised to the fourth place.


![centrality](https://user-images.githubusercontent.com/79585810/204105959-64b0e040-4607-4ba7-88b5-1a1ea09b2f59.jpg)

