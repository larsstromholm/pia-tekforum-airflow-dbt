from datetime import datetime

from demo_dlt.extract.destination import postgres_destination
from demo_dlt.extract.nobel import nobel_pipeline, nobel_source
from dlt.helpers.airflow_helper import PipelineTasksGroup

from airflow.decorators import dag


@dag(
    schedule="@daily",
    start_date=datetime(2023, 1, 1),
    catchup=False,
    max_active_runs=1,
)
def load_data():
    tasks = PipelineTasksGroup("nobel", use_data_folder=False, wipe_local_data=True)
    # Create the source, the "serialize" decompose option
    # will convert dlt resources into Airflow tasks.
    # Use "none" to disable it.
    tasks.add_run(
        nobel_pipeline(postgres_destination),
        nobel_source,
        decompose="serialize",
        trigger_rule="all_done",
        retries=0,
        provide_context=True,
    )


load_data()
