#!/bin/bash

echo "Mypy"
mypy ../src/
echo "Ruff"
ruff check ../src/