# syntax=docker/dockerfile:1.9
# Base Dockerfile for Airflow

ARG AIRFLOW_VERSION
ARG PYTHON_VERSION

FROM apache/airflow:${AIRFLOW_VERSION}-python${PYTHON_VERSION}

# Install the Akheloos project in editable mode
COPY requirements.txt .
RUN uv pip install "apache-airflow==${AIRFLOW_VERSION}" -r requirements.txt

ENV HOME=/home/airflow
