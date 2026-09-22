USE PortfolioAnalytics;
GO

IF OBJECT_ID('dbo.ForecastBands', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.ForecastBands (
        forecast_day INT NOT NULL,

        portfolio_5th DECIMAL(14,2) NOT NULL,
        portfolio_median DECIMAL(14,2) NOT NULL,
        portfolio_95th DECIMAL(14,2) NOT NULL,

        spy_5th DECIMAL(14,2) NOT NULL,
        spy_median DECIMAL(14,2) NOT NULL,
        spy_95th DECIMAL(14,2) NOT NULL,

        CONSTRAINT PK_ForecastBands
            PRIMARY KEY (forecast_day),

        CONSTRAINT CK_ForecastBands_Day
            CHECK (forecast_day > 0),

        CONSTRAINT CK_ForecastBands_Values
            CHECK (
                portfolio_5th > 0
                AND portfolio_median > 0
                AND portfolio_95th > 0
                AND spy_5th > 0
                AND spy_median > 0
                AND spy_95th > 0
            ),

        CONSTRAINT CK_ForecastBands_PortfolioOrder
            CHECK (
                portfolio_5th <= portfolio_median
                AND portfolio_median <= portfolio_95th
            ),

        CONSTRAINT CK_ForecastBands_SPYOrder
            CHECK (
                spy_5th <= spy_median
                AND spy_median <= spy_95th
            )
    );

    PRINT 'ForecastBands table created successfully.';
END
ELSE
BEGIN
    PRINT 'ForecastBands table already exists.';
END;
GO