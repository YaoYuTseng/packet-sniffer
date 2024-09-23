from dataclasses import dataclass, field
from typing import Optional


@dataclass
class PacketSummary:
    ipsrc: Optional[str] = None
    ipdst: Optional[str] = None
    transport: Optional[str] = None
    port_src: Optional[str] = None
    port_dst: Optional[str] = None
    summary: Optional[str] = None
    appearance: int = 1

    def generate_key(self):
        if self.summary:
            return self.summary
        else:
            return f"{self.ipsrc}->{self.ipdst}/{self.transport}/{self.port_src}->{self.port_dst}"


@dataclass
class SummaryResults:
    complete: dict[str, PacketSummary] = field(default_factory=dict)
    special: dict[str, PacketSummary] = field(default_factory=dict)
