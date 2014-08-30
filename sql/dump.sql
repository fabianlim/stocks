SELECT * FROM ticker_ticker;

SELECT 
ticker_quote.date, 
ticker_quote.time,
ticker_ticker.name
FROM
ticker_ticker,
ticker_quote
WHERE
ticker_ticker.id = ticker_quote.ticker_id
;
