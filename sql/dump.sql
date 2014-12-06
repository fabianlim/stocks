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

-- this restarts the sequence if we cannot DROP the table
DELETE FROM ticker_quote;
ALTER SEQUENCE ticker_quote_id_seq RESTART WITH 1;

-- drop TABLE to start from scratch
DROP TABLE t_ticker_quote;
DROP SEQUENCE t_ticker_quote_id_seq;

-- this duplicates ticker_quote into t_ticker_quote
CREATE TABLE t_ticker_quote (LIKE ticker_quote INCLUDING ALL);
ALTER TABLE t_ticker_quote ALTER id DROP DEFAULT;
CREATE SEQUENCE t_ticker_quote_id_seq;
INSERT INTO t_ticker_quote SELECT * FROM ticker_quote;
SELECT setval('t_ticker_quote_id_seq', (SELECT max(id) FROM t_ticker_quote), true);
ALTER TABLE t_ticker_quote ALTER id SET DEFAULT nextval('t_ticker_quote_id_seq');
DELETE  FROM t_ticker_quote; -- clear table

-- clear temp_table
DROP TABLE temp_table;
DROP SEQUENCE temp_table_id_seq;

-- this copies duplicates ticker a temporary table temp_table
CREATE TABLE temp_table (LIKE ticker_quote INCLUDING ALL);
ALTER TABLE temp_table ALTER id DROP DEFAULT;
CREATE SEQUENCE temp_table_id_seq;
INSERT INTO temp_table SELECT * FROM ticker_quote;
SELECT setval('temp_table_id_seq', (SELECT max(id) FROM temp_table), true);
ALTER TABLE temp_table ALTER id SET DEFAULT nextval('temp_table_id_seq');

DELETE FROM temp_table; -- clear table

-- add in the columns it has less than the csv file
ALTER TABLE temp_table ADD symbol text;
ALTER TABLE temp_table ADD name text;
ALTER TABLE temp_table ADD industry text;
ALTER TABLE temp_table ADD industry_id integer;
ALTER TABLE temp_table ADD stockrecord_ptr_id integer;

-- DROP PRIMARY KEY constraint as this needs to be adjusted
ALTER TABLE temp_table DROP CONSTRAINT temp_table_pkey;

-- read in the csv
COPY temp_table (id,symbol,name,industry,industry_id,stockrecord_ptr_id,ticker_id,last_trade_date,last_trade_time,date,time,annual_gain,book_value,change,change_inpercent,dividend_share,dividend_yield,eps_est_current_year,eps_est_next_quarter,eps_est_next_year,earnings_share,"fifty_day_MA",oneyr_target_price,peg_ratio,pe_ratio,ebitda,market_cap,percent_change_from_year_high,percent_change,"percent_change_fifty_MA","percent_change_twohund_MA",percent_change_from_year_low,price_book,price_eps_est_current_year,price_eps_est_next_year,price_sales,"twohund_MA",volume,year_high,year_low,last_trade_price) 
FROM '/home/flim/Django/stocks/csv_data/data.csv' DELIMITER ',' CSV;
-- FROM '/home/flim/Django/stocks/csv_data/data.csv' DELIMITER ',' CSV HEADER

-- insert into ticker_quote
INSERT INTO ticker_quote (ticker_id,last_trade_date,last_trade_time,date,time,annual_gain,book_value,change,change_inpercent,dividend_share,dividend_yield,eps_est_current_year,eps_est_next_quarter,eps_est_next_year,earnings_share,"fifty_day_MA",oneyr_target_price,peg_ratio,pe_ratio,ebitda,market_cap,percent_change_from_year_high,percent_change,"percent_change_fifty_MA","percent_change_twohund_MA",percent_change_from_year_low,price_book,price_eps_est_current_year,price_eps_est_next_year,price_sales,"twohund_MA",volume,year_high,year_low,last_trade_price)
SELECT ticker_id,last_trade_date,last_trade_time,date,time,annual_gain,book_value,change,change_inpercent,dividend_share,dividend_yield,eps_est_current_year,eps_est_next_quarter,eps_est_next_year,earnings_share,"fifty_day_MA",oneyr_target_price,peg_ratio,pe_ratio,ebitda,market_cap,percent_change_from_year_high,percent_change,"percent_change_fifty_MA","percent_change_twohund_MA",percent_change_from_year_low,price_book,price_eps_est_current_year,price_eps_est_next_year,price_sales,"twohund_MA",volume,year_high,year_low,last_trade_price FROM temp_table;
