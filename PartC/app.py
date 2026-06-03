from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st


DATA_FILE = Path(__file__).with_name("Trader_analysis.csv")
NUMERIC_COLUMNS = [
    "Daily_PnL",
    "Avg_Trade_Size",
    "Trades_Per_Day",
    "Win_Rate",
    "Long_Trades",
    "Short_Trades",
    "Long_Short_Ratio_Fixed",
]
HEATMAP_COLUMNS = [
    "Daily_PnL",
    "Win_Rate",
    "Trades_Per_Day",
    "Avg_Trade_Size",
    "Long_Short_Ratio_Fixed",
]
CHART_COLORS = ["#1F4E79", "#2E86AB", "#F18F01", "#C73E1D", "#6B8E23"]


def configure_page() -> None:
    st.set_page_config(page_title="Trader Sentiment Dashboard", layout="wide")
    sns.set_theme(style="whitegrid", palette=CHART_COLORS)
    st.title("Bitcoin Sentiment & Trader Behavior Dashboard")
    st.caption(
        "Explore how sentiment, trading bias, and execution patterns relate to "
        "profitability and win rate."
    )


@st.cache_data
def load_data(file_path: Path) -> pd.DataFrame:
    df = pd.read_csv(file_path)
    df["Trade_Date"] = pd.to_datetime(df["Trade_Date"], dayfirst=True, errors="coerce")

    for column in NUMERIC_COLUMNS:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    return df


def format_metric(value: float, template: str) -> str:
    if pd.isna(value):
        return "N/A"
    return template.format(value)


