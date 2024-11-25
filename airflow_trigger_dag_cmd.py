import subprocess

if __name__ == "__main__":
    subprocess.run(["airflow", "dags", "trigger", "extract_equinor_prices"])
