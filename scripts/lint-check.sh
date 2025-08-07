#!/bin/bash

echo "Black"
black ../src/ --check
echo "Isort"
isort ../src/ --check
echo "Mypy"
mypy ../src/
echo "Flake 8"
flake8 ../src/