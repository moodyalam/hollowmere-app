# Fallback: the app on Google Cloud Run

Lecturer only. Use this if the laptop tunnel (`ops/phones.sh`) can't reach
phones on the day. Students never need it.

## One-off set-up (about 30 minutes, the week before)

1. Install the Google Cloud CLI and sign in: `gcloud auth login`, then
   `gcloud auth configure-docker europe-west2-docker.pkg.dev`.
2. Choose a project with billing on, and **set a budget with an alert** (Billing →
   Budgets & alerts). With one instance capped, the expected cost of a lecture is
   pennies, but a budget is the habit.
3. Turn on the APIs and make the image store:

   ```bash
   gcloud services enable run.googleapis.com artifactregistry.googleapis.com
   gcloud artifacts repositories create hollowmere --repository-format=docker --location=europe-west2
   ```

## On the day

| Laptop route (H-A) | Cloud Run route (H-B) |
|---|---|
| Edit the tag in `compose.yaml`, `docker compose up -d` | `GCP_PROJECT=<id> ops/cloudrun/deploy.sh 1.1` (roll back: `... 1.0`) |
| `curl localhost:8000/version` | `curl $CLOUD_RUN_URL/version` |
| Change `FEST_NAME` in `compose.yaml`, `up -d` | `FEST_NAME="..." ops/cloudrun/deploy.sh 1.0` |
| `docker compose ps` shows `(healthy)` | Cloud Run console: the revision is *Ready* (it checks the port is open) |
| `docker compose logs app \| grep 482` | `gcloud logging read 'resource.labels.service_name="hollowmere" AND textPayload:"482"' --limit 20 --format 'value(textPayload)'` |
| Prometheus scrapes `app:8000` | `docker compose -f compose.yaml -f cloudrun/compose.override.yaml up -d prometheus crowd` after editing `cloudrun/prometheus.yml` |

Afterwards: `gcloud run services delete hollowmere --region europe-west2` (logs
hold no names, but delete the service so nothing keeps running).
