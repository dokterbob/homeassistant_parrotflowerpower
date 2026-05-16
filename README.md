# Parrot Flower Power BLE sensor integration for Home Assistant

A Home Assistant custom integration for Parrot Flower Power plant sensors via Bluetooth Low Energy. Supports ESPHome BLE proxies.

## Sensors

- Air Temperature (°C)
- Soil Temperature (°C)
- Light Intensity (lux)
- Soil Moisture (%)
- Calibrated Moisture (%, firmware 1.1.0+)
- Soil Conductivity (µS/cm)
- Battery (%)

## Requirements

- Home Assistant 2023.9+
- A Bluetooth adapter (local or ESPHome BLE proxy)
- The device must be in BLE range of the adapter/proxy

## Installation

### HACS (recommended)

1. Add this repository as a custom repository in HACS (Integration type)
2. Install "Parrot Flower Power"
3. Restart Home Assistant

### Manual

1. Copy the `custom_components/parrotflowerpower` folder to your Home Assistant `config/custom_components/` directory
2. Restart Home Assistant

## Configuration

This integration uses the Home Assistant UI for setup (no YAML configuration).

1. Go to **Settings > Integrations > Add Integration**
2. Search for "Parrot Flower Power"
3. Either:
   - Select a discovered device from the list, or
   - Enter the Bluetooth MAC address manually

The device will be auto-discovered if your Bluetooth adapter or ESPHome BLE proxy can see it advertising.

## Migrating from v1.x

If you previously used the YAML-based configuration:

1. Remove the `sensor: platform: parrotflowerpower` entry from `configuration.yaml`
2. Restart Home Assistant
3. Add the integration via the UI as described above

## Resources

- [WatchFlower](https://github.com/emericg/WatchFlower) — BLE protocol reference
- [Home Assistant Plant](https://www.home-assistant.io/integrations/plant/) — use sensor data with HA's plant integration
- [ESPHome Bluetooth Proxy](https://esphome.io/components/bluetooth_proxy/) — extend BLE range with ESP32
