from datetime import datetime

import pandas as pd
import psycopg2
import requests
from functions import daily_currency_dataframe
from utils.settings import settings

from airflow.datasets import Dataset
from airflow.decorators import dag, task

NORGES_BANK_API = "https://data.norges-bank.no/api/data/EXR/B.USD.NOK.SP?format=sdmx-json&startPeriod=2022-01-01&endPeriod=2024-11-24&locale=no"


def send_email_on_failure(recipients): ...


@dag(
    schedule="@daily",
    start_date=datetime(2023, 1, 1),
    catchup=False,
    max_active_runs=1,
    on_failure_callback=send_email_on_failure(["lars.stromholm@gmail.com"]),
    tags=["demo"],
)
def extract_currency_nok_usd():
    """Extract, transform and load currencies."""

    @task
    def extract_currency_data_from_norges_bank_api():
        """Extract data."""

        # Extract Norges Bank valutakurs NOK/USD
        response = requests.get(NORGES_BANK_API)

        return response.json()

    @task
    def transform_api_response_to_pandas(data: pd.DataFrame):
        """Transform data from JSON to pandas dataframe."""

        data = daily_currency_dataframe(data)

        return data

    @task(outlets=[Dataset("currency_nok_usd")])
    def load_to_database(data: pd.DataFrame):
        """Load data to database/data warehouse."""

        with psycopg2.connect(settings.postgres_dsn) as conn:
            with conn.cursor() as cur:
                query = "INSERT INTO public.currency_nok_usd_daily SELECT * FROM json_populate_recordset(NULL::public.currency_nok_usd_daily, %s)"

                cur.execute("TRUNCATE TABLE public.currency_nok_usd_daily")
                cur.execute(query, (data.to_json(orient="records"),))

    # Create dependencies
    source_data = extract_currency_data_from_norges_bank_api()

    transformed_data = transform_api_response_to_pandas(source_data)

    load_to_database(transformed_data)


extract_currency_nok_usd()
