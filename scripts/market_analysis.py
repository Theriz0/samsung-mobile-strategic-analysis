import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

def render_market_analysis(filtered_df):
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
