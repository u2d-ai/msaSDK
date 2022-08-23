from threading import Thread
import httpx
import time
from u2d_msa_sdk.schemas.service import MSAHealthDefinition


class MSAHealthCheck(Thread):
    def __init__(self, healthdefinition: MSAHealthDefinition):
        super().__init__()
        self.url = healthdefinition.path
        self.interval = healthdefinition.interval
        self._is_running = True
        self.healthy = True

    def get_health(self):
        return self.healthy

    def run(self):
        while self._is_running:
            try:
                resp = httpx.get(self.url, timeout=3)
                status_code = resp.status_code
            except Exception as e:
                status_code = 400
            self.healthy = (
                "positiv:" + str(status_code) if (200 <= status_code < 300) else "negativ:" + str(
                    status_code)
            )
            time.sleep(self.interval)

    def stop(self):
        self._is_running = False
