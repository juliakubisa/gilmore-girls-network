import streamlit as st
import charts_data
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit.components.v1 as components
from streamlit_option_menu import option_menu
st.set_page_config(layout="wide")


# Load datasets
characters = pd.read_csv("data/characters_info.csv", sep='\t') # List of characters
script = pd.read_csv("data/Gilmore_Girls_Lines.csv", sep=',', index_col=0)

# Add title
st.title('Gilmore Girls script analysis')
st.write('This is a description of this project')
def Home():
    # Add first stats
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
    st.markdown('---')
    char1, char2 = st.columns(2)
    with char1:
        tab1, tab2 = st.tabs(["Lines per season", "Characters per season"])
        with tab1:
            count_lines = charts_data.num_lines_per_season(script)
            fig1 = px.bar(count_lines, x = 'Season', y='Line', color_discrete_sequence=['#cb8a58'])
            st.plotly_chart(fig1, theme="streamlit", use_container_width=True)
        with tab2:
            seasons_char = charts_data.num_characters_per_season(script)
            fig2 = px.bar(seasons_char, x='Season', y='Character')
            st.plotly_chart(fig2, theme="streamlit", use_container_width=True)
    with char2:
        st.write('Percent of lines spoken by characters')
        lines_by_char = charts_data.count_lines_by_character(script)
        fig3 = px.pie(lines_by_char[:15], values='Percent', names='Character')
        st.plotly_chart(fig3, theme="streamlit", use_container_width=True)


def Network():
    network_df = charts_data.prepare_network_data(script, characters)
    HtmlFile = charts_data.build_network(network_df)
    components.html(HtmlFile.read(), width = 1200, height = 800)

# Add sidebar
def Sidebar():
    with st.sidebar:
        selected = option_menu(
            menu_title="Main Menu",
            options=["Home", "Network"],
            icons=["house", "diagram-2"],
            menu_icon="cast",
            default_index=0
        )
    if selected == "Home":
        Home()
    if selected == "Network":
        Network()

Sidebar()