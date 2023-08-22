#!/bin/bash

cd "$(dirname "$0")" || exit 1

PY_VERSION=3.8
VENV_DIR=venv

info(){
    echo "\e[01;34m$1\e[0m"
}

info "Checking Python version..."
if [ -x "$(command -v python${PY_VERSION})" ]; then
    info "  Python ${PY_VERSION} already exists"
else
    info "  Installing Python ${PY_VERSION}..."
    sudo apt install -y software-properties-common
    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt update
    sudo apt install -y python${PY_VERSION}
    sudo apt install -y python${PY_VERSION}-dev
    sudo apt install -y python${PY_VERSION}-pip
fi

info "Checking Python Virtualenv..."
if [ ! -d ${VENV_DIR} ]; then
    info "  Installing Python Virtualenv..."
    sudo apt install -y python${PY_VERSION}-venv
    python${PY_VERSION} -m venv ${VENV_DIR}
fi

${VENV_DIR}/bin/pip install -r requirements.txt

while true; do
  pids=$(ps -ef | pgrep gunicorn)
  if [ -n "$pids" ]; then
    for pid in $pids; do
      if [ -n "$pid" ]; then
        kill -15 "$pid"
        echo "ending gunicorn process"
        sleep 1
      fi
    done
  else
    break
  fi
done

nohup ${VENV_DIR}/bin/gunicorn run:app -w 1 -b 0.0.0.0:9101 --access-logfile gunicorn.log &
