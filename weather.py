import streamlit as st
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px


@st.cache_data
def load_data():
    data = pd.read_csv('weatherHistory.csv')
    return data

data = load_data()

# CSS
st.markdown(
    """
    <style>
    .streamlit-table {
        width: 100%;
        margin: 0 auto;
        overflow-x: auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar navigation
st.sidebar.title('Main Menu')
section = st.sidebar.radio("Go to", ["Introduction", "Descriptive Statistics", "Histograms & Box Plots", "Correlation", "Interactive Visualizations", "Conclusion"])

# Introduction Section
if section == "Introduction":

    # Cover Photo 
    st.image('report-cover.png', use_column_width=True)

    st.title('Weather Data Exploration Report')
    
    st.header('Introduction')
    st.write("""
    This report explores the weather dataset the **Weather in Szeged 2006-2016** sourced from Kaggle. This dataset provides a 
    comprehensive overview of historical weather conditions in Szeged, Hungary, over a decade. Sourced from the Darksky.net 
    API, this dataset serves as a crucial resource for analyzing and comparing weather patterns in relation to weather folklore.
    Spanning from 2006 to 2016, it includes hourly and daily weather summaries, encapsulated in a CSV file that features key 
    attributes such as:

    - timestamp
    - weather summary
    - precipitation type
    - recorded temperature
    - apparent temperature (which considers factors like humidity and wind)
    - humidity levels 
    - wind speed and direction
    - visibility distance
    - cloud cover; and
    - atmospheric pressure.

    By examining this data, researchers and enthusiasts can gain insights into historical weather trends and their potential 
    correlations with cultural beliefs surrounding weather phenomena.
    """)

    if st.checkbox("Show raw data"):
        st.write(data)

# Descriptive Statistics Section
elif section == "Descriptive Statistics":
    st.title('Descriptive Statistics')
    
    # Select only numerical columns
    numeric_cols = data.select_dtypes(include=['float64', 'int64'])
    
    columns_of_interest = [
        'Temperature (C)', 
        'Apparent Temperature (C)', 
        'Humidity', 
        'Wind Speed (km/h)', 
        'Wind Bearing (degrees)', 
        'Visibility (km)', 
        'Loud Cover', 
        'Pressure (millibars)'
    ]
    
    # Calculate statistics
    stats_dict = {
        'Mean': numeric_cols[columns_of_interest].mean().round(2),
        'Median': numeric_cols[columns_of_interest].median().round(2),
        'Mode': numeric_cols[columns_of_interest].mode().iloc[0].round(2),
        'Std Dev': numeric_cols[columns_of_interest].std().round(2),
        'Variance': numeric_cols[columns_of_interest].var().round(2),
        'Min': numeric_cols[columns_of_interest].min().round(2),
        'Max': numeric_cols[columns_of_interest].max().round(2),
        'Range': (numeric_cols[columns_of_interest].max() - numeric_cols[columns_of_interest].min()).round(2),
        '25th Percentile': numeric_cols[columns_of_interest].quantile(0.25).round(2),
        '50th Percentile': numeric_cols[columns_of_interest].quantile(0.50).round(2),
        '75th Percentile': numeric_cols[columns_of_interest].quantile(0.75).round(2),
    }


    stats_df = pd.DataFrame(stats_dict)

    stats_df.index.name = 'Weather Variable'
    
    # Statistics
    st.subheader("Summary Statistics Table")
    st.write("""
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur eget tempus arcu. Vestibulum vitae cursus turpis. 
    Morbi dapibus nunc eget neque mattis, non sagittis ex viverra. Phasellus hendrerit nisl ac lorem ultricies, ac varius 
    quam lobortis. Integer iaculis enim elit, et faucibus nulla gravida in. Duis sem felis, ultrices vel mi sed, fringilla 
    bibendum elit. Sed sit amet diam ante. Nulla facilisi. In non sem interdum diam tristique cursus. Vivamus in massa a 
    nisi dapibus suscipit. Pellentesque quis velit nec lacus pretium egestas. Fusce lacinia augue nibh, ac tempus erat 
    feugiat at. Maecenas iaculis in tortor id blandit.
    """)

    st.markdown("<br>", unsafe_allow_html=True)

    st.write(stats_df) 

# Histograms and Box Plots Section
elif section == "Histograms & Box Plots":
    st.title('Histograms and Box Plots')

    st.write("""
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur eget tempus arcu. Vestibulum vitae cursus turpis. 
    Morbi dapibus nunc eget neque mattis, non sagittis ex viverra. Phasellus hendrerit nisl ac lorem ultricies, ac varius 
    quam lobortis.
    """)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Select only numerical columns
    numeric_cols = data.select_dtypes(include=['float64', 'int64'])

    # Create histogram data for each numerical column
    histogram_data = [numeric_cols[col].dropna() for col in numeric_cols.columns]

    # Create box plot data for each numerical column
    boxplot_data = [numeric_cols[col].dropna() for col in numeric_cols.columns]

    # Initialize the current graph index for histograms
    if 'current_hist_index' not in st.session_state:
        st.session_state.current_hist_index = 0

    # List of explanatory texts for each histogram
    explanatory_texts_histogram = [
        "Temperature (C): This histogram shows the distribution of temperatures over the recorded period.",
        "Apparent Temperature (C): This histogram depicts the perceived temperature experienced by individuals.",
        "Humidity: This histogram illustrates the variation in humidity levels during the observation period.",
        "Wind Speed (km/h): This histogram represents the distribution of wind speeds encountered.",
        "Wind Bearing (degrees): This histogram shows the directional distribution of wind during the recordings.",
        "Visibility (km): This histogram displays the range of visibility measured in kilometers.",
        "Loud Cover: This histogram indicates the distribution of loud cover values throughout the dataset.",
        "Pressure (millibars): This histogram represents the atmospheric pressure levels recorded."
    ]

    # List of explanatory texts for each box plot
    explanatory_texts_boxplot = [
        "Temperature (C): This box plot shows the range and distribution of temperature values, highlighting outliers and the interquartile range.",
        "Apparent Temperature (C): This box plot illustrates the variation in apparent temperature, indicating its central tendency and variability.",
        "Humidity: This box plot represents the distribution of humidity levels, showcasing the median, quartiles, and any outliers.",
        "Wind Speed (km/h): This box plot shows the distribution of wind speeds, highlighting potential outliers and the range of values.",
        "Wind Bearing (degrees): This box plot illustrates the wind bearing distribution, providing insights into the variability of wind directions.",
        "Visibility (km): This box plot shows the distribution of visibility measurements, highlighting the spread of values and outliers.",
        "Loud Cover: This box plot indicates the distribution of loud cover values, showcasing their central tendency and variability.",
        "Pressure (millibars): This box plot represents the atmospheric pressure distribution, illustrating the central value and any outliers."
    ]

    # Function to display histogram
    def display_histogram(index):
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.hist(histogram_data[index], bins=20, alpha=0.7)
        ax.set_title(numeric_cols.columns[index])
        ax.set_xlabel('Value')
        ax.set_ylabel('Frequency')
        st.pyplot(fig)

    # Function to display box plot
    def display_boxplot(index):
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.boxplot(boxplot_data[index])
        ax.set_title(numeric_cols.columns[index])
        ax.set_xticklabels([numeric_cols.columns[index]])
        st.pyplot(fig)

    # Histogram Section
    st.subheader("Histograms")
    
    # Explanatory text for the current histogram
    st.write(explanatory_texts_histogram[st.session_state.current_hist_index])
    
    display_histogram(st.session_state.current_hist_index)

    # Navigation buttons for box plots
    col1, col2, col3 = st.columns([1, 8.5, 1])

    with col1:
        if st.button("Prev"):
            st.session_state.current_hist_index = (st.session_state.current_hist_index - 1) % len(numeric_cols.columns)

    with col3:
        if st.button("Next"):
            st.session_state.current_hist_index = (st.session_state.current_hist_index + 1) % len(numeric_cols.columns)
        

    st.markdown("<br>", unsafe_allow_html=True)

    # Box Plot Section
    st.subheader("Box Plots")

    # Explanatory text for the current box plot
    st.write(explanatory_texts_boxplot[st.session_state.current_hist_index])

    display_boxplot(st.session_state.current_hist_index)

    # Navigation buttons for box plots
    col1, col2, col3 = st.columns([1, 8.5, 1])

    with col1:
        if st.button("Prev", key="prev_box"):
            st.session_state.current_hist_index = (st.session_state.current_hist_index - 1) % len(numeric_cols.columns)

    with col3:
        if st.button("Next", key="next_box"):
            st.session_state.current_hist_index = (st.session_state.current_hist_index + 1) % len(numeric_cols.columns)


# Correlation Section
elif section == "Correlation":
    st.title('Correlation Analysis')

    st.write("""
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur eget tempus arcu. Vestibulum vitae cursus turpis. 
    Morbi dapibus nunc eget neque mattis, non sagittis ex viverra. Phasellus hendrerit nisl ac lorem ultricies, ac varius 
    quam lobortis. Integer iaculis enim elit, et faucibus nulla gravida in. Duis sem felis, ultrices vel mi sed, fringilla 
    bibendum elit. Sed sit amet diam ante. Nulla facilisi. In non sem interdum diam tristique cursus. Vivamus in massa a 
    nisi dapibus suscipit. Pellentesque quis velit nec lacus pretium egestas. Fusce lacinia augue nibh, ac tempus erat 
    feugiat at. Maecenas iaculis in tortor id blandit.
    """)
    
    # Select only numerical columns
    numeric_cols = data.select_dtypes(include=['float64', 'int64'])

    # Correlation matrix and heatmap
    st.subheader("Correlation Heatmap")
    corr_matrix = numeric_cols.corr()
    plt.figure(figsize=(10, 6))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
    st.pyplot(plt)

#Interactive Visualilization
elif section == "Interactive Visualizations":
 st.title('Additional Graphs')
 st.subheader('Interactive Visualizations')
 
 # Tentative: Interactive Bar Plot (e.g., Precip Type vs. Wind Speed)
 st.write("Here is an interactive bar plot showing the average Wind Speed for each Precipitation Type:")
 fig = px.bar(data, x='Precip Type', y='Wind Speed (km/h)', color='Precip Type',
             title='Average Wind Speed by Precipitation Type', 
             labels={'Precip Type': 'Precipitation Type', 'Wind Speed (km/h)': 'Wind Speed (km/h)'},
             barmode='group')
 st.plotly_chart(fig)

 # Tentative: Interactive Scatter Plot (e.g., Temperature vs. Humidity)
 st.write("An interactive scatter plot visualizing the relationship between Temperature and Humidity:")
 scatter_fig = px.scatter(data, x='Temperature (C)', y='Humidity', color='Precip Type',
                         title='Temperature vs Humidity by Precipitation Type',
                         labels={'Temperature (C)': 'Temperature (°C)', 'Humidity': 'Humidity (%)'})
 st.plotly_chart(scatter_fig)

# Conclusion Section
elif section == "Conclusion":
    st.title('Conclusion')
    st.write(""" 
    This dataset shows that Szeged, Hungary, usually has high humidity,
    moderate temperatures, and sporadic calm breezes. The environment is
    characterized by clear sky and steady air pressure, with a few exceptions such
    as chilly days, high gusts, and changes in wind direction. The dataset's balance
    of pressure and temperature points to a largely steady and predictable
    environment, while daily weather impressions may be influenced by changes in
    wind and high humidity.
             
    Further study, including studies on climate change, weather forecasting, or
    even the validation of traditional weather folklore against real data patterns, can
    be based on this methodology.
    """)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Meet the Team Section
    st.header("Meet the Team")
    
    # Names of the Members
    team_members = [
        "Member Name",
        "Member Name",
        "Member Name",
        "Member Name",
        "Member Name",
        "Member Name"
    ]

    cols = st.columns(len(team_members))  
    for i, member in enumerate(team_members):
        with cols[i]:
            st.markdown(
                f"<div style='width: 100px; height: 100px; border-radius: 50%; background-color: lightgray; display: flex; align-items: center; justify-content: center; margin: 0 auto; font-size: 12px;'>{member}</div>", 
                unsafe_allow_html=True
            )
            st.write(member) 

