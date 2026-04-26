import requests
import time

# Cache results so we don't call the API repeatedly for same IP
# (ip-api.com has a rate limit of 45 requests/minute for free)
_cache = {}

def get_location(ip_address):
    """
    Given an IP address, return its geographic location.
    Returns a dict with country, city, lat, lon, ISP info.
    """

    # Return cached result if we've seen this IP before
    if ip_address in _cache:
        return _cache[ip_address]

    # Skip private/local IPs (like 127.0.0.1 on your own computer)
    if ip_address.startswith("127.") or ip_address.startswith("192.168.") or ip_address == "localhost":
        return {
            "ip": ip_address,
            "country": "LOCAL",
            "countryCode": "LO",
            "city": "Localhost",
            "lat": 0.0,
            "lon": 0.0,
            "isp": "Local Network",
            "proxy": False,
            "hosting": False
        }

    try:
        # Call the free ip-api.com service
        # Fields we want: status, country, countryCode, city,
        #                 lat, lon, isp, proxy, hosting
        url = f"http://ip-api.com/json/{ip_address}?fields=status,message,country,countryCode,city,lat,lon,isp,proxy,hosting"
        response = requests.get(url, timeout=5)
        data = response.json()

        if data.get("status") == "success":
            location = {
                "ip": ip_address,
                "country": data.get("country", "Unknown"),
                "countryCode": data.get("countryCode", "??"),
                "city": data.get("city", "Unknown"),
                "lat": data.get("lat", 0.0),
                "lon": data.get("lon", 0.0),
                "isp": data.get("isp", "Unknown"),
                "proxy": data.get("proxy", False),    # Is it a VPN/proxy?
                "hosting": data.get("hosting", False)  # Is it a datacenter/bot?
            }
            # Cache the result
            _cache[ip_address] = location
            return location
        else:
            return _make_unknown(ip_address)

    except Exception as e:
        print(f"Geo lookup failed for {ip_address}: {e}")
        return _make_unknown(ip_address)


def _make_unknown(ip):
    return {
        "ip": ip,
        "country": "Unknown",
        "countryCode": "??",
        "city": "Unknown",
        "lat": 0.0,
        "lon": 0.0,
        "isp": "Unknown",
        "proxy": False,
        "hosting": False
    }


def check_ip_reputation(ip_address):
    """
    Extra check: flag IPs that are proxies, VPNs, or datacenters.
    Pirates often use these to hide their real location.
    """
    location = get_location(ip_address)
    flags = []

    if location.get("proxy"):
        flags.append({
            "flag": True,
            "reason": f"IP {ip_address} is a known VPN or proxy",
            "severity": "HIGH"
        })

    if location.get("hosting"):
        flags.append({
            "flag": True,
            "reason": f"IP {ip_address} is a datacenter/bot host — not a real user",
            "severity": "HIGH"
        })

    return flags, location