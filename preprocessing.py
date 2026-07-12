import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv(
    r"C:\Users\anil\Downloads\40811eyack.com.MAIL_xsbsxxypt8dh6!App\Nassau Candy Distributor.csv"
)

# Convert Order Date and Ship Date to Date format

df["Order Date"] = pd.to_datetime(
    df["Order Date"],
    format="mixed",
    dayfirst=True
)

df["Ship Date"] = pd.to_datetime(
    df["Ship Date"],
    format="mixed",
    dayfirst=True
)

# Calculate Shipping Lead Time

df["Lead Time"] = (
    df["Ship Date"] - df["Order Date"]
).dt.days

# Remove invalid lead times (if any)
df = df[df["Lead Time"] >= 0]

# Display dataset
print(df.head())
print(df.info())
print(df.columns)
print(df.shape)
print(df.isnull().sum())

# Check data types
print(df.dtypes)

# Display Order Date, Ship Date and Lead Time
print(df[["Order Date", "Ship Date", "Lead Time"]].head())

# Product Name → Factory Mapping
factory_mapping = {

    "Wonka Bar - Nutty Crunch Surprise": "Lot's O' Nuts",
    "Wonka Bar - Fudge Mallows": "Lot's O' Nuts",
    "Wonka Bar -Scrumdiddlyumptious": "Lot's O' Nuts",

    "Wonka Bar - Milk Chocolate": "Wicked Choccy's",
    "Wonka Bar - Triple Dazzle Caramel": "Wicked Choccy's",

    "Laffy Taffy": "Sugar Shack",
    "SweeTARTS": "Sugar Shack",
    "Nerds": "Sugar Shack",
    "Fun Dip": "Sugar Shack",
    "Fizzy Lifting Drinks": "Sugar Shack",

    "Everlasting Gobstopper": "Secret Factory",
    "Lickable Wallpaper": "Secret Factory",
    "Wonka Gum": "Secret Factory",

    "Hair Toffee": "The Other Factory",
    "Kazookles": "The Other Factory"
}

# Create Factory Column
df["Factory"] = df["Product Name"].map(factory_mapping)

# Display Product Name and Factory
print(df[["Product Name", "Factory"]].head(15))

# Check if any products are not mapped
print("Missing Factory Values:", df["Factory"].isnull().sum())


# ===========================
# STEP 12: CREATE ROUTE COLUMN
# ===========================

# Create Route Column
df["Route"] = df["Factory"] + " → " + df["State/Province"]

# Display Factory, State and Route
print(df[["Factory", "State/Province", "Route"]].head(10))

# Check if any Route values are missing
print("Missing Route Values:", df["Route"].isnull().sum())

# Save cleaned dataset (optional but recommended)
df.to_csv("cleaned_nassau_candy.csv", index=False)

print(df.columns.tolist())

df["Route"] = df["Factory"] + " → " + df["State/Province"]
# Display Factory, State and Route
print(df[["Factory", "State/Province", "Route"]].head(10))

# Check if any Route values are missing
print("Missing Route Values:", df["Route"].isnull().sum())

# Save cleaned dataset
df.to_csv("cleaned_nassau_candy.csv", index=False)

print("✅ Cleaned dataset saved successfully!")

# Total Shipments
total_shipments = len(df)
print("Total Shipments:", total_shipments)

# Average Lead Time
average_lead_time = df["Lead Time"].mean()
print("Average Lead Time:", round(average_lead_time, 2), "days")

# Total Sales
total_sales = df["Sales"].sum()
print("Total Sales: $", round(total_sales, 2))

# Total Gross Profit
total_profit = df["Gross Profit"].sum()
print("Total Gross Profit: $", round(total_profit, 2))

# Total Units
total_units = df["Units"].sum()
print("Total Units Sold:", total_units)

# Delay Frequency
delay_frequency = (df["Lead Time"] > 5).mean() * 100

print("Delay Frequency:", round(delay_frequency, 2), "%")

# ===========================
# STEP 14 : ROUTE SUMMARY
# ===========================

route_summary = df.groupby("Route").agg(
    {
        "Order ID": "count",
        "Lead Time": "mean",
        "Sales": "sum",
        "Gross Profit": "sum",
        "Units": "sum"
    }
).reset_index()

route_summary.rename(
    columns={
        "Order ID": "Total Shipments",
        "Lead Time": "Average Lead Time",
        "Sales": "Total Sales",
        "Gross Profit": "Total Profit",
        "Units": "Total Units"
    },
    inplace=True
)

print(route_summary.head())

fastest_routes = route_summary.sort_values(
    "Average Lead Time"
)

print(fastest_routes.head(10))

slowest_routes = route_summary.sort_values(
    "Average Lead Time",
    ascending=False
)

print(slowest_routes.head(10))

route_summary.to_csv(
    "route_summary.csv",
    index=False
)


from sklearn.preprocessing import MinMaxScaler


