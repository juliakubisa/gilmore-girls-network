import streamlit as st

st.set_page_config(layout="wide")
st.title('Gilmore Girls script analysis')
st.write('Welcome to my Streamlit app!')


# Add sidebar
with st.sidebar:
    st.write('This is sidebar')


# Add first stats 
col1, col2 = st.columns((1,1))
with col1:
    st.write('Column one!')

with col2:
    st.write('Column two!')

# Add bottom chart