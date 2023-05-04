import numpy as np
import pandas as pd
import streamlit as st
import altair as alt

st.markdown('''
# H-1B Visa Analysis and Visualization
''')

@st.cache_data()
def load_data():
    h1b_data = pd.read_csv("data/h-1b-data-export.csv")
    return h1b_data

h1b_data = load_data()


# Sidebar
st.sidebar.image("data/h1b-image.png", use_column_width=True)
st.sidebar.header('Amount Adjustment')
approval_amount = st.sidebar.slider("Amount of Approval",min_value=0, max_value=3500, value=50, step=1)
denail_amount = st.sidebar.slider("Amount of Denial",min_value=0, max_value=50, value=2, step=1)


tab1, tab2, tab3, tab4, tab5 = st.tabs(['Overview', 'Dataset','Approval', 'Denial', 'Map'])

with tab1:
    st.subheader("H-1B Visa")
    st.write("The H-1B visa is a valuable opportunity for skilled foreign workers seeking specialized employment in fields such as science, engineering, math, and computer programming within the United States. This visa offers a pathway for foreign workers to pursue career opportunities in the U.S. However, the process of identifying which employers are most receptive to H-1B sponsorship can be challenging. To provide greater clarity and transparency for foreign job seekers, this study aims to identify the companies that sponsor the most H-1B visas while also highlighting companies that have a high rate of H-1B visa denials in North Carolina. By using data visualization to present this information, foreign job seekers can better understand which companies are more H-1B friendly and which ones are non H-1B friendly. This information will be useful when seeking employment opportunities in North Carolina.")

with tab2:
    st.subheader("First 20 Rows of the Dataset")
    df = h1b_data.head(20)

    # CSS to hide row indices
    hide_table_row_index = """
        <style>
        thead tr th:first-child {display:none}
        tbody th {display:none}
        </style>
        """

    # Inject CSS with Markdown
    st.markdown(hide_table_row_index, unsafe_allow_html=True)

    # Display the table
    st.table(df)

with tab3:
    st.subheader("H-1B Sum of Approval by Employee")
    h1b_data_count = h1b_data.groupby('Employer')['Sum Approval'].count().reset_index()
    h1b_data_count.columns = ['Employer', 'Count']
    h1b_data_merged = pd.merge(h1b_data, h1b_data_count, on='Employer', how='left')
    filtered_data = h1b_data_merged[h1b_data_merged['Sum Approval'] >= approval_amount]
    barchart = alt.Chart(filtered_data).mark_bar().encode(
        alt.X("Sum Approval", title="Sum of Approval"),
        alt.Y("Employer", sort=alt.EncodingSortField(field="Sum Approval", op="sum", order="descending")),
        tooltip=["Employer", "Sum Approval", "Count"]
    ).configure_view(
        fill='#F0F0F0'
    )
    
    st.altair_chart(barchart, use_container_width=True)
    st.write("The list above displays the H-1B approval sum by employee in descending order, with IBM CORPORATION having the highest number of approvals, surpassing all other companies in North Carolina considerably. This suggests that IBM employees have a good chance of being selected for H-1B visas. The top 10 companies on this list have high approval amounts, indicating their H-1B visa sponsorship friendliness.")



with tab4:
    st.subheader("H-1B Sum of Denial by Employee")
    h1b_data_count = h1b_data.groupby('Employer')['Sum Denial'].count().reset_index()
    h1b_data_count.columns = ['Employer', 'Count']
    h1b_data_merged = pd.merge(h1b_data, h1b_data_count, on='Employer', how='left')
    filtered_data = h1b_data_merged[h1b_data_merged['Sum Denial'] >= denail_amount]
    barchart = alt.Chart(filtered_data).mark_bar().encode(
        alt.X("Sum Denial", title="Sum of Denial"),
        alt.Y("Employer", sort=alt.EncodingSortField(field="Sum Denial", op="sum", order="descending")),
        tooltip=["Employer", "Sum Denial", "Count"]
    ).configure_view(
        fill='#F0F0F0'
    )
    st.altair_chart(barchart, use_container_width=True)
    st.write("The list above showcases the H-1B denial sum by employee in descending order, with IBM CORPORATION having the highest number of denials. However, IBM CORPORATION remains H-1B friendly due to its large number of approvals. While some companies on the list may be perceived as non-H-1B friendly, it is essential to evaluate both their denial and approval numbers to have a comprehensive understanding of their H-1B visa practices.")



import plotly.express as px

with tab5:
    st.subheader("H-1B Visa Approval by Location (Zip Code)")
    st.write("In this section, a map visualization of H-1B visa approvals by zip code is presented. This allows foreign job seekers to have a better understanding of the geographical distribution of H-1B friendly companies in North Carolina.")

    # Group the data by Zip Code and calculate the sum of approvals for each Zip Code
    zip_data = h1b_data.groupby("Zip")["Sum Approval"].sum().reset_index()

    # Create a choropleth map using Plotly
    map_chart = px.choropleth(zip_data,
                              geojson="https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/master/nc_north_carolina_zip_codes_geo.min.json",
                              featureidkey='properties.ZCTA5CE10',
                              locations='Zip',
                              color='Sum Approval',
                              color_continuous_scale='blues',
                              scope='usa',
                              labels={'Sum Approval': 'Amount of Approval'},
                              hover_name='Zip',
                              hover_data=['Sum Approval'],
                              title='H-1B Visa Approval by Zip Code in North Carolina')

    # Set the map properties
    map_chart.update_geos(fitbounds="locations", visible=False)
    map_chart.update_layout(margin={"r": 0, "t": 30, "l": 0, "b": 0})

    # Display the map
    st.plotly_chart(map_chart, use_container_width=True)
    st.write("The map above displays the locations of zip codes in North Carolina, with each zip code area colored based on the sum of H-1B visa approvals. The color of the zip code areas ranges from light blue to dark blue, indicating the amount of H-1B visa approvals. Dark blue zip code areas signify higher approval rates, while light blue areas indicate lower approval rates. Foreign job seekers can utilize this map to identify potential H-1B friendly employers in specific areas within North Carolina.")
