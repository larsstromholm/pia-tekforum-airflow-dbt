ARG PYTHON_VERSION

FROM mcr.microsoft.com/devcontainers/python:1-${PYTHON_VERSION}-bookworm

ARG AIRFLOW_VERSION
ARG USERNAME
ARG USER_UID
ARG USER_GID

ENV HOME="/home/$USERNAME"

USER root

# Dependencies for Airflow (https://airflow.apache.org/docs/apache-airflow/stable/installation/dependencies.html#debian-bookworm-12)
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
    apt-utils \
    ca-certificates \
    curl \
    dumb-init \
    freetds-bin \
    krb5-user \
    libgeos-dev \
    ldap-utils \
    libsasl2-2 \
    libsasl2-modules \
    libxmlsec1 locales \
    libffi8 \
    libldap-2.5-0 \
    libssl3 \
    netcat-openbsd \
    lsb-release \
    openssh-client \
    python3-selinux \
    rsync \
    sasl2-bin \
    sqlite3 \
    sudo \
    unixodbc

# Create the required user
COPY .devcontainer/user.sh /root/user.sh
RUN /root/user.sh

# Fix permissions
RUN chown -R $USERNAME: ${HOME}

USER $USERNAME

RUN pip install --upgrade uv

ENV PATH="${HOME}/.local/bin:$PATH"

# Run sleep infinity so that the dev container stays alive
CMD [ "sleep", "infinity" ]
