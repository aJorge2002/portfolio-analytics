USE [PortfolioAnalytics]
GO

/****** Object:  Table [dbo].[PortfolioTransactions]    Script Date: 9/22/2026 3:43:03 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[PortfolioTransactions](
	[transaction_id] [int] IDENTITY(1,1) NOT NULL,
	[transaction_date] [date] NOT NULL,
	[ticker] [varchar](10) NOT NULL,
	[transaction_type] [varchar](4) NOT NULL,
	[shares] [int] NOT NULL,
	[purchase_price] [decimal](12, 2) NOT NULL,
	[cost_basis] [decimal](14, 2) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[transaction_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[PortfolioTransactions]  WITH CHECK ADD  CONSTRAINT [FK_Transaction_Securities] FOREIGN KEY([ticker])
REFERENCES [dbo].[Securities] ([ticker])
GO

ALTER TABLE [dbo].[PortfolioTransactions] CHECK CONSTRAINT [FK_Transaction_Securities]
GO

ALTER TABLE [dbo].[PortfolioTransactions]  WITH CHECK ADD  CONSTRAINT [CK_Transaction_Shares] CHECK  (([shares]>(0)))
GO

ALTER TABLE [dbo].[PortfolioTransactions] CHECK CONSTRAINT [CK_Transaction_Shares]
GO

ALTER TABLE [dbo].[PortfolioTransactions]  WITH CHECK ADD  CONSTRAINT [CK_Transaction_Type] CHECK  (([transaction_type]='SELL' OR [transaction_type]='BUY'))
GO

ALTER TABLE [dbo].[PortfolioTransactions] CHECK CONSTRAINT [CK_Transaction_Type]
GO


