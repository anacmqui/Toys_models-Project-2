import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import sqlalchemy as sql
import datetime

primaryColor = '#77FFE3'


st.title('Project 2!')

# Using object notation
add_selectbox = st.sidebar.selectbox(
    "Select company's department",
    ["Sales", "Finance","Logistics", "HR"],
    )

# # Using "with" notation
# with st.sidebar:
#     add_radio = st.radio(
#         "Choose a shipping method",
#         ("Sales", "Finance")
#     )

if add_selectbox == 'Sales':
    st.markdown('''Welcome to *Sales*''')
elif add_selectbox == 'Finance':
    st.markdown('''Hi, _this_ is **Finance**''')
elif add_selectbox == 'Logistics':
    st.markdown('''Hi, _this_ is **Logistics**''')
else:
    st.markdown('''Hi, _this_ is **HR**''')