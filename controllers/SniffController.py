import threading
from typing import Callable, Optional

from scapy.all import sniff
from scapy.plist import Packet

from logging_setup import LOGGER
from models.PacketSummary import PacketSummary, SummaryResults

from .mask_locals import mask_ip, mask_summary


class SniffController:
    def __init__(
        self,
        update_complete_view: Callable[[dict[str, PacketSummary]], None] = None,
        update_special_view: Callable[[dict[str, PacketSummary]], None] = None,
    ):
        self.update_complete_view = update_complete_view
        self.update_special_view = update_special_view
        self._sniff_thread: Optional[threading.Thread] = None
        self._is_sniffing: bool = False
        self._results = SummaryResults()

    def toggle_sniffing(self):
        # Create a new thread and start sniffing on said thread
        if not self._is_sniffing:
            self._is_sniffing = True
            try:
                self._sniff_thread = threading.Thread(target=self._start_sniffing)
                self._sniff_thread.start()
                LOGGER.info("Start sniffing thread")
            except Exception as e:
                LOGGER.error(e)
            LOGGER.info("Start sniffing...")
        # Stop the sniffing (thread), wait for it to finish, and clear the thread reference
        else:
            self._is_sniffing = False
            try:
                if self._sniff_thread.is_alive():
                    self._sniff_thread.join()
                    LOGGER.info("Terminate sniffing thread")
            except Exception as e:
                LOGGER.critical(f"Thread termination failed. {e}")
            self._sniff_thread = None
            LOGGER.info("Stop sniffing")

    def _start_sniffing(self):
        while self._is_sniffing:
            try:
                sniff(prn=self._process_packet, store=False, count=1, timeout=1)
            except Exception as e:
                LOGGER.error(e)

    # Decapsulate from layer 2 to four and get packet info
    # If designated info not acquire, use packet.summary() instead
    def _process_packet(self, packet: Packet):
        connection = PacketSummary()
        # Iterate over layers within the packet dynamically
        current_layer = packet
        layer_index = 2

        while current_layer:
            # Network
            if layer_index == 3:
                for field in current_layer.fields_desc:
                    fname = field.name
                    fvalue = current_layer.getfieldval(fname)
                    if fname == "src":
                        connection.ipsrc = mask_ip(fvalue)
                    elif fname == "dst":
                        connection.ipdst = mask_ip(fvalue)
            # Transport
            elif layer_index == 4:
                connection.transport = current_layer.__class__.__name__
                for field in current_layer.fields_desc:
                    fname = field.name
                    fvalue = current_layer.getfieldval(fname)
                    if fname == "sport":
                        connection.port_src = fvalue
                    elif fname == "dport":
                        connection.port_dst = fvalue

            # Move to the next layer
            layer_index += 1
            current_layer = (
                current_layer.payload if hasattr(current_layer, "payload") else None
            )
        # Use summary if unable to parse designated fields
        essential = [
            connection.ipsrc,
            connection.ipdst,
            connection.transport,
            connection.port_src,
            connection.port_dst,
        ]
        if not all(essential):
            connection.summary = mask_summary(packet.summary())

        # Store/update results
        key = connection.generate_key()
        self._update_summaries(key, connection)

    # Update packet summary result and call PacketView updates
    ### Beaware that under large volumn the current thread would affect view update
    ### Consider adding a update time restriction if such scenario occur
    def _update_summaries(self, key: str, connection: PacketSummary):
        r_complete = self._results.complete
        r_special = self._results.special

        # Update complete results and view if layer 2~4 info specified above are acquired
        if not connection.summary:
            if key in r_complete:
                r_complete[key].appearance += 1
            else:
                r_complete[key] = connection
            if self.update_complete_view:
                rows = [vars(val) for val in r_complete.values()]
                self.update_complete_view(rows)
        # Update special results and view if layer 2~4 info specified above are absence
        # Use the packet.summary instead (see PacketView)
        else:
            if key in r_special:
                r_special[key].appearance += 1
            else:
                r_special[key] = connection
            if self.update_special_view:
                rows = [vars(val) for val in r_special.values()]
                self.update_special_view(rows)
