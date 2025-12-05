 # mqqt-temp-sens

A comprehensive IoT solution for temperature and humidity sensing using the MQTT protocol with a captive portal for easy configuration of network settings and MQTT credentials.

## Overview
`mqqt-temp-sens` is an IoT project that utilizes the popular [HTU21D](https://www.honeywell.com/us/en/search?q=htu21d) sensor to collect temperature and humidity data, and sends it via MQTT protocol to a specified broker.

## Dependencies
- MicroPython: <https://micropython.org/>
- urequests: <https://docs.micropython.org/en/latest/library/urequests.html>
- umqtt.simple: <https://github.com/micropython-UMQTT/micropython-umqtt>

## Folder Structure
```markdown
mqqt-temp-sens/
│
├── lib/           - Contains necessary classes and functions for the project
│   ├── dnsquery.py
│   ├── filehelper.py
│   └── htu21d.py
│
├── websettings.py  - Handles HTML templates and configuration files
│
└── main.py        - Main script that runs the project
```

## Usage
To use this project, follow these steps:

1. Connect your HTU21D sensor to the appropriate pins on your microcontroller (e.g., ESP32/ESP8266).
2. Configure network settings and MQTT credentials using a captive portal, accessible via the Access Point created by the project.
3. Once configured, the script will connect to your Wi-Fi network and start sending temperature and humidity data to the specified MQTT broker every 10 minutes (configurable).

### Initializing Settings
To clear the current configuration or set a custom one, you can use the following functions from `websettings.py`:

```python
# To clear existing settings
websets = websettings()
websets.clear_settings()

# To set custom network credentials and MQTT details
websets.setTemplate('set_ap.html')  # Set the template for the captive portal
websets.setregexp(['networkname','password','mqaddress','mqname', 'mqpass'])  # Define capture groups for form data
```

### Running the Project
After setting up your hardware and configurations, you can run the main script with:

```bash
python main.py
```

## Troubleshooting
In case of issues, ensure that the necessary dependencies are installed correctly and that the HTU21D sensor is properly connected to the microcontroller.

## Contribution
If you'd like to contribute to this project, feel free to open an issue or submit a pull request on GitHub.

## License
This project is licensed under the [MIT License](LICENSE).