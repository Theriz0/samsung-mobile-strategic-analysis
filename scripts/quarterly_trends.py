import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

def render_quarterly_trends(filtered_df):
    st.subheader("Quarterly Performance Trends")
    
    if 'Year' in filtered_df.columns and 'Quarter' in filtered_df.columns:
        trend_df = filtered_df.copy()
        trend_df['Period'] = trend_df['Year'].astype(str) + " " + trend_df['Quarter']
        # Sort by Year and Quarter ensuring chronological order
        trend_df = trend_df.sort_values(by=['Year', 'Quarter'])
        
        fig, ax = plt.subplots(2, 1, figsize=(14, 12))
        
        # Quarterly Revenue by Market Segment
        sns.lineplot(
            data=trend_df,
            x='Period',
            y='Revenue ($)',
            hue='Market Segment',
            marker='o',
            errorbar=None,
            ax=ax[0]
        )
        ax[0].set_title("Quarterly Revenue by Market Segment")
        ax[0].set_ylabel("Revenue ($)")
        ax[0].tick_params(axis='x', rotation=45)
        
        # Quarterly Units Sold by Market Segment
        sns.lineplot(
            data=trend_df,
            x='Period',
            y='Units Sold',
            hue='Market Segment',
            marker='o',
            errorbar=None,
            ax=ax[1]
        )
        ax[1].set_title("Quarterly Units Sold by Market Segment")
        ax[1].set_ylabel("Units Sold")
        ax[1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        st.pyplot(fig)
    else:
        st.info("Year and Quarter data is not available for trend analysis.")
