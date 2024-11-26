import random
from datetime import datetime

from airflow.decorators import dag, task


@dag(
    schedule=None,
    start_date=datetime(2023, 1, 1),
    catchup=False,
    max_active_runs=1,
    tags=["demo"],
)
def task_branching():
    @task
    def task_a():
        return {"num": random.randint(1, 10)}

    @task.branch()
    def choose_branch(data):
        if data["num"] < 5:
            return "task_b"

        else:
            return "task_c"

    @task
    def task_b():
        return "task_b"

    @task
    def task_c():
        return "task_c"

    result = task_a()

    choose_branch(result) >> [task_b(), task_c()]


task_branching()
