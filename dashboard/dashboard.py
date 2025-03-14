import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np
import datetime
import os
from babel.numbers import format_currency
sns.set(style='dark')

# Load file CSV ke dalam dataframe
df_day_initial = pd.read_csv(os.path.join(os.path.dirname(__file__), "day_data.csv"))
df_hour_initial = pd.read_csv(os.path.join(os.path.dirname(__file__), "hour_data.csv"))

min_date = df_hour_initial["dteday"].min()
max_date = df_hour_initial["dteday"].max()

# Mengurutkan data dteday pada dataframe df_day_initial
df_day_initial.sort_values(by="dteday", inplace=True)
df_day_initial.reset_index(inplace=True)
df_day_initial['dteday'] = pd.to_datetime(df_day_initial['dteday'])

# Mengurutkan data dteday pada dataframe df_hour_initial
df_hour_initial.sort_values(by="dteday", inplace=True)
df_hour_initial.reset_index(inplace=True)
df_hour_initial['dteday'] = pd.to_datetime(df_hour_initial['dteday'])

# ------------------------------------------ SIDEBAR-------------------------------
with st.sidebar:
    # Memilih mode daily atau hourly
    mode = st.selectbox(
        label="Dashboard Mode",
        options=('Custom Period', 'Daily')
    )
    # Mengambil start_date & end_date dari date_input
    if mode == 'Custom Period':
        start_date, end_date = st.date_input(
            label='Time Period',min_value=min_date,
            max_value=max_date,
            value=[min_date, max_date]
        )
        df_day = df_day_initial[(df_day_initial["dteday"] >= str(start_date)) & (df_day_initial["dteday"] <= str(end_date))]
    elif mode == 'Daily':
        chosen_date = st.date_input("Date", value=min_date, min_value=min_date,
            max_value=max_date)
        df_hour = df_hour_initial[(df_hour_initial["dteday"] == str(chosen_date))]
# ------------------------------------------------------------------------------------


# ------------------------------- MAIN CONTENT ----------------------------------------
if mode == 'Custom Period':
    # ------------------------------ TITLE ------------------------------------------------
    st.title("Bike Sharing System Dashboard")

    # --------------------------- LINE CHART ---------------------------
    st.header('User Trend')

    st.line_chart(df_day, x='dteday', y='cnt', x_label='Time period', y_label='Number of users')

    # --------------------------- PIE CHART -------------------------------
    st.header('User Distribution')

    labels = 'Casual', 'Registered'
    sizes = [df_day['casual'].sum(), df_day['registered'].sum()]
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', radius=0.7)
    st.pyplot(fig)

    # -------------------------- SCATTERPLOT ---------------------------------
    st.header('Clustering')
    st.text('Group each day into three different categories (Low, Medium, High) based on number of users')

    st.scatter_chart(df_day, x="casual", y="registered", x_label="Casual user", y_label="Registered user", color="performance_rating")


elif mode == 'Daily':
    # ---------------------------- TITLE --------------------------------------
    st.header("Bike Sharing System Dashboard")

    # -------------------------- LINE CHART ----------------------------
    st.header('User Trend (in a day)')
    st.line_chart(df_hour, x='hr', y='cnt', x_label='Hour', y_label='Number of Users')

    # -------------------------- PIE CHART -----------------------------
    st.header('User Distribution')

    labels = 'Casual', 'Registered'
    sizes = [df_hour['casual'].sum(), df_hour['registered'].sum()]
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', radius=0.7)
    st.pyplot(fig)

    # --------------------------- SCATTERPLOT --------------------------------
    st.header('Clustering')
    st.text('Group each hour into three different categories (Low, Medium, High) based on number of users')

    st.scatter_chart(df_hour, x="casual", y="registered", x_label="Casual user", y_label="Registered user", color="performance_rating")

    