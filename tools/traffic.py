"""Pretend festival-goers: check the line-up, over and over.

Compose runs this for you (the "crowd" service in ops/compose.yaml), so the
graphs are never empty even before any phone joins. Standard library only.

    python tools/traffic.py http://localhost:8000
"""

import random
import sys
import time
import urllib.error
import urllib.request

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
# Who's checking: people with no wristband yet, ticket 102 (General) and
# ticket 103 (Luna Vale, VIP). About one check in seven is Luna's.
VISITS = ["/lineup", "/lineup", "/lineup?ticket=102", "/lineup?ticket=102",
          "/lineup?ticket=102", "/lineup?ticket=103", "/version"]

print(f"Festival-goers are checking {BASE} (Ctrl+C to stop)", flush=True)
while True:
    path = random.choice(VISITS)
    try:
        with urllib.request.urlopen(BASE + path, timeout=5) as reply:
            status = reply.status
    except urllib.error.HTTPError as error:
        status = error.code  # 500 and friends arrive as an exception
    except OSError:
        status = "no answer"  # the app is down or restarting
    if status != 200:
        print(f"{path} -> {status}", flush=True)
    time.sleep(random.uniform(0.2, 0.6))
