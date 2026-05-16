#!/bin/bash
# 03-deploy-infrastructure.sh

if [ -f .env ]; then
    export $(cat .env | grep -v '#' | xargs)
fi

echo "Deploying infrastructure with Terraform..."

cd terraform
terraform init
terraform apply -auto-approve \
    -var="project_id=$GOOGLE_CLOUD_PROJECT_ID" \
    -var="bucket_name=$GENMEDIA_BUCKET"

echo "Infrastructure deployed!"
