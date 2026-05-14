import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

def render_product_strategy(filtered_df):
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
