USE PortfolioAnalytics;
GO

IF OBJECT_ID('dbo.ForecastSummary', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.ForecastSummary (
        investment VARCHAR(20) NOT NULL,
        forecast_days INT NOT NULL,

        current_value DECIMAL(14,2) NOT NULL,
        baseline_forecast DECIMAL(14,2) NOT NULL,
        conservative_5th DECIMAL(14,2) NOT NULL,
        median_50th DECIMAL(14,2) NOT NULL,
        optimistic_95th DECIMAL(14,2) NOT NULL,

        probability_below_current DECIMAL(12,10) NOT NULL,
        mae DECIMAL(12,10) NOT NULL,
        rmse DECIMAL(12,10) NOT NULL,

        CONSTRAINT PK_ForecastSummary
            PRIMARY KEY (investment),

        CONSTRAINT CK_ForecastSummary_Days
            CHECK (forecast_days > 0),

        CONSTRAINT CK_ForecastSummary_Values
            CHECK (
                current_value > 0
                AND baseline_forecast > 0
                AND conservative_5th > 0
                AND median_50th > 0
                AND optimistic_95th > 0
            ),

        CONSTRAINT CK_ForecastSummary_Order
            CHECK (
                conservative_5th <= median_50th
                AND median_50th <= optimistic_95th
            ),

        CONSTRAINT CK_ForecastSummary_Probability
            CHECK (
                probability_below_current >= 0
                AND probability_below_current <= 1
            ),

        CONSTRAINT CK_ForecastSummary_Errors
            CHECK (mae >= 0 AND rmse >= 0)
    );

    PRINT 'ForecastSummary table created successfully.';
END
ELSE
BEGIN
    PRINT 'ForecastSummary table already exists.';
END;
GO
