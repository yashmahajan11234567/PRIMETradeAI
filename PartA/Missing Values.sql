-- Check missing values

SELECT
SUM(CASE WHEN Account IS NULL THEN 1 ELSE 0 END) AS Missing_Account,
SUM(CASE WHEN Coin IS NULL THEN 1 ELSE 0 END) AS Missing_Coin,
SUM(CASE WHEN [Execution Price] IS NULL THEN 1 ELSE 0 END) AS Missing_Price,
SUM(CASE WHEN [Closed PnL] IS NULL THEN 1 ELSE 0 END) AS Missing_PnL
FROM dbo.historical_data$;