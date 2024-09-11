# PIA Tekforum // Airflow & dbt

[![Devcontainer](https://img.shields.io/static/v1?label=Remote%20-%20Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/larsstromholm/pia-tekforum-airflow-dbt.git)

## Requirements

- [VSCode](https://code.visualstudio.com/download)
- [Docker](https://www.docker.com/products/docker-desktop/)

## Getting started

1. Clone repo ved å trykke på [linken](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/larsstromholm/pia-tekforum-airflow-dbt.git).

2. [pgAdmin](http://localhost:5057/browser/) for å koble til databasen.

   - Brukernavn: `username@pgadmin.no`
   - Passord: `password`

   Tilgang til database i pgAdmin:

   - Airflow passord: `password`
   - DBT passord: `password`

3. [Airflow](http://localhost:8087/)

   - Brukernavn: `username`
   - Passord: `password`

## Running this project

1. Ensure your dbt profile is setup correctly with a connection to the database:

```bash
$ dbt debug
```

2. Load the CSVs with demo data. This command materializes the CSVs as tables in your target schema.

```bash
$ dbt seed
```

3. Run the models:

```bash
$ dbt run
```

4. Test the models:

```bash
$ dbt test
```

5. Generate documentation from dbt `.yml` and `.md` files:

```bash
$ dbt docs generate
```

6. Host your documentation locally:

```bash
$ dbt docs serve
```

## Buildint a dlt pipeline

```bash
dlt init rest_api postgres
```

## Links:

- [dbt](https://docs.getdbt.com/)
- [dbt Labs](https://github.com/dbt-labs)
- [Airflow](https://airflow.apache.org/)
- [Astronomer](https://www.astronomer.io/docs/learn/airflow-dbt)
