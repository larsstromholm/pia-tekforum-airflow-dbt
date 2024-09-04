#!/usr/bin/env bash
set -x

# git config
git config --global push.autoSetupRemote true
git config --global core.editor 'code --wait'


# Install all Python dependencies
uv venv --python ${PYTHON_VERSION}
source ${WORKSPACE_DIR}/.venv/bin/activate
uv pip install -r requirements.txt

echo "
source ${WORKSPACE_DIR}/.venv/bin/activate
" > ${HOME}/.bashrc

# Python autocompletion
activate-global-python-argcomplete --yes &

wait
