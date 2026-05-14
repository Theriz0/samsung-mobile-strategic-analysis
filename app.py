import streamlit as st
import pandas as pd
import os
from scripts.analytics import run_sales_strategy, calculate_efficiency_score, forecast_retention
from scripts.error_logger import log_event

# Import modular tab functions
from scripts.overview import render_overview
from scripts.market_analysis import render_market_analysis
from scripts.quarterly_trends import render_quarterly_trends
from scripts.product_strategy import render_product_strategy
from scripts.ai_assistant import render_ai_assistant

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
    # TABS
    # -----------------------
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Overview",
        "Market Analysis",
        "Quarterly Trends",
        "Product Strategy",
        "AI Assistant"
    ])

    with tab1:
        render_overview(filtered_df)

    with tab2:
        render_market_analysis(filtered_df)

    with tab3:
        render_quarterly_trends(filtered_df)

    with tab4:
        render_product_strategy(filtered_df)

    with tab5:
        render_ai_assistant(filtered_df)

    # -----------------------
    # DATA TABLE
    # -----------------------
    st.markdown("---")
    st.subheader("Data Explorer")
    st.dataframe(filtered_df)


if __name__ == "__main__":
    main()