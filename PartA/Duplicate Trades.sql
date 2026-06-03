-- Find duplicate trade IDs

SELECT
[Trade ID],
COUNT(*) AS Duplicate_Count
FROM dbo.historical_data$
GROUP BY [Trade ID]
HAVING COUNT(*) > 1;