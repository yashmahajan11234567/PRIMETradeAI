-- Daily trader profit/loss

SELECT
Account,

CAST(
DATEADD(
SECOND,
CAST([Timestamp]/1000 AS BIGINT),
'1970-01-01'
)
AS DATE
) AS Trade_Date,

SUM([Closed PnL]) AS Daily_PnL

FROM dbo.historical_data$

GROUP BY
Account,

CAST(
DATEADD(
SECOND,
CAST([Timestamp]/1000 AS BIGINT),
'1970-01-01'
)
AS DATE
);