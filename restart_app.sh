#!/bin/bash

echo "================================================================"
echo "Deactivating any existing virtual environment..."
echo "================================================================"
if [[ -n "$VIRTUAL_ENV" ]]; then
    deactivate
fi

echo "================================================================"
echo "Activating virtual environment 'images-to-stl-env'..."
echo "================================================================"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
pyenv activate images-to-stl-env

echo "================================================================"
echo "Running the application..."
echo "================================================================"
python app.py
