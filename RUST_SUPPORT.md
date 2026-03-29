# Adding Rust Support to spark4

This guide explains how to use Rust with the spark4 Docker environment.

## What's Included

The custom Dockerfile extends `jupyter/all-spark-notebook:latest` with:

- **Rust & Cargo**: Latest stable version installed via rustup
- **Rust Tools**: 
  - `rustfmt` - Code formatting
  - `clippy` - Linter and suggestions
  - `cargo-edit` - Manage dependencies
  - `cargo-watch` - Auto-reload on file changes
- **Jupyter Rust Kernel**: `evcxr_jupyter` for interactive Rust notebooks
- **Python-Rust Integration**:
  - `maturin` - Build Python packages from Rust
  - `PyO3` - Add as a Rust dependency in your Cargo.toml

## Building the Container

```bash
# Build the custom image with Rust support
docker compose build

# Run the container
docker compose up
```

> **Note**: The first build will take several minutes as Rust is downloaded and compiled.

## Using Rust in Notebooks

### Create a Rust Notebook

1. Open JupyterLab (http://localhost:8888)
2. Create a new notebook with the **Rust** kernel
3. Start coding!

### Example: Basic Rust in Jupyter

```rust
fn main() {
    let nums = vec![1, 2, 3, 4, 5];
    let sum: i32 = nums.iter().sum();
    println!("Sum: {}", sum);
}
```

### Example: Using Rust with PySpark

You can combine Rust for performance-critical operations with PySpark for distributed processing:

```python
# In a Python cell, call Rust functions compiled with maturin
from my_rust_module import fast_computation

# Use the Rust function with Spark data
result = spark.rdd.map(lambda x: fast_computation(x)).collect()
```

## Building Rust Libraries for Python (maturin)

### Create a New Rust-Python Project

```bash
# In the container's /home/jovyan/work directory
cargo new --name my_lib my_rust_python_lib

cd my_rust_python_lib
maturin init
```

### Example: Simple Rust Function Exposed to Python

**src/lib.rs:**
```rust
use pyo3::prelude::*;

#[pyfunction]
fn add(a: i32, b: i32) -> i32 {
    a + b
}

#[pymodule]
fn my_lib(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(add, m)?)?;
    Ok(())
}
```

**Cargo.toml:**
```toml
[package]
name = "my_lib"
version = "0.1.0"
edition = "2021"

[dependencies]
pyo3 = { version = "0.20", features = ["extension-module"] }
```

### Build and Install

```bash
# In the notebook or terminal within container
maturin develop
```

Then use in Python:
```python
import my_lib
result = my_lib.add(5, 3)
print(result)  # Output: 8
```

## Common Rust Tasks in the Container

### Check Rust Installation

```bash
rustc --version
cargo --version
```

### Create a New Cargo Project

```bash
cd /home/jovyan/work
cargo new my_project
cd my_project
cargo build
cargo run
```

### Watch for File Changes

```bash
cargo watch -x build -x test
```

### Format Code

```bash
cargo fmt
```

### Run Linter

```bash
cargo clippy
```

### Add Dependencies

```bash
cargo add tokio
cargo add serde --features derive
```

## Performance Considerations

### Rust for PySpark UDFs

For computationally intensive operations, you can use Rust to create compiled extensions:

```python
from my_rust_module import compute_intensive

# Define a UDF using the Rust function
from pyspark.sql.functions import pandas_udf
import pandas as pd

@pandas_udf("double")
def rust_powered_udf(s: pd.Series) -> pd.Series:
    return s.apply(lambda x: compute_intensive(x))

result = df.withColumn("processed", rust_powered_udf(df.value))
```

## Troubleshooting

### Container Build Fails

- The Rust installation is memory-intensive. Ensure Docker has sufficient memory (4GB+)
- If build hangs on `rustup`, try rebuilding with `docker compose build --no-cache`

### Rust Kernel Not Available in Jupyter

- Restart the Jupyter kernel or refresh the page
- Verify installation: open a Terminal in JupyterLab and run `evcxr_jupyter --version`

### maturin Build Fails

- Ensure you're in the correct directory with `Cargo.toml`
- Check that PyO3 version in Cargo.toml matches the Python version in the container

## Resources

- [Rust Book](https://doc.rust-lang.org/book/)
- [evcxr - Rust REPL and Jupyter Kernel](https://github.com/google/evcxr)
- [maturin - Build Python Packages from Rust](https://www.maturin.rs/)
- [PyO3 - Rust/Python Interop](https://pyo3.rs/)
- [Cargo Documentation](https://doc.rust-lang.org/cargo/)

