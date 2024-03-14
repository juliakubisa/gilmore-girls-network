# Gilmore Girls Network 
<img width="1435" alt="Zrzut ekranu 2024-03-14 o 10 59 19" src="https://github.com/juliakubisa/gilmore-girls-network/assets/79585810/69ee178f-b25d-4a77-b043-45e4a4df21bf">

### Data Scraping
First, the list of all characters was acquired from [Gilmore Girls fandom wiki](https://gilmoregirls.fandom.com) using Selenium-Webdriver. Then, also using Seleninum, the scripts from each episodes were scraped from [this website](https://transcripts.foreverdreaming.org/viewforum.php?f=22). The script dataset contains: 
- character
- line
- season

### Data cleaning and EDA 
Because the data didn't have any missing values, only small spelling mistakes (such as Loreai -> Lorelai) were manually corrected. Then using visualitaion tools (seaborn, matplotlib and NLP libraries (NLTK, re), the simple analysis of the Gilmore Girls script was conducted and placed into a dashboard. Moreover, a wordcloud was created. 

### Relationships Network
<img width="994" alt="image" src="https://user-images.githubusercontent.com/79585810/204050458-c819b4e1-7b95-4399-be10-816f4fe3a737.png">
The network was created using NetworkX and the more visually pleasing graph was possible with Pyvis Network.

### Centrality 
There are multiple measures of centrality used in the network anlaysis. Four of them were tested and visually represented in this project:
- **Degree Centrality**:
- **Betweenness Centrality**: 
- **Closeness Centrality**: 
- **Eigenvector Centrality**:
- 
![centrality](https://user-images.githubusercontent.com/79585810/204105959-64b0e040-4607-4ba7-88b5-1a1ea09b2f59.jpg)

