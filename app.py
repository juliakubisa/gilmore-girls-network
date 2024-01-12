import streamlit as st
import charts_data
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
st.set_page_config(page_title="Gilmore Girls Dasboard", layout="wide")


# Load datasets
characters = pd.read_csv("data/characters_info.csv", sep='\t')  # List of characters
script = pd.read_csv("data/Gilmore_Girls_Lines.csv", sep=',', index_col=0)



def home():
    # Add title
    st.title('Gilmore Girls script analysis')
    st.caption("The main goal of this project is to analyze the various aspects of Gilmore Girls TV Show, such as characters distribution, their relationships or most common words. ")
    st.caption("The dataset contains every line that was spoken over 7 seasons, and was acquired by scraping"
               " https://transcripts.foreverdreaming.org. The second used dataset was scraped from https://gilmoregirls.fandom.com/wiki"
               "and contains the information about each character (full name, number of episodes, actor)")
    # Add general stats
    tot1, tot2, tot3, tot4 = st.columns(4)
    total_episodes, total_characters, total_lines, total_seasons = (
        charts_data.compute_basic_analytics(script, characters))

    with tot1:
        st.metric(label='# Seasons', value=f"{total_seasons}")
    with tot2:
        st.metric(label='# Episodes', value=f"{total_episodes}")
    with tot3:
        st.metric(label='# Characters', value=f"{total_characters}")
    with tot4:
        st.metric(label='# Lines', value=f"{total_lines}")

    # Add bottom charts
    st.divider()
    bar1, pie1 = st.columns(2)
    with bar1:
        tab1, tab2 = st.tabs(["Lines per season", "Characters per season"])
        with tab1:
            count_lines = charts_data.num_lines_per_season(script)
            barplot1 = px.bar(count_lines, x='Season', y='Line',
                              color_discrete_sequence=['#8d91ba'])
            st.plotly_chart(barplot1, theme="streamlit", use_container_width=True)
            with st.expander("See explanation"):
                st.write(r"""To provide an overview of line and character distribution, bar charts were generated. This barchart
                            illustrates character distribution across seasons, indicating a increase until a peak in season 6,
                            followed by a decline in season 7. It seems reasonable, as at the beginning the viewers get to know
                            the most important characters and while the story progresses, more and more characters appear""")

        with tab2:
            seasons_char = charts_data.num_characters_per_season(script)
            barplot2 = px.bar(seasons_char, x='Season', y='Character', color_discrete_sequence=['#8d91ba'])
            st.plotly_chart(barplot2, theme="streamlit", use_container_width=True)
            with st.expander("See explanation"):
                st.write(r"""This barchart displays line distribution by season, revealing relative consistency across 
seasons, although the last three seasons have a slight decrease compared to seasons 2-4.""")

    with pie1:
        st.write('Percent of lines spoken by characters')
        lines_by_char = charts_data.count_lines_by_character(script)
        pieplot1 = px.pie(lines_by_char[:15], values='Percent',
                          names='Character', color_discrete_sequence=
                          ['#8d91ba', '#BAB888', '#82815f', '#BAA388', '#fff9ee', '#b488ba', '#82775f'])
        st.plotly_chart(pieplot1, theme="streamlit", use_container_width=True)
        st.write("")
        with st.expander("See explanation"):
            st.write(r"""The characters distribution in the show can be shown by counting the lines spoken the character. 
                    Here, over 1/3 of all lines was said by Lorelai Gilmore, one of the titular main characters. 
                    It’s due to her principal role and also to her tendency to speak a lot. The second titular character, her daughter Rory Gilmore said 24% of all lines. The third titular character: Emily Gilmore contributes to 6.71% of lines, which is 
                    however less than Luke (with 9.95%), the only male among the top 5 characters with most lines.""")
            st.write(r"""Other principal characters contribute between 1% and 4% of lines.""")

    violin1, scatter1 = st.columns(2)
    with violin1:
        st.write('Distribution of characters number of episodes')
        episode_distr = characters.loc[characters['num_episodes'] >= 5]
        violinplot1 = px.violin(episode_distr, y="num_episodes", box=True,
                                points='all', color_discrete_sequence=['#82815f']).update_layout(yaxis_title='Episodes')
        st.plotly_chart(violinplot1, theme="streamlit", use_container_width=True)
        with st.expander("See explanation"):
            st.write(r"""A violin chart 
                    illustrates the distribution of the number of episodes each character has participated in. With the 
                    maximum number of episodes being 158, the median is 15. The minimum is 5, because only the 
                    characters that are credited have been chosen, Notably, the inclusion of one-episode cameos would 
                    result in lower median and minimum episode counts.""")
            st.write(r"""The density of 
                    characters total episodes varies. For example, there are several characters that appeared in 5-22 
                    episodes, followed by a more densely populated “cluster” appearing in 34-57 episodes. There is a
                    break, and the next set of characters featured in 103-121 episodes. The final group of characters 
                    appeared in 149-158 episodes. This observation makes clear the distinction between main, primary, 
                    secondary """)

    with scatter1:
        st.write('Correlation between number of episodes and number of said lines')
        script['Line_Length'] = script['Line'].str.len()
        episodes_and_num_lines = pd.merge(lines_by_char, characters, left_on='Character', right_on='name')
        scatterplot1 = px.scatter(episodes_and_num_lines[
                              (episodes_and_num_lines['Line'] > 100) & (episodes_and_num_lines['num_episodes'] > 1)],
                          y='Line', x="num_episodes", color_discrete_sequence=['#BAA388']).update_layout(xaxis_title='Episodes')
        st.plotly_chart(scatterplot1, theme="streamlit", use_container_width=True)
        with st.expander("See explanation"):
            st.write(r"""The scatterplot has been created to verify whether the number of episodes the characters appeared 
            on corresponds strictly to their number of lines.
            As expected, with the increase of episodes, the number of lines rises too, although this correlation 
            resembles more a logarithmic function than linear one. For the characters with fewer than 50 
            episodes, the lines count remains relatively flat before increasing more sharply. 
            The values for characters that appeared in approximately 150 episodes include one outlier, one 
            character that despite appearing in all episodes, spoke on average equally to characters that 
            appeared in 1/3 of episodes. This character serves as a comic relief in the series, on average getting 
            one or two scenes in each episodes, that are considered funny or silly.""")

    st.write('Distribution of average length of lines per season')
    avg_line = (script[script['Line_Length'] < 300].groupby(['Character', 'Season'])
                .agg({'Line_Length': 'mean'}).reset_index())
    boxplot1 = (px.box(avg_line, x='Season', y="Line_Length",
                      color_discrete_sequence=['#b488ba'])
                .update_layout(yaxis_title='Average Line Length'))
    st.plotly_chart(boxplot1, theme="streamlit", use_container_width=True)
    with st.expander("See explanation"):
        st.write(r"""This set of boxplots has was created to check if over the 
            seasons the characteristics of characters’ speeches has changed. 
            There aren’t significant changes in the median and IQR for each season. The highest 
            median of average line length appeared in season 7 (47) and the lowest in the season 1 (37). The 
            season first in general features a lower maximum than the rest and the shortest whiskers – indicating
            more concise way of speaking of the characters.
            In each season there are some outliers which suggest that some character spoke on average much 
            more than others or were given monologues, which increased significantly their average words
            spoken per line. The peak appeared in season 6, when one character averaged 253 words per line.""")


