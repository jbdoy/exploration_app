import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# --- GENERAL SETTINGS ---
PAGE_TITLE = "Team Eyy | Data Exploration Techniques"
PAGE_ICON = ":ok_hand:"
st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON)

# Sidebar for navigation
st.sidebar.title("Dashboard")
page = st.sidebar.radio("", [
    "📄 Cover Page",
    "📖 Introduction",
    "📊 Data Visualization"
])

# # Cover Page
if page == "📄 Cover Page":
    st.image("assets/logo.png", width=200)
    st.title("Cebu Institute of Technology – University")
    st.subheader("School of Computer Studies")
    st.write("Natalio Bacalso Ave, Cebu City, 6000")
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.title("DATA EXPLORATION TECHNIQUES IN WEATHER DATASET")
    st.markdown("<br><br><br>", unsafe_allow_html=True)

# Introduction Page
elif page == "📖 Introduction":
    st.title("Introduction to the Szeged Weather Dataset")
    st.write("""
        ### Dataset Title: [Weather in Szeged 2006-2016](https://www.kaggle.com/datasets/budincsevity/szeged-weather)
        - **Source**: Darksky.net API
        - **Location**: Szeged, Hungary
        - **Time Period**: 2006 to 2016
        - **Data Attributes**: Time, Summary, Precip Type, Temperature, Apparent Temperature, Humidity, Wind Speed, Wind Bearing, Visibility, Cloud Cover, Pressure
        - **Purpose**: The main purpose of studying the Szeged Weather Dataset is to analyze weather patterns and trends, which helps identify seasonal variations and extreme weather events. It can be used for climate change research, detecting long-term changes in temperature and precipitation. The dataset supports predictive modeling to forecast future weather conditions with greater accuracy. It also aids in public health and safety assessments by examining the effects of weather on health and disaster preparedness. Additionally, the dataset can inform agricultural planning and urban development by providing insights into how weather influences crop yields and infrastructure resilience.
        """)

