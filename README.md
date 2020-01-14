# chaos-agent

Runs in Kubernetes, kills random Kubernetes pods / nodes.

## To Do

- [x] Dry Run mode
- [x] Randomise mode
- [x] Num Pods to Delete
- [x] make config filename configurable
- [x] make grace period configurable
- [x] Excluding namespaces for pod deletion
- [ ] Namespace inclusion option
- [ ] Dockerfile
- [ ] CI in gitlab
- [ ] Reenable node deletion (setup test cluster to autoheal first)
- [ ] Num Nodes to Delete
- [ ] Missing tests for nodes

---

## Running The Tool

The agent will run against the current Kubernetes context. In other words, it'll start finding and deleting pods/nodes against your locally authenticated cluster.

It is also designed to run within the cluster itself - acting on other resources accordingly.

/// add note about RBAC here

You can specify a config file to set a number of options to change the agent's behaviour. Defaults are set in `class Config` in `chaos_agent/utils.py`. This file defaults to `./config.yaml`, but can be overridden with `export CFG_FILE=/path/to/yaml`.

## Local Development

`pipenv install --dev --python=$(which python)`

You can then quite easily `pipenv run pytest`, `pipenv run ptw` or `pipenv run python3 main.py`.

> NB: In its default configuration, it will run in dry-run mode! Change values in config.yaml to have it actually delete stuff

Running the tests should be fully stubbed, but remember that running it directly (e.g. from `pipenv shell` or `pipenv run` will do its thing against your current default context'd Kubernetes cluster). **That means if you've set the config up to delete pods/nodes, it will! :)**

glhf :)
