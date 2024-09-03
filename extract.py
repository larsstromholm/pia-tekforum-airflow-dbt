from settings import settings
import sqlalchemy
import pandas as pd
import requests

engine = sqlalchemy.create_engine(
        f"postgresql+psycopg2://"
        f"{settings.postgres_user}:"
        f"{settings.postgres_password}@"
        f"{settings.postgres_host}:"
        f"{settings.postgres_port}/"
        f"{settings.postgres_db}"
        )


response = requests.get("https://api.github.com/repos/dbt-labs/dbt-core/issues")

json = response.json()

df = pd.DataFrame(json)

df.to_sql(
    name="dbt_issues", 
    schema="tekforum", 
    con=engine, 
    if_exists="replace", 
    dtype={
        "user": sqlalchemy.types.JSON,
        "assignee": sqlalchemy.types.JSON,
        "assignees": sqlalchemy.types.JSON,
        "pull_request": sqlalchemy.types.JSON, 
        "labels": sqlalchemy.types.JSON,
        "milestone": sqlalchemy.types.JSON,
        "reactions": sqlalchemy.types.JSON
        }
    )