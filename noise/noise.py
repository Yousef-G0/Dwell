"""Low-volume benign browser-like traffic for the optional noise profile."""
import os
import random
import time
import urllib.request

INTERVAL = max(5, int(os.environ.get("NOISE_INTERVAL_SECONDS", "25")))
PATHS = ("/", "/#/search?q=juice", "/assets/public/images/products/", "/login")

while True:
    try:
        urllib.request.urlopen("http://proxy" + random.choice(PATHS), timeout=8).read(128)
    except Exception:
        pass  # The service may start before the proxy; retry on the next cycle.
    time.sleep(INTERVAL + random.randint(0, max(1, INTERVAL // 3)))
