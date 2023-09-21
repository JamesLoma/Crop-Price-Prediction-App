import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import folium
import pathlib

BASE_DIR = pathlib.Path(__file__).parent

# Define a green color palette
green_palette = sns.color_palette("Greens")

# Disable the PyplotGlobalUseWarning
st.set_option('deprecation.showPyplotGlobalUse', False)

# Set the style for seaborn plots
sns.set_palette(green_palette)

def create_dashboard(df):
    # Set the page details
    # Title and navigation bar with logo
    st.markdown(
        '<div style="background-color: #4CAF50; color: white; padding: 10px 0; box-shadow: 0px 3px 6px rgba(0, 0, 0, 0.1); display: flex; align-items: center; justify-content: center;">',
        unsafe_allow_html=True)
    st.image('logo.jpg', width=100)
    st.title('Crop Price Prediction Dashboard')
    st.markdown('</div>', unsafe_allow_html=True)

    # Filters - Arrange horizontally in three rows
    # Row 1: Select Year(s)
    selected_years = st.multiselect('Select Year(s)', df['year'].unique(), default=df['year'].unique())

    # Row 2: Select Regional(s) and District(s)
    selected_regionals = st.multiselect('Select Regional(s)', df['regional'].unique(),
                                            default=df['regional'].unique())
    districts_in_selected_regionals = df[df['regional'].isin(selected_regionals)]['district'].unique()
    selected_districts = st.multiselect('Select District(s)', districts_in_selected_regionals,
                                           default=districts_in_selected_regionals)

    # Row 3: Select Market(s) and Commodity(s)
    markets_in_selected_region_district = df[
        df['regional'].isin(selected_regionals) & df['district'].isin(selected_districts)]['market'].unique()
    selected_markets = st.multiselect('Select Market(s)', markets_in_selected_region_district,
                                          default=markets_in_selected_region_district)
    selected_commodities = st.multiselect('Select Commodity(s)', df['commodity'].unique(),
                                              default=df['commodity'].unique())

    # Apply filters
    year_filter = df['year'].isin(selected_years)
    regional_filter = df['regional'].isin(selected_regionals)
    district_filter = df['district'].isin(selected_districts)
    commodity_filter = df['commodity'].isin(selected_commodities)
    market_filter = df['market'].isin(selected_markets)

    # Apply filters
    filtered_df = df[year_filter & regional_filter & district_filter & commodity_filter & market_filter]

    # Pagination
    page_size = st.slider("Items Per Page", 1, len(filtered_df), 10)
    page_number = st.number_input("Page Number", 1, len(filtered_df) // page_size + 1, 1)

    start_idx = (page_number - 1) * page_size
    end_idx = start_idx + page_size

    # Data Preview
    st.subheader("Filtered Data Preview")
    st.write(filtered_df[start_idx:end_idx])

    # Export Filtered Data
    if not filtered_df.empty:
        if st.button("Export Filtered Data to CSV"):
            csv_file = "filtered_data.csv"
            filtered_df[start_idx:end_idx].to_csv(csv_file, index=False)
            st.success(f"Filtered data exported to {csv_file}")

            # Provide a download button
            download_button = st.download_button(
                label="Download Filtered Data as CSV",
                data=open(BASE_DIR / csv_file),
                file_name=csv_file,
                key="download_button"
        )

    # Data Insights Section
    st.subheader('Insights into Crop Prices')

    col1, col2 = st.columns(2)

    # Insight 1: Category Distribution (Bar Chart)
    with col1:
        st.markdown("#### Category Distribution")
        category_counts = filtered_df['category'].value_counts()
        fig = px.bar(category_counts, x=category_counts.index, y=category_counts.values,
                    labels={'x': 'Category', 'y': 'Count'})
        st.plotly_chart(fig)

    # Insight 2: Price Distribution (Histogram)
    with col2:
        st.markdown("#### Price Distribution")
        fig = px.histogram(filtered_df, x='price', nbins=10, labels={'x': 'Price'})
        st.plotly_chart(fig)

    col1, col2 = st.columns(2)
    # Insight 3: Commodity Distribution (Pie Chart)
    with col1:
        st.markdown("#### Commodity Distribution")
        commodity_counts = filtered_df['commodity'].value_counts()
        fig = px.pie(commodity_counts, names=commodity_counts.index, values=commodity_counts.values,
                    title="Commodity Distribution")
        st.plotly_chart(fig)

    #Insight 4: Market Distribution (Pie Chart)
    with col2:
        st.markdown("#### Market Distribution")
        market_counts = filtered_df['market'].value_counts()
        fig = px.pie(market_counts, names=market_counts.index, values=market_counts.values,
                    title="Market Distribution")
        st.plotly_chart(fig)

    col1, col2 = st.columns(2)
    # Insight 5: Calendar Heatmap
    with col1:
        st.subheader('Calendar Heatmap')

        # Allow the user to select a commodity class for the heatmap
        selected_commodity_class = st.selectbox('Select a commodity class (for heatmap)', df['commodity'].unique())

        # Filter the DataFrame for the selected commodity class
        filtered_df = df[df['commodity'] == selected_commodity_class]

        # Create a new column combining 'year' and 'month'
        filtered_df['year_month'] = filtered_df['year'].astype(str) + '-' + filtered_df['month'].astype(str)

        # Create a pivot table with year_month as index and price as values
        pivot_table = filtered_df.pivot_table(index='year_month', values='price', aggfunc='mean')

        # Extract year and month from the year_month index
        pivot_table['year'], pivot_table['month'] = pivot_table.index.str.split('-').str
        pivot_table['year'] = pivot_table['year'].astype(int)
        pivot_table['month'] = pivot_table['month'].astype(int)

        # Pivot the table again to create the heatmap
        heatmap_data = pivot_table.pivot_table(index='month', columns='year', values='price')

        # Sort the columns and rows
        heatmap_data = heatmap_data.reindex(sorted(heatmap_data.columns), axis=1)
        heatmap_data = heatmap_data.reindex(sorted(heatmap_data.index), axis=0)

        fig = px.imshow(
            heatmap_data,
            labels=dict(x="Year", y="Month", color="Price"),
            x=heatmap_data.columns,
            y=heatmap_data.index,
            color_continuous_scale='Inferno',  # Use 'Viridis' color scale
            title=f'Calendar Heatmap of Price for {selected_commodity_class}',
        )

        # Adjust the x-axis and y-axis labels for readability
        fig.update_xaxes(tickvals=list(range(len(heatmap_data.columns))), ticktext=heatmap_data.columns)
        fig.update_yaxes(tickvals=list(range(len(heatmap_data.index))), ticktext=heatmap_data.index)

        # Add hover text to display the price values
        fig.update_traces(text=heatmap_data.values, hoverinfo="text")

        st.plotly_chart(fig)

    # Insight 6: Time Series Plot
    with col2:
        st.subheader('Time Series Plot')

        # Allow the user to select one or more commodities for time series analysis
        selected_commodity = st.selectbox('Select a Commodity', df['commodity'].unique())

        # Allow the user to select one or more markets
        selected_market = st.selectbox('Select a Market', df['market'].unique())

        # Filter the DataFrame for the selected commodity and market
        filtered_df_ts = df[(df['commodity'] == selected_commodity) & (df['market'] == selected_market)]

        fig = px.line(
            filtered_df_ts,
            x='year',
            y='price',
            markers=True,
            labels={'year': 'Year', 'price': 'Price'},
            title=f'Price Trends Over Time for {selected_commodity} in {selected_market}',
        )

        # Add hover text
        fig.update_traces(text=filtered_df_ts['price'])
        fig.update_traces(textposition='top center')

        st.plotly_chart(fig)
    col1, col2 = st.columns(2)
    # Insight 7: Line Chart for Maximum and Minimum Prices by Year
    with col1:
        st.subheader('Maximum and Minimum Prices by Year')

        # Calculate maximum and minimum prices by year for each market-commodity combination
        max_prices = filtered_df.groupby(['year', 'market', 'commodity'])['price'].max().reset_index()
        min_prices = filtered_df.groupby(['year', 'market', 'commodity'])['price'].min().reset_index()

        # Allow the user to select a specific market and commodity for the line chart
        selected_market_line = st.selectbox('Select a Market', max_prices['market'].unique())
        selected_commodity_line = st.selectbox('Select a Commodity', max_prices['commodity'].unique())

        # Filter the data for the selected market and commodity
        max_prices_filtered = max_prices[
            (max_prices['market'] == selected_market_line) & (max_prices['commodity'] == selected_commodity_line)]
        min_prices_filtered = min_prices[
            (min_prices['market'] == selected_market_line) & (min_prices['commodity'] == selected_commodity_line)]

        # Create line charts for maximum and minimum prices
        fig = px.line(max_prices_filtered, x='year', y='price',
                    title=f'Maximum Price Over Time for {selected_market_line}-{selected_commodity_line}',
                    labels={'year': 'Year', 'price': 'Maximum Price'})
        fig.add_scatter(x=min_prices_filtered['year'], y=min_prices_filtered['price'], mode='lines', name='Minimum Price')
        st.plotly_chart(fig)

    # Create a map with markers for each data point using latitude and longitude columns
    st.subheader('Map of Market Distribution')
    st.map(df[['latitude', 'longitude']], zoom=5, use_container_width=True)

    # Create two columns for dLab information and development team credits
    col1, col2 = st.columns(2)

    # dLab Tanzania information
    with col1:
        st.markdown('---')
        st.image('dlab_logo.png', width=100)
        st.write("dLab Tanzania")
        st.write("Address Line: P. O. Box 33335, DSM")
        st.write("Email Address: connect@dlab.or.tz")
        st.write("Phone Number: 0225 222 410 645 / 0222 410 690")

    # Development team credits
    with col2:
        st.markdown('---')
        st.markdown("### Development Team")
        st.write("Meet the talented individuals who made this app possible:")
        st.write("- Basilisa Katani, Email: lisakatani1008@gmail.com")
        st.write("- James Loma, Email: jamesloma80@gmail.com")
        st.write("- Geoffrey Muchunguzi, Email: geoffreymuchunguzi@gmail.com")
        st.write("- Juma Omar, Email: jumaomar97@gmail.com")
        st.write("We appreciate their dedication and creativity in making this app extraordinary!")
        
# Load your dataset (replace 'your_dataset.csv' with the actual file path)
df = pd.read_csv('wholesale_dataset.csv', usecols=[
    'date', 'regional', 'district', 'market', 'latitude', 'longitude',
    'category', 'commodity', 'unit', 'priceflag', 'pricetype', 'currency',
    'price', 'usdprice', 'year', 'month'
])

# Call the create_dashboard function with the loaded DataFrame
create_dashboard(df)
