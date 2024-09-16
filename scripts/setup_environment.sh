#!/bin/bash

# Set up development environment for Code Skeptic Scanner

# Install required system dependencies
echo "Installing system dependencies..."
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv nodejs npm postgresql

# Set up Python virtual environment
echo "Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Install Node.js and npm (if not already installed)
if ! command -v node &> /dev/null
then
    echo "Installing Node.js and npm..."
    curl -sL https://deb.nodesource.com/setup_14.x | sudo -E bash -
    sudo apt-get install -y nodejs
fi

# Install frontend dependencies
echo "Installing frontend dependencies..."
cd frontend
npm install
cd ..

# Configure Google Cloud SDK
echo "Configuring Google Cloud SDK..."
# HUMAN ASSISTANCE NEEDED
# Please provide the correct project ID and region for Google Cloud SDK configuration
gcloud init
gcloud auth application-default login

# Set up local development database
echo "Setting up local development database..."
sudo -u postgres psql -c "CREATE DATABASE code_skeptic_scanner;"
sudo -u postgres psql -c "CREATE USER code_skeptic WITH PASSWORD 'password';"
sudo -u postgres psql -c "ALTER ROLE code_skeptic SET client_encoding TO 'utf8';"
sudo -u postgres psql -c "ALTER ROLE code_skeptic SET default_transaction_isolation TO 'read committed';"
sudo -u postgres psql -c "ALTER ROLE code_skeptic SET timezone TO 'UTC';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE code_skeptic_scanner TO code_skeptic;"

# Initialize Git hooks for pre-commit checks
echo "Initializing Git hooks..."
cp hooks/pre-commit .git/hooks/
chmod +x .git/hooks/pre-commit

echo "Development environment setup complete!"