from pathlib import Path
from urllib.parse import quote_plus

import pandas as pd
from sqlalchemy import create_engine, text


# Locate the CSV relative to this Python file
project_root = Path(__file__).resolve().parent.parent
csv_path = project_root / "data" / "daily_prices.csv"

required_columns = [
    "price_date",
    "ticker",
    "open_price",
    "high_price",
    "low_price",
    "close_price",
    "adjusted_close",
    "volume"
]

expected_tickers = {"AAPL", "JPM", "NVDA", "SPY", "XLF"}

# Read the SQL-ready CSV
daily_prices = pd.read_csv(
    csv_path,
    parse_dates=["price_date"]
)

# Validate columns
missing_columns = set(required_columns) - set(daily_prices.columns)

if missing_columns:
    raise ValueError(f"Missing columns: {missing_columns}")

daily_prices = daily_prices[required_columns].copy()

# Validate missing values
if daily_prices.isna().any().any():
    raise ValueError("Daily price data contains missing values.")

# Validate duplicate date-and-ticker combinations
duplicate_rows = daily_prices.duplicated(
    subset=["price_date", "ticker"]
)

if duplicate_rows.any():
    raise ValueError("Daily price data contains duplicate keys.")

# Validate ticker membership
actual_tickers = set(daily_prices["ticker"])

if actual_tickers != expected_tickers:
    raise ValueError(
        f"Ticker mismatch. Found: {sorted(actual_tickers)}"
    )

# Read and validate portfolio performance data
performance_csv_path = (
    project_root / "data" / "performance_summary.csv"
)

performance_required_columns = [
    "performance_date",
    "portfolio_value",
    "portfolio_gain_loss",
    "portfolio_return",
    "benchmark_value",
    "benchmark_return",
    "active_return"
]

portfolio_performance = pd.read_csv(
    performance_csv_path,
    parse_dates=["Date"]
)

# Map the CSV field name to the SQL column name
portfolio_performance = portfolio_performance.rename(
    columns={"Date": "performance_date"}
)

missing_performance_columns = (
    set(performance_required_columns)
    - set(portfolio_performance.columns)
)

if missing_performance_columns:
    raise ValueError(
        "Missing performance columns: "
        f"{missing_performance_columns}"
    )

portfolio_performance = portfolio_performance[
    performance_required_columns
].copy()

if portfolio_performance.isna().any().any():
    raise ValueError(
        "Portfolio performance data contains missing values."
    )

if portfolio_performance["performance_date"].duplicated().any():
    raise ValueError(
        "Portfolio performance contains duplicate dates."
    )

# Confirm that both datasets contain the same trading dates
price_dates = set(daily_prices["price_date"].dt.date)

performance_dates = set(
    portfolio_performance["performance_date"].dt.date
)

if performance_dates != price_dates:
    raise ValueError(
        "Performance dates do not match daily price dates."
    )

# Read and validate forecast summary data
forecast_csv_path = (
    project_root / "data" / "forecast_summary.csv"
)

forecast_required_columns = [
    "investment",
    "forecast_days",
    "current_value",
    "baseline_forecast",
    "conservative_5th",
    "median_50th",
    "optimistic_95th",
    "probability_below_current",
    "mae",
    "rmse"
]

forecast_summary = pd.read_csv(forecast_csv_path)

missing_forecast_columns = (
    set(forecast_required_columns)
    - set(forecast_summary.columns)
)

if missing_forecast_columns:
    raise ValueError(
        f"Missing forecast columns: {missing_forecast_columns}"
    )

forecast_summary = forecast_summary[
    forecast_required_columns
].copy()

if forecast_summary.isna().any().any():
    raise ValueError(
        "Forecast summary contains missing values."
    )

if forecast_summary["investment"].duplicated().any():
    raise ValueError(
        "Forecast summary contains duplicate investments."
    )

expected_investments = {"Portfolio", "SPY"}
actual_investments = set(forecast_summary["investment"])

