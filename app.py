import streamlit as st
import altair as alt
import pandas as pd
import numpy as np

st.set_page_config(layout="wide")
regions = ["LATAM", "EMEA", "NA", "APAC"]
colors = [
    "#aa423a",
    "#f6b404",
    "#327a88",
    "#303e55",
    "#c7ab84",
    "#b1dbaa",
    "#feeea5",
    "#3e9a14",
    "#6e4e92",
    "#c98149",
    "#d1b844",
    "#8db6d8",
]
months = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]
st.title("2022 Sales Dashboard")


@st.cache_data
def get_data():
    dates = pd.date_range(start="1/1/2022", end="12/31/2022")
    data = pd.DataFrame()
    sellers = {
        "LATAM": ["S01", "S02", "S03"],
        "EMEA": ["S10", "S11", "S12", "S13"],
        "NA": ["S21", "S22", "S23", "S24", "S25", "S26"],
        "APAC": ["S31", "S32", "S33", "S34", "S35", "S36"],
    }
    rows = 25000
    data["transaction_date"] = np.random.choice([str(i) for i in dates], size=rows)
    data["region"] = np.random.choice(regions, size=rows, p=[0.1, 0.3, 0.4, 0.2])
    data["transaction_amount"] = np.random.uniform(100, 250000, size=rows).round(2)
    data["seller"] = data.apply(
        lambda x: np.random.choice(sellers.get(x["region"])), axis=1
    )
    data["month"] = pd.to_datetime(data["transaction_date"]).dt.month    
    return data.sort_values(by="transaction_date").reset_index(drop=True)


sales_data = get_data()
sales_data
region_select = alt.selection_single(fields=["region"], empty="all")
seller_select = alt.selection_single(fields=["seller"], empty="all")
month_select = alt.selection_single(fields=["month"], empty="all")

region_pie = (
    (
        alt.Chart(sales_data)
        .mark_arc(innerRadius=50)
        .encode(
            theta=alt.Theta(
                "transaction_amount",
                type="quantitative",
                aggregate="sum",
                title="Sum of Transactions",
            ),
            color=alt.Color(
                field="region",
                type="nominal",
                scale=alt.Scale(domain=regions, range=colors),
                title="Region",
            ),
            opacity=alt.condition(region_select, alt.value(1), alt.value(0.25)),
        )
    )
    .add_selection(region_select)
    .transform_filter(seller_select)
    .transform_filter(month_select)
    .properties(title="Region Sales")
)

region_summary = (
    alt.Chart(sales_data)
    .mark_bar()
    .encode(
        x=alt.X(
            "month:T",
            title="Month",
        ),
        y=alt.Y(
            "transaction_amount:Q",
            aggregate="sum",
            title="Total Sales",
        ),
        color=alt.Color(
            "region:N",
            title="Regions",
            scale=alt.Scale(domain=regions, range=colors),
            legend=alt.Legend(
                direction="vertical",
                symbolType="triangle-left",
                tickCount=4,
            ),
        ),
        tooltip=alt.Tooltip(["month:T", "sum(transaction_amount):Q"]),
        opacity=alt.condition(month_select, alt.value(1), alt.value(0.25)),
    )
    .transform_filter(region_select)
    .transform_filter(seller_select)
    .add_selection(month_select)
    .properties(width=700, title="Monthly Sales")
)


sellers_monthly_pie = (
    (
        alt.Chart(sales_data)
        .mark_arc(innerRadius=10)
        .encode(
            theta=alt.Theta(
                field="transaction_amount",
                type="quantitative",
                aggregate="sum",
                title="Total Transactions",
            ),
            color=alt.Color(
                "month(transaction_date)",
                type="temporal",
                title="Month",
                scale=alt.Scale(domain=months, range=colors),
                legend=alt.Legend(
                    direction="vertical",
                    symbolType="triangle-left",
                    tickCount=12,
                ),
            ),
            facet=alt.Facet(
                field="seller",
                type="nominal",
                columns=8,
                title="Sellers",
            ),
            tooltip=alt.Tooltip(["sum(transaction_amount)", "month(transaction_date)"]),
            opacity=alt.condition(seller_select, alt.value(1), alt.value(0.25)),

        )
    )
    .transform_filter(month_select)
    .transform_filter(region_select)
    .add_selection(seller_select)
    .properties(width=150, height=150, title="Sellers transactions per month")
)

top_row = region_pie | region_summary
full_chart = top_row & sellers_monthly_pie
st.altair_chart(full_chart)

# with st.sidebar:
#     st.write('sidebar')

tab1, tab2 = st.tabs(["tab1", "tab2"])
with tab1:
    "tab1"
    top_row = region_pie | region_summary
    st.altair_chart(top_row)

with tab2:
    "Tab2"
    st.altair_chart(sellers_monthly_pie)


