#!/bin/bash
apt-get update
apt-get install -y python-pip python-dev build-essential
pip install numpy pillow

gsutil cp gs://datasets-simone/unet-2.0.tar .
pip install unet-2.0.tar