if actual_investments != expected_investments:
    raise ValueError(
        "Forecast investments do not match "
        f"{sorted(expected_investments)}."
    )

if (forecast_summary["forecast_days"] <= 0).any():
    raise ValueError(
        "Forecast days must be greater than zero."
    )

invalid_percentiles = (
    (
        forecast_summary["conservative_5th"]
        > forecast_summary["median_50th"]
    )
    | (
        forecast_summary["median_50th"]
        > forecast_summary["optimistic_95th"]
    )
)

if invalid_percentiles.any():
    raise ValueError(
        "Forecast percentiles are not correctly ordered."
    )

invalid_probabilities = ~forecast_summary[
    "probability_below_current"
].between(0, 1)

if invalid_probabilities.any():
    raise ValueError(
        "Forecast probabilities must be between 0 and 1."
    )

# Read and validate forecast bands
forecast_bands_path = (
    project_root / "data" / "forecast_bands.csv"
)

forecast_bands_columns = [
    "forecast_day",
    "portfolio_5th",
    "portfolio_median",
    "portfolio_95th",
    "spy_5th",
    "spy_median",
    "spy_95th"
]

forecast_bands = pd.read_csv(forecast_bands_path)

missing_band_columns = (
    set(forecast_bands_columns)
    - set(forecast_bands.columns)
)

if missing_band_columns:
    raise ValueError(
        f"Missing forecast-band columns: {missing_band_columns}"
    )

forecast_bands = forecast_bands[
    forecast_bands_columns
].copy()

if forecast_bands.isna().any().any():
    raise ValueError(
        "Forecast bands contain missing values."
    )

if forecast_bands["forecast_day"].duplicated().any():
    raise ValueError(
        "Forecast bands contain duplicate days."
    )

forecast_horizons = set(forecast_summary["forecast_days"])

if len(forecast_horizons) != 1:
    raise ValueError(
        "Forecast summary contains inconsistent horizons."
    )

forecast_horizon = int(next(iter(forecast_horizons)))

expected_days = set(range(1, forecast_horizon + 1))
actual_days = set(forecast_bands["forecast_day"])

if actual_days != expected_days:
    raise ValueError(
        "Forecast bands do not contain every expected day."
    )

invalid_portfolio_bands = (
    (forecast_bands["portfolio_5th"]
     > forecast_bands["portfolio_median"])
    |
    (forecast_bands["portfolio_median"]
     > forecast_bands["portfolio_95th"])
)

invalid_spy_bands = (
    (forecast_bands["spy_5th"]
     > forecast_bands["spy_median"])
    |
    (forecast_bands["spy_median"]
     > forecast_bands["spy_95th"])
)

if invalid_portfolio_bands.any():
    raise ValueError(
        "Portfolio forecast bands are incorrectly ordered."
    )

if invalid_spy_bands.any():
    raise ValueError(
        "SPY forecast bands are incorrectly ordered."
    )

# Build the SQL Server connection

connection_string = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=PortfolioAnalytics;"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)

connection_url = (
    "mssql+pyodbc:///?odbc_connect="
    + quote_plus(connection_string)
)

engine = create_engine(connection_url)

# Refresh DailyPrices inside one database transaction

