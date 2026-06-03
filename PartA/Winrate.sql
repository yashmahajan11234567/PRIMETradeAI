-- Percentage of profitable trades

SELECT

Account,

COUNT(*) AS Total_Trades,

SUM(
CASE
WHEN [Closed PnL] > 0 THEN 1
ELSE 0
END
) AS Winning_Trades,

ROUND(
100.0 *
SUM(
CASE
WHEN [Closed PnL] > 0 THEN 1
ELSE 0
END
)
/
COUNT(*)
,2
) AS Win_Rate

FROM dbo.historical_data$

GROUP BY Account;