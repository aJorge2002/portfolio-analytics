USE [PortfolioAnalytics]
GO

/****** Object:  Table [dbo].[Securities]    Script Date: 9/22/2026 3:40:56 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Securities](
	[ticker] [varchar](10) NOT NULL,
	[security_name] [varchar](100) NOT NULL,
	[asset_type] [varchar](20) NOT NULL,
	[sector] [varchar](50) NOT NULL,
	[is_benchmark] [bit] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[ticker] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[Securities] ADD  DEFAULT ((0)) FOR [is_benchmark]
GO


