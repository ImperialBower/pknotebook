FROM folkengine/spark4:1.0.2

# Install pkpy (Python bindings for pkcore poker engine) via maturin
# Rust toolchain and maturin are already present in folkengine/spark4
RUN pip install --no-cache-dir "git+https://github.com/ImperialBower/pkpy.git@v0.0.36"
