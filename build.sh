#!/usr/bin/env bash

# Install Python requirements (including git-lfs)
pip install -r requirements.txt

mkdir models
curl -L -o models/frWac_no_postag_phrase_500_cbow_cut10_stripped.bin https://github.com/NicolasNin/cemantix_solve/raw/refs/heads/master/models/frWac_no_postag_phrase_500_cbow_cut10_stripped.bin
