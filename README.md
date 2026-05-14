# Samsung Market Intelligence Dashboard

A Streamlit-based interactive dashboard designed to analyze mobile device sales, 5G adoption, and product strategy for Samsung's North American market.

## Overview

This project provides strategic insights into the performance of various Samsung device segments (Flagship, Budget, and Foldables/Specialty). It automatically runs a data processing pipeline to generate clean analytics metrics, which are then visualized in an interactive Tableau-style interface.

### Key Features
- **Data Pipeline Integrated:** Automatically ingests raw mobile sales data, calculates efficiency scores, assigns market segments, and forecasts device retention.
- **North America Focus:** The analysis has been tailored to strictly evaluate the North American region to provide deep, actionable market insights.
- **Interactive Visualizations:** View revenue distributions, units sold, and 5G adoption metrics broken down by device segments.
- **Product Strategy Analysis:** Compare the performance of flagship S-Series devices against budget A-Series models.

## Project Structure

- `app.py`: The main Streamlit application. It also automatically handles executing the data processing pipeline if the processed data is missing.
- `scripts/`: Contains Python modules used for data analytics and error logging (`analytics.py`, `error_logger.py`).
- `data/`: Directory containing the raw input (`mobile_sales.csv`) and the processed output data (`samsung_us_strategic_data.csv`).
- `app.bat` / `app.sh`: Convenience scripts for Windows and Unix to safely install dependencies and launch the dashboard.
- `requirements.txt`: Required Python packages.

## Getting Started

### Prerequisites
Ensure that Python 3.7+ is installed on your system.

### How to Run

**On Windows:**
Simply run the batch script from your terminal. It will install any missing dependencies and start the dashboard.
```powershell
.\app.bat
```

**On Mac/Linux:**
Execute the shell script:
```bash
bash app.sh
```

**Manual Execution:**
If you prefer not to use the automated scripts, you can run the app manually:
```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## How It Works

1. **ETL Process:** When `app.py` is launched, it checks if the processed data `samsung_us_strategic_data.csv` exists.
2. If it does not exist, the app automatically triggers the analytics pipeline, reading `mobile_sales.csv`, calculating business-relevant metrics, and caching the output.
3. **Visualization:** The Streamlit frontend loads the cleaned data and renders four main tabs:
   - **Overview:** Executive summary metrics and high-level charts.
   - **Market Analysis:** Detailed revenue boxplots and top-performing models.
   - **5G Insights:** Scatterplots contrasting 5G speeds, preferences, and subscribers.
   - **Product Strategy:** A breakdown of specific device series performance in the market.
