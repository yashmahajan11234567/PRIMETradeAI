-- Risk exposure distribution

SELECT

CASE

WHEN [Size USD] < 1000
THEN 'Small'

WHEN [Size USD] < 5000
THEN 'Medium'

ELSE 'Large'

END AS Trade_Size_Group,

COUNT(*) AS Trades

FROM dbo.historical_data$

GROUP BY

CASE

WHEN [Size USD] < 1000
THEN 'Small'

WHEN [Size USD] < 5000
THEN 'Medium'

ELSE 'Large'

END;