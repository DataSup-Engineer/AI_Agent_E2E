#!/bin/bash
# 02-build-images.sh

if [ -f .env ]; then
    export $(cat .env | grep -v '#' | xargs)
fi

echo "Building Docker image for $GOOGLE_CLOUD_PROJECT_ID..."

# Build and push to GCR
docker build -t gcr.io/$GOOGLE_CLOUD_PROJECT_ID/storygen-backend .
docker push gcr.io/$GOOGLE_CLOUD_PROJECT_ID/storygen-backend

echo "Images pushed successfully!"
