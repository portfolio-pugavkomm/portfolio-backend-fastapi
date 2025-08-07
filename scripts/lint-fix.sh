#!/bin/bash

echo "Black"
black ../src/
echo "Isort"
isort ../src/
echo "Mypy"
mypy ../src/
echo "Flake 8"
flake8 ../src/