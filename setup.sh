#!/bin/bash

# initialize conda for bash
source ~/miniconda3/etc/profile.d/conda.sh

conda create -n slack_bot python=3.11 -y
conda activate slack_bot

python -m pip install -r requirements.txt

django-admin startproject slackbot
cd slackbot
python manage.py startapp events