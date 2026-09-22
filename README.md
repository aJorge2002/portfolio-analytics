\# Portfolio Analytics \& Forecasting Dashboard



An end-to-end portfolio analytics project built with Python, SQL Server, and Power BI. The project tracks a rule-based $10,000 portfolio, compares its performance against the S\&P 500, and models a 30-day forecast using Monte Carlo simulation.



\## Key Results

*Results from the September 2026 analysis run*

\- Latest portfolio value: \*\*$10,998.70\*\*

\- Portfolio return: \*\*9.99%\*\*

\- Active return versus SPY: \*\*0.06 percentage points\*\*

\- 30-day median forecast: \*\*$11,207.38\*\*

\- Conservative forecast (5th percentile): \*\*$10,276.55\*\*

\- Optimistic forecast (95th percentile): \*\*$12,199.34\*\*

\- Probability of finishing below the current value: \*\*34.80%\*\*

\- Portfolio backtest MAE: \*\*0.61%\*\*

\- Portfolio backtest RMSE: \*\*0.77%\*\*



\## Technology



\- Python

\- pandas

\- NumPy

\- yfinance

\- scikit-learn

\- SQL Server

\- SQLAlchemy

\- pyodbc

\- Power BI



\## Portfolio Rules



\- Initial capital: \*\*$10,000\*\*

\- Initial date: \*\*January 2, 2026\*\*

\- Holdings: \*\*SPY, XLF, AAPL, JPM, and NVDA\*\*

\- Equal target allocation across holdings

\- Whole shares only

\- Unused capital remains as cash

\- SPY is used as the benchmark



\## Project Workflow



1\. Download historical market data with Python and yfinance.

2\. Clean and transform the market data using pandas.

3\. Calculate portfolio values, returns, and benchmark performance.

4\. Backtest the daily-return forecasting baseline.

5\. Run 1,000 Monte Carlo simulations over a 30-day horizon.

6\. Load the analysis results into SQL Server.

7\. Visualize portfolio performance and forecast risk in Power BI.



\## Repository Structure



```text

portfolio-analytics/

├── data/           # Generated CSV datasets

├── docs/           # Portfolio rules and documentation

├── power\_bi/       # Power BI template and dashboard PDF

├── SQL/            # Database creation and validation scripts

├── src/            # Python pipeline scripts

├── .gitignore

├── README.md

└── requirements.txt

