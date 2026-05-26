#!/usr/bin/env python3
"""
Rakuten MiFi Signal Probe
A lightweight Python script to monitor signal parameters and network speed 
for Rakuten Mobile 4G MiFi routers in real-time.

Disclaimer:
Only tested on Rakuten WiFi Pocket Platinum (4G).
This script is intended solely for convenience to help users easily find 
an optimal physical location for better cellular signal reception.
"""

import urllib.request
import urllib.parse
import urllib.error
import json
import time
import os
import sys

# Locate config.json relative to the script's own directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(SCRIPT_DIR, "config.json")


def setup_config():
    """
    Guides the user to configure the router connection interactively
    and saves the configuration to config.json.
    """
    print("=" * 60)
    print("  Welcome to Rakuten MiFi Signal Probe Interactive Setup!  ")
    print("=" * 60)
    print("No configuration file found. Let's create one now.\n")

    # 1. Ask for Router IP
    default_ip = "192.168.0.1"
    router_ip = input(f"Enter Router IP Address [Default: {default_ip}]: ").strip()
    if not router_ip:
        router_ip = default_ip

    # 2. Ask for Username
    default_user = "admin"
    username = input(f"Enter Admin Username [Default: {default_user}]: ").strip()
    if not username:
        username = default_user

    # 3. Ask for Password
    password = ""
    while not password:
        password = input("Enter Admin Password (Required): ").strip()
        if not password:
            print("Password cannot be empty. Please enter a valid password.")

    # 4. Construct configuration dict
    config = {
        "router_ip": router_ip,
        "username": username,
        "password": password
    }

    # 5. Write to config.json
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)
        print(f"\n[+] Configuration successfully saved to '{CONFIG_FILE}'.")
        print("[+] This file is automatically ignored by Git to keep your credentials safe.")
        print("=" * 60 + "\n")
        return config
    except Exception as e:
        print(f"\n[-] Error writing configuration file: {e}")
        sys.exit(1)


def load_config():
    """
    Loads configuration from config.json. If the file does not exist,
    triggers the interactive setup.
    """
    if not os.path.exists(CONFIG_FILE):
        return setup_config()

    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            config = json.load(f)
        
        # Verify required keys
        required_keys = ["router_ip", "username", "password"]
        if not all(key in config for key in required_keys):
            print(f"[-] Invalid configuration format in '{CONFIG_FILE}'. Re-running setup...")
            return setup_config()
            
        return config
    except json.JSONDecodeError:
        print(f"[-] '{CONFIG_FILE}' is corrupted or not a valid JSON. Re-running setup...")
        return setup_config()
    except Exception as e:
        print(f"[-] Error loading configuration: {e}")
        sys.exit(1)


def format_speed(rate_bytes):
    """
    Formats transmission rate (bytes/s) into human-readable speeds.
    """
    rate_kb = rate_bytes / 1024.0
    if rate_kb > 1024.0:
        return f"{rate_kb / 1024.0:.2f} MiB/s"
    return f"{rate_kb:.2f} KiB/s"


