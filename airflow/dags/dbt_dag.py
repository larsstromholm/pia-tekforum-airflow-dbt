"""Generate DBT DAGs using Airflow."""

from datetime import datetime

from cosmos import DbtDag
from utils.dbt_project import execution_config, profile_config, project_config

dbt_dag = DbtDag(
    execution_config=execution_config,
    profile_config=profile_config,
    project_config=project_config,
    schedule="@daily",
    start_date=datetime(2023, 1, 1),
    catchup=False,
    dag_id="cosmos_dag",
)
