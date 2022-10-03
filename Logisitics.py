import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title('Logistics')

link = "https://github.com/anacmqui/Toys_models-Project-2/blob/main/Q3_Logisitics_P2.ipynb"

df_Logistics01 = pd.read_html(link)
df_Logistics01 