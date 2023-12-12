# Data reading
import pandas as pd
import numpy as np

# Visualization
import matplotlib.pyplot as plt

# NLP
# from nltk.corpus import stopwords
import nltk
from wordcloud import WordCloud
import re
import collections

# Network
import networkx as nx
from pyvis.network import Network
import community.community_louvain as cl

# Import stopwords
nltk.download('stopwords')
stop_words = nltk.corpus.stopwords.words('english')
stop_words.extend(["uh", "oh", "okay", "im", "dont", "know", "yeah", "thats", "youre", "well", "what", "ok", "isnt", "dont",
                  "yes", "no", "theres", "cant", "didnt", "whats"])


def compute_basic_analytics(script, characters):
    total_seasons = int(script['Season'].max())
    total_episodes = int(characters['num_episodes'].max())
    total_characters = int(characters['name'].count())
    total_lines = int(script['Line'].count())
    return total_episodes, total_characters, total_lines, total_seasons


def count_lines_by_character(script):
    char_lines = (script.groupby(['Character'], as_index=False)['Line']
                  .count().sort_values(['Line'], ascending=False))
    char_lines['Percent'] = char_lines['Line'] / char_lines['Line'].sum()
    return char_lines


def num_characters_per_season(script):
    seasons_char = (script.groupby(['Season'], as_index=False)['Character']
                    .nunique().sort_values('Character', ascending=False))
    return seasons_char


def num_lines_per_season(script):
    count_lines = (script.groupby(['Season'], as_index=False)['Line']
                   .count().sort_values('Line', ascending=True))
    return count_lines


def extract_character_lines(character_name, script):
    character_lines = script[script['Character'] == character_name].reset_index(drop=True)
    character_lines = character_lines['Line']
    return character_lines


def clean_data(character_lines):
    data = " ".join(character_lines)  # Join the text
    data = re.sub(r'[^\w\s]', '', data)  # Delete unwanted characters
    tokens = data.split()
    tokens = [word.lower() for word in tokens]  # Lower all the letters
    tokens = [word for word in tokens if not word in stop_words]  # Ignore stopwords
    text = " ".join(tokens)  # Create one joined sentence
    return text


def word_count(text):
    # Create an empty dictionary named 'counts' to store word frequencies.
    counts = dict()

    # Split the input string 'str' into a list of words using spaces as separators and store it in the 'words' list.
    words = text.split()

    # Iterate through each word in the 'words' list.
    for word in words:
        # Check if the word is already in the 'counts' dictionary.
        if word in counts:
            # If the word is already in the dictionary, increment its frequency by 1.
            counts[word] += 1
        else:
            # If the word is not in the dictionary, add it to the dictionary with a frequency of 1.
            counts[word] = 1
    # Return the 'counts' dictionary, which contains word frequencies.
    return counts


def generate_wordcloud(text):
    word_cloud = WordCloud(width=1920, height=1080, background_color="white",
                           colormap='tab20b', collocations=False).generate(text)
    return word_cloud


def prepare_network_data(script, characters):
    input = 23338
    output = list(range(input + 1))
    scenes = list(np.repeat(output, 5))
    script = script[7:]
    script['Scene'] = scenes[5:]  # Add number of a scene to column

    char_dict = {}
    for group, group_df in script.groupby(['Scene']):  # Group by scenes of 5

        # Get the list of characters that appear in scene, sorted alphabetically
        char_in_scene = str(group_df['Character'].sort_values().unique().tolist())[1:-1].replace("'", "")

        # Add to dictionary
        if char_in_scene in char_dict.keys():
            char_dict[char_in_scene] += 1
        else:
            char_dict[char_in_scene] = 1

    # Sort the dictionary by count (second item)
    sorted_char_list = sorted(char_dict.items(), key=lambda item: item[1], reverse=True)
    sorted_dict = {}
    for k, v in sorted_char_list:
        sorted_dict[k] = v

    # Get the relations of 2 characters from the character's list
    relations = []
    for x in characters['name']:
        for y in characters['name']:
            if x != y and x < y:  # Alphabetically
                relations.append(x + ', ' + y)

    # Add to dictionary only the elements that appear in relations list
    rel_dict = {}
    for x in relations:
        if x in sorted_dict.keys():
            rel_dict[x] = sorted_dict[x]

    # List sorted by count
    sorted_rel = sorted(rel_dict.items(), key=lambda item: item[1], reverse=True)

    # Create a dataframe
    network_df = pd.DataFrame(sorted_rel, columns=['Source', 'Count'])
    network_df[['Source', 'Target']] = network_df['Source'].str.split(',', expand=True)

    # Delete rows with less than 2 scenes in the show
    network_df['Count'] = network_df[network_df['Count'] > 2]['Count']
    network_df = network_df.dropna()
    network_df['Count'] = network_df['Count'].astype(int)

    # Change columns position
    network_df = network_df.loc[:, ['Source', 'Target', 'Count']]
    return network_df


def build_network(network_df):
    # Edges
    network_df.columns = ['Source', 'Target', 'Count']
    network_df['Source'] = network_df['Source'].str.replace(' ', '')  # Delete accidental spaces
    network_df['Target'] = network_df['Target'].str.replace(' ', '')

    # Create a graph from a pandas dataframe
    G = nx.from_pandas_edgelist(network_df,
                                source="Source",
                                target="Target",
                                edge_attr="Count",
                                create_using=nx.Graph())
    communities = cl.best_partition(G)
    # node_degree = nx.betweenness_centrality(G)
    node_degree = dict(G.degree)

    # Set attribute by the community
    nx.set_node_attributes(G, communities, 'group')

    # Set attribute by the number of interactions
    nx.set_node_attributes(G, node_degree, 'size')

    # Create a graph
    net = Network(notebook=False, width="1000px", height="900px", bgcolor='white', font_color='black')
    net.from_nx(G)
    net.save_graph('GilmoreGirlsNetwork.html')
    HtmlFile = open('GilmoreGirlsNetwork.html', 'r', encoding='utf-8').read()
    HtmlFile = HtmlFile.replace('border: 1px solid lightgray;', '')
    return G, HtmlFile


def centralities_charts(G):
    # Degree centrality
    degree_dict = nx.degree_centrality(G)
    degree_df = (pd.DataFrame(degree_dict.items(), columns=['name', 'centrality'])
                 .sort_values(['centrality'], ascending=False))

    # Betweenness centrality
    beetweenness_dict = nx.betweenness_centrality(G)
    beetweenness_df = (pd.DataFrame(beetweenness_dict.items(), columns=['name', 'centrality'])
                       .sort_values(['centrality'], ascending=False))

    # Closeness centrality
    closeness_dict = nx.closeness_centrality(G)
    closeness_df = (pd.DataFrame(closeness_dict.items(), columns=['name', 'centrality'])
                    .sort_values(['centrality'], ascending=False))

    # Eigenvector centrality
    eigenvector_dict = nx.eigenvector_centrality(G)
    eigenvector_df = (pd.DataFrame(eigenvector_dict.items(), columns=['name', 'centrality'])
                      .sort_values(['centrality'], ascending=False))
    return degree_df, beetweenness_df, closeness_df, eigenvector_df
