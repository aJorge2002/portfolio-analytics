import yfinance as yf
import pandas as pd
import numpy as np

tickers = ["SPY", "XLF", "AAPL", "JPM", "NVDA"]
start_date = "2026-01-02"
starting_capital = 10000

market_prices_raw = yf.download(tickers, start=start_date, auto_adjust=False)
market_prices_raw.to_csv("data/market_prices_raw.csv")
print(len(market_prices_raw))

#Closing Market Prices
close_prices = market_prices_raw["Close"]

print(close_prices.isna().sum())

missing_close_rows = close_prices[close_prices.isna().any(axis=1)]
print(missing_close_rows)

close_clean = close_prices.dropna(how="all")
print(close_clean.head())
close_clean.to_csv("data/closing_prices.csv")



#Opening Market Prices
open_clean = market_prices_raw["Open"]
print(open_clean.head())
open_clean.to_csv("data/opening_prices.csv")


#Market High Prices
high_clean = market_prices_raw["High"]
print(high_clean.head())
high_clean.to_csv("data/high_prices.csv")


#Market Low Prices
low_clean = market_prices_raw["Low"]
print(low_clean.head())
low_clean.to_csv("data/low_prices.csv")


#Volume
volume_prices = market_prices_raw["Volume"]
print(volume_prices.head())
volume_prices.to_csv("data/volume.csv")


#Print Missing Values
print(close_clean.isna().sum())
print(open_clean.isna().sum())
print(high_clean.isna().sum())
print(low_clean.isna().sum())
print(volume_prices.isna().sum())

#Format Data

closing_with_date = close_clean.reset_index()
print(closing_with_date.head())

start_prices = close_clean.loc[start_date]
print(start_prices)

allocation_per_holding = starting_capital / len(tickers)

print(allocation_per_holding)

#Whole Shares Purchased

