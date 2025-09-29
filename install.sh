#!/bin/bash
set -e

read -p "Python interpreter (e.g. python3.11): " base_python_interpreter

# Создание виртуального окружения
$base_python_interpreter -m venv venv

# Активация окружения
source ./venv/bin/activate

# Установка зависимостей
pip install -U pip
pip install -r requirements.txt
