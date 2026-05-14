import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from scripts.analytics import run_sales_strategy, calculate_efficiency_score, forecast_retention
from scripts.error_logger import log_event

st.set_page_config(
    page_title="Samsung Market Intelligence Dashboard",
    layout="wide"
)

# -----------------------
# LOAD DATA
# -----------------------
@st.cache_data
def load_data():
    raw_data_path = 'data/mobile_sales.csv'
    output_path = 'data/samsung_us_strategic_data.csv'
    
    if os.path.exists(output_path):
        return pd.read_csv(output_path)
        
    if not os.path.exists(raw_data_path):
        log_event("CRITICAL: raw_data_path not found.")
        return None

    try:
        df = pd.read_csv(raw_data_path)
        df = run_sales_strategy(df)
        df = calculate_efficiency_score(df)
        df = forecast_retention(df)
        
        df.to_csv(output_path, index=False)
        log_event("SUCCESS: Pipeline completed successfully.")
        return df
        
    except Exception as e:
        log_event(f"ERROR: Pipeline failed - {str(e)}")
        return None


def main():
    st.title("Samsung Market Intelligence Dashboard")

    df = load_data()

    if df is None:
        st.error("Data could not be loaded or processed. Please check your data files.")
        return

    cols_to_drop = [
        'Regional 5G Coverage (%)', '5G Subscribers (millions)', 
        'Avg 5G Speed (Mbps)', 'Preference for 5G (%)', 
        'Efficiency_Score', 'Value_Score'
    ]
    df = df.drop(columns=[c for c in cols_to_drop if c in df.columns], errors='ignore')

    # Focus exclusively on the North American market
    df = df[df['Region'] == 'North America']

    # Remove A50 and A70 series as they are not found in the USA
    df = df[~df['Product Model'].str.contains(r'Galaxy A[57]', case=False, na=False)]

    # -----------------------
    # SIDEBAR FILTERS
    # -----------------------
    st.sidebar.header("Global Filters")

    segment = st.sidebar.selectbox(
        "Market Segment",
        ["All"] + sorted(df['Market Segment'].dropna().unique())
    )

    filtered_df = df.copy()

    if segment != "All":
        filtered_df = filtered_df[filtered_df['Market Segment'] == segment]

    # -----------------------
    # TABS (TABLEAU STYLE)
    # -----------------------
    tab1, tab2, tab3 = st.tabs([
        "Overview",
        "Market Analysis",
        "Product Strategy"
    ])

    # =========================
    # TAB 1: OVERVIEW
    # =========================
    with tab1:
        st.subheader("Executive Overview")

        col1, col2, col3 = st.columns(3)

        col1.metric("Total Records", len(filtered_df))
        col2.metric("Top Segment", filtered_df['Market Segment'].mode()[0])
        col3.metric("Focus Market", "North America")

        st.markdown("---")

        fig, ax = plt.subplots(1, 2, figsize=(14, 6))

        sns.countplot(
            data=filtered_df,
            x='Market Segment',
            order=filtered_df['Market Segment'].value_counts().index,
            ax=ax[0]
        )
        ax[0].set_title("Segment Distribution")
        ax[0].tick_params(axis='x', rotation=30)

        sns.scatterplot(
            data=filtered_df,
            x='Revenue ($)',
            y='Units Sold',
            hue='Market Segment',
            ax=ax[1]
        )
        ax[1].set_title("Revenue vs Units Sold")

        st.pyplot(fig)

    # =========================
    # TAB 2: MARKET ANALYSIS
    # =========================
    with tab2:
        st.subheader("Market Performance")

        fig, ax = plt.subplots(figsize=(10, 6))

        sns.boxplot(
            data=filtered_df,
            x='Market Segment',
            y='Revenue ($)',
            ax=ax
        )
        ax.set_title("Revenue Distribution by Segment")
        ax.tick_params(axis='x', rotation=30)

        st.pyplot(fig)

        st.markdown("### Top Performing Models")

        top_models = filtered_df.sort_values(
            by='Revenue ($)', ascending=False
        ).head(10)

        st.dataframe(top_models)

    # =========================
    # TAB 3: PRODUCT STRATEGY
    # =========================
    with tab3:
        st.subheader("Product Strategy View")

        if filtered_df.empty:
            st.info("No data available.")
        else:
            col1, col2 = st.columns(2)

            # Flagship
            flagship = filtered_df[filtered_df['Market Segment'] == 'S-Series (Flagship)']
            fig1, ax1 = plt.subplots(figsize=(6, 4))

            sns.barplot(
                data=flagship,
                x='Product Model',
                y='Revenue ($)',
                ax=ax1
            )
            ax1.set_title("Flagship Revenue")
            ax1.tick_params(axis='x', rotation=45)

            col1.pyplot(fig1)

            # A-Series
            budget = filtered_df[filtered_df['Market Segment'] == 'A-Series (Budget)']
            fig2, ax2 = plt.subplots(figsize=(6, 4))

            sns.barplot(
                data=budget,
                x='Product Model',
                y='Units Sold',
                ax=ax2
            )
            ax2.set_title("A-Series Units Sold")
            ax2.tick_params(axis='x', rotation=45)

            col2.pyplot(fig2)

    # -----------------------
    # DATA TABLE
    # -----------------------
    st.markdown("---")
    st.subheader("Data Explorer")
    st.dataframe(filtered_df)


if __name__ == "__main__":
    main()