FROM folkengine/spark4:latest

# Install pkpy (Python bindings for pkcore poker engine) via maturin
# Rust toolchain and maturin are already present in folkengine/spark4
RUN pip install --no-cache-dir "git+https://github.com/ImperialBower/pkpy.git"
