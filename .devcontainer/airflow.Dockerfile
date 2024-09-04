# syntax=docker/dockerfile:1.9
# Base Dockerfile for Airflow

ARG AIRFLOW_VERSION
ARG PYTHON_VERSION

FROM apache/airflow:${AIRFLOW_VERSION}-python${PYTHON_VERSION}

ARG CACHE_DIR
ARG AIRFLOW_UID

# Prepare the cache directory
USER root
ENV CACHE_DIR=${CACHE_DIR}
RUN mkdir -p ${CACHE_DIR} && \
    chown -R ${AIRFLOW_UID}:0 ${CACHE_DIR} && \
    chmod -R 0755 ${CACHE_DIR}
VOLUME ${CACHE_DIR}

USER airflow

# Install the Akheloos project in editable mode
COPY requirements.txt .
RUN uv pip install -r requirements.txt

ENV HOME=/home/airflow
