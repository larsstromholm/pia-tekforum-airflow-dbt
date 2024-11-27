from datetime import datetime

import pandas as pd
import psycopg2
from utils.settings import settings

from airflow.datasets import Dataset
from airflow.decorators import dag, task

# Trigger this DAG when dataset `equnior_prices` and `currency_nok_usd` is updated
schedule = [Dataset("equinor_prices"), Dataset("currency_nok_usd")]


def send_email_on_failure(recipients): ...


def update_dashboard(dashboard_id): ...


@dag(
    schedule=schedule,
    start_date=datetime(2023, 1, 1),
    catchup=False,
    max_active_runs=1,
    on_failure_callback=send_email_on_failure(["lars.stromholm@gmail.com"]),
    on_success_callback=update_dashboard("my_dashboard"),
    tags=["demo"],
)
def transform_equinor_prices():
    """Join equinor prices to denote in USD currency."""

    @task
    def read_equinor_prices_from_database():
        """Read equinor prices and return pandas df."""

        with psycopg2.connect(settings.postgres_dsn) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM public.equinor_prices")

                columns = [desc[0] for desc in cur.description]  # Extract column names
                data = cur.fetchall()

        df = pd.DataFrame(data, columns=columns)

        return df

    @task
    def read_currency_nok_usd_daily_from_database():
        """Read currency usd/nok and return pandas df."""

        with psycopg2.connect(settings.postgres_dsn) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM public.currency_nok_usd_daily")

                columns = [desc[0] for desc in cur.description]  # Extract column names
                data = cur.fetchall()

        df = pd.DataFrame(data, columns=columns)

        return df

    @task
    def merge_eqnr_price_with_currencies(
        price_df: pd.DataFrame, currency_df: pd.DataFrame
    ):
        """Join EQNR prices with currencies to denote in USD."""
        merged_df = pd.merge(
            price_df, currency_df, left_on="date", right_on="timestamp", how="left"
        )

        merged_df["ticker"] = "EQNR"
        merged_df["close_nok"] = merged_df["close"]
        merged_df["close_usd"] = merged_df["close"] / merged_df["exchange_rate"]

        result_df = merged_df[["date", "ticker", "close_nok", "close_usd"]]

        return result_df

    @task
    def load_to_database(data: pd.DataFrame):
        with psycopg2.connect(settings.postgres_dsn) as conn:
            with conn.cursor() as cur:
                query = "INSERT INTO public.equinor_prices_nok_usd SELECT * FROM json_populate_recordset(NULL::public.equinor_prices_nok_usd, %s)"

                cur.execute("TRUNCATE TABLE public.equinor_prices_nok_usd")
                cur.execute(query, (data.to_json(orient="records", date_format="iso"),))

    # Create dependencies
    price_df = read_equinor_prices_from_database()

    currency_df = read_currency_nok_usd_daily_from_database()

    df = merge_eqnr_price_with_currencies(price_df, currency_df)

    load_to_database(df)


transform_equinor_prices()
