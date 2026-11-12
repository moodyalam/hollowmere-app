#!/usr/bin/env bash
# Fallback H-B (lecturer only): run the app on Google Cloud Run instead of
# tunnelling to the laptop. Phones get a fixed https address, so its QR code can
# go on a slide in advance.
#
# One-off set-up (see README.md next to this file): gcloud installed, signed in,
# a project with billing, a budget, and the Artifact Registry and Run APIs on.
#
#   ops/cloudrun/deploy.sh 1.0      # deploy (or roll back to) release 1.0
#   ops/cloudrun/deploy.sh 1.1      # deploy release 1.1 (the incident)
set -euo pipefail
VERSION="${1:?Which release? e.g. 1.0}"
PROJECT="${GCP_PROJECT:?Set GCP_PROJECT to your Google Cloud project ID}"
REGION="${GCP_REGION:-europe-west2}"          # London
SERVICE="hollowmere"
SOURCE="ghcr.io/novastack-hq/hollowmere-app:$VERSION"
TARGET="$REGION-docker.pkg.dev/$PROJECT/hollowmere/hollowmere-app:$VERSION"

# Cloud Run pulls from Artifact Registry, so copy the published image there.
# --platform: Cloud Run runs Intel (amd64) machines.
docker pull --platform linux/amd64 "$SOURCE"
docker tag "$SOURCE" "$TARGET"
docker push "$TARGET"

# One instance at most (one set of metrics, one set of logs, a capped bill),
# and one kept warm so the first phone doesn't wait for a cold start.
gcloud run deploy "$SERVICE" \
  --project "$PROJECT" --region "$REGION" \
  --image "$TARGET" \
  --min-instances 1 --max-instances 1 --concurrency 200 \
  --set-env-vars "FEST_NAME=${FEST_NAME:-Hollowmere Festival},LOG_LEVEL=INFO" \
  --allow-unauthenticated

URL=$(gcloud run services describe "$SERVICE" --project "$PROJECT" --region "$REGION" --format 'value(status.url)')
echo "Phones join at: $URL/join"
echo "Crew screen:    $URL/crew"
