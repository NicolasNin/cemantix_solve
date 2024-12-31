#!/usr/bin/env bash

# Install Python requirements (including git-lfs)
pip install -r requirements.txt

# Initialize git-lfs
git lfs install

# Pull LFS files
git lfs pull