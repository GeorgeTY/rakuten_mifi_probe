# Rakuten MiFi Signal Probe

[日本語版はこちら (Japanese Edition)](README.ja.md)

A zero-dependency, lightweight command-line utility written in Python to monitor signal strength metrics and real-time network speeds for Rakuten Mobile 4G MiFi routers in real-time.

> [!IMPORTANT]
> **Tested Device**: Only tested on **Rakuten WiFi Pocket Platinum (4G)**.
> **Purpose**: This script is intended solely for convenience to help users easily find an optimal physical location for better cellular signal reception.

It runs directly in your terminal, making it ideal for running on laptops, NAS devices, Raspberry Pis, or any home server to help you locate the best spot for maximum cellular reception.

---

## Features

- **Real-Time Polling**: Updates signal parameters and traffic rates every second.
- **Key Metrics Displayed**:
  - **RSRP** (Reference Signal Received Power) in dBm
  - **RSRQ** (Reference Signal Received Quality) in dB
  - **SNR** (Signal-to-Noise Ratio) in dB
  - **Upload ↑** and **Download ↓** network speeds (KiB/s or MiB/s)
- **Zero Dependencies**: Built entirely using Python's standard library (`urllib` and `json`). No `pip` installations needed!
- **Interactive Setup Wizard**: Automatically guides you to configure credentials and saves them securely upon the first launch.
- **Git-Safe**: The generated `config.json` containing your router's login password is automatically ignored by Git to prevent accidental leaks.

---

## Installation & Setup

1. **Clone or Copy** the folder to your preferred workspace.
2. Ensure you have **Python 3** installed:
   ```bash
   python3 --version
   ```

---

## Usage

Simply run the script in your terminal:

```bash
python3 probe.py
```

### First-Time Interactive Configuration
If no `config.json` is found in the directory, the interactive setup wizard will launch automatically. It will prompt you for:
- **Router IP Address** (Default: `192.168.0.1`)
- **Admin Username** (Default: `admin`)
- **Admin Password** (Your custom MiFi login password)

Once inputted, the script automatically generates `config.json` for you and starts polling signal stats.

### Manual Configuration
You can also manually create a `config.json` file in the same directory prior to running the script. Use the format provided in `config.example.json`:

```json
{
  "router_ip": "192.168.0.1",
  "username": "admin",
  "password": "YOUR_ROUTER_PASSWORD"
}
```

---

## Terminal Output Example

Once running, you will see a clean live feed in your terminal:

```text
[*] Connecting to router at http://192.168.0.1...
[*] Authenticating...
[+] Login successful!
[*] Polling signal parameters... (Press Ctrl+C to exit)
----------------------------------------------------------------------------------------
RSRP:  -92 dBm  |  RSRQ:  -14 dB  |  SNR:   0.0 dB  |  Upload ↑:   4.63 KiB/s  |  Download ↓:   7.02 KiB/s
RSRP:  -92 dBm  |  RSRQ:  -14 dB  |  SNR:   0.0 dB  |  Upload ↑:   1.53 KiB/s  |  Download ↓:   3.12 KiB/s
RSRP:  -92 dBm  |  RSRQ:  -14 dB  |  SNR:  -0.8 dB  |  Upload ↑:   1.53 KiB/s  |  Download ↓:   3.12 KiB/s
RSRP:  -92 dBm  |  RSRQ:  -14 dB  |  SNR:  -0.8 dB  |  Upload ↑:   3.66 KiB/s  |  Download ↓:   1.10 KiB/s
```

Press `Ctrl+C` at any time to quit safely.

---

## License & Disclaimer
This project is licensed under the [MIT License](LICENSE).

**Disclaimer**: This project is an unofficial community tool. It is not affiliated with, authorized, or endorsed by Rakuten Mobile or any hardware manufacturer. It was only tested on **Rakuten WiFi Pocket Platinum (4G)** and is designed solely to assist users in locating a better cellular signal. Use it at your own risk.