def render_filter_panel(df: pd.DataFrame) -> dict[str, object]:
    st.subheader("Filters")
    st.caption("Use these controls to narrow the dashboard view.")

    sentiment_options = sorted(df["classification"].dropna().unique())
    bias_options = sorted(df["Trading_Bias"].dropna().unique())

    min_date = df["Trade_Date"].min().date()
    max_date = df["Trade_Date"].max().date()
    max_trades = int(df["Trades_Per_Day"].max())

    selected_sentiments = st.multiselect(
        "Sentiment",
        options=sentiment_options,
        default=sentiment_options,
    )
    selected_biases = st.multiselect(
        "Trading Bias",
        options=bias_options,
        default=bias_options,
    )
    selected_dates = st.date_input(
        "Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )
    min_win_rate = st.slider("Minimum Win Rate (%)", min_value=0.0, max_value=100.0, value=0.0, step=1.0)
    min_trades = st.slider(
        "Minimum Trades Per Day",
        min_value=0,
        max_value=max_trades,
        value=0,
        step=10 if max_trades >= 10 else 1,
    )

    if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
        start_date, end_date = selected_dates
    else:
        start_date = end_date = selected_dates

    st.divider()
    st.markdown("#### Current View")
    st.write(f"Sentiments: {len(selected_sentiments)}")
    st.write(f"Bias Types: {len(selected_biases)}")
    st.write(f"Win Rate Floor: {min_win_rate:.0f}%")
    st.write(f"Trades Floor: {min_trades}")

    return {
        "sentiments": selected_sentiments,
        "biases": selected_biases,
        "start_date": pd.Timestamp(start_date),
        "end_date": pd.Timestamp(end_date),
        "min_win_rate": min_win_rate,
        "min_trades": min_trades,
    }


def apply_filters(df: pd.DataFrame, filters: dict[str, object]) -> pd.DataFrame:
    mask = (
        df["classification"].isin(filters["sentiments"])
        & df["Trading_Bias"].isin(filters["biases"])
        & df["Trade_Date"].between(filters["start_date"], filters["end_date"])
        & (df["Win_Rate"] >= filters["min_win_rate"])
        & (df["Trades_Per_Day"] >= filters["min_trades"])
    )
    return df.loc[mask].copy()


def render_overview(df: pd.DataFrame) -> None:
    start_date = df["Trade_Date"].min()
    end_date = df["Trade_Date"].max()
    sentiment_count = df["classification"].nunique()
    account_count = df["Account"].nunique()

    st.subheader("Overview")
    st.write(
        f"Showing **{len(df):,}** records across **{sentiment_count}** sentiment groups "
        f"and **{account_count:,}** trader accounts."
    )
    st.caption(
        f"Date coverage: {start_date:%d %b %Y} to {end_date:%d %b %Y}"
    )


def render_metrics(df: pd.DataFrame) -> None:
    st.subheader("Key Metrics")

    metrics = [
        ("Average PnL", format_metric(df["Daily_PnL"].mean(), "${:,.0f}")),
        ("Average Win Rate", format_metric(df["Win_Rate"].mean(), "{:.2f}%")),
        (
            "Average Trade Size",
            format_metric(df["Avg_Trade_Size"].mean(), "${:,.0f}"),
        ),
        (
            "Average Trades/Day",
            format_metric(df["Trades_Per_Day"].mean(), "{:,.0f}"),
        ),
    ]

    for column, (label, value) in zip(st.columns(len(metrics)), metrics):
        column.metric(label, value)


def annotate_bar_values(ax: plt.Axes, prefix: str = "", suffix: str = "") -> None:
    for patch in ax.patches:
        value = patch.get_width()
        y_position = patch.get_y() + patch.get_height() / 2
        ax.text(
            value,
            y_position,
            f" {prefix}{value:,.1f}{suffix}",
            va="center",
            fontsize=9,
        )


def render_average_pnl_chart(df: pd.DataFrame) -> None:
    chart_data = (
        df.groupby("classification", as_index=False)["Daily_PnL"]
        .mean()
        .sort_values("Daily_PnL", ascending=True)
    )

    fig, ax = plt.subplots(figsize=(8, 4.5))
    sns.barplot(data=chart_data, x="Daily_PnL", y="classification", ax=ax, color="#2E86AB")
    ax.set_title("Average Daily PnL by Sentiment", loc="left", fontsize=13, weight="bold")
    ax.set_xlabel("Average Daily PnL")
    ax.set_ylabel("Sentiment")
    annotate_bar_values(ax, prefix="$")
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


def render_average_win_rate_chart(df: pd.DataFrame) -> None:
    chart_data = (
        df.groupby("classification", as_index=False)["Win_Rate"]
        .mean()
        .sort_values("Win_Rate", ascending=True)
    )

    fig, ax = plt.subplots(figsize=(8, 4.5))
    sns.barplot(data=chart_data, x="Win_Rate", y="classification", ax=ax, color="#F18F01")
    ax.set_title("Average Win Rate by Sentiment", loc="left", fontsize=13, weight="bold")
    ax.set_xlabel("Win Rate (%)")
    ax.set_ylabel("Sentiment")
    annotate_bar_values(ax, suffix="%")
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


def render_pnl_distribution_chart(df: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(8, 4.5))
    sns.boxplot(
        data=df,
        x="classification",
        y="Daily_PnL",
        ax=ax,
        palette=CHART_COLORS,
        showfliers=False,
    )
    ax.set_title("PnL Distribution by Sentiment", loc="left", fontsize=13, weight="bold")
    ax.set_xlabel("Sentiment")
    ax.set_ylabel("Daily PnL")
    ax.tick_params(axis="x", rotation=15)
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


def render_scatter_chart(df: pd.DataFrame) -> None:
    scatter_df = df.dropna(subset=["Trades_Per_Day", "Daily_PnL", "Win_Rate", "classification"])

    fig, ax = plt.subplots(figsize=(8, 4.5))
    sns.scatterplot(
        data=scatter_df,
        x="Trades_Per_Day",
        y="Daily_PnL",
        hue="classification",
        size="Win_Rate",
        sizes=(40, 240),
        alpha=0.75,
        ax=ax,
    )
    ax.set_title("Trades Per Day vs Daily PnL", loc="left", fontsize=13, weight="bold")
    ax.set_xlabel("Trades Per Day")
    ax.set_ylabel("Daily PnL")
    ax.legend(loc="upper right", fontsize=8, frameon=True)
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


def render_trading_bias_chart(df: pd.DataFrame) -> None:
    chart_data = (
        df["Trading_Bias"]
        .value_counts(normalize=False)
        .rename_axis("Trading_Bias")
        .reset_index(name="Count")
        .sort_values("Count", ascending=True)
    )
    total = chart_data["Count"].sum()

    fig, ax = plt.subplots(figsize=(8, 4.5))
    sns.barplot(data=chart_data, x="Count", y="Trading_Bias", ax=ax, color="#6B8E23")
    ax.set_title("Trading Bias Distribution", loc="left", fontsize=13, weight="bold")
    ax.set_xlabel("Number of Records")
    ax.set_ylabel("Trading Bias")

    for patch in ax.patches:
        value = patch.get_width()
        share = (value / total) * 100 if total else 0
        y_position = patch.get_y() + patch.get_height() / 2
        ax.text(value, y_position, f" {share:.1f}%", va="center", fontsize=9)

    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


def render_heatmap(df: pd.DataFrame) -> None:
    heatmap_data = df[HEATMAP_COLUMNS].corr()

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.heatmap(heatmap_data, annot=True, cmap="YlGnBu", fmt=".2f", linewidths=0.5, ax=ax)
    ax.set_title("Feature Correlation Heatmap", loc="left", fontsize=13, weight="bold")
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


def render_dataset_preview(df: pd.DataFrame) -> None:
    with st.expander("View Filtered Dataset", expanded=False):
        st.dataframe(df, use_container_width=True)


def render_dashboard(df: pd.DataFrame) -> None:
    render_overview(df)
    render_metrics(df)
    st.divider()

    row_one_col1, row_one_col2 = st.columns(2, gap="large")
    with row_one_col1:
        render_average_pnl_chart(df)
    with row_one_col2:
        render_average_win_rate_chart(df)

    row_two_col1, row_two_col2 = st.columns(2, gap="large")
    with row_two_col1:
        render_pnl_distribution_chart(df)
    with row_two_col2:
        render_scatter_chart(df)

    row_three_col1, row_three_col2 = st.columns(2, gap="large")
    with row_three_col1:
        render_trading_bias_chart(df)
    with row_three_col2:
        render_heatmap(df)

    render_dataset_preview(df)


def main() -> None:
    configure_page()
    df = load_data(DATA_FILE)

    main_col, filter_col = st.columns([4.4, 1.6], gap="large")

    with filter_col:
        filters = render_filter_panel(df)

    filtered_df = apply_filters(df, filters)

    with main_col:
        if filtered_df.empty:
            st.warning("No data matches the selected filters. Try widening the date or metric ranges.")
            return

        render_dashboard(filtered_df)


if __name__ == "__main__":
    main()
