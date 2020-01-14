# chaos-agent

Runs in Kubernetes, kills random Kubernetes pods / nodes.

## To Do

- [x] Dry Run mode
- [x] Randomise mode
- [x] Num Pods to Delete
- [x] make config filename configurable
- [x] make grace period configurable
- [x] Excluding namespaces for pod deletion
- [x] Namespace inclusion option
- [x] Dockerfile
- [x] Missing tests for nodes
- [x] CI in gitlab
- [ ] Reenable node deletion (setup test cluster to autoheal first)
  - [ ] May need some threading?
- [ ] Num Nodes to Delete
- [ ] assertions for test_find_no_pods & test_find_no_nodes

---

## Running The Tool

The agent will run against the current Kubernetes context. In other words, it'll start finding and deleting pods/nodes against your locally authenticated cluster.

It is also designed to run within the cluster itself - acting on other resources accordingly. See `./go build` and `./go deploy` for pointers on how this works.

/// add note about RBAC here

You can specify a config file to set a number of options to change the agent's behaviour:

- Defaults are set in `class Config` in `chaos_agent/utils.py`
- When using `./go run`, the `local-config.yaml` will be loaded ...
- ... or you can run the python directly through `pipenv` and override it with `export CFG_FILE=/path/to/yaml`.
- In k8s, a `ConfigMap` is used

---

## Local Development

I like to use wrappers through a `./go` bash script to save my typing, see:

1. `./go init` to create your pip venv
2. `./go test` to run pytest locally
3. `./go watch-tests` to run pytest continuously for faster feedback
4. You can also `./go run` to run the tool locally - this **will connect to your current kubectl context and try to do stuff!**
   - by default the config uses dry-run mode (prints what it would do, rather than delete stuff), but if you've changed it ... ;)

---
