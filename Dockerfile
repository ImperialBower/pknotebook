FROM jupyter/all-spark-notebook:latest

# Install Rust and Cargo
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y && \
    . /home/jovyan/.cargo/env && \
    rustup update && \
    rustup component add rustfmt clippy

# Install additional Rust tools
RUN . /home/jovyan/.cargo/env && \
    cargo install cargo-edit && \
    cargo install cargo-watch && \
    cargo install evcxr_jupyter && \
    evcxr_jupyter --install

# Set up Rust in PATH for all users
ENV PATH="/home/jovyan/.cargo/bin:${PATH}"

# Update pip and install Rust-related Python packages
RUN pip install --upgrade pip && \
    pip install maturin


USER jovyan

