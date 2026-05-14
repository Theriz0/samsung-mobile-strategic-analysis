import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

def render_overview(filtered_df):
    st.subheader("Executive Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Records", len(filtered_df))
    if not filtered_df.empty:
        col2.metric("Top Segment", filtered_df['Market Segment'].mode()[0])
    else:
        col2.metric("Top Segment", "N/A")
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
