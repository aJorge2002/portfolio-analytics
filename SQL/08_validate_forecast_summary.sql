USE PortfolioAnalytics;
GO

SELECT
    investment,
    forecast_days,
    current_value,
    baseline_forecast,
    conservative_5th,
    median_50th,
    optimistic_95th,
    CAST(
        probability_below_current * 100
        AS DECIMAL(6,2)
    ) AS downside_probability_pct,
    CAST(mae * 100 AS DECIMAL(6,4)) AS mae_pct,
    CAST(rmse * 100 AS DECIMAL(6,4)) AS rmse_pct
FROM dbo.ForecastSummary
ORDER BY
    CASE
        WHEN investment = 'Portfolio' THEN 1
        WHEN investment = 'SPY' THEN 2
        ELSE 3
    END;