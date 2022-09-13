# -*- coding: utf-8 -*-
__version__ = '0.1.1'

import time
from threading import Thread

import httpx

from msaSDK.models.service import MSAHealthDefinition


class MSAHealthCheck(Thread):
    def __init__(self, healthdefinition: MSAHealthDefinition, host: str, port: int):
        """MSAHealthCheckObject, provides a thread to give a healthcheck.

        Args:
            healthdefinition: The MSAHealthDefinition instance
            host: IP/URl to call the healtcheck endpoint
            port: Port of the healtcheck endpoint server listener/endpoint
        """
        super().__init__()
        self.url = "http://{}:{}/".format(host, port)
        self.interval = healthdefinition.interval
        self._is_running = True
        self.healthy: str = "No Healthcheck executed yet:400"
        self.is_healthy: bool = False
        self.error: str = ""

    async def get_health(self) -> str:
        """Get the last health check result

        The string is "positiv: status_code" or "negative: status_code"

        """
        return self.healthy

    def run(self):
        """Run the Healthcheck Thread

        Sleeps by the interval provided by the MSAHealthDefinition.

        Uses httpx to call the healthcheck endpoint which is http://{}:{}/".format(host, port)

        Any 200 <= response.status_code < 300 is healthy, rest is not healthy
        """
        while self._is_running:
            try:
                self.error = ""
                resp = httpx.get(url=self.url, timeout=3.0)
                status_code = resp.status_code
                if 200 <= status_code < 300:
                    self.is_healthy = True
                else:
                    self.is_healthy = False
            except Exception as e:
                status_code = 400
                self.is_healthy = False
                self.error = e.__str__()

            self.healthy = (
                "positiv:" + str(status_code) if (200 <= status_code < 300) else "negativ:" + str(
                    status_code)
            )

            time.sleep(self.interval)

    async def stop(self):
        """Stops the Healthcheck Thread."""
        self._is_running = False
