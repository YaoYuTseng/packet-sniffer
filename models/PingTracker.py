from dataclasses import dataclass

from welford import Welford


@dataclass
class PingTracker:
    sent: int = 0
    recevied: int = 0
    stats: Welford = Welford()


@dataclass
class PingResult:
    latency: str
    jitter: str
    packet_loss: str
