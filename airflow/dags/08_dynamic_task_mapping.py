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
def dynamic_task_mapping():
    @task
    def create_numbers():
        numbers = []
        for i in range(random.randint(1, 10)):
            numbers.append(i)

        return numbers

    @task
    def process_number(number):
        return number

    numbers = create_numbers()

    process_number.expand(number=numbers)


dynamic_task_mapping()