# Data Exploration Report Page
elif page == "📊 Data Visualization":
    st.title("DATA VISUALIZATION")
    
    # Placeholder for the overview text
    overview_placeholder = st.empty()
    overview_text = """The data visualization tools utilized in this analysis includes:
- **Histograms** are chosen to illustrate the distribution of continuous variables, helping to identify patterns in temperature and humidity levels, as well as revealing any potential outliers or skewness in the data.
- **Box plots** provide a visual summary of central tendency and variability, showcasing the median, quartiles, and outliers for each variable, which is essential for comparing multiple variables simultaneously.
- **Correlation matrices and heatmaps** are employed to visualize relationships between various weather parameters, enabling the identification of correlations that shed light on how different variables interact.

Together, these visualization methods offer a comprehensive understanding of the dataset, aiding in the analysis of trends and patterns critical for further exploration and decision-making.
"""


    # Display the default overview message initially
    overview_placeholder.markdown(f"### Overview: {overview_text}")

    # Sidebar for selecting visualization type
    st.sidebar.title("Visualization Selector")
    selected_visualization = st.sidebar.selectbox("Select Visualization Type", ["Overview", "Histogram", "Box Plot", "Correlation Matrix / Heatmap"])

    if selected_visualization == "Histogram":
        st.title("Histogram")
        selected_histogram_variable = st.sidebar.selectbox("Select a Variable for Histogram", [
            "Temperature (C)",
            "Apparent Temperature (C)",
            "Humidity",
            "Wind Speed (km/h)",
            "Wind Bearing (degrees)",
            "Visibility (km)",
            "Loud Cover",
            "Pressure (millibars)"
        ])

        # Update overview text based on selected variable
        if selected_histogram_variable == "Temperature (C)":
            overview_text = "Description: Change it here please"
            st.image("assets/hTemp.png", caption="Temperature (C)", use_column_width=True)

        elif selected_histogram_variable == "Apparent Temperature (C)":
            overview_text = "Description: Change it here please"
            st.image("assets/hATemp.png", caption="Apparent Temperature (C)", use_column_width=True)

        elif selected_histogram_variable == "Humidity":
            overview_text = "Description: Change it here please"
            st.image("assets/hHumid.png", caption="Humidity", use_column_width=True)

        elif selected_histogram_variable == "Wind Speed (km/h)":
            overview_text = "Description: Change it here please"
            st.image("assets/hWSpeed.png", caption="Wind Speed (km/h)", use_column_width=True)

        elif selected_histogram_variable == "Wind Bearing (degrees)":
            overview_text = "Description: Change it here please"
            st.image("assets/hWBear.png", caption="Wind Bearing (degrees)", use_column_width=True)

        elif selected_histogram_variable == "Visibility (km)":
            overview_text = "Description: Change it here please"
            st.image("assets/hVis.png", caption="Visibility (km)", use_column_width=True)

        elif selected_histogram_variable == "Loud Cover":
            overview_text = "Description: Change it here please"
            st.image("assets/hLCover.png", caption="Loud Cover", use_column_width=True)

        elif selected_histogram_variable == "Pressure (millibars)":
            overview_text = "Description: Change it here please"
            st.image("assets/hPressure.png", caption="Pressure (millibars)", use_column_width=True)

    elif selected_visualization == "Box Plot":
        st.title("Box Plot")
        selected_box_plot_variable = st.sidebar.selectbox("Select a Variable for Box Plot", [
            "Temperature (C)",
            "Apparent Temperature (C)",
            "Humidity",
            "Wind Speed (km/h)",
            "Wind Bearing (degrees)",
            "Visibility (km)",
            "Loud Cover",
            "Pressure (millibars)"
        ])

        # Update overview text based on selected variable
        if selected_box_plot_variable == "Temperature (C)":
            overview_text = "Description: Change it here please"
            st.image("assets/boxTemp.png", caption="Box Plot of Temperature (C)", use_column_width=True)

        elif selected_box_plot_variable == "Apparent Temperature (C)":
            overview_text = "Description: Change it here please"
            st.image("assets/boxATemp.png", caption="Box Plot of Apparent Temperature (C)", use_column_width=True)

        elif selected_box_plot_variable == "Humidity":
            overview_text = "Description: Change it here please"
            st.image("assets/boxHumid.png", caption="Box Plot of Humidity", use_column_width=True)

        elif selected_box_plot_variable == "Wind Speed (km/h)":
            overview_text = "Description: Change it here please"
            st.image("assets/boxWSpeed.png", caption="Box Plot of Wind Speed (km/h)", use_column_width=True)

        elif selected_box_plot_variable == "Wind Bearing (degrees)":
            overview_text = "Description: Change it here please"
            st.image("assets/boxWBear.png", caption="Box Plot of Wind Bearing (degrees)", use_column_width=True)

        elif selected_box_plot_variable == "Visibility (km)":
            overview_text = "Description: Change it here please"
            st.image("assets/boxVis.png", caption="Box Plot of Visibility (km)", use_column_width=True)

        elif selected_box_plot_variable == "Loud Cover":
            overview_text = "Description: Change it here please"
            st.image("assets/boxLCover.png", caption="Box Plot of Loud Cover", use_column_width=True)

        elif selected_box_plot_variable == "Pressure (millibars)":
            overview_text = "Description: Change it here please"
            st.image("assets/boxPressure.png", caption="Box Plot of Pressure (millibars)", use_column_width=True)

    elif selected_visualization == "Correlation Matrix / Heatmap":
        st.title("Correlation Matrix and Heatmap")
        overview_text = "Description: Change it here please"
        st.image("assets/heatmap.png", caption="Correlation Matrix and Heatmap", use_column_width=True)

    # Update the overview placeholder with the selected overview text
    overview_placeholder.markdown(f"### {overview_text}")

# Footer or other global elements can be added at the bottom
st.markdown("<br><br><br>", unsafe_allow_html=True)
