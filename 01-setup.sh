#!/bin/bash
# 01-setup.sh

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '#' | xargs)
fi

echo "Setting up Google Cloud Project: $GOOGLE_CLOUD_PROJECT_ID"

# Authenticate
gcloud auth login
gcloud config set project $GOOGLE_CLOUD_PROJECT_ID

# Enable APIs
gcloud services enable \
    run.googleapis.com \
    containerregistry.googleapis.com \
    aiplatform.googleapis.com \
    storage.googleapis.com

echo "Setup complete!"
