import streamlit as st
import pandas as pd

st.title("Test App")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('data/financial_data.csv')
    return df

df = load_data()

st.write("Data loaded successfully!")
st.write(f"Shape: {df.shape}")
st.dataframe(df.head())

# File upload test
uploaded_file = st.file_uploader("Upload CSV", type=['csv'])

if uploaded_file is not None:
    new_df = pd.read_csv(uploaded_file)
    st.write("Uploaded data:")
    st.dataframe(new_df)