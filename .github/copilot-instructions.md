# GitHub Copilot Instructions for spark4

This file provides guidance for GitHub Copilot to understand the development environment, coding standards, and best practices for the **spark4** project—a Docker-based JupyterLab environment with Apache Spark and PySpark.

## Project Overview

**spark4** is a containerized Jupyter notebook environment configured for Apache Spark development and data analysis:
- **Container**: `jupyter/all-spark-notebook:latest` via Docker Compose
- **Languages**: Python (primary), Jupyter notebooks
- **Framework**: Apache Spark 3.5.0 / PySpark
- **IDE**: JupyterLab
- **Port**: 8888 (localhost:8888)

## Development Environment Setup

### Quick Start
```bash
docker compose up          # Run in foreground
docker-compose up -d       # Run in background
```

### Volumes & Paths
- **Host**: `./notebooks` directory
- **Container**: `/home/jovyan/work`
- Notebooks are mounted as volumes for live development and persistence

### Environment
- JupyterLab is enabled by default (`JUPYTER_ENABLE_LAB=yes`)
- All notebooks run within the container's Spark-enabled Python environment

## Code Style & Python Standards

### Python Conventions
- **Style Guide**: Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- **Indentation**: 4 spaces (not tabs)
- **Line Length**: 88 characters (Black formatter standard)
- **Naming**: 
  - `snake_case` for variables and functions
  - `PascalCase` for classes
  - `UPPER_SNAKE_CASE` for constants

### Notebook Best Practices
- **Cell Structure**: Each cell should have a clear purpose
- **Documentation**: Include markdown cells explaining logic and outputs
- **Imports**: Group imports logically (stdlib, third-party, local)
- **Output**: Clear, labeled output for data exploration and results
- **Reproducibility**: Ensure notebooks can be re-run from top to bottom

### PySpark Patterns
- Use `spark` context for DataFrame operations
- Prefer DataFrame API over RDD for better performance
- Include schema definitions for external data sources
- Add comments explaining transformations and aggregations

## File Organization

```
spark4/
├── notebooks/           # Jupyter notebooks (mounted to /home/jovyan/work)
│   ├── *.ipynb         # Individual notebook files
│   └── data/           # Data files for analysis
├── bin/                # Executable scripts for development tasks
├── docker-compose.yml  # Container configuration
├── README.md           # Project documentation
└── copilot-instructions.md  # This file
```

## Git & Contribution Standards

- **Commit Messages**: Clear, descriptive commit messages
- **Branches**: Use feature branches for new notebooks or features
- **Pull Requests**: Include context about notebook purpose and functionality
- **Licensing**: Project uses Apache 2.0, GPLv3, and MIT licenses

## Debugging & Troubleshooting

### Container Issues
- Check container logs: `docker compose logs`
- Ensure port 8888 is available: `lsof -i :8888`
- Restart container: `docker compose restart`

### Jupyter/Notebook Issues
- Clear notebook output if experiencing performance issues
- Restart kernel in JupyterLab when dependencies change
- Check browser console for JavaScript errors

### Spark Issues
- Monitor memory usage in long-running jobs
- Use `spark.sql()` for SQL queries on DataFrames
- Check Spark UI (typically at localhost:4040) for job metrics

## Recommended Tools & Extensions

### For Development
- **Jupyter Notebooks**: Standard `.ipynb` format
- **Python Debugger**: Use `pdb` or `%debug` magic in notebooks
- **Git Integration**: Visual Studio Code with Jupyter extension, or command line

### For Data Analysis
- **Pandas**: Interop with Spark DataFrames via `.toPandas()`
- **Matplotlib/Seaborn**: Visualization libraries in notebooks
- **NumPy**: Numerical computing support

## Rust Development

### Rust Support
The container includes full Rust support with:
- **Rust Toolchain**: Latest stable via rustup with rustfmt and clippy
- **Jupyter Kernel**: Interactive Rust notebooks via evcxr_jupyter
- **Python-Rust Integration**: maturin for building Python extensions from Rust (PyO3 is added as a Cargo dependency)
- **Cargo Tools**: cargo-edit, cargo-watch for productivity

### Using Rust in Notebooks
- Create a new notebook and select the **Rust** kernel
- Write Rust code directly in notebook cells with REPL feedback
- Combine with PySpark for high-performance distributed computing

### Building Python Packages from Rust
```python
# Use maturin to build Rust libraries as Python packages
# Details in RUST_SUPPORT.md
```

**See RUST_SUPPORT.md for comprehensive Rust guide, examples, and troubleshooting.**

## Working with the bin Directory

Scripts in `./bin/` demonstrate project workflows:
- Add to your `PATH` to run from project root: `export PATH="./bin:$PATH"`
- Scripts serve as both executable documentation and proof-of-concept
- Keep scripts simple and well-commented

## Common Tasks

### Create a New Notebook
1. Use JupyterLab's "New Notebook" feature
2. Select Python kernel
3. Save to `notebooks/` directory with descriptive name
4. Follow the notebook best practices above

### Load Data
```python
import pyspark.sql.functions as F
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

# Read CSV
df = spark.read.csv("/home/jovyan/work/data/books.csv", header=True)

# Display schema and sample
df.printSchema()
df.show(5)
```

### Export Results
```python
# To CSV
df.write.mode("overwrite").csv("/home/jovyan/work/output")

# To Pandas
pandas_df = df.toPandas()
```

## Performance Considerations

- Keep DataFrame operations efficient; avoid excessive `.collect()` calls
- Use partitioning for large datasets
- Monitor Spark's web UI for bottlenecks
- Cache DataFrames if reusing multiple times: `df.cache()`

## Resources

- [Apache Spark Documentation](https://spark.apache.org/docs/latest/)
- [PySpark API Reference](https://spark.apache.org/docs/3.5.0/api/python/index.html)
- [JupyterLab Documentation](https://jupyterlab.readthedocs.io/)
- [PySpark Cheat Sheet](https://cartershanklin.github.io/pyspark-cheatsheet/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)

## Code Review Checklist

When Copilot suggests code, ensure it meets these criteria:
- ✅ Follows PEP 8 style guidelines
- ✅ Has clear, descriptive variable/function names
- ✅ Includes docstrings for functions and classes
- ✅ Handles errors appropriately
- ✅ Includes comments for complex logic
- ✅ Is compatible with Spark 3.5.0 / PySpark
- ✅ Works within containerized environment constraints

## Notes for Copilot

- This is a **data analysis and prototyping environment**, not a production system
- Notebooks should be **exploratory and reproducible**
- Always consider **memory constraints** in the container
- Prioritize **clarity and documentation** over clever one-liners
- Suggest **PySpark DataFrame operations** over raw Python where applicable
- Remember **relative paths** within container context (`/home/jovyan/work/`)

