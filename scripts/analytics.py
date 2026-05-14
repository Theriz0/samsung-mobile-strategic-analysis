import pandas as pd
import numpy as np

def get_col(df, possible_names):
    """Find a column even if capitalization/spacing differs."""
    for name in possible_names:
        for col in df.columns:
            if col.strip().lower() == name.lower():
                return col
    return None


def clean_numeric(series):
    """Convert messy numeric strings like '$999' or '128GB' into floats."""
    return pd.to_numeric(
        series.astype(str).str.replace(r'[^0-9.]', '', regex=True),
        errors='coerce'
    )


def run_sales_strategy(df):
    # Find model column
    col = get_col(df, ['Model', 'Product Model', 'Name', 'Phone'])
    if not col:
        raise KeyError(f"Could not find a 'Model' column. Available: {df.columns.tolist()}")

    # Ensure string type (prevents .str errors)
    df[col] = df[col].astype(str)

    # Improved segmentation logic
    conditions = [
        df[col].str.contains(r'Galaxy\s*A\d+', case=False, na=False),
        df[col].str.contains(r'Galaxy\s*S\d+', case=False, na=False) &
        ~df[col].str.contains('FE', case=False, na=False),
        df[col].str.contains(r'(FE|Z Fold|Z Flip)', case=False, na=False)
    ]

    values = [
        'A-Series (Budget)',
        'S-Series (Flagship)',
        'Strategic (FE/Foldable)'
    ]

    df['Market Segment'] = np.select(conditions, values, default='Specialty')
    return df

def calculate_efficiency_score(df):
    units_col = get_col(df, ['Units Sold'])
    revenue_col = get_col(df, ['Revenue ($)', 'Revenue'])
    market_col = get_col(df, ['Market Share (%)', 'Market Share'])

    if not all([units_col, revenue_col, market_col]):
        raise KeyError(f"""
Missing required columns.
Found: {df.columns.tolist()}
Expected:
- Units Sold
- Revenue ($)
- Market Share (%)
""")

    # Clean numeric data
    df[units_col] = clean_numeric(df[units_col])
    df[revenue_col] = clean_numeric(df[revenue_col])
    df[market_col] = clean_numeric(df[market_col])

    # Drop bad rows
    df = df.dropna(subset=[units_col, revenue_col, market_col])

    # Avoid division issues
    df = df[df[units_col] > 0]

    # New efficiency formula (business-relevant)
    df['Efficiency_Score'] = (
        df[revenue_col] / df[units_col]
    ) * (df[market_col] / 100)

    return df.round(2)

def forecast_retention(df):
    retention_map = {
        'A-Series (Budget)': 3,
        'S-Series (Flagship)': 5,
        'Strategic (FE/Foldable)': 4
    }

    df['Est_Support_Years'] = df['Market Segment'].map(retention_map).fillna(2)

    # Optional: Add value score (business metric)
    if 'Efficiency_Score' in df.columns:
        df['Value_Score'] = df['Efficiency_Score'] * df['Est_Support_Years']

    return df