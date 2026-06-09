FROM nvidia/cuda:12.1.1-runtime-ubuntu22.04

WORKDIR /workspace

# System dependencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    git \
    && rm -rf /var/lib/apt/lists/*

# Python packages
RUN pip install --no-cache-dir fastai jupyter matplotlib pandas scikit-learn polars

# Expose Jupyter
EXPOSE 8888

CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]