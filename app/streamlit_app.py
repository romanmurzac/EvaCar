# *****IMPORTS*****
# Import necessary packages
import streamlit as st
import pandas as pd
import altair as alt
import os

# *****UTILITIES*****
# Define constants and variables
DATA_SOURCE = {"December 2023": "23-12-10",
               "January 2024": "24-01-10",}
dir_path = os.path.dirname(os.path.realpath(__file__))


# Define function to read data
def select_dataset(dataset_name: str) -> pd.DataFrame:
    full_path = dir_path + f"/data/ProcessedDataDB-{DATA_SOURCE[dataset_name]}.csv"
    return pd.read_csv(full_path)


# Define function to select file
def select_value() -> str:
    return list(DATA_SOURCE.keys())


# *****SETTINGS*****
# Set up page characteristics
st.set_page_config(
    page_title="EvaCar",
    page_icon=dir_path + "/favicon.ico",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get help": "https://www.linkedin.com/in/roman-murzac/",
        "Report a bug": "https://github.com/romanmurzac/EvaCar",
        "About": "EvaCar - Evaluation & Prediction on Romanian second-hand car market: https://github.com/romanmurzac/EvaCar",
    },
)

# Link the CSS file
with open(dir_path + "/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# *****SIDEBAR*****
# Sidebar - add logo and description
st.sidebar.image(dir_path + '/logo.png', caption='Evaluation & Prediction of Romanian second-hand car market')
st.sidebar.markdown("""---""")

# Sidebar - select data source
st.sidebar.subheader("Data source")
data_source = st.sidebar.selectbox("Select data", (select_value()))

# Sidebar - select fuel type
st.sidebar.subheader("Top 10 sold brands")
container = st.sidebar.container()
all = st.sidebar.checkbox("Select all", value=True)
if all:
    fuel_type = container.multiselect("Select fuel type",
         list(select_dataset(data_source)["fuel"].unique()),
         list(select_dataset(data_source)["fuel"].unique()))
else:
    fuel_type =  container.multiselect("Select fuel type",
        list(select_dataset(data_source)["fuel"].unique()))

# Sidebar - select year
st.sidebar.subheader("Average price by year")
years_list = list(select_dataset(data_source)["year"].unique())
selected_years = st.sidebar.slider("Select year", min_value=min(years_list), max_value=max(years_list), value=[min(years_list), max(years_list)], step=1)

# Sidebar - Footer
st.sidebar.markdown(
    """
    ---
    Created with ❤️ by [Roman Murzac](https://www.linkedin.com/in/roman-murzac/).
    """
)

# *****DATA*****
# Data definition
std_dataset = select_dataset("December 2023")
dataset = select_dataset(data_source)

no_cars = dataset.shape[0]
no_cars_delta = dataset.shape[0] - std_dataset.shape[0]

max_price = int(dataset["price"].max())
max_price_delta = int(dataset["price"].max()) - int(std_dataset["price"].max())

min_price = int(dataset["price"].min())
min_price_delta = int(dataset["price"].min()) - int(std_dataset["price"].min())

max_mileage = int(dataset["mileage"].max())
max_mileage_delta = int(dataset["mileage"].max()) - int(std_dataset["mileage"].max())

old_car = int(dataset["year"].min())
old_car_delta = int(dataset["year"].min()) - int(std_dataset["year"].min())

max_capacity = int(dataset["capacity"].max())
max_capacity_delta = int(dataset["capacity"].max()) - int(std_dataset["capacity"].max())

max_power = int(dataset["power"].max())
max_power_delta = int(dataset["power"].max()) - int(std_dataset["power"].max())

top_fuel = dataset["fuel"].value_counts().sort_values(ascending=False).head(1).index[:].to_list()[0]

top_10_manufact = pd.DataFrame()
top_10_manufact["count"] = dataset[dataset["fuel"].isin(fuel_type)]["manufacturer"].value_counts().sort_values(ascending=False).head(10)
top_10_manufact["names"] = top_10_manufact.index[:].to_list()

avg_price = pd.DataFrame()
avg_price["price"]= dataset.loc[(dataset["year"] >= int(selected_years[0])) & (dataset["year"] <= int(selected_years[1]))].groupby('year')['price'].mean()
avg_price["year"] = avg_price.index[:].to_list()

# *****GRAPHS*****
# Row A - Metrics
st.markdown("### Key Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Number of cars", f'{no_cars:,}', f'{no_cars_delta:,}')
col2.metric("Max car price [Eur]", f'{max_price:,}', f'{max_price_delta:,}')
col3.metric("Max car mileage [km]", f'{max_mileage:,}', f'{max_mileage_delta:,}')
col4.metric("Max capacity [cm3]", f'{max_capacity:,}', f'{max_capacity_delta:,}')
col1, col2, col3, col4 = st.columns(4)
col1.metric("Top fuel type", top_fuel)
col2.metric("Min car price [Eur]", f'{min_price:,}', f'{min_price_delta:,}')
col3.metric("Oldest car [Year]", old_car, old_car_delta)
col4.metric("Max power [HP]", f'{max_power:,}', f'{max_power_delta:,}')
st.text("")
st.text("")
st.text("")
st.text("")
st.text("")

# Row B - Bar Chart
st.markdown("### Top 10 sold brands")
st.altair_chart(alt.Chart(top_10_manufact).mark_bar().encode(
    x=alt.X('names', sort=None, title="Brand"),
    y=alt.Y('count', title="No. cars")
), use_container_width=True)

# Row C - Scatter Chart
st.markdown("### Price by county")
st.scatter_chart(dataset, x="county", y="price", color="fuel", height=500)

# Row D - Line Chart
st.markdown("### Average price by year")
st.altair_chart(alt.Chart(avg_price).mark_line().encode(
    x=alt.X("year", sort=None, title="Year", ),
    y=alt.Y("price",  title="Avg. price")
), use_container_width=True)


# *****PREDICTION*****
# # Define user inputs
# predict_brand = st.selectbox("Select Brand", list(dataset["manufacturer"].unique()))
# predict_model = st.selectbox("Select Model", list(dataset[dataset["manufacturer"] == predict_brand]["model"].unique()))
# predict_mileage = int(st.text_input('Select Mileage', '100000'))
# predict_capacity = int(st.text_input('Select Capacity', '1500'))
# predict_power = int(st.text_input('Select Power', '100'))
# predict_year = st.selectbox("Select Year", sorted(list(select_dataset(data_source)["year"].unique()), reverse=True))
# predict_fuel = st.selectbox("Select Fuel", list(dataset["fuel"].unique()))

# # Define new input data
# new_data = {'manufacturer': [predict_brand],
#             'model': [predict_model], 
#             'mileage': [predict_mileage], 
#             'capacity': [predict_capacity], 
#             'power': [predict_power], 
#             'year': [predict_year], 
#             'fuel': [predict_fuel]
#             }

# st.write('The predicted price is', predict_model)
