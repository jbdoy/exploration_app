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
section = st.sidebar.radio("Go to", ["Introduction", "Descriptive Statistics", "Histograms & Box Plots", "Correlation", "Additional Graphs", "Conclusion"])

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
    The summary statistics provide an overview of key weather variables, including temperature, humidity, wind speed, and 
    pressure. The mean values indicate typical conditions during the observation period, with an average temperature of 
    approximately 11.93°C and humidity levels around 73%. The wind speed averaged 10.81 km/h, while visibility remained
    steady at about 10.35 km. The median and percentile values offer insights into the data's distribution, with temperature 
    and apparent temperature both having a median of 12°C, and wind bearings typically around 180°. This analysis helps 
    identify the general trends and variability in the weather data, allowing for a deeper understanding of day-to-day 
    conditions.
    """)

    st.markdown("<br>", unsafe_allow_html=True)

    st.write(stats_df) 

# Histograms and Box Plots Section
elif section == "Histograms & Box Plots":
    st.title('Histograms and Box Plots')

    st.write("""
    In this section, we visualize the distribution and spread of key weather variables through histograms and box plots. 
    Histograms provide a detailed look at how frequently different values occur, highlighting the underlying distribution 
    of each variable. Box plots, on the other hand, give a concise summary of the data's range, median, and any potential 
    outliers. Together, these visualizations offer a clearer understanding of the variability in temperature, humidity, 
    wind speed, and other weather metrics, helping to identify trends and anomalies in the dataset.
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
        "Temperature (C): This histogram shows the distribution of temperature data, with most values clustering between -10°C and 30°C, peaking around 10°C. The bell-shaped pattern indicates a normal distribution, with fewer extreme cold and hot temperatures, highlighting the typical temperature range and rare outliers in the dataset.",
        "Apparent Temperature (C): This histogram depicts the distribution of apparent temperature values, with most data points clustering between -10°C and 30°C, and a peak around 20°C. The bell-shaped curve suggests a normal distribution, with fewer extreme cold and hot apparent temperatures, illustrating the range of how temperatures feel to humans based on factors like wind and humidity.",
        "Humidity: This histogram illustrates the variation in humidity levels, with most of the data concentrated between 0.6 and 1.0, indicating relatively high humidity levels. The frequency increases steadily as humidity approaches 1.0, peaking just below this maximum value. This suggests that the dataset commonly experiences high humidity, with lower humidity values occurring less frequently.",
        "Wind Speed (km/h): This histogram represents the distribution of wind speeds encountered, wind speeds in the dataset are mostly between 5 and 15 km/h, with a peak around 10 km/h, and fewer occurrences of wind speeds above 30 km/h, indicating a right-skewed distribution with generally low wind speeds.",
        "Wind Bearing (degrees): This histogram shows the directional distribution of wind bearings (in degrees), where the wind comes from different directions. The data is relatively evenly distributed across all angles, with noticeable peaks around 150°, 0°, and 300°, indicating that winds from these directions are more frequent compared to others. There are also troughs around 50° and 250°, suggesting fewer winds from those angles.",
        "Visibility (km): This histogram displays the range of visibility measured in kilometers. Most of the visibility readings are clustered around two distinct values: around 10 km, with a very high frequency, and around 16 km, also quite common. Visibility below 10 km is much less frequent, with relatively consistent low counts across the range from 0 to 8 km. This suggests that the majority of observations had either clear or nearly clear conditions (10-16 km), while poor visibility conditions are rarer.",
        "CLoud Cover: This histogram indicates the distribution of cloud cover values throughout the dataset. The data is highly skewed, with nearly all values concentrated at zero, indicating either missing or homogeneous data for cloud cover in the dataset. This indicates that the variable may require further investigation or alternative handling methods in the analysis.",
        "Pressure (millibars): This histogram represents the atmospheric pressure levels recorded (in millibars), where most values are clustered near 1000 millibars, with a few near zero. This suggests the dataset primarily contains typical atmospheric pressure values, but also some outliers or possibly erroneous data, which may need additional validation or adjustment."
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
    The correlation analysis provides valuable insights into the relationships between various weather variables. The heatmap 
    visually represents these correlations, with colors indicating the strength and direction of the relationships. For example, 
    temperature and apparent temperature show a strong positive correlation, while temperature and humidity display a negative 
    correlation. Other variables, such as wind speed and pressure, exhibit weaker or negligible correlations with most 
    parameters. This analysis helps identify key patterns in the data, which can inform further exploration and predictive 
    modeling.
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
elif section == "Additional Graphs":
 st.title('Additional Graphs')
 st.subheader('Interactive Visualizations')
 
 # Tentative: Interactive Bar Plot (e.g., Precip Type vs. Wind Speed)
 st.write("Here is an interactive bar plot showing the average Wind Speed for each Precipitation Type:")
 fig = px.bar(data, x='Precip Type', y='Wind Speed (km/h)', color='Precip Type',
             title='Average Wind Speed by Precipitation Type', 
             labels={'Precip Type': 'Precipitation Type', 'Wind Speed (km/h)': 'Wind Speed (km/h)'},
             barmode='group')
 st.plotly_chart(fig)
 st.write("""
 This bar chart shows that areas with rain experience significantly higher wind speeds compared to those with snow. Rain is 
 associated with nearly 0.8 million km/h of wind speed, while snow conditions see much lower wind speeds, around 0.2 million 
 km/h. This indicates that rainy weather typically comes with stronger winds than snowy conditions.
 """)

 st.markdown("---")

 # Tentative: Interactive Scatter Plot (e.g., Temperature vs. Humidity)
 st.write("An interactive scatter plot visualizing the relationship between Temperature and Humidity:")
 scatter_fig = px.scatter(data, x='Temperature (C)', y='Humidity', color='Precip Type',
                         title='Temperature vs Humidity by Precipitation Type',
                         labels={'Temperature (C)': 'Temperature (°C)', 'Humidity': 'Humidity (%)'})
 st.plotly_chart(scatter_fig)
 st.write("""
 The data reveals that snow typically occurs at lower temperatures, ranging from around -20°C to 10°C, and is associated with 
 higher humidity levels. In contrast, rain is present across a wider range of temperatures, from approximately 0°C to 40°C, 
 but tends to have lower humidity values as temperatures increase. This suggests that rain is more common in warmer and drier 
 conditions, while snow is found in colder, more humid environments.
 """)
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

