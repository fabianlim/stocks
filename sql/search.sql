-- basic query
SELECT * from ticker_ticker;

-- full text search on keywords
SELECT * 
FROM (SELECT name,
            (to_tsvector(coalesce(industry)) || 
            to_tsvector(coalesce(name))) as document
     FROM ticker_ticker) p_search
WHERE p_search.document @@ to_tsquery('steel');


-- update the search_index on Ticker
UPDATE ticker_ticker
    SET search_index = ( 
        SELECT to_tsvector('pg_catalog.english', name) || 
               to_tsvector('pg_catalog.english', symbol) || 
               to_tsvector('pg_catalog.english', industry)
);

-- to restart the sequence
alter sequence ticker_ticker_id_seq restart with 1;
alter sequence ticker_quote_id_seq restart with 1;
