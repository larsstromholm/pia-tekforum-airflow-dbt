from cosmos import ExecutionConfig, ExecutionMode, ProfileConfig, ProjectConfig
from cosmos.constants import InvocationMode
from utils.settings import settings

project_config = ProjectConfig(dbt_project_path=settings.dbt_project_dir)
profile_config = ProfileConfig(
    profile_name="tekforum",
    target_name="dev",
    profiles_yml_filepath=settings.dbt_profiles_dir / "profiles.yml",
)
execution_config = ExecutionConfig(
    execution_mode=ExecutionMode.LOCAL, invocation_mode=InvocationMode.DBT_RUNNER
)
