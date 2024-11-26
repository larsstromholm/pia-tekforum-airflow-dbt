from datetime import datetime

from airflow.decorators import dag, task


@dag(
    schedule=None,
    start_date=datetime(2023, 1, 1),
    catchup=False,
    max_active_runs=1,
    tags=["demo"],
)
def dag_basics():
    @task
    def task_a():
        return "task a"

    @task
    def task_b():
        return "task b"

    @task
    def task_c():
        return "task c"

    task_a() >> task_b() >> task_c()


dag_basics()
