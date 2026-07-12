import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Nassau Candy Dashboard",
    layout="wide"
)

st.title("🍬 Nassau Candy Distributor")
st.subheader("Factory-to-Customer Shipping Route Efficiency Analysis")


# Load Dataset
df = pd.read_csv("cleaned_nassau_candy.csv")

st.success("Dataset Loaded Successfully!")



# ===========================
# FILTERS
# ===========================

st.sidebar.header("🔎 Dashboard Filters")


# Convert dates
df["Order Date"] = pd.to_datetime(
    df["Order Date"]
)


date_range = st.sidebar.date_input(
    "Select Order Date Range",
    [
        df["Order Date"].min(),
        df["Order Date"].max()
    ]
)

# Region Filter

regions = df["Region"].unique()

selected_region = st.sidebar.multiselect(
    "Select Region",
    regions,
    default=regions
)


# State Filter

states = df["State/Province"].unique()

selected_state = st.sidebar.multiselect(
    "Select State",
    states,
    default=states
)

# Ship Mode Filter

ship_modes = df["Ship Mode"].unique()


selected_ship_mode = st.sidebar.multiselect(
    "Select Ship Mode",
    ship_modes,
    default=ship_modes
)

# Lead Time Filter

max_lead_time = int(
    df["Lead Time"].max()
)


lead_time_limit = st.sidebar.slider(
    "Maximum Lead Time (Days)",
    0,
    max_lead_time,
    max_lead_time
)

# ===========================
# APPLY FILTERS
# ===========================


filtered_df = df[
    (df["Region"].isin(selected_region))
    &
    (df["State/Province"].isin(selected_state))
    &
    (df["Ship Mode"].isin(selected_ship_mode))
    &
    (df["Lead Time"] <= lead_time_limit)
]


filtered_df = filtered_df[
    (filtered_df["Order Date"] >= pd.to_datetime(date_range[0]))
    &
    (filtered_df["Order Date"] <= pd.to_datetime(date_range[1]))
]

st.header("📊 Filtered Shipment Data")

st.write(
    "Total Records:",
    len(filtered_df)
)

st.dataframe(
    filtered_df.head(50)
)





# ===========================
# KPI Calculations (Filtered Data)
# ===========================

total_shipments = len(filtered_df)


avg_lead_time = round(
    filtered_df["Lead Time"].mean(),
    2
)


total_sales = round(
    filtered_df["Sales"].sum(),
    2
)


total_profit = round(
    filtered_df["Gross Profit"].sum(),
    2
)

st.header("📊 Filtered Shipment Data")

st.write(
    "Total Records:",
    len(filtered_df)
)

st.dataframe(
    filtered_df.head(50)
)


# KPI Display

col1, col2, col3, col4 = st.columns(4)


with col1:
    st.metric(
        "Total Shipments",
        total_shipments
    )


with col2:
    st.metric(
        "Average Lead Time",
        str(avg_lead_time) + " Days"
    )


with col3:
    st.metric(
        "Total Sales",
        "$ " + str(total_sales)
    )


with col4:
    st.metric(
        "Total Profit",
        "$ " + str(total_profit)
    )


# Route Efficiency Chart

st.header("🚚 Route Efficiency Leaderboard")


# Route Analysis using Filtered Data

route_df = filtered_df.groupby("Factory").agg(
    {
        "Lead Time":"mean",
        "Order ID":"count"
    }
).reset_index()


route_df.rename(
    columns={
        "Lead Time":"Average Lead Time",
        "Order ID":"Total Shipments"
    },
    inplace=True
)



fig = px.bar(
    route_df,
    x="Average Lead Time",
    y="Factory",
    orientation="h",
    title="Factory Shipping Performance"
)


st.plotly_chart(
    fig,
    use_container_width=True
)

# ==================================
# Geographic Shipping Analysis
# ==================================

st.header("📍 Geographic Shipping Bottleneck Analysis")


state_df = filtered_df.groupby(
    "State/Province"
).agg(
    {
        "Lead Time":"mean",
        "Order ID":"count"
    }
).reset_index()


