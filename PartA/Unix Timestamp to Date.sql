-- Convert Unix timestamp (milliseconds) to SQL date

SELECT TOP 10
[Timestamp],

DATEADD
(
SECOND,
CAST([Timestamp]/1000 AS BIGINT),
'1970-01-01'
) AS Trade_DateTime

FROM dbo.historical_data$;