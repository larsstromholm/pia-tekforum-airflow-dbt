-- Table: public.currency_nok_usd_daily

-- DROP TABLE IF EXISTS public.currency_nok_usd_daily;

CREATE TABLE IF NOT EXISTS public.currency_nok_usd_daily
(
    "timestamp" date,
    base_currency character(3) COLLATE pg_catalog."default",
    quote_currency character(3) COLLATE pg_catalog."default",
    exchange_rate numeric
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.currency_nok_usd_daily
    OWNER to username;

---------------------------------------

-- Table: public.equinor_prices

-- DROP TABLE IF EXISTS public.equinor_prices;

CREATE TABLE IF NOT EXISTS public.equinor_prices
(
    date date,
    open numeric,
    high numeric,
    low numeric,
    last numeric,
    close numeric,
    number_of_shares bigint,
    number_of_trades bigint,
    turnover bigint,
    vwap numeric
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.equinor_prices
    OWNER to username;

---------------------------------------

-- Table: public.equinor_prices_nok_usd

-- DROP TABLE IF EXISTS public.equinor_prices_nok_usd;

CREATE TABLE IF NOT EXISTS public.equinor_prices_nok_usd
(
    date date,
	ticker char(4),
    close_nok numeric,
	close_usd numeric
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.equinor_prices_nok_usd
    OWNER to username;