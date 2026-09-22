USE PortfolioAnalytics;
GO

SELECT
    COUNT(*) AS performance_rows,
    MIN(performance_date) AS first_date,
    MAX(performance_date) AS last_date
FROM dbo.PortfolioPerformance;

SELECT TOP (5)
    performance_date,
    portfolio_value,
    portfolio_gain_loss,
    portfolio_return,
    benchmark_value,
    benchmark_return,
    active_return
FROM dbo.PortfolioPerformance
ORDER BY performance_date;