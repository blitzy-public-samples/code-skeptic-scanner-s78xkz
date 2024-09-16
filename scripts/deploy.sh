#!/bin/bash

# Set environment variables
export PROJECT_ID="code-skeptic-scanner"
export REGION="us-central1"
export BACKEND_IMAGE="gcr.io/${PROJECT_ID}/backend"
export FRONTEND_BUCKET="code-skeptic-scanner-frontend"

# Authenticate with Google Cloud
gcloud auth activate-service-account --key-file=${GCP_KEY_FILE}
gcloud config set project ${PROJECT_ID}

# Build and push Docker images
docker build -t ${BACKEND_IMAGE} ./backend
docker push ${BACKEND_IMAGE}

# Deploy backend services to Cloud Run
gcloud run deploy code-skeptic-backend \
    --image ${BACKEND_IMAGE} \
    --platform managed \
    --region ${REGION} \
    --allow-unauthenticated

# Deploy frontend to Cloud Storage and set up Cloud CDN
gsutil rsync -R ./frontend/build gs://${FRONTEND_BUCKET}
gsutil web set -m index.html -e 404.html gs://${FRONTEND_BUCKET}
gcloud compute backend-buckets create code-skeptic-frontend-bucket --gcs-bucket-name=${FRONTEND_BUCKET}
gcloud compute url-maps create code-skeptic-frontend-urlmap --default-backend-bucket=code-skeptic-frontend-bucket
gcloud compute target-http-proxies create code-skeptic-frontend-proxy --url-map=code-skeptic-frontend-urlmap
gcloud compute forwarding-rules create code-skeptic-frontend-http --target-http-proxy=code-skeptic-frontend-proxy --ports=80

# Update Cloud Functions
gcloud functions deploy code-skeptic-analyzer \
    --runtime python39 \
    --trigger-http \
    --allow-unauthenticated \
    --source ./functions/analyzer

# Run post-deployment tests
./scripts/run_tests.sh

# Notify team of deployment status
if [ $? -eq 0 ]; then
    echo "Deployment successful. Notifying team..."
    # Add notification logic here (e.g., send email, Slack message, etc.)
else
    echo "Deployment failed. Notifying team..."
    # Add notification logic here for failure case
fi

# HUMAN ASSISTANCE NEEDED
# The following areas may need human review and customization:
# 1. Ensure the correct GCP_KEY_FILE path is set in the environment
# 2. Verify the PROJECT_ID, REGION, and other environment variables
# 3. Customize the Cloud Run deployment options if needed
# 4. Adjust the frontend deployment steps if using a different hosting method
# 5. Implement the notification logic for deployment status
# 6. Review and update the Cloud Function deployment if necessary