#!/usr/bin/env bash
set -euo pipefail

if [[ -z ${IMAGE_NAME:-} ]]; then
  IMAGE_NAME=chaos-agent
fi 

function help() {
  echo -e "Usage: go <command>"
  echo -e
  echo -e "    help               Print this help"
  echo -e "    run                Run locally without building binary"
  echo -e "    build              Build binary locally"
  echo -e "    deploy             Deploy to Kubernetes"
  echo -e "    test               Run local unit tests and linting"
  echo -e "    watch-tests        Run local tests continuously while developing"
  echo -e "    init               Set up local virtual env"
  echo -e 
  exit 0
}

function init() {
  _console_msg "Initialising local virtual environment ..." INFO true
  pipenv install --dev
  _console_msg "Init complete" INFO true
}

function run() {
  _console_msg "Running python:main ..." INFO true
  pipenv run python3 main.py "$@"
  _console_msg "Execution complete" INFO true
}

function test() {
    _console_msg "Running flake8 ..." INFO true
    pipenv run flake8 . || true
    _console_msg "Running unit tests ..." INFO true
    pipenv run pytest -s -v --cov-report=term-missing --cov=.
    _console_msg "Tests complete" INFO true
}

function watch-tests() {
  pushd $(dirname $BASH_SOURCE[0]) > /dev/null
  _console_msg "Following unit tests ..." INFO true
  pipenv run ptw -- -s -v --cov-report=term-missing --cov=.
  popd > /dev/null
}

function build() {

  _console_msg "Building python docker image ..." INFO true

  if [[ ${CI_SERVER:-} == "yes" ]]; then
    _assert_variables_set GOOGLE_CREDENTIALS CI_COMMIT_SHA GCP_PROJECT_ID CONTAINER_REGISTRY
    IMAGE_NAME=${CONTAINER_REGISTRY}/${GCP_PROJECT_ID}/${IMAGE_NAME}
    echo "${GOOGLE_CREDENTIALS}" | gcloud auth activate-service-account --key-file -
    trap "gcloud auth revoke --verbosity=error" EXIT
  fi

  _console_msg "Image Name: ${IMAGE_NAME}"

  docker pull ${IMAGE_NAME}:latest || true
  docker build --cache-from ${IMAGE_NAME}:latest --tag ${IMAGE_NAME}:latest .

  if [[ ${CI_SERVER:-} == "yes" ]]; then
    _console_msg "Pushing image to registry ..."
    docker tag ${IMAGE_NAME}:latest ${IMAGE_NAME}:${CI_COMMIT_SHA}
    docker push ${IMAGE_NAME}:${CI_COMMIT_SHA}
  fi

  _console_msg "Build complete" INFO true

}

# ------------------------------------------------------------------

function _assert_variables_set() {

  local error=0
  local varname

  for varname in "$@"; do
    if [[ -z "${!varname-}" ]]; then
      echo "${varname} must be set" >&2
      error=1
    fi
  done

  if [[ ${error} = 1 ]]; then
    exit 1
  fi

}

function _console_msg() {

  local msg=${1}
  local level=${2:-}
  local ts=${3:-}

  if [[ -z ${level} ]]; then level=INFO; fi
  if [[ -n ${ts} ]]; then ts=" [$(date +"%Y-%m-%d %H:%M")]"; fi

  echo ""

  if [[ ${level} == "ERROR" ]] || [[ ${level} == "CRIT" ]] || [[ ${level} == "FATAL" ]]; then
    (echo 2>&1)
    (echo >&2 "-> [${level}]${ts} ${msg}")
  else 
    (echo "-> [${level}]${ts} ${msg}")
  fi

  echo ""

}

function ctrl_c() {
    if [ ! -z ${PID:-} ]; then
        kill ${PID}
    fi
    exit 1
}

trap ctrl_c INT

if [[ ${1:-} =~ ^(help|run|build|deploy|test|watch-tests|init)$ ]]; then
  COMMAND=${1}
  shift
  $COMMAND "$@"
else
  help
  exit 1
fi
