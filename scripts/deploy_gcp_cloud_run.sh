#!/bin/sh
gcloud auth activate-service-account --project=$PROJECT_ID --key-file=secrets/service-account.json
gcloud builds submit --tag gcr.io/$PROJECT_ID/user-sound:1.0.0 .
gcloud run deploy --image=gcr.io/$PROJECT_ID/user-sound:1.0.0 --platform managed --port 8000