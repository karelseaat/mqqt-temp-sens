# mqqt-temp-sens

I built this to get reliable temp/humidity readings from an HTU21D sensor on an ESP32, push them over MQTT, and avoid hardcoding network or broker credentials. Works out of the box with a simple captive portal for setup.

## What it does

- Reads temperature and humidity from the [HTU21D](https://www.honeywell.com/us/en/search?q=htu21d) sensor  
- Sends data via MQTT every 10 minutes (configurable)  
- Sets up a Wi-Fi AP with a captive portal for easy initial config  
- Persists settings to `config.json` so you only configure once  

## Dependencies

- MicroPython (tested on ESP32/ESP8266)  
- `urequests` (built into recent MicroPython firmwares)  
- `umqtt.simple` — install via `upip` or drop into `lib/`  

## Folder layout

```markdown
mqqt-temp-sens/
├── lib/
│   ├── dnsquery.py    # Lightweight DNS server for captive portal
│   ├── filehelper.py  # Helper to read/write JSON configs
│   └── htu21d.py      # MicroPython driver for HTU21D
├── websettings.py     # Handles captive portal UI + config parsing
└── main.py            # Boot script — sets up Wi-Fi → config → reads sensor → publishes
```

## Usage

1. Wire the HTU21D:  
   - `VCC` → 3.3V  
   - `GND` → GND  
   - `SCL`/`SDA` → I²C pins (default: `GPIO22`/`GPIO21` on ESP32)  

2. Flash MicroPython and upload all files to the board.  

3. Power up — the device creates an AP named `MQTT-Sensor-XXXXXX`. Connect and open `http://192.168.4.1` to configure Wi-Fi and MQTT broker details.  

4. After saving, it rejoins your network, connects to MQTT, and starts publishing.  
   - Topic: `sensors/htu21d`  
   - Payload JSON: `{"temp": 23.4, "hum": 45.1}`  

### Configuring via code (optional)

If you prefer scripting over the portal:

```python
from websettings import websettings

# Wipe existing config
websets = websettings()
websets.clear_settings()

# Customize portal UI and form fields
websets.setTemplate('set_ap.html')
websets.setregexp(['networkname','password','mqaddress','mqname', 'mqpass'])
```

### Running

Drop `main.py` as `main.py` on the device. It runs automatically on boot.

## Troubleshooting

- **No AP shows up?** Check I²C wiring — the sensor init fails silently if SDA/SCL are swapped.  
- **MQTT won’t connect?** Verify broker reachable from your network, and credentials match.  
- **Config lost after reset?** Ensure `config.json` is saved (check SD card or flash write isn’t disabled).  

## Contributing

PRs welcome. Keep it MicroPython-friendly — no external libs beyond what’s listed.  

## License

MIT — see [LICENSE](LICENSE).