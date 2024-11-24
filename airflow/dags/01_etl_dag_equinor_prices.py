from datetime import datetime

import pandas as pd
import psycopg2
from functions import rename_columns
from utils.settings import settings

from airflow.decorators import dag, task

EQUINOR_DATA = (
    "/workspaces/pia-tekforum-airflow-dbt/data_in/oslobors/EQUINOR_historical_price.csv"
)


def send_email_on_failure(recipients): ...


def update_bi_dashboard_on_success(dashboard_id): ...


@dag(
    schedule="@daily",
    start_date=datetime(2023, 1, 1),
    catchup=False,
    max_active_runs=1,
    on_failure_callback=send_email_on_failure(["lars.stromholm@gmail.com"]),
    on_success_callback=update_bi_dashboard_on_success("my_dashboard"),
    tags=["demo"],
)
def equinor_prices_etl():
    """Extract, transform and load stock prices."""

    @task
    def extract_stock_price_data():
        """Extract data."""

        df = pd.read_csv(EQUINOR_DATA)

        return df

    @task
    def transform_column_names(data: pd.DataFrame):
        """Transform data."""

        data = rename_columns(data)

        return data

    @task
    def load_to_database(data: pd.DataFrame):
        """Load data to database/data warehouse."""

        with psycopg2.connect(settings.postgres_dsn) as conn:
            with conn.cursor() as cur:
                query = "INSERT INTO public.prices SELECT * FROM json_populate_recordset(NULL::public.prices, %s)"

                cur.execute(query, (data.to_json(orient="records"),))

    # Create dependencies
    equinor_stock_prices = extract_stock_price_data()

    transformed_data = transform_column_names(equinor_stock_prices)

    load_to_database(transformed_data)


equinor_prices_etl()