def run_probe(config):
    """
    Main probe logic: handles router authentication and periodically polls signal parameters.
    """
    router_ip = config["router_ip"]
    username = config["username"]
    password = config["password"]
    
    base_url = f"http://{router_ip}"
    login_url = f"{base_url}/login.php"
    password_api = f"{base_url}/controller/password.php"
    nav_api = f"{base_url}/controller/nav.php"
    home_api = f"{base_url}/controller/home.php"

    print(f"[*] Connecting to router at {base_url}...")

    # Step 1: Get the login page to retrieve CSRF token and session cookie
    try:
        req = urllib.request.Request(login_url)
        with urllib.request.urlopen(req, timeout=5) as response:
            html = response.read().decode("utf-8")
            # Extract session cookie from response headers
            set_cookie_header = response.headers.get("Set-Cookie")
            cookie = set_cookie_header.split(";")[0] if set_cookie_header else None
    except urllib.error.URLError as e:
        print(f"\n[-] Connection failed: Could not reach {base_url}.")
        print("    Please check if your device is connected to the MiFi's Wi-Fi network.")
        print(f"    Error details: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n[-] Unexpected error during initial handshake: {e}")
        sys.exit(1)

    # Extract CSRF Token from JavaScript in home HTML
    try:
        csrf_token = html.split('sessionStorage.setItem("csrfToken","')[1].split('");')[0]
    except IndexError:
        print("\n[-] Error: Failed to parse CSRF Token from the login page.")
        print("    This script may not be compatible with your router model or firmware version.")
        sys.exit(1)

    # Step 2: Authenticate and log in
    print("[*] Authenticating...")
    login_data = urllib.parse.urlencode({
        "operate": "login",
        "username": username,
        "password": password,
        "csrfToken": csrf_token
    }).encode("utf-8")

    req_login = urllib.request.Request(password_api, data=login_data)
    if cookie:
        req_login.add_header("Cookie", cookie)

    try:
        with urllib.request.urlopen(req_login, timeout=5) as response:
            login_response = json.loads(response.read().decode("utf-8"))
            
            # Check authentication status
            # A typical successful API response usually contains a success status.
            # We print the response to help debug if it fails.
            if "status" in login_response and login_response["status"] != "0":
                print(f"\n[-] Authentication failed! Response: {login_response}")
                print("    Please double-check your username and password in config.json.")
                sys.exit(1)
    except Exception as e:
        print(f"\n[-] Error during login authentication: {e}")
        sys.exit(1)

    print("[+] Login successful!")
    print("[*] Polling signal parameters... (Press Ctrl+C to exit)")
    print("-" * 88)

    # Step 3: Start polling loop
    while True:
        # Request body for signal strength
        signal_data = urllib.parse.urlencode({
            "operate": "get_nav_signal", 
            "csrfToken": csrf_token
        }).encode("utf-8")

        req_signal = urllib.request.Request(nav_api, data=signal_data)
        if cookie:
            req_signal.add_header("Cookie", cookie)

        try:
            # Poll signal properties
            with urllib.request.urlopen(req_signal, timeout=3) as response:
                signal_resp = json.loads(response.read().decode("utf-8"))
                
            if "msgbody" in signal_resp:
                rsrp = signal_resp["msgbody"].get("rsrp", "N/A")
                rsrq = signal_resp["msgbody"].get("rsrq", "N/A")
                snr = signal_resp["msgbody"].get("snr")

                # Format Signal-to-Noise Ratio (SNR is typically reported * 10 by routers)
                if snr is not None:
                    try:
                        snr_formatted = f"{float(snr) / 10.0:.1f}"
                    except ValueError:
                        snr_formatted = str(snr)
                else:
                    snr_formatted = "N/A"

                # Poll data rate / traffic speed
                traffic_data = urllib.parse.urlencode({
                    "flag": "trafficRate",
                    "csrfToken": csrf_token
                }).encode("utf-8")

                req_traffic = urllib.request.Request(home_api, data=traffic_data)
                if cookie:
                    req_traffic.add_header("Cookie", cookie)

                tx_rate = 0.0
                rx_rate = 0.0
                try:
                    with urllib.request.urlopen(req_traffic, timeout=3) as response_traffic:
                        traffic_text = response_traffic.read().decode("utf-8")
                        if traffic_text:
                            # Sanitize weird JSON nesting if any
                            traffic_text = traffic_text.replace('"{', '{').replace('}"', '}')
                            traffic_resp = json.loads(traffic_text)
                            if (
                                "traffic_rate_info" in traffic_resp 
                                and "msgbody" in traffic_resp["traffic_rate_info"]
                            ):
                                traffic_body = traffic_resp["traffic_rate_info"]["msgbody"]
                                tx_rate = float(traffic_body.get("tx_rate", 0))
                                rx_rate = float(traffic_body.get("rx_rate", 0))
                except Exception:
                    # Ignore traffic errors to maintain signal polling continuity
                    pass

                # Output formatted metric row to terminal
                print(
                    f"RSRP: {rsrp:>4} dBm  |  "
                    f"RSRQ: {rsrq:>4} dB  |  "
                    f"SNR: {snr_formatted:>5} dB  |  "
                    f"Upload ↑: {format_speed(tx_rate):>12}  |  "
                    f"Download ↓: {format_speed(rx_rate):>12}"
                )
            else:
                print(f"[-] Unexpected API response: {signal_resp}")

        except urllib.error.URLError as e:
            print(f"[!] Network polling error (reconnecting...): {e}")
        except Exception as e:
            print(f"[!] Error: {e}")

        time.sleep(1)


if __name__ == "__main__":
    try:
        conf = load_config()
        run_probe(conf)
    except KeyboardInterrupt:
        print("\n\n[+] Probe stopped. Goodbye!")
        sys.exit(0)
