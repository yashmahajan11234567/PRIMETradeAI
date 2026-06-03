# Bitcoin Market Sentiment vs Trader Performance Analysis

## Objective

Analyze whether Bitcoin market sentiment (Fear/Greed Index) influences trader behavior and profitability.

## Dataset

1. Bitcoin Fear & Greed Index
2. Hyperliquid Historical Trader Data

## Methodology

### Part A – Data Preparation

* Imported both datasets into SQL Server
* Checked row counts, missing values, and duplicate records
* Converted Unix timestamps into SQL datetime format
* Aligned trading activity with daily sentiment data
* Created a consolidated analysis table containing:

  * Daily PnL
  * Win Rate
  * Average Trade Size
  * Trades Per Day
  * Long Trades
  * Short Trades
  * Trading Bias
  * Market Sentiment

### Part B – Analysis

Analyzed:

* PnL by sentiment
* Win rate by sentiment
* Drawdown proxy by sentiment
* Trade frequency by sentiment
* Position size by sentiment
* Long/Short trading bias

Created trader segments:

* Frequent vs Infrequent Traders
* High Risk vs Low Risk Traders
* Consistent Winners vs Inconsistent Traders

### Part C – Advanced Analytics

* Predictive model for profitability classification
* K-Means clustering for trader archetypes
* Streamlit dashboard for interactive exploration

## How To Run

Install dependencies:

pip install -r requirements.txt

Run dashboard:

streamlit run app.py

## Technologies

* SQL Server
* Python
* Pandas
* Matplotlib
* Seaborn
* Scikit-Learn
* Streamlit

## Author

Yash Mahajan
