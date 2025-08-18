#!/bin/bash
set -eou pipefail

apt-get update && apt upgrade -y && apt-get install -y  --no-install-recommends \
    apt-utils \
    ca-certificates \
    curl \
    && \
    update-ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
