USE PortfolioAnalytics;
GO

CREATE TABLE DailyPrices (
    price_date DATE NOT NULL,
    ticker VARCHAR(10) NOT NULL,
    open_price DECIMAL(12,4) NOT NULL,
    high_price DECIMAL(12,4) NOT NULL,
    low_price DECIMAL(12,4) NOT NULL,
    close_price DECIMAL(12,4) NOT NULL,
    adjusted_close DECIMAL(12,4) NULL,
    volume BIGINT NOT NULL,

    CONSTRAINT PK_DailyPrices
        PRIMARY KEY (price_date, ticker),

    CONSTRAINT FK_DailyPrices_Securities
        FOREIGN KEY (ticker) REFERENCES Securities(ticker),

    CONSTRAINT CK_DailyPrices_Prices
        CHECK (
            open_price > 0 AND
            high_price > 0 AND
            low_price > 0 AND
            close_price > 0
        ),

    CONSTRAINT CK_DailyPrices_HighLow
        CHECK (high_price >= low_price),

    CONSTRAINT CK_DailyPrices_Volume
        CHECK (volume >= 0)
);
GO