USE PortfolioAnalytics;
GO

IF OBJECT_ID('dbo.PortfolioPerformance', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.PortfolioPerformance (
        performance_date DATE NOT NULL,

        portfolio_value DECIMAL(14,2) NOT NULL,
        portfolio_gain_loss DECIMAL(14,2) NOT NULL,
        portfolio_return DECIMAL(16,10) NOT NULL,

        benchmark_value DECIMAL(14,2) NOT NULL,
        benchmark_return DECIMAL(16,10) NOT NULL,
        active_return DECIMAL(16,10) NOT NULL,

        CONSTRAINT PK_PortfolioPerformance
            PRIMARY KEY (performance_date),

        CONSTRAINT CK_PortfolioPerformance_Values
            CHECK (
                portfolio_value > 0
                AND benchmark_value > 0
            )
    );

    PRINT 'PortfolioPerformance table created successfully.';
END
ELSE
BEGIN
    PRINT 'PortfolioPerformance table already exists.';
END;
GO