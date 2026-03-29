# CLAUDE.md — spark4

This file provides context and coding guidance for Claude when working in the **spark4** project—a Docker-based JupyterLab environment with Apache Spark, PySpark, and Rust support.

## Project Overview

- **Container**: Custom image built on `jupyter/all-spark-notebook:latest` via Docker Compose
- **Languages**: Python (primary), Rust (via evcxr Jupyter kernel)
- **Framework**: Apache Spark 3.5.0 / PySpark
- **IDE**: JupyterLab (port 8888)
- **Build**: `docker compose build && docker compose up`

## Repository Structure

```
spark4/
├── .github/
│   └── copilot-instructions.md  # GitHub Copilot guidance
├── notebooks/                   # Jupyter notebooks (mounted to /home/jovyan/work)
│   ├── *.ipynb
│   └── data/                    # Data files for analysis
├── bin/                         # Executable scripts (add to PATH for local dev)
├── Dockerfile                   # Custom image with Rust support
├── docker-compose.yml           # Container configuration
├── RUST_SUPPORT.md              # Rust integration guide
├── CLAUDE.md                    # This file
└── README.md
```

## Development Environment

### Container

The project uses a custom Dockerfile that extends `jupyter/all-spark-notebook:latest` with:
- Rust toolchain (rustup, rustfmt, clippy)
- Cargo tools: cargo-edit, cargo-watch
- Jupyter Rust kernel: evcxr_jupyter
- Python package: maturin (for building Rust-Python extensions)

### Key Paths

| Host | Container |
|------|-----------|
| `./notebooks` | `/home/jovyan/work` |

### Quick Start

```bash
docker compose build   # Build custom image (first time or after Dockerfile changes)
docker compose up      # Start JupyterLab in foreground
docker compose up -d   # Start in background
```

## Python Coding Standards

Follow **PEP 8** throughout. Key rules:
- **Indentation**: 4 spaces
- **Line length**: 88 characters (Black formatter standard)
- **Variables/functions**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **Docstrings**: Required for all functions and classes
- **Error handling**: Always handle exceptions explicitly; avoid bare `except:`

## Jupyter Notebook Standards

- Each cell must have a single, clear purpose
- Precede complex code cells with a Markdown cell explaining intent and expected output
- Group imports in the first cell: stdlib → third-party → local
- Notebooks must be fully reproducible (runnable top to bottom without errors)
- Clear all outputs before committing to git

## PySpark Patterns

Always prefer the **DataFrame API** over RDD. Use `spark` (the pre-configured `SparkSession`):

```python
import pyspark.sql.functions as F
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

# Define schema explicitly for external data
schema = StructType([
    StructField("id", IntegerType(), nullable=False),
    StructField("title", StringType(), nullable=True),
])

df = spark.read.csv("/home/jovyan/work/data/books.csv", header=True, schema=schema)
df.printSchema()
df.show(5)
```

Common patterns:
- Cache reused DataFrames: `df.cache()`
- Avoid `.collect()` on large datasets
- Use `spark.sql()` for complex SQL logic on registered temp views
- Use `.toPandas()` only for small, finalized result sets

## Rust Development

Rust notebooks use the **evcxr** Jupyter kernel. Select the "Rust" kernel when creating a new notebook.

PyO3 is **not a pip package** — add it as a Cargo dependency in `Cargo.toml`:

```toml
[dependencies]
pyo3 = { version = "0.22", features = ["extension-module"] }
```

Use `maturin` to build Rust extensions for Python:

```bash
cd /home/jovyan/work/my_rust_lib
maturin develop   # builds and installs into the current Python environment
```

See **RUST_SUPPORT.md** for full examples and troubleshooting.

## Docker & Dockerfile Rules

- Always run `apt-get` commands as root; switch to `USER jovyan` only at the end
- Do **not** use `pip install` for Rust crates (e.g., PyO3 is not on PyPI)
- Chain related `RUN` commands with `&&` to reduce image layers
- Do not add cleanup steps (`apt-get clean`, `rm -rf /var/lib/apt/lists/*`) unless running as root

## bin Directory

Scripts in `./bin/` act as executable documentation:
- Add to PATH: `export PATH="./bin:$PATH"`
- Keep scripts short, commented, and idempotent
- Prefer shell scripts that demonstrate a single workflow step

## Git Standards

- **Commits**: Short imperative subject line (`Add books analysis notebook`)
- **Branches**: Feature branches for new notebooks or features
- **PRs**: Describe notebook purpose, data sources used, and key outputs
- **Notebooks**: Clear output cells before committing

## Troubleshooting Reference

| Problem | Command |
|---------|---------|
| Container won't start | `docker compose logs` |
| Port 8888 in use | `lsof -i :8888` |
| Restart container | `docker compose restart` |
| Rebuild image | `docker compose build --no-cache` |
| Spark job metrics | Open http://localhost:4040 |

## Code Review Checklist

Before suggesting or finalising any code, verify:

- [ ] Follows PEP 8 (Python) or `rustfmt` conventions (Rust)
- [ ] Descriptive variable and function names
- [ ] Docstrings present on all functions and classes
- [ ] Errors handled explicitly
- [ ] Complex logic is commented
- [ ] Compatible with Spark 3.5.0 / PySpark
- [ ] Uses container paths (`/home/jovyan/work/`) not host paths
- [ ] Notebook cells are ordered and independently reproducible

## Reminders

- This is a **prototyping environment**, not production — favour clarity over cleverness
- Always consider **container memory limits** in Spark jobs
- Prefer **PySpark DataFrame operations** over plain Python loops
- PyO3 is a **Rust dependency** (Cargo.toml), not a pip package

