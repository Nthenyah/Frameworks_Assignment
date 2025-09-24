# app.py - Simple CORD-19 explorer
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="CORD-19 Explorer", layout="wide")
st.title("CORD-19 Metadata Explorer (sample)")
st.write("Simple exploration of COVID-19 research metadata (cleaned sample)")

@st.cache_data
def load_data(path="metadata_clean_sample.csv"):
    return pd.read_csv(path, parse_dates=['publish_time_dt'], low_memory=False)

df_small = load_data()

# Year filter
years = sorted([int(y) for y in df_small['year'].dropna().unique()])
yr_min, yr_max = st.select_slider("Select year range", options=years, value=(min(years), max(years)))

filtered = df_small[(df_small['year'] >= yr_min) & (df_small['year'] <= yr_max)]

st.write(f"Showing {len(filtered)} records between {yr_min} and {yr_max}")
st.dataframe(filtered[['title','authors','journal','year']].head(20))

# Plot publications by year
counts = filtered['year'].value_counts().sort_index()
fig, ax = plt.subplots()
sns.barplot(x=counts.index.astype(int), y=counts.values, ax=ax)
ax.set_title("Publications by Year (filtered)")
ax.set_xlabel("Year")
ax.set_ylabel("Count")
st.pyplot(fig)
