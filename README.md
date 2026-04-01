[![Build and Test](https://github.com/ImperialBower/pknotebook/actions/workflows/CI.yml/badge.svg)](https://github.com/ImperialBower/pknotebook/actions/workflows/CI.yml)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE-GPLv3)

---

# Jupyter All Spark Poker Notebook

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

## Makefile

A `Makefile` is provided for common Docker build and lifecycle tasks. Run `make` to see all available targets, or `make ayce` to build and validate the image in one step.

## Features

- **Python & PySpark**: Full data processing and analysis with Apache Spark
- **Rust Support**: Interactive Rust notebooks and Python-Rust integration via PyO3 and maturin
- **JupyterLab**: Modern notebook interface with multiple kernels

## Rust Integration

This image includes Rust support for building high-performance extensions and working with Rust alongside PySpark. See [RUST_SUPPORT.md](RUST_SUPPORT.md) for detailed documentation.

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
