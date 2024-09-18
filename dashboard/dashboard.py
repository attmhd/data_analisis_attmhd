import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd 
import matplotlib.pyplot as plt

# Set page title and icon
st.set_page_config(page_title="AQI Dashboard", page_icon=":bar_chart:", layout="wide")

# Load data
try:
    data = pd.read_csv('dashboard/data.csv')
except FileNotFoundError:
    st.error('Data not found. Please upload data first.')




with st.sidebar:
    selected = option_menu("Main Menu", ["Home", 'Data'], 
        icons=['house','file'], menu_icon="cast", default_index=0)
    selected = selected.lower()

if selected == 'home':
    # Display data aqi data dengan aqi category berdasarkan input date dan hour
    st.title("Air Quality Index Data")
    st.write("Select Date and Hour")

    # Input form
    tanggal = st.date_input("Date", pd.to_datetime('2013-03-01'))
    hour = st.selectbox("Hour", data['hour'].unique())
    station = st.selectbox("Station", data['station'].unique())

    
    # Filter data
    filtered_data = data[ (data['Date'] == '2014-01-10') & (data['hour'] == hour) & (data['station'] == station)]

    nilai_aqi = filtered_data['AQI'].values[0]
    nilai_aqi_category = filtered_data['AQI Category'].values[0]

    # pengkondisian untuk background color berdasarkan nilai aqi category
    if nilai_aqi_category == 'Excellent':
        color = '#90EE90'
    elif nilai_aqi_category == 'Good':
        color = '#FFFF00'
    elif nilai_aqi_category == 'Lightly Polluted':
        color = '#FFD580'
    elif nilai_aqi_category == 'Heavily Polluted':
        color = '#FF7F7F'
    elif nilai_aqi_category == 'Moderately Polluted':
        color = '#4B0082'
    elif nilai_aqi_category == 'Severely Polluted':
        color = '#D2B48C'
    else:
        color = '#000000'


    # Menampilkan nilai aqi dan aqi category
    st.markdown(
    f"""
    <style>
    .custom-box {{
        background-color: {color}; /* Ganti dengan warna yang diinginkan */
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        display:flex;
        justify-content:space-between;
    }}
    </style>
    <div class="custom-box">
        <span style="font-size: 24px; font-weight: bold;">{nilai_aqi_category}</span>
        <span style="font-size: 24px; font-weight: bold;">{nilai_aqi}</span>
    </div>
    """,
    unsafe_allow_html=True
)

    


    

elif selected == 'data':
    st.title("Data")
    st.write("Here is the data used in this dashboard.")
    st.write(data)

    st.write("## Data Visualization")

    tab1, tab2 = st.tabs(["Line Chart", "Pie Chart"])

    with tab1:
        st.write("### Line Chart")
        st.write("Line chart of PM2.5 data")

        # input data berdasarkan statiun
        station_line = st.selectbox("Station Line", data['station'].unique())

        # Line chart
        plt.figure(figsize=(12, 8))
        data[data['station'] == station_line].groupby('Date')['PM2.5'].mean().plot()
        plt.axhline(y=35, color='green', linestyle='--', label='Excelent')
        plt.axhline(y=75, color='yellow', linestyle='--', label='Good')
        plt.axhline(y=115, color='orange', linestyle='--', label='Lightly Polluted')
        plt.axhline(y=150, color='red', linestyle='--', label='Moderately Polluted')
        plt.axhline(y=250, color='purple', linestyle='--', label='Heavily Polluted')
        plt.axhline(y=500, color='maroon', linestyle='--', label='Severely Polluted')
        plt.title('PM2.5 di Stasiun ' + station_line)
        plt.xlabel('Date')
        plt.ylabel('PM2.5')
        st.pyplot(plt)

        
    
    with tab2:
        st.write("### Pie Chart")
        st.write("Pie chart of AQI Category data")

        # input data berdasarkan statiun
        station_pie = st.selectbox("Station Pie", data['station'].unique())


        # Pie chart
        plt.figure(figsize=(12, 8))
        data[data['station'] == station_pie]['AQI Category'].value_counts().plot.pie(autopct='%1.1f%%', startangle=45, colors=['green', 'yellow', 'orange', 'red', 'purple', 'brown', 'black'])
        plt.title('AQI Level di Stasiun ' + station_pie)
        plt.ylabel('')
        st.pyplot(plt)