state_df.rename(
    columns={
        "Lead Time":"Average Lead Time",
        "Order ID":"Total Shipments"
    },
    inplace=True
)


fig_state = px.bar(
    state_df.sort_values(
        "Average Lead Time",
        ascending=False
    ).head(10),
    x="Average Lead Time",
    y="State/Province",
    orientation="h",
    title="Top 10 States with Highest Shipping Lead Time"
)

# ==================================
# Ship Mode Performance
# ==================================

st.header("🚢 Ship Mode Performance Analysis")

ship_df = filtered_df.groupby("Ship Mode").agg(
    {
        "Lead Time":"mean",
        "Order ID":"count"
    }
).reset_index()


ship_df.rename(
    columns={
        "Lead Time":"Average Lead Time",
        "Order ID":"Total Shipments"
    },
    inplace=True
)

fig_ship = px.bar(
    ship_df,
    x="Ship Mode",
    y="Average Lead Time",
    title="Average Lead Time by Ship Mode"
)


st.header("📦 Shipment Distribution by Ship Mode")


fig_pie = px.pie(
    ship_df,
    names="Ship Mode",
    values="Total Shipments",
    title="Shipment Volume by Shipping Method"
)

# ==================================
# State Summary for Map
# ==================================

state_map = filtered_df.groupby("State/Province").agg(
    {
        "Lead Time": "mean",
        "Order ID": "count"
    }
).reset_index()

state_map.rename(
    columns={
        "State/Province": "State",
        "Lead Time": "Average Lead Time",
        "Order ID": "Total Shipments"
    },
    inplace=True
)

st.header("🗺 US Shipping Lead Time Map")

fig_map = px.choropleth(
    state_map,
    locations="State",
    locationmode="USA-states",
    color="Average Lead Time",
    scope="usa",
    hover_name="State",
    hover_data={
        "Average Lead Time": True,
        "Total Shipments": True
    },
    color_continuous_scale="Reds",
    title="Average Shipping Lead Time by State"
)

print(df["State/Province"].unique())

state_codes = {
    "Alabama":"AL",
    "Alaska":"AK",
    "Arizona":"AZ",
    "Arkansas":"AR",
    "California":"CA",
    "Colorado":"CO",
    "Connecticut":"CT",
    "Delaware":"DE",
    "Florida":"FL",
    "Georgia":"GA",
    "Hawaii":"HI",
    "Idaho":"ID",
    "Illinois":"IL",
    "Indiana":"IN",
    "Iowa":"IA",
    "Kansas":"KS",
    "Kentucky":"KY",
    "Louisiana":"LA",
    "Maine":"ME",
    "Maryland":"MD",
    "Massachusetts":"MA",
    "Michigan":"MI",
    "Minnesota":"MN",
    "Mississippi":"MS",
    "Missouri":"MO",
    "Montana":"MT",
    "Nebraska":"NE",
    "Nevada":"NV",
    "New Hampshire":"NH",
    "New Jersey":"NJ",
    "New Mexico":"NM",
    "New York":"NY",
    "North Carolina":"NC",
    "North Dakota":"ND",
    "Ohio":"OH",
    "Oklahoma":"OK",
    "Oregon":"OR",
    "Pennsylvania":"PA",
    "Rhode Island":"RI",
    "South Carolina":"SC",
    "South Dakota":"SD",
    "Tennessee":"TN",
    "Texas":"TX",
    "Utah":"UT",
    "Vermont":"VT",
    "Virginia":"VA",
    "Washington":"WA",
    "West Virginia":"WV",
    "Wisconsin":"WI",
    "Wyoming":"WY"
}

state_map["State"] = state_map["State"].map(state_codes)

left_col, right_col = st.columns(2)

with left_col:
    st.plotly_chart(fig_ship, use_container_width=True)

with right_col:
    st.plotly_chart(fig_state, use_container_width=True)

    st.markdown("---")
st.markdown(
    "Developed by **Oshin Kalbande** | Nassau Candy Distributor Shipping Route Efficiency Analysis"
)

