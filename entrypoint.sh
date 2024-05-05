#!/bin/bash

source ~/miniconda3/etc/profile.d/conda.sh

conda activate openmmlab

cd gradio_app
python app.py
