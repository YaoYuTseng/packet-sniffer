from nicegui import ui

from .constants import PACKET_VIEW_COMPLETE, PACKET_VIEW_SPECIAL


# Two tables displaying sniffed standard (with ip & port src/dst) and special packets
class PacketsView(ui.column):
    def __init__(self) -> None:
        self._complete_cols = PACKET_VIEW_COMPLETE
        self._special_cols = PACKET_VIEW_SPECIAL
        super().__init__()
        with self.classes("w-full"):
            self.create_complete_table([])
            self.create_special_table([])

    @ui.refreshable
    def create_complete_table(self, rows: list[str]):
        if rows:
            rows = sorted(rows, key=lambda x: x["appearance"], reverse=True)
        ui.table(columns=self._complete_cols, rows=rows).classes("w-full").props("flat")

    @ui.refreshable
    def create_special_table(self, rows: list[str]):
        if rows:
            rows = sorted(rows, key=lambda x: x["appearance"], reverse=True)
        ui.table(columns=self._special_cols, rows=rows).classes("w-full").props("flat")
