#!/usr/bin/env bash

# Inspired by https://github.com/h4l/dev-container-docker-compose-volume-or-bind/blob/main/.devcontainer/gen-docker-compose-workspace-env.sh
# See https://github.com/microsoft/vscode-remote-release/issues/171

while [[ $# -gt 0 ]]; do
  case $1 in
    --local-workspace-dir)
      LOCAL_WORKSPACE_DIR="$2"
      shift; shift
      ;;
  esac
done

if [[ ${LOCAL_WORKSPACE_DIR:-} == '' ]]; then
  echo "$0: --local-workspace-dir option or LOCAL_WORKSPACE_DIR envar must be set" >&2
  exit 1
fi

WORKSPACE_DIR="${LOCAL_WORKSPACE_DIR:?}"

CONTAINER_ID="$(hostname)"
# shellcheck disable=SC2016
WORKSPACE_MOUNT_SOURCE_FMT='
{{- $source := "" }}
{{- range .HostConfig.Mounts }}
    {{- if (and (eq .Type "volume") (eq .Target "/workspaces")) }}
    {{- $source = .Source }}
    {{- end }}
{{- end }}
{{- $source }}'

WORKSPACE_VOLUME_NAME=$(docker container inspect "$CONTAINER_ID" --format="$WORKSPACE_MOUNT_SOURCE_FMT")


# LOCAL_WORKSPACE_DIR is the path of the workspace dir in the mounted
# container volume (e.g. /workspaces/myproject), and this same path is
# also the path of the workspace in the devcontainer (container volume
# workspaces ignore the value of "workspaceFolder" in devcontainer.json).

WORKSPACE_VOLUME_TARGET="$(dirname "${WORKSPACE_DIR:?}")"

ENVARS="$(
env -i WORKSPACE_VOLUME_NAME="${WORKSPACE_VOLUME_NAME:-}" \
       WORKSPACE_VOLUME_TARGET="${WORKSPACE_VOLUME_TARGET:-}" \
       WORKSPACE_DIR="${WORKSPACE_DIR:-}" \
       env
)"

{
    echo ""
    echo "# Generated by $0 - do not modify by hand";
    echo ""
    echo "$ENVARS";
    echo ""
} > .devcontainer/workspace.env

cat .devcontainer/*.env > .devcontainer/.env

source .devcontainer/.env

# Make sure to apply the right permissions to the directory
chown -R "${USER_UID:?}:${USER_GID:?}" .
