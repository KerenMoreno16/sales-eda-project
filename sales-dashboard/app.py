import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

# -----------------------------------
# LOAD DATA
# -----------------------------------

@st.cache_data
def load_data():
    df = pd.read_csv("./data/SampleSuperstore.csv")
    return df

df = load_data()

# -----------------------------------
# SIDEBAR
# -----------------------------------

st.sidebar.header("Filters")

region = st.sidebar.multiselect(
    "Select Region",
    options=df['Region'].unique(),
    default=df['Region'].unique()
)

category = st.sidebar.multiselect(
    "Select Category",
    options=df['Category'].unique(),
    default=df['Category'].unique()
)

filtered_df = df[
    (df['Region'].isin(region)) &
    (df['Category'].isin(category))
]

# -----------------------------------
# TITLE
# -----------------------------------

st.title("Superstore Sales Dashboard")

st.markdown("""
Interactive dashboard for exploratory analysis of retail sales data.
""")

# -----------------------------------
# KPI CARDS
# -----------------------------------

total_sales = filtered_df['Sales'].sum()
total_profit = filtered_df['Profit'].sum()

col1, col2, col3 = st.columns(3)

col1.metric("Total Sales", f"${total_sales:,.0f}")
col2.metric("Total Profit", f"${total_profit:,.0f}")

# -----------------------------------
# SALES BY CATEGORY
# -----------------------------------

category_sales = filtered_df.groupby('Category')['Sales'].sum().reset_index()

fig_category = px.bar(
    category_sales,
    x='Category',
    y='Sales',
    title='Sales by Category',
    text_auto=True
)

st.plotly_chart(fig_category, use_container_width=True)

# -----------------------------------
# PROFIT BY REGION
# -----------------------------------

region_profit = filtered_df.groupby('Region')['Profit'].sum().reset_index()

fig_region = px.pie(
    region_profit,
    names='Region',
    values='Profit',
    title='Profit by Region'
)

st.plotly_chart(fig_region, use_container_width=True)

# -----------------------------------
# TOP PRODUCTS
# -----------------------------------

top_products = (
    filtered_df.groupby('Sub-Category')['Sales']
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig_products = px.bar(
    top_products,
    x='Sales',
    y='Sub-Category',
    orientation='h',
    title='Top 10 Products by Sales'
)

st.plotly_chart(fig_products, use_container_width=True)

# -----------------------------------
# DISCOUNT VS PROFIT
# -----------------------------------

fig_scatter = px.scatter(
    filtered_df,
    x='Discount',
    y='Profit',
    size='Sales',
    color='Category',
    title='Discount vs Profit'
)

st.plotly_chart(fig_scatter, use_container_width=True)

# -----------------------------------
# FOOTER
# -----------------------------------

st.markdown("---")
st.markdown("Created with Streamlit • Data Analysis Portfolio Project")