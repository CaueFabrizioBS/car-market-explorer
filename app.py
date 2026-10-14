"""Car Market Explorer: a Streamlit app for used car listings."""

import pandas as pd
import plotly.express as px
import streamlit as st


@st.cache_data
def load_data():
    """Load the cleaned vehicles dataset.

    The date column is parsed because CSV files do not keep data types.
    """
    return pd.read_csv("datasets/vehicles_clean.csv", parse_dates=["date_posted"])


def plot_price_histogram(df):
    """Build the histogram of listing prices.

    The y-axis is logarithmic, so each step represents ten times more
    listings.
    """
    return px.histogram(
        df,
        x="price",
        nbins=60,
        title="<b>Distribution of Car Prices</b>",
        color_discrete_sequence=["#2E86AB"],
        opacity=0.85,
        log_y=True,
        width=700,
        height=400,
    ).update_yaxes(dtick=1, tickformat=",")


def plot_price_vs_odometer(df):
    """Build the scatter plot of price vs. odometer.

    Each dot is a car listing from a random sample of up to 2,000 rows.
    The correlation between price and odometer is shown with a LOWESS
    trendline.
    """
    return px.scatter(
        df.sample(min(2000, len(df)), random_state=32),
        x="odometer",
        y="price",
        opacity=0.7,
        trendline="lowess",
        trendline_color_override="#E4572E",
        color_discrete_sequence=["#2E86AB"],
        range_y=[0, 60000],
        title="<b>Price vs. Odometer</b>",
        width=700,
        height=450,
    )


def plot_price_by_condition(df):
    """Build the box plot of price by condition.

    Each box represents the distribution of prices for a given condition.
    """
    return px.box(
        df,
        x="condition",
        y="price",
        category_orders={
            "condition": ["new", "like new", "excellent", "good", "fair", "salvage"]
        },
        color_discrete_sequence=["#2E86AB"],
        range_y=[0, 80000],
        title="<b>Price by Vehicle Condition</b>",
        width=700,
        height=400,
    )


def plot_top_brands(df):
    """Build the bar chart of the top 10 brands by number of listings.

    Each bar represents a brand and its height is the number of listings
    for that brand.
    """
    return px.bar(
        df["brand"].value_counts().head(10).reset_index(),
        x="brand",
        y="count",
        text_auto=",d",
        color_discrete_sequence=["#2E86AB"],
        opacity=0.85,
        title="<b>Top 10 Brands by Number of Listings</b>",
        labels={"brand": "Brand", "count": "Number of listings"},
        width=700,
        height=400,
    ).update_traces(textangle=0)


def plot_top_cars(df):
    """Build the bar chart of the top 5 most listed cars.

    Each bar represents a car and its length is the number of listings
    for that car. The top three get medals.
    """
    return (
        px.bar(
            df["car_name"]
            .value_counts()
            .head(5)
            .reset_index()
            .assign(
                label=lambda d: pd.Series(["🥇", "🥈", "🥉", "4th", "5th"])
                + " "
                + d["car_name"].str.title()
            ),
            x="count",
            y="label",
            color="label",
            orientation="h",
            text_auto=",d",
            color_discrete_sequence=[
                "#FFD700",
                "#C0C0C0",
                "#CD7F32",
                "#9AA5B1",
                "#9AA5B1",
            ],
            title="<b>Top 5 Most Listed Cars</b>",
            labels={"count": "Number of listings", "label": ""},
            width=800,
            height=400,
        )
        .update_layout(
            showlegend=False,
            hovermode=False,
            yaxis={"categoryorder": "total ascending", "automargin": True},
        )
        .update_traces(textangle=0)
    )


def plot_transmission_share(df):
    """Build the pie chart of listings by transmission type.

    Each slice represents a transmission type: automatic, manual or other.
    """
    return px.pie(
        df,
        names="transmission",
        color_discrete_sequence=["#2E86AB", "#67CC58", "#EBAB36"],
        title="<b>Listings by Transmission Type</b>",
        width=700,
        height=400,
    )


def plot_4wd_share(df):
    """Build the pie chart of 4WD listings.

    Each slice represents the share of 4WD and non-4WD listings.
    """
    return px.pie(
        names=df["is_4wd"].map({True: "4WD", False: "Not 4WD"}),
        color_discrete_sequence=["#2E86AB", "#67CC58"],
        title="<b>Share of 4WD Listings</b>",
        width=700,
        height=400,
    )


st.title("Car Market Explorer")

all_df = load_data()

DEFAULT_BRANDS = ["ford", "toyota", "kia", "bmw", "ram", "mercedes-benz"]

st.sidebar.header("Filters")
selected_brands = st.sidebar.multiselect(
    "Brands", options=sorted(all_df["brand"].unique()), default=DEFAULT_BRANDS
)
only_4wd = st.sidebar.checkbox("Show only 4WD listings")

vehicles_df = all_df
if selected_brands:
    vehicles_df = vehicles_df[vehicles_df["brand"].isin(selected_brands)]
if only_4wd:
    vehicles_df = vehicles_df[vehicles_df["is_4wd"]]

if vehicles_df.empty:
    st.warning("No listings match these filters.")
    st.stop()

st.plotly_chart(plot_price_histogram(vehicles_df))
st.plotly_chart(plot_price_vs_odometer(vehicles_df))
st.plotly_chart(plot_price_by_condition(vehicles_df))
st.plotly_chart(plot_top_brands(vehicles_df))
st.plotly_chart(plot_top_cars(vehicles_df))
st.plotly_chart(plot_transmission_share(vehicles_df))
st.plotly_chart(plot_4wd_share(vehicles_df))
