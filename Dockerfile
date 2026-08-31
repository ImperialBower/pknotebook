FROM folkengine/spark4:1.0.2

# Install pkcore.py (Python bindings for the pkcore poker engine).
# The distribution is named "pkcore.py"; the import name is "pkcore".
# Pre-built manylinux wheels are published, so no Rust compile is needed here.
RUN pip install --no-cache-dir pkcore.py jupyterquiz
