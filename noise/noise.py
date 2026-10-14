"""Low-volume benign browser-like traffic for the optional noise profile."""
import logging
import os
import random
import time
import urllib.request

LOGGER = logging.getLogger(__name__)
INTERVAL = max(5, int(os.environ.get("NOISE_INTERVAL_SECONDS", "25")))
PATHS = ("/", "/#/search?q=juice", "/assets/public/images/products/", "/login")

while True:
    try:
        urllib.request.urlopen("http://proxy" + random.choice(PATHS), timeout=8).read(128)
    except Exception:  # The service may start before the proxy; retry on the next cycle.
        LOGGER.debug("noise request failed; retrying on next cycle", exc_info=True)
    time.sleep(INTERVAL + random.randint(0, max(1, INTERVAL // 3)))