def network():
    st.title('Relationships network in Gilmore Girls')
    network_df = charts_data.prepare_network_data(script, characters)
    G, HtmlFile = charts_data.build_network(network_df)
    components.html(HtmlFile, width=1000, height=800)
    with st.expander("See explanation"):
        st.write(r"""The interactive network has been done to illustrate the relationship between characters across the
                seasons. To do it, the script was divided into small scenes, each containing 5 lines and then the 
                interactions between characters was counted.
                """)
        st.write(r"""As shown below, the different groups of characters were color-coded, for example yellow 
                concentrates on Rory, a highschooler who mostly interacts with her classmates and peers. The size of 
                node in each character depends on the number of different interactions they had – notably the main
                characters such as Lorelai, Rory or Luke have the largest nodes.""")
    st.divider()
    st.header('Centralities')
    degree_df, beetweenness_df, closeness_df, eigenvector_df = charts_data.centralities_charts(G)
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    with col1:
        st.write('Degree centrality')
        barplot3 = px.bar(degree_df[:10], x='name', y='centrality',
                          color_discrete_sequence=['#8d91ba'])
        st.plotly_chart(barplot3, theme="streamlit", use_container_width=True)
        with st.expander("See explanation"):
            st.write(r"""The simplest way of decribing centrality. It's the number of edges (links) 
            that are connected to each node. To achieve standarized scores, each score was divided by n-1 (where n = the number of nodes in the network) In the Gilmore Girls series, only the three 
            characters (Lorelai, Rory, Luke) have significantly higher number of links, while the other 
            characters stay at around the same level.""")
    with col2:
        st.write('Beetweenness centrality')
        barplot4 = px.bar(beetweenness_df[:10], x='name', y='centrality',
                          color_discrete_sequence=['#8d91ba'])
        st.plotly_chart(barplot4, theme="streamlit", use_container_width=True)
        with st.expander("See explanation"):
            st.write(r"""This is the measure of how important the node is to the flow of 
            information through a network. It's measured as the number of shortest paths (between any 
            couple of nodes in the graphs) that pass through each node. For example, Zach or Sookie 
            (who didn't appear in the degree centrality plot) turned out to be important characters who 
            link others.""")
    with col3:
        st.write('Closeness centrality')
        barplot5 = px.bar(closeness_df[:10], x='name', y='centrality',
                          color_discrete_sequence=['#8d91ba'])
        st.plotly_chart(barplot5, theme="streamlit", use_container_width=True)
        with st.expander("See explanation"):
            st.write(r"""It shows how close a node is to other nodes in the network. It is 
            calculated as the average of the shortest path length from the node to every other node in 
            the network. Basically, the more 'central' position of the node, the higher its score. This time, 
            there is no significant difference between three main characters and the rest of them. The 
            centrality score remains at the similiar level.""")

    with col4:
        st.write('Eigenvector centrality')
        barplot6 = px.bar(eigenvector_df[:10], x='name', y='centrality',
                          color_discrete_sequence=['#8d91ba'])
        st.plotly_chart(barplot6, theme="streamlit", use_container_width=True)
        with st.expander("See explanation"):
            st.write(r"""It measures the 
            nodes importance while taking under consideration its neighbours' importance. That is why, 
            for example Dean who scored lower in the terms of edges number, by his connection to the 
            most important characters in the series, rised to the fourth place""")


