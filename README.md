[![Build and Test](https://github.com/devplaybooks/spark4/actions/workflows/CI.yml/badge.svg)](https://github.com/devplaybooks/spark4/actions/workflows/CI.yml)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](CODE_OF_CONDUCT.md)
[![License: Apache 2.0](https://img.shields.io/badge/license-Apache%202.0-blue?style=flat-square)](LICENSE-APACHE)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE-GPLv3)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue?style=flat-square)](LICENSE-MIT)

---

# Jupyter All Spark Notebook

A [Docker Compose](https://docs.docker.com/compose/)
[Jupyter notebook](https://docs.jupyter.org/en/latest/) image with
[Apache Spark](https://spark.apache.org/),
[PySpark 3.5.0](https://spark.apache.org/docs/3.5.0/api/python/index.html),
[JupyterLab](https://github.com/jupyterlab/jupyterlab), and
[Rust](https://www.rust-lang.org/) support.

## TL;DR

```shell
docker compose build
docker compose up
```
To run in the background:

```shell
docker-compose up -d
```

Access JupyterLab at http://localhost:8888

## Features

- **Python & PySpark**: Full data processing and analysis with Apache Spark
- **Rust Support**: Interactive Rust notebooks and Python-Rust integration via PyO3 and maturin
- **JupyterLab**: Modern notebook interface with multiple kernels

## Rust Integration

This image includes Rust support for building high-performance extensions and working with Rust alongside PySpark. See [RUST_SUPPORT.md](RUST_SUPPORT.md) for detailed documentation.

## Contributing

### Prerequisites

Install [asdf](https://asdf-vm.com/), then add the required plugins and install all tool versions:

```shell
asdf plugin add python
asdf plugin add java
asdf plugin add nodejs
asdf plugin add scala
asdf plugin add spark
asdf plugin add sbt
asdf plugin add coursier
asdf install
```

This will provision the exact versions defined in `.tool-versions`.

### Running Tests

```shell
pip install -r requirements.txt
pytest
```

### Running Locally with Docker

```shell
docker compose up
```

Access JupyterLab at http://localhost:8888. Notebooks in `./notebooks` are mounted automatically.

## Resources

- [hub.docker.com/r/jupyter/all-spark-notebook](https://hub.docker.com/r/jupyter/all-spark-notebook)
- [Data science with JupyterLab](https://docs.docker.com/guides/jupyter/#run-and-access-a-jupyterlab-container)
- [Supercharging AI/ML Development with JupyterLab and Docker](https://www.docker.com/blog/supercharging-ai-ml-development-with-jupyterlab-and-docker/)
- [PySpark Cheat Sheet](https://cartershanklin.github.io/pyspark-cheatsheet/)
- [Rust Support Guide](RUST_SUPPORT.md)
