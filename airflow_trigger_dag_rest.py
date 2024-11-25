import requests
from requests.auth import HTTPBasicAuth


def trigger_dag(dag_name: str):
    response = requests.get(
        f"http://airflow-webserver:8080/api/v1/dags/{dag_name}/details",
        headers={"Content-Type": "application/json"},
        auth=HTTPBasicAuth("username", "password"),
    )

    print(response.json())


if __name__ == "__main__":
    trigger_dag("extract_equinor_prices")
