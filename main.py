from nicegui import ui

from controllers.PingController import PingController
from controllers.SniffController import SniffController
from views.HealthCheckView import HealthCheckView
from views.PacketsView import PacketsView
from views.SniffButton import SniffButton

if __name__ == "__main__":
    # Create sniffing thread controller
    sniffer = SniffController()
    checker = PingController()

    # Create view
    with ui.column().classes("w-full"):
        with ui.row().classes("w-full items-center justify-between"):
            sniff_toggle = SniffButton(sniffer.toggle_sniffing)
            health_check = HealthCheckView()
        packet_view = PacketsView().classes("w-full h-full")

    # Deferred binding of view updates
    sniffer.update_complete_view = packet_view.create_complete_table.refresh
    sniffer.update_special_view = packet_view.create_special_table.refresh
    checker.update_ICMP_view = health_check._create_result_bar.refresh

    # Start health check and ui program
    checker.start_ping()
    ui.run(window_size=(1280, 720), reload=False)
