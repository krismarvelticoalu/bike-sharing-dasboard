import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np
import datetime
from babel.numbers import format_currency
# sns.set(style='dark')


# Load CSV file into dataframes
df_day_initial = pd.read_csv('day_data.csv')
df_hour_initial = pd.read_csv('hour_data.csv')

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
        options=('Daily', 'Hourly')
    )
    # Mengambil start_date & end_date dari date_input
    if mode == 'Daily':
        start_date, end_date = st.date_input(
            label='Rentang Waktu',min_value=min_date,
            max_value=max_date,
            value=[min_date, max_date]
        )
        df_day = df_day_initial[(df_day_initial["dteday"] >= str(start_date)) & (df_day_initial["dteday"] <= str(end_date))]
    elif mode == 'Hourly':
        chosen_date = st.date_input("What day?", datetime.date(2011, 1, 1))
        df_hour = df_hour_initial[(df_hour_initial["dteday"] == str(chosen_date))]
# ------------------------------------------------------------------------------------


# ------------------------------- MAIN CONTENT ----------------------------------------
if mode == 'Daily':
    st.header("Bike Sharing System Dashboard")

    # --------------------------- LINE CHART ---------------------------
    st.subheader('Daily Rents')

    st.line_chart(df_day, x='dteday', y='cnt')

    # --------------------------- BAR CHART ----------------------------
    st.subheader('Weekday User Performance')

    st.bar_chart(df_day, x='weekday', y='cnt', y_label='Number of users')

    # ----------------------------- PIE CHART ----------------------------
    # st.subheader('User Distribution')

    # labels = 'Casual', 'Registered'
    # sizes = [df_day['casual'].sum(), df_day['registered'].sum()]
    # fig, ax = plt.subplots()
    # ax.pie(sizes, labels=labels, autopct='%1.1f%%')
    # st.pyplot(fig)

    # Best performing season/day/year/month based on casual/registered/cnt using bar chart
    # st.subheader('Best Performing day')
    # st.bar_chart(df_day, x="weekday", y="cnt")


elif mode == 'Hourly':
    st.header("Bike Sharing System Dashboard")

    # -------------------------- LINE CHART ----------------------------
    st.subheader('Hourly Rents')
    st.line_chart(df_hour, x='hr', y='cnt')

    # -------------------------- PIE CHART -----------------------------
    # st.subheader('User Distribution')

    # labels = 'Casual', 'Registered'
    # sizes = [df_hour['casual'].sum(), df_hour['registered'].sum()]
    # fig, ax = plt.subplots()
    # ax.pie(sizes, labels=labels, autopct='%1.1f%%')
    # st.pyplot(fig)

    # Best performing time of the day based on casual/registered/cnt using bar chart