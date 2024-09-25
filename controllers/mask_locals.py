from . import ip_config


# A simple masking (Not necessary) to hide local IPs
# If not configure return the original value
def mask_ip(address: str):
    if address == ip_config["LOCALV4"]:
        return "LOCALv4"
    elif ip_config["LOCALV6_PREFIX"] in address:
        return "LOCALv6"
    elif address == ip_config["GATEWAY_IPV4"]:
        return "GATEWAYv4"
    elif address == ip_config["GATEWAY_IPV6"]:
        return "GATEWAYv6"
    else:
        return address


def mask_summary(summary: str):
    if ip_config["LOCALV4"] in summary:
        summary = summary.replace(ip_config["LOCALV4"], "Localv4")
    if ip_config["LOCALV6_PREFIX"] in summary:
        summary = summary.replace(ip_config["LOCALV6_PREFIX"], "Localv6")
    if ip_config["GATEWAY_IPV4"] in summary:
        summary = summary.replace(ip_config["GATEWAY_IPV4"], "GATEWAYv4")
    if ip_config["GATEWAY_IPV6"] in summary:
        summary = summary.replace(ip_config["GATEWAY_IPV6}"], "GATEWAYv6")
    return summary
