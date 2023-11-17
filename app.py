import streamlit as st
import charts_data
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="centered")

# Load datasets
characters = pd.read_csv("data/characters_info.csv", sep='\t') # List of characters
script = pd.read_csv("data/Gilmore_Girls_Lines.csv", sep=',', index_col=0)

# Add title
st.title('Gilmore Girls script analysis')
st.write('This is a description of this project')

# Add sidebar
with st.sidebar:
    st.write('Select options')
    options = st.multiselect(
        'Character',
        ['Rory', 'Lorelai', 'Luke', 'Emily'])

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
char1, char2 = st.columns(2)
with char1:
    count_lines = charts_data.num_lines_per_season(script)
    fig = plt.figure()
    ax = plt.axes()
    plt.bar(count_lines['Season'], count_lines['Line'], color='#562B1A', width=0.6,
            alpha=None)
    plt.xlabel("Season")
    plt.ylabel("No. of lines")
    plt.ylim(bottom=12000, top=20000)
    fig.patch.set_alpha(0)
    ax.patch.set_alpha(0)

    st.pyplot(fig)
    # st.bar_chart(count_lines, color = ['#562B1A', '#562B2A'])
with char2:
    st.write('Test')
