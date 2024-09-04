"""Generate DBT DAGs using Airflow."""

from datetime import datetime

from cosmos import DbtDag, ExecutionConfig, ExecutionMode, ProfileConfig, ProjectConfig
from cosmos.constants import InvocationMode
from utils.settings import settings

dbt_dag = DbtDag(
    project_config=ProjectConfig(dbt_project_path=settings.dbt_project_dir),
    profile_config=ProfileConfig(
        profile_name="tekforum",
        target_name="dev",
        profiles_yml_filepath=settings.dbt_profiles_dir / "profiles.yml",
    ),
    execution_config=ExecutionConfig(
        execution_mode=ExecutionMode.LOCAL, invocation_mode=InvocationMode.DBT_RUNNER
    ),
    # normal dag parameters
    schedule_interval="@daily",
    start_date=datetime(2023, 1, 1),
    catchup=False,
    dag_id="cosmos_dag",
    default_args={"retries": 2},
)