def wordcloud():
    st.title('Wordcloud of the most used words')
    character_name = st.selectbox('select a character', ['Lorelai', 'Rory', 'Emily', 'Lane', 'Sookie'])
    st.divider()

    lines = charts_data.extract_character_lines(character_name, script)
    text = charts_data.clean_data(lines)
    word_cloud = charts_data.generate_wordcloud(text)
    fig, ax = plt.subplots(figsize=(12, 12))
    ax.imshow(word_cloud)
    plt.axis("off")
    st.pyplot(fig)
    with st.expander("See explanation"):
        st.write(r"""Wordcloud was generated as a simple tool to see what were the words that characters frequently
used. It excludes contextually irrelevant words (eg. me, you, yes, no). The simple analysis reveals that 
for each character, their most used words icnlude the names of their close family or significant ones. 
For instance, Emily’s favourite words (as shown below) are “Rory”, “Lorelai” and “Richard”. For Lorelai
however, the most used words (apart from “go”, “good” and “hey”) are “Rory”, “Luke”, “mom”""")


# Add sidebar
def sidebar():
    with st.sidebar:
        selected = option_menu(
            menu_title="Menu",
            options=["Home", "Network", 'Wordcloud'],
            icons=["house", "diagram-2", "cloud"],
            menu_icon="cast",
            default_index=0
        )
    if selected == "Home":
        home()
    if selected == "Network":
        network()
    if selected == "Wordcloud":
        wordcloud()


sidebar()
