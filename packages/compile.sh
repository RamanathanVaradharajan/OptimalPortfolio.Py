#!/bin/bash

# stops the script in case of an error.
set -e

# Go to the directory of this script.
cd "$(dirname "$0$")"

echo "Checking for Pip and Pip-tools updates."
pip install --upgrade pip
pip install --upgrade pip-tools

echo "Compiling required packages, please wait..."
pip-compile --upgrade ./dev.in