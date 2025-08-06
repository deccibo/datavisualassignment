import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Data App Assignment, Declan O'Halloran")

# Load the data
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)
df["Order_Date"] = pd.to_datetime(df["Order_Date"])

interactive_df = df.copy()

st.write("### Input Data and Examples")
st.dataframe(df)

# Default bar chart without aggregation
st.bar_chart(df, x="Category", y="Sales")

# Aggregated bar chart
st.dataframe(df.groupby("Category").sum(numeric_only=True))
st.bar_chart(df.groupby("Category", as_index=False).sum(numeric_only=True), x="Category", y="Sales", color="#04f")

# Monthly sales trend
df.set_index('Order_Date', inplace=True)
sales_by_month = df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()
st.dataframe(sales_by_month)
st.line_chart(sales_by_month, y="Sales")



#Catdropdown
category_selected = st.selectbox("Select a Category", interactive_df["Category"].unique())

#SubCat dropdown
filtered_subcats = interactive_df[interactive_df["Category"] == category_selected]["Sub_Category"].unique()
subcats_selected = st.multiselect("Select Sub-Category", filtered_subcats)

#linechart of sales
if subcats_selected:
    filtered_df = interactive_df[
        (interactive_df["Category"] == category_selected) &
        (interactive_df["Sub_Category"].isin(subcats_selected))
    ]

    sales_trend = (
        filtered_df.groupby(pd.Grouper(key="Order_Date",freq='M'))["Sales"]
        .sum()
        .reset_index()
        .set_index("Order_Date")
    )

    st.line_chart(sales_trend, y="Sales")

    #metrics
    total_sales = filtered_df["Sales"].sum()
    total_profit = filtered_df["Profit"].sum()
    profit_margin = (total_profit / total_sales) * 100 if total_sales != 0 else 0

    #delta
    overall_profit_margin = (interactive_df["Profit"].sum() / interactive_df["Sales"].sum()) * 100

    st.metric("Total Sales", f"${total_sales:,.2f}")
    st.metric("Total Profit", f"${total_profit:,.2f}")
    st.metric(
        "Profit Margin (%)",
        f"{profit_margin:.2f}%",
        delta=f"{(profit_margin - overall_profit_margin):+.2f}%",
    )
else:
    st.info("Please select at least one Sub-Category to view charts and metrics.")