with engine.begin() as connection:

    database_name = connection.execute(
        text("SELECT DB_NAME()")
    ).scalar_one()

    if database_name != "PortfolioAnalytics":
        raise RuntimeError(
            f"Wrong database connection: {database_name}"
        )

    rows_before = connection.execute(
        text("SELECT COUNT(*) FROM dbo.DailyPrices")
    ).scalar_one()

    connection.execute(
        text("DELETE FROM dbo.DailyPrices")
    )

    daily_prices.to_sql(
        name="DailyPrices",
        con=connection,
        schema="dbo",
        if_exists="append",
        index=False,
        chunksize=100
    )

    rows_after = connection.execute(
        text("SELECT COUNT(*) FROM dbo.DailyPrices")
    ).scalar_one()

    if rows_after != len(daily_prices):
        raise RuntimeError(
            f"Row-count mismatch: CSV has {len(daily_prices)}, "
            f"but SQL has {rows_after}."
        )



    # Refresh PortfolioPerformance

    performance_rows_before = connection.execute(
        text(
            "SELECT COUNT(*) "
            "FROM dbo.PortfolioPerformance"
        )
    ).scalar_one()

    connection.execute(
        text("DELETE FROM dbo.PortfolioPerformance")
    )

    portfolio_performance.to_sql(
        name="PortfolioPerformance",
        con=connection,
        schema="dbo",
        if_exists="append",
        index=False,
        chunksize=100
    )

    performance_rows_after = connection.execute(
        text(
            "SELECT COUNT(*) "
            "FROM dbo.PortfolioPerformance"
        )
    ).scalar_one()

    if performance_rows_after != len(portfolio_performance):
        raise RuntimeError(
            "Performance row-count mismatch: "
            f"CSV has {len(portfolio_performance)}, "
            f"but SQL has {performance_rows_after}."
        )

    # Refresh ForecastSummary
    forecast_rows_before = connection.execute(
        text("SELECT COUNT(*) FROM dbo.ForecastSummary")
    ).scalar_one()

    connection.execute(
        text("DELETE FROM dbo.ForecastSummary")
    )

    forecast_summary.to_sql(
        name="ForecastSummary",
        con=connection,
        schema="dbo",
        if_exists="append",
        index=False,
        chunksize=100
    )

    forecast_rows_after = connection.execute(
        text("SELECT COUNT(*) FROM dbo.ForecastSummary")
    ).scalar_one()

    if forecast_rows_after != len(forecast_summary):
        raise RuntimeError(
            "Forecast row-count mismatch: "
            f"CSV has {len(forecast_summary)}, "
            f"but SQL has {forecast_rows_after}."
        )

    # Refresh ForecastBands
    forecast_band_rows_before = connection.execute(
        text("SELECT COUNT(*) FROM dbo.ForecastBands")
    ).scalar_one()

    connection.execute(
        text("DELETE FROM dbo.ForecastBands")
    )

    forecast_bands.to_sql(
        name="ForecastBands",
        con=connection,
        schema="dbo",
        if_exists="append",
        index=False,
        chunksize=100
    )

    forecast_band_rows_after = connection.execute(
        text("SELECT COUNT(*) FROM dbo.ForecastBands")
    ).scalar_one()

    if forecast_band_rows_after != len(forecast_bands):
        raise RuntimeError(
            "Forecast-band row-count mismatch: "
            f"CSV has {len(forecast_bands)}, "
            f"but SQL has {forecast_band_rows_after}."
        )

print(f"Validated CSV rows: {len(daily_prices)}")
print(f"Validated tickers: {sorted(actual_tickers)}")
print(
    f"Validated performance rows: "
    f"{len(portfolio_performance)}"
)
print(
    f"Validated forecast rows: "
    f"{len(forecast_summary)}"
)

print(f"Connected to: {database_name}")

print(f"DailyPrices rows before: {rows_before}")
print(f"DailyPrices rows after: {rows_after}")

print(
    f"PortfolioPerformance rows before: "
    f"{performance_rows_before}"
)
print(
    f"PortfolioPerformance rows after: "
    f"{performance_rows_after}"
)

print(
    f"ForecastSummary rows before: "
    f"{forecast_rows_before}"
)
print(
    f"ForecastSummary rows after: "
    f"{forecast_rows_after}"
)

print(
    f"Validated forecast-band rows: "
    f"{len(forecast_bands)}"
)
print(
    f"ForecastBands rows before: "
    f"{forecast_band_rows_before}"
)
print(
    f"ForecastBands rows after: "
    f"{forecast_band_rows_after}"
)

print("SQL refresh committed successfully.")
