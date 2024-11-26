from datetime import datetime

import functions as fn
import pandas as pd
import psycopg2
from utils.settings import settings

from airflow.datasets import Dataset
from airflow.decorators import dag, task
from airflow.sensors.filesystem import FileSensor

SENSOR_DIRECTORY = "/workspaces/pia-tekforum-airflow-dbt/data_in/sensor_example"

file_sensor = FileSensor(
    task_id="wait_for_stock_prices",
    filepath=SENSOR_DIRECTORY,
    deferrable=True,
    poke_interval=10,
    soft_fail=True,  # Will set the task state to `skipped` if timeout
    timeout=60 * 5,  # Timeout after 5 minutes
)


EQUINOR_DATA = SENSOR_DIRECTORY + "/EQUINOR_historical_price.csv"


def send_email_on_failure(recipients): ...


@dag(
    schedule="@daily",
    start_date=datetime(2023, 1, 1),
    catchup=False,
    max_active_runs=1,
    on_failure_callback=send_email_on_failure(["lars.stromholm@gmail.com"]),
    tags=["demo"],
)
def extract_equinor_prices_sensor():
    """Extract, transform and load stock prices."""

    @task
    def extract_stock_price_data():
        """Extract data."""

        df = pd.read_csv(EQUINOR_DATA)

        return df

    @task
    def rename_columns(data: pd.DataFrame):
        """Rename columns."""

        data = fn.rename_columns(data)

        return data

    @task(outlets=[Dataset("equinor_prices")])
    def load_to_database(data: pd.DataFrame):
        """Load data to database/data warehouse."""

        with psycopg2.connect(settings.postgres_dsn) as conn:
            with conn.cursor() as cur:
                query = "INSERT INTO public.equinor_prices SELECT * FROM json_populate_recordset(NULL::public.equinor_prices, %s)"

                cur.execute("TRUNCATE TABLE public.equinor_prices")
                cur.execute(query, (data.to_json(orient="records"),))

    # Create dependencies
    equinor_stock_prices = extract_stock_price_data()

    file_sensor >> equinor_stock_prices

    transformed_data = rename_columns(equinor_stock_prices)

    load_to_database(transformed_data)


extract_equinor_prices_sensor()
