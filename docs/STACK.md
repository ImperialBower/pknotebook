# Technology Stack

This document describes the layers that make up the `folkengine/pknotebook` Docker image and how they relate to each other.

## Layer Overview

```
folkengine/pknotebook   ← this repo
        │
        │  adds: pkpy (Python bindings for pkcore)
        │
folkengine/spark4       ← devplaybooks/spark4
        │
        │  adds: Rust toolchain, evcxr kernel, maturin
        │
jupyter/all-spark-notebook
        │
        │  adds: PySpark, JupyterLab, conda, Python
        │
base Ubuntu image
```

---

## Layer 1 — `jupyter/all-spark-notebook`

The foundation. Maintained by the Jupyter project, it provides:

- **Python 3** via conda
- **JupyterLab** — browser-based notebook interface
- **Apache Spark 3.5.0** and **PySpark** — distributed data processing
- Standard data science libraries (NumPy, pandas, matplotlib, etc.)

Source: [hub.docker.com/r/jupyter/all-spark-notebook](https://hub.docker.com/r/jupyter/all-spark-notebook)

---

## Layer 2 — `folkengine/spark4`

Source: [github.com/devplaybooks/spark4](https://github.com/devplaybooks/spark4)
Image: `folkengine/spark4:latest`

Extends `jupyter/all-spark-notebook` with a full Rust development environment:

| Addition | Purpose |
|----------|---------|
| `rustup` + stable toolchain | Compile Rust code inside the container |
| `rustfmt` / `clippy` | Formatting and linting |
| `cargo-edit` / `cargo-watch` | Dependency management and auto-rebuild |
| `evcxr_jupyter` | Rust kernel for interactive Rust notebooks |
| `maturin` (pip) | Build and install Rust-backed Python extensions |

This layer makes it possible to write Rust in a Jupyter notebook and to compile Rust crates into Python-importable extensions using PyO3 and maturin — without any local Rust installation on the host.

---

## Layer 3 — `folkengine/pknotebook`

Source: [github.com/ImperialBower/pknotebook](https://github.com/ImperialBower/pknotebook) (this repo)
Image: `folkengine/pknotebook:latest`

Adds a pre-built poker analysis library:

```dockerfile
FROM folkengine/spark4:latest
RUN pip install --no-cache-dir "git+https://github.com/ImperialBower/pkpy.git"
```

The `pip install` step:
1. Clones the `pkpy` repository
2. Invokes `maturin` as the build backend (declared in pkpy's `pyproject.toml`)
3. Cargo fetches and compiles `pkcore` as a Rust dependency
4. Installs the compiled extension into the image's Python environment

---

## pkcore

Source: [github.com/ImperialBower/pkcore](https://github.com/ImperialBower/pkcore)
Type: Rust crate (library)

The core poker engine, written entirely in Rust. Provides:

- **Card representation** using the Cactus Kev 32-bit binary encoding — each card is a single `u32`, enabling O(1) hand evaluation via lookup tables
- **Hand evaluation** for Texas Hold'em and other variants
- **Simulation** — equity calculation, Monte Carlo runs
- **Outs calculation** — how many cards improve a given hand

`pkcore` is a pure Rust library with no Python dependency. It is consumed as a Cargo dependency by `pkpy`.

---

## pkpy

Source: [github.com/ImperialBower/pkpy](https://github.com/ImperialBower/pkpy)
Type: Rust crate + Python package (maturin / PyO3)

The Python binding layer for `pkcore`. It exposes `pkcore`'s Rust API to Python using:

- **PyO3** — Rust crate that generates a CPython-compatible extension module
- **maturin** — build tool that compiles the Rust code and packages the result as a standard Python wheel

`pkpy` declares `pkcore` as a Cargo dependency, wraps selected types and functions with `#[pyclass]` / `#[pyfunction]` attributes, and publishes them under the `pkpy` Python namespace.

Once installed, usage in a notebook is straightforward:

```python
import pkpy

# example — exact API depends on pkpy version
hand = pkpy.Hand.parse("As Ks Qs Js Ts")
print(hand.rank())
```

---

## Build & Run

```bash
docker compose build   # compiles pkpy/pkcore, builds image
docker compose up      # starts JupyterLab on http://localhost:8888
```

The first build is slow because Cargo compiles `pkcore` from source. Subsequent builds use Docker layer cache and skip recompilation unless the `pkpy` source changes.

---

## CI

GitHub Actions runs two jobs on every push and pull request:

| Job | What it checks |
|-----|---------------|
| `test` | Python unit tests via pytest |
| `docker-build` | Full Docker image build + `import pkpy` smoke test |

The `docker-build` job uses GitHub Actions cache (`type=gha`) to persist Docker layer cache between runs, keeping Rust recompilation rare.
