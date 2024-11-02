#!/bin/bash
base_python_interpreter=""
project_path="pwd"

read -p "Python interpreter: " base_python_interpreter

`$base_python_interpreter -m venv venv`

source ./venv/bin/activate

pip install -U pip
pip install -r requirements.txt
