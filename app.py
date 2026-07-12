import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================
# PAGE SETTINGS
# ==========================

st.set_page_config(
    page_title="Nassau Candy Dashboard",
    layout="wide"
)

st.title("🍬 Nassau Candy Distributor")
st.subheader("Factory-to-Customer Shipping Route Efficiency Analysis")

# ==========================
# LOAD DATA
# ==========================

df = pd.read_csv("cleaned_nassau_candy.csv")

df["Order Date"] = pd.to_datetime(df["Order Date"])

st.success("Dataset Loaded Successfully!")

# ==========================
# SIDEBAR FILTERS
# ==========================

st.sidebar.header("🔎 Dashboard Filters")

date_range = st.sidebar.date_input(
    "Select Order Date Range",
    [df["Order Date"].min(), df["Order Date"].max()]
)

regions = sorted(df["Region"].dropna().unique())

selected_region = st.sidebar.multiselect(
    "Select Region",
    regions,
    default=regions
)

states = sorted(df["State/Province"].dropna().unique())

selected_state = st.sidebar.multiselect(
    "Select State",
    states,
    default=states
)

ship_modes = sorted(df["Ship Mode"].dropna().unique())

selected_ship_mode = st.sidebar.multiselect(
    "Select Ship Mode",
    ship_modes,
    default=ship_modes
)

max_lead = int(df["Lead Time"].max())

lead_limit = st.sidebar.slider(
    "Maximum Lead Time",
    0,
    max_lead,
    max_lead
)

# ==========================
# FILTER DATA
# ==========================

filtered_df = df[
    (df["Region"].isin(selected_region))
    &
    (df["State/Province"].isin(selected_state))
    &
    (df["Ship Mode"].isin(selected_ship_mode))
    &
    (df["Lead Time"] <= lead_limit)
]

filtered_df = filtered_df[
    (filtered_df["Order Date"] >= pd.to_datetime(date_range[0]))
    &
    (filtered_df["Order Date"] <= pd.to_datetime(date_range[1]))
]

# ==========================
# FILTERED TABLE
# ==========================

st.header("📊 Filtered Shipment Data")

st.write("Total Records:", len(filtered_df))

st.dataframe(filtered_df.head(50))

# ==========================
# KPI SECTION
# ==========================

total_shipments = len(filtered_df)

avg_lead = round(filtered_df["Lead Time"].mean(),2)

total_sales = round(filtered_df["Sales"].sum(),2)

total_profit = round(filtered_df["Gross Profit"].sum(),2)

col1,col2,col3,col4 = st.columns(4)

col1.metric("Total Shipments", total_shipments)
col2.metric("Average Lead Time", f"{avg_lead} Days")
col3.metric("Total Sales", f"$ {total_sales}")
col4.metric("Total Profit", f"$ {total_profit}")

# ==========================
# ROUTE ANALYSIS
# ==========================

st.header("🚚 Route Efficiency Leaderboard")

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

fig_route = px.bar(
    route_df,
    x="Average Lead Time",
    y="Factory",
    orientation="h",
    color="Average Lead Time",
    title="Factory Shipping Performance"
)

st.plotly_chart(fig_route, use_container_width=True)

# ==========================
# STATE ANALYSIS
# ==========================

st.header("📍 Geographic Shipping Bottleneck Analysis")

state_df = filtered_df.groupby("State/Province").agg(
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
    color="Average Lead Time",
    title="Top 10 States with Highest Lead Time"
)

st.plotly_chart(fig_state, use_container_width=True)

# ==========================
# SHIP MODE ANALYSIS
# ==========================

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
    color="Ship Mode",
    title="Average Lead Time by Ship Mode"
)

st.plotly_chart(fig_ship, use_container_width=True)

# ==========================
# PIE CHART
# ==========================

st.header("📦 Shipment Distribution by Ship Mode")

fig_pie = px.pie(
    ship_df,
    names="Ship Mode",
    values="Total Shipments",
    title="Shipment Distribution"
)

st.plotly_chart(fig_pie, use_container_width=True)

# ==========================
# US MAP
# ==========================

state_codes = {
    "Alabama":"AL","Alaska":"AK","Arizona":"AZ","Arkansas":"AR",
    "California":"CA","Colorado":"CO","Connecticut":"CT","Delaware":"DE",
    "Florida":"FL","Georgia":"GA","Hawaii":"HI","Idaho":"ID",
    "Illinois":"IL","Indiana":"IN","Iowa":"IA","Kansas":"KS",
    "Kentucky":"KY","Louisiana":"LA","Maine":"ME","Maryland":"MD",
    "Massachusetts":"MA","Michigan":"MI","Minnesota":"MN",
    "Mississippi":"MS","Missouri":"MO","Montana":"MT","Nebraska":"NE",
    "Nevada":"NV","New Hampshire":"NH","New Jersey":"NJ",
    "New Mexico":"NM","New York":"NY","North Carolina":"NC",
    "North Dakota":"ND","Ohio":"OH","Oklahoma":"OK","Oregon":"OR",
    "Pennsylvania":"PA","Rhode Island":"RI","South Carolina":"SC",
    "South Dakota":"SD","Tennessee":"TN","Texas":"TX","Utah":"UT",
    "Vermont":"VT","Virginia":"VA","Washington":"WA",
    "West Virginia":"WV","Wisconsin":"WI","Wyoming":"WY"
}

state_map = filtered_df.groupby("State/Province").agg(
    {
        "Lead Time":"mean",
        "Order ID":"count"
    }
).reset_index()

state_map.rename(
    columns={
        "State/Province":"State",
        "Lead Time":"Average Lead Time",
        "Order ID":"Total Shipments"
    },
    inplace=True
)

state_map["State"] = state_map["State"].map(state_codes)

fig_map = px.choropleth(
    state_map,
    locations="State",
    locationmode="USA-states",
    color="Average Lead Time",
    scope="usa",
    hover_name="State",
    hover_data={
        "Average Lead Time":True,
        "Total Shipments":True
    },
    color_continuous_scale="Reds",
    title="Average Shipping Lead Time by State"
)

st.header("🗺 US Shipping Lead Time Map")

st.plotly_chart(fig_map, use_container_width=True)

# ==========================
# FOOTER
# ==========================

st.markdown("---")

st.markdown(
    "### Developed by **Oshin Kalbande**"
)

st.caption(
    "Nassau Candy Distributor | Factory-to-Customer Shipping Route Efficiency Analysis"
)
