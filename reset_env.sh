#!/bin/bash

# Function to print messages
print_message() {
    echo "================================================================"
    echo $1
    echo "================================================================"
}

# Function to run a command and print its output
run_command() {
    echo "Running: $1"
    eval $1 2>&1 | tee -a reset_env.log
}

# Start logging
echo "Starting environment reset at $(date)" > reset_env.log

# Deactivate any active virtual environment
if [[ "$VIRTUAL_ENV" != "" ]]; then
    print_message "Deactivating current virtual environment..."
    run_command "source deactivate"
fi

# Remove the existing virtual environment if it exists
if pyenv versions | grep -q "images-to-stl-env"; then
    print_message "Removing existing virtual environment 'images-to-stl-env'..."
    run_command "pyenv uninstall -f images-to-stl-env"
fi

# Install Python 3.10.12 if it's not already installed
if ! pyenv versions | grep -q "3.10.12"; then
    print_message "Installing Python 3.10.12..."
    run_command "pyenv install 3.10.12"
fi

# Create a new virtual environment using pyenv-virtualenv
print_message "Creating new virtual environment 'images-to-stl-env'..."
run_command "pyenv virtualenv 3.10.12 images-to-stl-env"

# Activate the new virtual environment
print_message "Activating virtual environment 'images-to-stl-env'..."
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
pyenv activate images-to-stl-env

# Verify the Python version
print_message "Verifying Python version..."
python_version=$(python --version 2>&1)
echo "Python version: $python_version" | tee -a reset_env.log

# Create requirements.txt with updated dependencies
print_message "Creating requirements.txt with updated dependencies..."
cat <<EOL > requirements.txt
numpy==1.21.6
opencv-python==4.5.5.64
scikit-image==0.18.3
open3d==0.18.0
gradio==3.9.1
httpx==0.23.0
httpcore==0.15.0
EOL

# Install the dependencies
print_message "Installing dependencies from requirements.txt..."
run_command "pip install -r requirements.txt"

# Run the application to verify the setup
print_message "Running the application..."
run_command "python app.py"