whole_shares = (allocation_per_holding // start_prices).astype(int)

print(whole_shares)

# Purchase Cost

purchase_cost = whole_shares * start_prices
print(purchase_cost)

# Invested Amount and Remaining Cash
total_invested = purchase_cost.sum()
remaining_cash = starting_capital - total_invested

print(f"Total invested: ${total_invested:,.2f}")
print(f"Remaining cash: ${remaining_cash:,.2f}")

# Transaction Table
transactions = pd.DataFrame({

	"date": start_date,
	"ticker": start_prices.index,
	"type": "BUY",
	"shares": whole_shares.values,
	"purchase_price": start_prices.round(2).values,
	"cost_basis": purchase_cost.round(2).values

})

print(transactions)
transactions.to_csv("data/transactions.csv", index=False)

# Portfolio Reconciliation Check

portfolio_total_check = total_invested + remaining_cash

print(f"Portfolio total check: ${portfolio_total_check:,.2f}")


# Daily Position Values

daily_position_values = close_clean * whole_shares

print(daily_position_values.head())

# Daily Invested Value

daily_invested_value = daily_position_values.sum(axis=1)

print(daily_invested_value.head())

# Daily Total Portfolio Value

daily_portfolio_value = daily_invested_value + remaining_cash

print(daily_portfolio_value.head())

# Daily Gain or Loss

daily_gain_loss = daily_portfolio_value - starting_capital

print(daily_gain_loss.head())

# Daily Portfolio Return 

daily_return = daily_gain_loss / starting_capital

print((daily_return.head() * 100).round(2))

# SPY Benchmark Construction

spy_start_price = start_prices["SPY"]

benchmark_shares = int(starting_capital // spy_start_price)
benchmark_invested = benchmark_shares * spy_start_price
benchmark_cash = starting_capital - benchmark_invested


print(f"SPY benchmark shares: {benchmark_shares}")
print(f"SPY benchmark invested: ${benchmark_invested:,.2f}")
print(f"SPY benchmark cash: ${benchmark_cash:,.2f}")

# Daily SPY Benchmark Value

benchmark_daily_value = (
	close_clean["SPY"] * benchmark_shares
	+ benchmark_cash
)

print(benchmark_daily_value.head())


# Daily SPY benchmark Return

benchmark_return = (
	benchmark_daily_value - starting_capital
	) / starting_capital

print((benchmark_return.head() * 100).round(2))

# Portfolio Performance vs. SPY
performance_vs_spy = daily_return - benchmark_return

print((performance_vs_spy.head() * 100).round(2))

# Performance Summary Table

performance_summary = pd.DataFrame({

	"portfolio_value": daily_portfolio_value,
	"portfolio_gain_loss": daily_gain_loss,
	"portfolio_return": daily_return,
	"benchmark_value": benchmark_daily_value,
	"benchmark_return": benchmark_return,
	"active_return": performance_vs_spy
}).reset_index()

print(performance_summary.head())

performance_summary.to_csv(
	"data/performance_summary.csv",
	index=False
)

# Daily Portfolio Weights

daily_weights = daily_position_values.div(
    daily_portfolio_value,
    axis=0
)

daily_weights["Cash"] = remaining_cash / daily_portfolio_value

print((daily_weights.head() * 100).round(2))

# Weight Validation

weight_check = daily_weights.sum(axis=1)
print(weight_check.head())

daily_weights.reset_index().to_csv(
	"data/daily_weights.csv",
	index=False
)

# Holding Gain or Loss

holding_gain_loss = daily_position_values - purchase_cost
print(holding_gain_loss.head().round(2))

# Holding Contribution to Portfolio Return

holding_contribution = holding_gain_loss / starting_capital
print((holding_contribution.head() * 100).round(2))

# Individual Holding Returns

holding_returns = holding_gain_loss.div(
	purchase_cost,
	axis=1
)
print((holding_returns.head() * 100).round(2))

# Export Holding Data
daily_position_values.reset_index().to_csv(
    "data/daily_position_values.csv",
    index=False
)

holding_gain_loss.reset_index().to_csv(
    "data/holding_gain_loss.csv",
    index=False
)

holding_returns.reset_index().to_csv(
    "data/holding_returns.csv",
    index=False
)

holding_contribution.reset_index().to_csv(
    "data/holding_contribution.csv",
    index=False
)

# Final Phase Validation
assert abs(
    daily_portfolio_value.iloc[0] - starting_capital
) < 0.01

assert abs(
    benchmark_daily_value.iloc[0] - starting_capital
) < 0.01

assert (
    daily_weights.sum(axis=1) - 1
).abs().max() < 0.000001

assert (
    holding_contribution.sum(axis=1) - daily_return
).abs().max() < 0.000001

assert not performance_summary.isna().any().any()

print("Phase 3 validation passed.")

# Daily Returns
portfolio_daily_returns = daily_portfolio_value.pct_change(
	fill_method=None
).dropna()

benchmark_daily_returns = benchmark_daily_value.pct_change(
	fill_method=None
).dropna()

print((portfolio_daily_returns.head() * 100).round(2))
print((benchmark_daily_returns.head() * 100).round(2))

# Daily Return Statistics

portfolio_mean_return = portfolio_daily_returns.mean()
portfolio_volatility = portfolio_daily_returns.std()

benchmark_mean_return = benchmark_daily_returns.mean()
benchmark_volatility = benchmark_daily_returns.std()

print(
	f"Portfolio average daily return: "
	f"{portfolio_mean_return:.4%}"
)

print(
	f"Portfolio daily volatility: "
	f"{portfolio_volatility:.4%}"
)

print(
	f"SPY average daily return: "
	f"{benchmark_mean_return:.4%}"
)

print(
	f"SPY daily volatility: "
	f"{benchmark_volatility:.4%}"
)


# 30-Day Baseline Projection

forecast_days = 30

latest_portfolio_value = daily_portfolio_value.iloc[-1]
latest_benchmark_value = benchmark_daily_value.iloc[-1]

portfolio_baseline_forecast = (
	latest_portfolio_value
	* (1 + portfolio_mean_return) ** forecast_days
)

benchmark_baseline_forecast = (
	latest_benchmark_value
	* (1 + benchmark_mean_return) ** forecast_days
)

print(
	f"Portfolio 30-day baseline forecast: "
   	f"${portfolio_baseline_forecast:,.2f}"
)

print(
	f"SPY 30-day baseline forecast: "
	f"${benchmark_baseline_forecast:,.2f}"
)

# Time-Series Training and Testing Split
split_index = int(len(portfolio_daily_returns) * 0.80)

portfolio_train = portfolio_daily_returns.iloc[:split_index]
portfolio_test = portfolio_daily_returns.iloc[split_index:]

benchmark_train = benchmark_daily_returns.iloc[:split_index]
benchmark_test = benchmark_daily_returns.iloc[split_index:]

print(f"Portfolio training observations: {len(portfolio_train)}")
print(f"Portfolio testing observations: {len(portfolio_test)}")

print(f"Training period ends: {portfolio_train.index[-1]}")
print(f"Testing period begins: {portfolio_test.index[0]}")

# Baseline Test-Period Predictions
portfolio_training_mean = portfolio_train.mean()
benchmark_training_mean = benchmark_train.mean()

portfolio_predictions = pd.Series(
	portfolio_training_mean,
	index=portfolio_test.index
)

benchmark_predictions = pd.Series(
	benchmark_training_mean,
	index = benchmark_test.index
)

baseline_comparison = pd.DataFrame({
	"portfolio_actual": portfolio_test,
	"portfolio_predicted": portfolio_predictions,
	"spy_actual": benchmark_test,
	"spy_predicted": benchmark_predictions
})

print((baseline_comparison.head() * 100).round(2))


# Baseline Forecast Errors

portfolio_errors = portfolio_test - portfolio_predictions
benchmark_errors = benchmark_test - benchmark_predictions

portfolio_mae = portfolio_errors.abs().mean()
portfolio_rmse = (
    portfolio_errors.pow(2).mean()
) ** 0.5

benchmark_mae = benchmark_errors.abs().mean()
benchmark_rmse = (
    benchmark_errors.pow(2).mean()
) ** 0.5

print(f"Portfolio MAE: {portfolio_mae:.4%}")
print(f"Portfolio RMSE: {portfolio_rmse:.4%}")

print(f"SPY MAE: {benchmark_mae:.4%}")
print(f"SPY RMSE: {benchmark_rmse:.4%}")

# Monte Carlo Setup

np.random.seed(42)

simulation_count = 1000
simulation_days = 30

portfolio_simulated_returns = np.random.normal(
	loc = portfolio_train.mean(),
	scale = portfolio_train.std(),
	size = (simulation_days, simulation_count)
)

print(portfolio_simulated_returns.shape)

# Monte Carlo Portfolio Value Paths

portfolio_growth_paths = (
	1 + portfolio_simulated_returns
).cumprod(axis=0)

portfolio_value_paths = (
	latest_portfolio_value
	* portfolio_growth_paths
)

print(portfolio_value_paths.shape)
print(portfolio_value_paths[:5, :5].round(2))

# Portfolio Monte Carlo Outcomes

portfolio_final_values = portfolio_value_paths[-1,:]

portfolio_conservative = np.percentile(
	portfolio_final_values,
	5
)

portfolio_median = np.percentile(
	portfolio_final_values,
	50
)

portfolio_optimistic = np.percentile(
	portfolio_final_values,
	95
)

probability_below_current = (
	portfolio_final_values < latest_portfolio_value
).mean()

print(
    f"Conservative scenario (5th percentile): "
    f"${portfolio_conservative:,.2f}"
)

print(
    f"Median scenario (50th percentile): "
    f"${portfolio_median:,.2f}"
)

print(
	f"Optimistic scenario (95th percentile): "
	f"${portfolio_optimistic:,.2f}"
)

print(
	f"Probability of finishing below current value: "
	f"{probability_below_current:.2%}"
)

# Monte Carlo SPY Benchmark Paths

benchmark_simulated_returns = np.random.normal(
    loc=benchmark_train.mean(),
    scale=benchmark_train.std(),
    size=(simulation_days, simulation_count)
)

benchmark_growth_paths = (
    1 + benchmark_simulated_returns
).cumprod(axis=0)

benchmark_value_paths = (
    latest_benchmark_value
    * benchmark_growth_paths
)

benchmark_final_values = benchmark_value_paths[-1, :]

benchmark_conservative = np.percentile(
    benchmark_final_values,
    5
)

benchmark_median = np.percentile(
    benchmark_final_values,
    50
)

benchmark_optimistic = np.percentile(
    benchmark_final_values,
    95
)

benchmark_probability_below_current = (
    benchmark_final_values < latest_benchmark_value
).mean()

print(
    f"SPY conservative scenario: "
    f"${benchmark_conservative:,.2f}"
)

print(
    f"SPY median scenario: "
    f"${benchmark_median:,.2f}"
)

print(
    f"SPY optimistic scenario: "
    f"${benchmark_optimistic:,.2f}"
)

print(
    f"SPY probability below current value: "
    f"{benchmark_probability_below_current:.2%}"
)

# Forecast Summary Table

forecast_summary = pd.DataFrame({
    "investment": ["Portfolio", "SPY"],
    "forecast_days": [simulation_days, simulation_days],
    "current_value": [
        latest_portfolio_value,
        latest_benchmark_value
    ],
    "baseline_forecast": [
        portfolio_baseline_forecast,
        benchmark_baseline_forecast
    ],
    "conservative_5th": [
        portfolio_conservative,
        benchmark_conservative
    ],
    "median_50th": [
        portfolio_median,
        benchmark_median
    ],
    "optimistic_95th": [
        portfolio_optimistic,
        benchmark_optimistic
    ],
    "probability_below_current": [
        probability_below_current,
        benchmark_probability_below_current
    ],
    "mae": [
        portfolio_mae,
        benchmark_mae
    ],
    "rmse": [
        portfolio_rmse,
        benchmark_rmse
    ]
})

print(forecast_summary)

forecast_summary.to_csv(
    "data/forecast_summary.csv",
    index=False
)



# Forecast Scenario Bands

forecast_bands = pd.DataFrame({
    "forecast_day": np.arange(1, simulation_days + 1),
    "portfolio_5th": np.percentile(
        portfolio_value_paths,
        5,
        axis=1
    ),
    "portfolio_median": np.percentile(
        portfolio_value_paths,
        50,
        axis=1
    ),
    "portfolio_95th": np.percentile(
        portfolio_value_paths,
        95,
        axis=1
    ),
    "spy_5th": np.percentile(
        benchmark_value_paths,
        5,
        axis=1
    ),
    "spy_median": np.percentile(
        benchmark_value_paths,
        50,
        axis=1
    ),
    "spy_95th": np.percentile(
        benchmark_value_paths,
        95,
        axis=1
    )
})

forecast_bands.to_csv(
    "data/forecast_bands.csv",
    index=False
)

baseline_comparison.reset_index().to_csv(
    "data/baseline_backtest.csv",
    index=False
)

# Final Phase 3.5 Validation

assert len(forecast_bands) == simulation_days
assert not forecast_summary.isna().any().any()
assert not forecast_bands.isna().any().any()

assert (
    forecast_summary["conservative_5th"]
    <= forecast_summary["median_50th"]
).all()

assert (
    forecast_summary["median_50th"]
    <= forecast_summary["optimistic_95th"]
).all()

assert forecast_summary[
    "probability_below_current"
].between(0, 1).all()

print("Phase 3.5 validation passed.")

# Prepare Normalized Daily Prices For SQL

daily_prices = (
	market_prices_raw
	.stack(level="Ticker", future_stack=True)
	.reset_index()
	.rename(columns={
		"Date": "price_date",
		"Ticker": "ticker",
		"Open": "open_price",
		"High": "high_price",
		"Low": "low_price",
		"Close": "close_price",
		"Adj Close": "adjusted_close",
		"Volume": "volume"
	})
)

# Remove Incomplete Market-Data Rows

daily_prices = daily_prices.dropna(
	subset=[
		"open_price",
		"high_price",
		"low_price",
		"volume"
	]
)

# Store Volume As Whole Numbers

daily_prices["volume"] = daily_prices["volume"].astype("int64")

# Arrange Columns In The Same Order As SQL Table

daily_prices = daily_prices[
	[
 	"price_date",
        "ticker",
        "open_price",
        "high_price",
        "low_price",
        "close_price",
        "adjusted_close",
        "volume"	
	]
]

# Exclude Incomplete Trading Days Before SQL Export

required_sql_columns = [
	"open_price",
	"high_price",
	"low_price",
	"adjusted_close",
	"volume"
]

daily_prices = daily_prices.dropna(
	subset = required_sql_columns
).copy()


daily_prices.to_csv("data/daily_prices.csv", index=False)

print(daily_prices.head())
print(f"SQL-ready price rows: {len(daily_prices)}")





















