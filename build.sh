#!/usr/bin/env bash
apt-get update && apt-get install -y git-lfs
git lfs install

# Pull LFS files
git lfs pullpip install -r requirements.txt