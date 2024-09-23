import threading
from time import sleep
from typing import Callable, Optional

import numpy as np
from ping3 import ping

from logging_setup import LOGGER
from models.PingTracker import PingResult, PingTracker


class PingController:
    def __init__(self, update_ICMP_view: Callable[[dict[str:str]], None] = None):
        self.update_ICMP_view = update_ICMP_view
        self._ping_thread: Optional[threading.Thread] = None
        self._is_pinging: bool = False
        self._ping_target = "8.8.8.8"
        self._ping_interval = 2
        self._ping_tracker = PingTracker()

    # Create a new thread and start health checking on said thread
    def start_ping(self):
        self._is_pinging = True
        try:
            self._ping_thread = threading.Thread(target=self.health_check)
            self._ping_thread.start()
            LOGGER.info("Start ping thread")
        except Exception as e:
            LOGGER.error(f"Health check failed. {e}")
            self._stop_ping()
        LOGGER.info("Start health check...")

    # Terminate ping thread
    def _stop_ping(self):
        self._is_pinging = False
        if self._ping_thread and self._ping_thread.is_alive():
            self._ping_thread.join()
        self._ping_thread = None
        LOGGER.info(f"Ping thread terminated, stop pining.")

    def health_check(self):
        while self._is_pinging:
            try:
                self._ping_tracker.sent += 1
                latency = ping(self._ping_target, unit="ms")
                if isinstance(latency, float):
                    self._ping_tracker.recevied += 1
                    adding = np.array([latency])
                    self._ping_tracker.stats.add(adding)
                else:
                    LOGGER.warning("Packet loss.")
            except Exception as e:
                self._stop_ping()
                LOGGER.error(f"Unexpected ping failed. {e}")

            sleep(self._ping_interval)

            # Start updating statistics from 2 or more packets for meaningful standard deviation
            # Use welford algorithm for incremental variance calculation
            # Verified with statistics package and acquire the same result
            if self._ping_tracker.stats.count >= 2:
                r_latency = self._ping_tracker.stats.mean[0]
                r_jitter = np.sqrt(self._ping_tracker.stats.var_s)[0]
                packet_loss = self._ping_tracker.sent - self._ping_tracker.stats.count
                loss_percent = round(packet_loss / self._ping_tracker.sent, 2)
                result = PingResult(
                    latency=f"{r_latency:.2f}",
                    jitter=f"{r_jitter:.2f}",
                    packet_loss=f"{loss_percent * 100}% ({self._ping_tracker.sent}/{self._ping_tracker.stats.count})",
                )
                self.update_ICMP_view(result)
