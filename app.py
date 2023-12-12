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
        with tab2:
            seasons_char = charts_data.num_characters_per_season(script)
            barplot2 = px.bar(seasons_char, x='Season', y='Character', color_discrete_sequence=['#8d91ba'])
            st.plotly_chart(barplot2, theme="streamlit", use_container_width=True)
    with pie1:
        st.write('Percent of lines spoken by characters')
        lines_by_char = charts_data.count_lines_by_character(script)
        pieplot1 = px.pie(lines_by_char[:15], values='Percent',
                          names='Character', color_discrete_sequence=
                          ['#8d91ba', '#BAB888', '#82815f', '#BAA388', '#fff9ee', '#b488ba', '#82775f'])
        st.plotly_chart(pieplot1, theme="streamlit", use_container_width=True)

    violin1, scatter1 = st.columns(2)
    with violin1:
        st.write('Distribution of characters number of episodes')
        episode_distr = characters.loc[characters['num_episodes'] >= 5]
        violinplot1 = px.violin(episode_distr, y="num_episodes", box=True,
                                points='all', color_discrete_sequence=['#82815f']).update_layout(yaxis_title='Episodes')
        st.plotly_chart(violinplot1, theme="streamlit", use_container_width=True)
    with scatter1:
        st.write('Correlation between number of episodes and number of said lines')
        script['Line_Length'] = script['Line'].str.len()
        episodes_and_num_lines = pd.merge(lines_by_char, characters, left_on='Character', right_on='name')
        scatterplot1 = px.scatter(episodes_and_num_lines[
                              (episodes_and_num_lines['Line'] > 100) & (episodes_and_num_lines['num_episodes'] > 1)],
                          y='Line', x="num_episodes", color_discrete_sequence=['#BAA388']).update_layout(xaxis_title='Episodes')
        st.plotly_chart(scatterplot1, theme="streamlit", use_container_width=True)

    st.write('Distribution of average length of lines per season')
    avg_line = (script[script['Line_Length'] < 300].groupby(['Character', 'Season'])
                .agg({'Line_Length': 'mean'}).reset_index())
    boxplot1 = (px.box(avg_line, x='Season', y="Line_Length",
                      color_discrete_sequence=['#b488ba'])
                .update_layout(yaxis_title='Average Line Length'))
    st.plotly_chart(boxplot1, theme="streamlit", use_container_width=True)


def network():
    st.title('Relationships network in Gilmore Girls')
    network_df = charts_data.prepare_network_data(script, characters)
    G, HtmlFile = charts_data.build_network(network_df)
    components.html(HtmlFile, width=1000, height=800)
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
    with col2:
        st.write('Beetweenness centrality')
        barplot4 = px.bar(beetweenness_df[:10], x='name', y='centrality',
                          color_discrete_sequence=['#8d91ba'])
        st.plotly_chart(barplot4, theme="streamlit", use_container_width=True)
    with col3:
        st.write('Closeness centrality')
        barplot5 = px.bar(closeness_df[:10], x='name', y='centrality',
                          color_discrete_sequence=['#8d91ba'])
        st.plotly_chart(barplot5, theme="streamlit", use_container_width=True)
    with col4:
        st.write('Eigenvector centrality')
        barplot6 = px.bar(eigenvector_df[:10], x='name', y='centrality',
                          color_discrete_sequence=['#8d91ba'])
        st.plotly_chart(barplot6, theme="streamlit", use_container_width=True)

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
