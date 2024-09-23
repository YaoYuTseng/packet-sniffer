from typing import Optional

from nicegui import ui

from models.PingTracker import PingResult


# Simple display for health check results
class HealthCheckView(ui.row):
    def __init__(self) -> None:
        super().__init__()
        self._result_bar: Optional[ui.row] = None
        with self:
            self._create_result_bar(PingResult("", "", ""))

    @ui.refreshable
    def _create_result_bar(self, result: Optional[PingResult] = None) -> None:
        with ui.row().classes("items-center") as result_bar:
            ui.label("Health check to 8.8.8.8").classes("font-bold mr-2")
            ui.label(f"Latency: {result.latency}")
            ui.label(f"Jitter: {result.jitter}")
            ui.label(f"Packet Loss: {result.packet_loss}").classes("min-w-44")
        self._result_bar = result_bar