# ===========================
# STEP 15 : ROUTE EFFICIENCY SCORE
# ===========================

scaler = MinMaxScaler()


route_summary["Lead Time Score"] = scaler.fit_transform(
    route_summary[["Average Lead Time"]]
)


route_summary["Efficiency Score"] = (
    1 - route_summary["Lead Time Score"]
) * 100


print(
    route_summary[
        ["Route",
         "Average Lead Time",
         "Efficiency Score"]
    ].head(10)
)


# Ranking
ranked_routes = route_summary.sort_values(
    "Efficiency Score",
    ascending=False
)

print("Top 10 Efficient Routes")
print(ranked_routes.head(10))


# Worst routes
worst_routes = route_summary.sort_values(
    "Efficiency Score"
)

print("Bottom 10 Routes")
print(worst_routes.head(10))


# Save file
route_summary.to_csv(
    "route_efficiency_analysis.csv",
    index=False
)

# ===========================
# ROUTE EFFICIENCY CHART
# ===========================

top_routes = route_summary.sort_values(
    "Efficiency Score",
    ascending=False
).head(10)


plt.figure(figsize=(10,6))

sns.barplot(
    data=top_routes,
    x="Efficiency Score",
    y="Route"
)

plt.title("Top 10 Most Efficient Shipping Routes")
plt.xlabel("Efficiency Score")
plt.ylabel("Route")

plt.show()


# ===========================
# WORST ROUTES CHART
# ===========================

worst_routes = route_summary.sort_values(
    "Average Lead Time",
    ascending=False
).head(10)


plt.figure(figsize=(10,6))

sns.barplot(
    data=worst_routes,
    x="Average Lead Time",
    y="Route"
)

plt.title("Top 10 Slowest Shipping Routes")
plt.xlabel("Average Lead Time (Days)")
plt.ylabel("Route")

plt.show()

# ===========================
# SHIP MODE CHART
# ===========================

plt.figure(figsize=(8,5))

sns.barplot(
    data=ship_mode_summary,
    x="Ship Mode",
    y="Average Lead Time"
)

plt.title("Average Lead Time by Ship Mode")
plt.xlabel("Shipping Mode")
plt.ylabel("Days")

plt.show()


# ===========================
# STATE BOTTLENECK CHART
# ===========================

bottleneck_states = state_summary.sort_values(
    "Average Lead Time",
    ascending=False
).head(10)


plt.figure(figsize=(10,6))

sns.barplot(
    data=bottleneck_states,
    x="Average Lead Time",
    y="State/Province"
)

plt.title("Top 10 State Shipping Bottlenecks")
plt.xlabel("Average Lead Time (Days)")
plt.ylabel("State")

plt.show()


# ===========================
# STEP 16 : SHIP MODE ANALYSIS
# ===========================

ship_mode_summary = df.groupby("Ship Mode").agg(
    {
        "Order ID": "count",
        "Lead Time": "mean",
        "Sales": "sum",
        "Gross Profit": "sum"
    }
).reset_index()


ship_mode_summary.rename(
    columns={
        "Order ID": "Total Shipments",
        "Lead Time": "Average Lead Time",
        "Sales": "Total Sales",
        "Gross Profit": "Total Profit"
    },
    inplace=True
)


print(ship_mode_summary)


# Delay analysis
delay_by_mode = df.groupby("Ship Mode").apply(
    lambda x: (x["Lead Time"] > 5).mean() * 100
).reset_index()


delay_by_mode.columns = [
    "Ship Mode",
    "Delay Frequency (%)"
]


print(delay_by_mode)


# Sort by speed
print(
    ship_mode_summary.sort_values(
        "Average Lead Time"
    )
)


# Save result
ship_mode_summary.to_csv(
    "ship_mode_analysis.csv",
    index=False
)

# ===========================
# STEP 17 : GEOGRAPHIC BOTTLENECK ANALYSIS
# ===========================

state_summary = df.groupby("State/Province").agg(
    {
        "Order ID": "count",
        "Lead Time": "mean",
        "Sales": "sum",
        "Gross Profit": "sum"
    }
).reset_index()


state_summary.rename(
    columns={
        "Order ID": "Total Shipments",
        "Lead Time": "Average Lead Time",
        "Sales": "Total Sales",
        "Gross Profit": "Total Profit"
    },
    inplace=True
)


print(state_summary)


# Slowest states
slow_states = state_summary.sort_values(
    "Average Lead Time",
    ascending=False
)

print("Top Bottleneck States")
print(slow_states.head(10))


# High volume + slow states
high_volume_slow = state_summary[
    (state_summary["Total Shipments"] > state_summary["Total Shipments"].mean())
    &
    (state_summary["Average Lead Time"] > state_summary["Average Lead Time"].mean())
]

print("High Volume + Poor Performance States")
print(high_volume_slow)


# Save file
state_summary.to_csv(
    "state_bottleneck_analysis.csv",
    index=False
)
