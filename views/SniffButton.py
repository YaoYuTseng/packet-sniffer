from typing import Callable

from nicegui import ui


# Button to start/pause sniffing
class SniffButton(ui.button):
    def __init__(
        self, toggle: Callable[[None], None], text: str = "Start Sniffing"
    ) -> None:
        self.toggle = toggle
        super().__init__(text, icon="play_circle")
        self.classes("text-base font-bold")
        self.props("outline")
        self.on_click(self.switch_btn_text)
        self.on_click(self.toggle)

    def switch_btn_text(self) -> None:
        if self.text == "Start Sniffing":
            self.set_text("Pause")
            self.icon = "pause"
        elif self.text == "Pause":
            self.set_text("Start Sniffing")
            self.icon = "play_circle"
