import psutil
import requests
import time
import os
import socket
import signal
from datetime import datetime
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# =============================
# Configuration
# =============================

CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", 30))
BASE_URL = os.getenv("BASE_URL", "https://test.com/monitor-health")
METRIC_ENDPOINT = f"{BASE_URL}/monitor/server/system-health/"
AGENT_TOKEN_ENDPOINT = f"{BASE_URL}/monitor/agent/token/"
IP_ADDRESS = os.getenv("IP_ADDRESS", socket.gethostname())

AGENT_TOKEN = os.getenv("AGENT_TOKEN")
AGENT_EMAIL = os.getenv("AGENT_EMAIL")
PASSWORD = os.getenv("PASSWORD")

DAYS = int(os.getenv("DAYS", 0))
HOURS = int(os.getenv("HOURS", 0))
MINUTES = int(os.getenv("MINUTES", 0))

# =============================
# HTTP Session with Retry
# =============================

session = requests.Session()

retries = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[500, 502, 503, 504],
)

adapter = HTTPAdapter(max_retries=retries)
session.mount("http://", adapter)
session.mount("https://", adapter)

# =============================
# Graceful Shutdown
# =============================

running = True


def shutdown_handler(signum, frame):
    global running
    print("\nShutting down monitor agent...")
    running = False


signal.signal(signal.SIGTERM, shutdown_handler)
signal.signal(signal.SIGINT, shutdown_handler)

# =============================
# Health Check Functions
# =============================


def get_cpu() -> float:
    return psutil.cpu_percent(interval=1)


def get_memory() -> float:
    return psutil.virtual_memory().percent


def get_disk() -> float:
    return psutil.disk_usage("/").percent


# =============================
# Send Metrics
# =============================


def send_metrics(payload: dict) -> None:
    global AGENT_TOKEN

    headers = {}

    if AGENT_TOKEN:
        headers["Authorization"] = f"Bearer {AGENT_TOKEN}"

    try:
        response = session.post(
            METRIC_ENDPOINT,
            json=payload,
            headers=headers,
            timeout=5,
        )

        # Token expired
        if response.status_code == 401:
            print("Token expired. Fetching new token...")
            get_agent_token()

            headers["Authorization"] = f"Bearer {AGENT_TOKEN}"

            response = session.post(
                METRIC_ENDPOINT,
                json=payload,
                headers=headers,
                timeout=5,
            )

        print(
            f"[{datetime.utcnow().isoformat()}] "
            f"Metrics sent | Status: {response.status_code}"
        )

    except Exception as e:
        print(f"[{datetime.utcnow().isoformat()}] Failed to send metrics: {e}")


# =============================
# Monitor Loop
# =============================


def monitor():
    print("Starting monitoring agent...")
    print(f"Server IP: {IP_ADDRESS}")
    print(f"Endpoint: {METRIC_ENDPOINT}")
    print(f"Interval: {CHECK_INTERVAL} seconds\n")

    while running:
        cpu = get_cpu()
        memory = get_memory()
        disk = get_disk()

        payload = {
            "ip_address": IP_ADDRESS,
            "cpu_usage_percent": cpu,
            "memory_usage_percent": memory,
            "disk_usage_percent": disk,
        }

        print(
            f"[{datetime.utcnow().isoformat()}] "
            f"CPU: {cpu}% | Memory: {memory}% | Disk: {disk}%"
        )

        send_metrics(payload)

        time.sleep(CHECK_INTERVAL)

    print("Monitor stopped.")


# =============================
# Token Management
# =============================


def get_agent_token():
    global AGENT_TOKEN
    payload = {"email": AGENT_EMAIL, "password": PASSWORD}

    try:
        TOKEN_REQUEST_TIMEOUT = (DAYS * 86400) + (HOURS * 3600) + (MINUTES * 60)
        response = session.post(
            AGENT_TOKEN_ENDPOINT, json=payload, timeout=TOKEN_REQUEST_TIMEOUT
        )

        if response.status_code == 200:
            data = response.json()
            AGENT_TOKEN = data["data"]["access"]

            print(
                f"[{datetime.utcnow().isoformat()}] New token generated successfully."
            )

        else:
            print(
                f"[{datetime.utcnow().isoformat()}] "
                f"Token generation failed: {response.status_code}"
            )

    except Exception as e:
        print(f"[{datetime.utcnow().isoformat()}] Token request failed: {e}")


if __name__ == "__main__":
    get_agent_token()
    monitor()
