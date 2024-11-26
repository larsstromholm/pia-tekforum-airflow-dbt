from datetime import datetime

import pandas as pd
import psycopg2
import requests
from functions import daily_currency_dataframe
from utils.settings import settings

from airflow.decorators import dag, task
from airflow.models.param import Param


def send_email_on_failure(recipients): ...


@dag(
    schedule=None,
    start_date=datetime(2023, 1, 1),
    catchup=False,
    max_active_runs=1,
    on_failure_callback=send_email_on_failure(["lars.stromholm@gmail.com"]),
    params={
        "from_date": Param("2024-01-01", type="string", format="date"),
        "to_date": Param("2024-12-31", type="string", format="date"),
    },
    tags=["demo"],
)
def currency_etl_nok_usd_with_parameters():
    """Extract, transform and load currencies."""

    @task
    def extract_currency_data_from_api(**context):
        """Extract data."""

        from_date = context["params"]["from_date"]
        to_date = context["params"]["to_date"]

        # Extract Norges Bank valutakurs NOK/USD
        response = requests.get(
            f"https://data.norges-bank.no/api/data/EXR/B.USD.NOK.SP?format=sdmx-json&startPeriod={from_date}&endPeriod={to_date}&locale=no"
        )

        return response.json()

    @task
    def transform_api_response_to_pandas(data: pd.DataFrame):
        """Transform data from JSON to pandas dataframe."""

        data = daily_currency_dataframe(data)

        return data

    @task
    def load_to_database(data: pd.DataFrame):
        """Load data to database/data warehouse."""

        with psycopg2.connect(settings.postgres_dsn) as conn:
            with conn.cursor() as cur:
                query = "INSERT INTO public.currency_nok_usd_daily SELECT * FROM json_populate_recordset(NULL::public.currency_nok_usd_daily, %s)"

                cur.execute("TRUNCATE TABLE public.currency_nok_usd_daily")
                cur.execute(query, (data.to_json(orient="records"),))

    # Create dependencies
    source_data = extract_currency_data_from_api()

    transformed_data = transform_api_response_to_pandas(source_data)

    load_to_database(transformed_data)


currency_etl_nok_usd_with_parameters()
