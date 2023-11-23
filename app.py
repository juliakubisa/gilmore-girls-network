import streamlit as st
import charts_data
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit.components.v1 as components
from streamlit_option_menu import option_menu
st.set_page_config(page_title = "Gilmore Girls Dasboard", layout="wide")


# Load datasets
characters = pd.read_csv("data/characters_info.csv", sep='\t') # List of characters
script = pd.read_csv("data/Gilmore_Girls_Lines.csv", sep=',', index_col=0)

# Add title
st.title('Gilmore Girls script analysis')

# Load css
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

def Home():
    # Add general stats
    tot1, tot2, tot3, tot4 = st.columns(4)
    total_episodes, total_characters, total_lines, total_seasons = charts_data.compute_basic_analytics(script, characters)

    with tot1:
        st.metric(label= '# Seasons', value=f"{total_seasons}")
    with tot2:
        st.metric(label= '# Episodes', value=f"{total_episodes}")
    with tot3:
        st.metric(label= '# Characters', value=f"{total_characters}")
    with tot4:
        st.metric(label='# Lines', value=f"{total_lines}")

    # Add bottom charts
    st.divider()
    bar1, pie1 = st.columns(2)
    with bar1:
        tab1, tab2 = st.tabs(["Lines per season", "Characters per season"])
        with tab1:
            count_lines = charts_data.num_lines_per_season(script)
            barplot1 = px.bar(count_lines, x = 'Season', y='Line',
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
                      names='Character', color_discrete_sequence = ['#8d91ba', '#BAB888','#82815f',
                                                                    '#BAA388', '#fff9ee', '#b488ba', '#82775f'])
        st.plotly_chart(pieplot1, theme="streamlit", use_container_width=True)

    violin1, scatter1 = st.columns(2)
    with violin1:
        st.write('Distribution of characters number of episodes')
        episode_distr = characters.loc[characters['num_episodes'] >= 5]
        violinplot1 = px.violin(episode_distr, y="num_episodes", box = True,
                         points = 'all', color_discrete_sequence=['#8d91ba']).update_layout(yaxis_title = 'Episodes')
        st.plotly_chart(violinplot1, theme="streamlit", use_container_width=True)
    with scatter1:
        st.write('Correlation between number of episodes and number of said lines')
        script['Line_Length'] = script['Line'].str.len()
        episodes_and_num_lines = pd.merge(lines_by_char, characters, left_on='Character', right_on='name')
        scatterplot1 = px.scatter(episodes_and_num_lines[
                              (episodes_and_num_lines['Line'] > 100) & (episodes_and_num_lines['num_episodes'] > 1)],
                          y='Line', x="num_episodes", color_discrete_sequence=['#8d91ba']).update_layout(xaxis_title = 'Episodes')
        st.plotly_chart(scatterplot1, theme="streamlit", use_container_width=True)

    st.write('Distribution of average length of lines per season')
    avg_line = (script[script['Line_Length'] < 300].groupby(['Character', 'Season'])
                .agg({'Line_Length':'mean'}).reset_index())
    boxplot1 = px.box(avg_line, x = 'Season', y="Line_Length",
                      color_discrete_sequence=['#8d91ba', '#BAB888','#82815f',
                                               '#BAA388', '#fff9ee', '#b488ba', '#82775f']).update_layout(yaxis_title = 'Average Line Length')
    st.plotly_chart(boxplot1, theme="streamlit", use_container_width=True)


def Network():
    st.markdown('<style> .card{border:none;} #mynetwork{border:none;} </style>', unsafe_allow_html=True)
    network_df = charts_data.prepare_network_data(script, characters)
    HtmlFile = charts_data.build_network(network_df)
    components.html(HtmlFile.read(), width = 800, height = 800)

# Add sidebar
def Sidebar():
    with st.sidebar:
        selected = option_menu(
            menu_title="Main Menu",
            options=["Home", "Network", 'Wordcloud'],
            icons=["house", "diagram-2", "cloud"],
            menu_icon="cast",
            default_index=0
        )
    if selected == "Home":
        Home()
    if selected == "Network":
        Network()

Sidebar()