# Runbook: FestErrorsHigh

**What it means.** More than 5% of `/lineup` requests have failed (HTTP 5xx) for
a whole minute. Festival-goers see "Sorry, something went wrong" and a reference.

**First, restore service. Then find out why.**

1. **Say you're on it.** Post in the crew channel: "Looking at FestErrorsHigh
   (time). Next update in 15 minutes."
2. **What changed?** Which version is live, and since when?

   ```bash
   curl localhost:8000/version
   docker compose ps
   ```

3. **Keep the evidence.** The logs go when the container goes:

   ```bash
   docker compose logs --no-log-prefix app > incident.log
   ```

4. **Roll back** if a release went out recently: put the previous tag back in
   `compose.yaml` (`image: ghcr.io/novastack-hq/hollowmere-app:<previous>`), then:

   ```bash
   docker compose up -d
   ```

5. **Check it worked:** `/version` shows the previous version, the errors stop,
   and the alert goes back to *inactive* within about a minute
   (<http://localhost:9090/alerts>).
6. **Update the channel:** "Service restored at (time) by rolling back to (version)."
7. **Now find the cause** in `incident.log` (search for `"level": "ERROR"`, a
   wristband number or a reference), fix it through the usual gate (a test, a
   pull request into `dev`, a green check, a release to `production`), and write
   the post-mortem (`POSTMORTEM-TEMPLATE.md`).
