# Samsung Market Intelligence Dashboard

A Streamlit-based interactive dashboard designed to analyze mobile device sales, quarterly trends, and product strategy for Samsung's North American market, supercharged with a Generative AI Assistant.

## Overview

This project provides strategic insights into the performance of various Samsung device segments (Flagship, Budget, and Foldables/Specialty). It automatically runs a data processing pipeline to generate clean analytics metrics, which are then visualized in an interactive, highly modular Tableau-style interface.

### Key Features
- **Data Pipeline Integrated:** Automatically ingests raw mobile sales data, assigns market segments, and forecasts device retention.
- **North America Focus:** The analysis has been tailored to strictly evaluate the North American region. Irrelevant metrics and specific devices (like A50/A70 series) are automatically filtered out.
- **Quarterly Trends:** New chronological line charts plotting `Revenue` and `Units Sold` over time by Market Segment.
- **Gemini AI Assistant:** Built-in generative AI data inspector. You can ask natural language questions about your dashboard data to instantly generate reports. It securely and automatically accesses your API key to fetch available models.
- **Modular Architecture:** The codebase is split into multiple files for extreme reading consistency and maintainability.

## Project Structure

```text
.
├── app.py                     # Main orchestrator, data loader, and global filters
├── .streamlit/
│   └── secrets.toml           # Secure configuration for GEMINI_API_KEY
├── scripts/                   # Core business logic and modular tab UI
│   ├── overview.py            # Renders Executive Overview
│   ├── market_analysis.py     # Renders Market Performance
│   ├── quarterly_trends.py    # Renders Time-series trends
│   ├── product_strategy.py    # Renders Product specific stats
│   ├── ai_assistant.py        # Connects to Gemini API for natural language queries
│   ├── analytics.py           # Core data transformation functions
│   └── error_logger.py        # Pipeline logging
├── data/                      # Raw and processed datasets
├── app.bat & app.sh           # OS-specific launcher scripts
└── requirements.txt           # Python dependencies
```

## Getting Started

### Prerequisites
1. Ensure that Python 3.7+ is installed on your system.
2. (Optional but Recommended) Get a free Gemini API key from [Google AI Studio](https://aistudio.google.com/) and place it inside `.streamlit/secrets.toml`:
   ```toml
   GEMINI_API_KEY = "your_api_key_here"
   ```

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

## How It Works

1. **ETL Process:** When `app.py` is launched, it checks if the processed data `samsung_us_strategic_data.csv` exists. If not, it executes the pipeline to clean the data.
2. **Filtering:** Irrelevant global data is dropped, focusing exclusively on the North American market.
3. **Visualization:** `app.py` passes the filtered dataset to the dedicated scripts in `scripts/` to render 5 distinct tabs:
   - **Overview:** Executive summary metrics and high-level charts.
   - **Market Analysis:** Detailed revenue boxplots and top-performing models.
   - **Quarterly Trends:** Revenue and sales growth plotted chronologically.
   - **Product Strategy:** A breakdown of specific device series performance (Flagship vs Budget).
   - **AI Assistant:** A secure chat interface to query the dashboard data using Google's Gemini models.
