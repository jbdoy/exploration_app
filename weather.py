import streamlit as st

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Cover Page", "Introduction", "Data Exploration Report"])

# Cove Page
if page == "Cover Page":
    st.image("logo.png", width=200)
    st.title("Cebu Institute of Technology – University")
    st.subheader("School of Computer Studies")
    st.write("Natalio Bacalso Ave, Cebu City, 6000")

    # Spacer
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.title("REPORT ON DATA EXPLORATION TECHNIQUES IN WEATHER DATASET")

    # Spacer
    st.markdown("<br><br><br>", unsafe_allow_html=True)

elif page == "Introduction":
    # Introduction page content
    st.title("Introduction to the Szeged Weather Dataset")
    st.write("""
        ### Dataset Title: Weather in Szeged 2006-2016

        - **Source**: The dataset is sourced from Darksky.net's API and was created for a project analyzing and comparing historical weather data with weather folklore.
        - **Type of Data**: The dataset contains hourly and daily weather summaries.
    
        ### Content Overview:
        - **Location**: Szeged, Hungary
        - **Time Period**: 2006 to 2016
        - **Data Attributes**: The CSV file includes the following fields:
            - Time: Timestamp of the observation
            - Summary: Brief description of the weather conditions
            - Precip Type: Type of precipitation (if any)
            - Temperature: Recorded temperature
            - Apparent Temperature: Perceived temperature, accounting for factors like humidity and wind
            - Humidity: Humidity level
            - Wind Speed: Speed of the wind
            - Wind Bearing: Direction of the wind
            - Visibility: Visibility distance
            - Cloud Cover: Cloud cover
             - Pressure: Atmospheric pressure

         ### Purpose of Exploration:
        The purpose of this exploration is to understand weather patterns, trends, and correlations in the city of Szeged, Hungary, between 2006 and 2016. By analyzing this dataset, we aim to discover insights related to temperature fluctuations, precipitation patterns, wind behaviors, and overall climatic conditions.
        """)
elif page == "Data Exploration Report":
    # Data exploration report page content
    st.title("REPORT ON DATA EXPLORATION TECHNIQUES IN WEATHER DATASET")
    st.markdown(
        """
        #### Overview
        This report examines various data exploration techniques applied to a weather dataset to uncover trends, correlations, and anomalies.
        """
    )
    
    # Add more detailed content for the report here

# Footer or other global elements can be added at the bottom
st.markdown("<br><br><br>", unsafe_allow_html=True)
