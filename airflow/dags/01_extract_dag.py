from datetime import datetime

import pandas as pd

from airflow.decorators import dag, task

PATH = "/workspaces/pia-tekforum-airflow-dbt/data_in/EQUINOR_historical_price.csv"


def send_mail(recipients): ...


@dag(
    schedule="@daily",
    start_date=datetime(2023, 1, 1),
    catchup=False,
    max_active_runs=1,
    on_failure_callback=send_mail(["lars.stromholm@gmail.com"]),
)
def etl_dag():
    """Extract, transform and load."""

    @task
    def extract():
        """Extract data."""

        df = pd.read_csv(PATH)

        return df.to_json(orient="records")

    extract()


etl_dag()
