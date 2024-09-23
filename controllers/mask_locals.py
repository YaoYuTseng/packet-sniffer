# A simple masking (Not necessary) to hide local IPs
# If not configure return the original value

LOCALV4 = "xxx.xxx.xxx.xxx"
LOCALV6_PREFIX = "xxx:xxx:xxx:xxx"

GATEWAY_IPV4 = "xxx.xxx.xxx.xxx"
GATEWAY_IPV6 = "xxx:xxx:xxx:xxx:xxx:xxx"


def mask_ip(address: str):
    if address == LOCALV4:
        return "LOCALv4"
    elif LOCALV6_PREFIX in address:
        return "LOCALv6"
    elif address == GATEWAY_IPV4:
        return "GATEWAYv4"
    elif address == GATEWAY_IPV6:
        return "GATEWAYv6"
    else:
        return address


def mask_summary(summary: str):
    if LOCALV4 in summary:
        summary = summary.replace(LOCALV4, "Localv4")
    if LOCALV6_PREFIX in summary:
        summary = summary.replace(LOCALV6_PREFIX, "Localv6")
    if GATEWAY_IPV4 in summary:
        summary = summary.replace(GATEWAY_IPV4, "GATEWAYv4")
    if GATEWAY_IPV6 in summary:
        summary = summary.replace(GATEWAY_IPV6, "GATEWAYv6")
    return summary
