from datetime import datetime

import pandas as pd
import psycopg2
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split as sk_train_test_split
from utils.settings import settings

from airflow.decorators import dag, task


def send_email_on_failure(recipients): ...


@dag(
    schedule=None,
    start_date=datetime(2023, 1, 1),
    catchup=False,
    max_active_runs=1,
    on_failure_callback=send_email_on_failure(["lars.stromholm@gmail.com"]),
    tags=["demo"],
)
def mlops_pipeline():
    """Machine learning operations DAG."""

    @task
    def read_stock_price_data_from_database():
        """Extract data."""

        with psycopg2.connect(settings.postgres_dsn) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM public.equinor_prices")

                columns = [desc[0] for desc in cur.description]  # Extract column names
                data = cur.fetchall()

        df = pd.DataFrame(data, columns=columns)

        return df

    @task
    def prepare_features(data: pd.DataFrame):
        """Feature engineering."""

        data["date"] = pd.to_datetime(data["date"])
        data["days_since_start"] = (data["date"] - data["date"].min()).dt.days

        return data

    @task
    def train_and_evaluate_model(data: pd.DataFrame):
        """Train test split."""

        X = data[["days_since_start"]]
        y = data["close"]

        X_train, X_test, y_train, y_test = sk_train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        model = LinearRegression()
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)

        mse = mean_squared_error(y_test, y_pred)

        return mse

    @task
    def upload_model_to_repository(model: LinearRegression): ...

    # Create dependencies
    data = read_stock_price_data_from_database()

    prepared_data = prepare_features(data)

    train_and_evaluate_model(prepared_data)


mlops_pipeline()
