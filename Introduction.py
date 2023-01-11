import streamlit as st
from streamlit import session_state as session

from stat_mod import *

st.set_page_config(page_title="EU Data Explorer📊", page_icon="📊")

st.title("EU Data Explorer📊")
st.markdown(intro_text, unsafe_allow_html=True)
