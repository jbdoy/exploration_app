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
section = st.sidebar.radio("Go to", ["Introduction", "Descriptive Statistics", "Data Visualizations", "Conclusion"])

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
    
    st.markdown("---")

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
elif section == "Data Visualizations":
    st.title('Histograms and Box Plots')

    st.write("""
    In this section, we visualize the distribution and spread of key weather variables through histograms and box plots. 
    Histograms provide a detailed look at how frequently different values occur, highlighting the underlying distribution 
    of each variable. Box plots, on the other hand, give a concise summary of the data's range, median, and any potential 
    outliers. Together, these visualizations offer a clearer understanding of the variability in temperature, humidity, 
    wind speed, and other weather metrics, helping to identify trends and anomalies in the dataset.
    """)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Initialize the current graph index for histograms and box plots independently
    if 'current_hist_index' not in st.session_state:
        st.session_state.current_hist_index = 0
    if 'current_boxplot_index' not in st.session_state:
        st.session_state.current_boxplot_index = 0

    # Function to load data and cache it to avoid reloading
    @st.cache_data
    def load_numeric_cols(data):
        return data.select_dtypes(include=['float64', 'int64'])

    # Function to display histogram (with caching)
    @st.cache_data
    def get_histogram_data(numeric_cols, index):
        return numeric_cols.iloc[:, index].dropna()

    # Function to display histogram
    def display_histogram(index, numeric_cols):
        histogram_data = get_histogram_data(numeric_cols, index)
        fig, ax = plt.subplots(figsize=(8, 5))  # Reduced figure size for better performance
        ax.hist(histogram_data, bins=20, alpha=0.7)
        ax.set_title(numeric_cols.columns[index])
        ax.set_xlabel('Value')
        ax.set_ylabel('Frequency')
        st.pyplot(fig)

    # Function to display box plot (with caching)
    @st.cache_data
    def get_boxplot_data(numeric_cols, index):
        return numeric_cols.iloc[:, index].dropna()

    # Function to display box plot
    def display_boxplot(index, numeric_cols):
        boxplot_data = get_boxplot_data(numeric_cols, index)
        fig, ax = plt.subplots(figsize=(8, 5))  # Reduced figure size for better performance
        ax.boxplot(boxplot_data)
        ax.set_title(numeric_cols.columns[index])
        ax.set_xticklabels([numeric_cols.columns[index]])
        st.pyplot(fig)

    # Fetch numeric columns (caching included)
    numeric_cols = load_numeric_cols(data)

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
        "Temperature (C): This box plot shows the range and distribution of temperature values, highlighting outliers and the interquartile range. It illustrates the distribution of temperatures in degrees Celsius. The median temperature is around 12°C, with the interquartile range showing that the middle 50% of temperatures lie between approximately 5°C and 19°C. The overall temperature range extends from approximately -10°C to 40°C, with some outliers below -10°C, indicating unusually cold conditions. This plot provides an overview of both the typical and extreme temperature values observed in the dataset.",
        "Apparent Temperature (C): This box plot illustrates the variation in apparent temperature, indicating its central tendency and variability. It provides a visual summary of the dataset's spread. The median apparent temperature is approximately 12°C, with the middle 50% of data (the interquartile range) falling between about 2°C and 19°C. The whiskers extend to a range of around -10°C to 40°C, showing the overall spread of most of the data points. Notably, there are outliers below -20°C, indicating that there were some significantly colder apparent temperatures compared to the bulk of the data. The plot offers a good overview of the typical and extreme apparent temperature values in this dataset.",
        "Humidity: This box plot represents the distribution of humidity levels, showcasing the median, quartiles, and any outliers. Most of the data is concentrated between 0.6 and 0.9. The central box shows the interquartile range (IQR), which represents the middle 50% of the values, while the green line inside the box indicates the median humidity, which is 0.78. The whiskers extend from the box to capture the overall range, excluding outliers. Several outliers are present below the lower whisker, representing unusually low humidity values around 0.0 to 0.2. Overall, the plot suggests that humidity values tend to be high, with a few extreme low outliers.",
        "Wind Speed (km/h): This box plot shows the distribution of wind speeds, highlighting potential outliers and the range of values. Most of the data is concentrated between approximately 5 and 15 km/h, as indicated by the interquartile range (IQR) within the central box. The median wind speed, shown by the green line, falls just below 10 km/h. The whiskers capture the overall spread of the data, excluding the many outliers. A significant number of outliers extend beyond the upper whisker, with values surpassing 30 km/h and going up to around 60 km/h, indicating a few unusually high wind speed measurements. Overall, the data is skewed towards lower wind speeds, with a notable cluster of high outliers.",
        "Wind Bearing (degrees): This box plot illustrates the wind bearing distribution, providing insights into the variability of wind directions. The median wind bearing is around 180° (south), with most wind directions ranging from southeast to west-southwest (100° to 250°). The full range extends from about 0° (north) to 350° (north-northwest), indicating a broad variability in wind direction. No extreme outliers are present.",
        "Visibility (km): This box plot shows the distribution of visibility measurements, highlighting the spread of values and outliers. The majority of the visibility data falls between approximately 8 and 14 km, as shown by the interquartile range (IQR) in the central box. The median visibility, marked by the green line, is around 10 km. The whiskers extend from the box, indicating the overall range of the data, with the minimum value reaching close to 0 km and the maximum just above 15 km. There are no significant outliers in this plot, and the visibility distribution appears fairly symmetric with a broad range.",
        "Loud Cover: This box plot indicates the distribution of loud cover values, showcasing their central tendency and variability. The box, which typically shows the interquartile range (IQR), is extremely small or almost non-existent, indicating that the values are tightly clustered around the median, which is approximately zero. The Y-axis ranges from -0.05 to 0.05, suggesting that the values lie very close to zero, with no significant outliers or large spread. The lack of visible whiskers or a substantial box indicates that the data might consist of repeated values or has very little variability. This minimal variation is the likely reason the plot appears so condensed.",
        "Pressure (millibars): This box plot represents the atmospheric pressure distribution, illustrating the central value and any outliers. The plot shows a distinct clustering of values around 1016 millibars with a few notable outliers. The majority of the data is concentrated in a narrow range near the top of the plot, where the box, which depicts the interquartile range (IQR), is situated. This indicates that most of the pressure values are closely packed together. The median value is also near 1016 millibars, as indicated by the horizontal line within the box, while an outlier around 0 millibars indicates some extreme pressure measurements."
    ]
    # Histogram and Box Plot Display
    st.subheader("Histograms")
    st.write(explanatory_texts_histogram[st.session_state.current_hist_index])  # Display corresponding explanation
    display_histogram(st.session_state.current_hist_index, numeric_cols)

    # Navigation buttons for histograms
    col_hist1, col_hist2, col_hist3 = st.columns([1, 8.5, 1])
    with col_hist1:
        if st.button("Prev", key="hist_prev"):
            st.session_state.current_hist_index = (st.session_state.current_hist_index - 1) % len(numeric_cols.columns)
    with col_hist3:
        if st.button("Next", key="hist_next"):
            st.session_state.current_hist_index = (st.session_state.current_hist_index + 1) % len(numeric_cols.columns)
    
    st.markdown("---")

    st.subheader("Box Plots")
    st.write(explanatory_texts_boxplot[st.session_state.current_boxplot_index])  # Display corresponding explanation
    display_boxplot(st.session_state.current_boxplot_index, numeric_cols)

    # Navigation buttons for box plots, placed below the graph
    col_box1, col_box2, col_box3 = st.columns([1, 8.5, 1])
    with col_box1:
        if st.button("Prev", key="box_prev"):
            st.session_state.current_boxplot_index = (st.session_state.current_boxplot_index - 1) % len(numeric_cols.columns)
    with col_box3:
        if st.button("Next", key="box_next"):
            st.session_state.current_boxplot_index = (st.session_state.current_boxplot_index + 1) % len(numeric_cols.columns)

    # Extra spacing
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")

    # Correlation
    st.title("Correlation Analysis")

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

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")

    # Correlation
    st.title("Graphical Insights")
 
    # Interactive Bar Plot (e.g., Precip Type vs. Wind Speed)
    st.write("Here is an interactive bar plot showing the average Wind Speed for each Precipitation Type:")
    @st.cache_data
    def create_bar_plot(data):
        fig = px.bar(data, x='Precip Type', y='Wind Speed (km/h)', color='Precip Type',
                    title='Average Wind Speed by Precipitation Type', 
                    labels={'Precip Type': 'Precipitation Type', 'Wind Speed (km/h)': 'Wind Speed (km/h)'},
                    barmode='group')

        # Center the title
        fig.update_layout(title={'x': 0.5, 'xanchor': 'center'})
        return fig
    
    bar_fig = create_bar_plot(data)
    st.plotly_chart(bar_fig)

    st.write("""
    This bar chart shows that areas with rain experience significantly higher wind speeds compared to those with snow. Rain is 
    associated with nearly 0.8 million km/h of wind speed, while snow conditions see much lower wind speeds, around 0.2 million 
    km/h. This indicates that rainy weather typically comes with stronger winds than snowy conditions.
    """)

    st.markdown("---")

    # Interactive Scatter Plot (e.g., Temperature vs. Humidity)
    st.write("An interactive scatter plot visualizing the relationship between Temperature and Humidity:")
    def create_scatter_plot(data):
        scatter_fig = px.scatter(data, x='Temperature (C)', y='Humidity', color='Precip Type',
                                title='Temperature vs Humidity by Precipitation Type',
                                labels={'Temperature (C)': 'Temperature (°C)', 'Humidity': 'Humidity (%)'})

        # Center the title
        scatter_fig.update_layout(title={'x': 0.5, 'xanchor': 'center'})
        return scatter_fig
    
    scatter_fig = create_scatter_plot(data)
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

