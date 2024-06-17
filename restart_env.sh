#!/bin/bash

echo "================================================================"
echo "Removing existing virtual environment 'images-to-stl-env'..."
echo "================================================================"
pyenv uninstall -f images-to-stl-env

echo "================================================================"
echo "Creating new virtual environment 'images-to-stl-env'..."
echo "================================================================"
pyenv virtualenv 3.10.12 images-to-stl-env

echo "================================================================"
echo "Activating virtual environment 'images-to-stl-env'..."
echo "================================================================"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
pyenv activate images-to-stl-env

echo "================================================================"
echo "Verifying Python version..."
echo "================================================================"
python --version

echo "================================================================"
echo "Installing dependencies from requirements.txt..."
echo "================================================================"
pip install -r requirements.txt

echo "================================================================"
echo "Running the application..."
echo "================================================================"
python app.py
