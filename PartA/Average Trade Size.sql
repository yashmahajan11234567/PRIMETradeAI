-- Average trade size in USD

SELECT

Account,

AVG([Size USD]) AS Avg_Trade_Size

FROM dbo.historical_data$

GROUP BY Account;