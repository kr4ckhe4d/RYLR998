# LoRa Communication: ESP32 WROVER-E to Raspberry Pi Zero

A simple wireless communication project using LoRa modules to send messages between an ESP32 WROVER-E and a Raspberry Pi Zero.

## Hardware Required

### ESP32 Transmitter Side
- ESP32 WROVER-E development board
- RYLR998 LoRa module (915MHz)
- Jumper wires
- Breadboard (optional)

### Raspberry Pi Receiver Side
- Raspberry Pi Zero (or any Pi with GPIO)
- RYLR998 LoRa module (915MHz)
- Jumper wires

## Wiring Diagrams

### ESP32 WROVER-E to RYLR998
```
ESP32 WROVER-E    RYLR998
GPIO 21       →   TX
GPIO 22       →   RX
3.3V          →   VCC
GND           →   GND
```

### Raspberry Pi Zero to RYLR998
```
Pi Zero           RYLR998
GPIO 14 (TX)  →   RX
GPIO 15 (RX)  →   TX
3.3V          →   VCC
GND           →   GND
```

## Software Setup

### ESP32 Setup (Arduino IDE)
1. Install ESP32 board support in Arduino IDE
2. Select "ESP32 Dev Module" as board
3. Upload the ESP32 transmitter code
4. Open Serial Monitor at 115200 baud to see transmission status

### Raspberry Pi Setup
1. Enable UART in raspi-config:
   ```bash
   sudo raspi-config
   # Interface Options → Serial Port
   # Enable serial port hardware, disable serial console
   ```

2. Add to `/boot/config.txt`:
   ```
   enable_uart=1
   ```

3. Install required Python package:
   ```bash
   pip3 install pyserial
   ```

4. Run the receiver:
   ```bash
   python3 simple_receiver.py
   ```

## Code Files

### `esp32_simple_lora_transmitter.ino `
- Configures ESP32 WROVER-E as LoRa transmitter
- Sends "Hello from ESP32!" every 5 seconds
- Uses address 1, sends to address 2

### `pi_zero_simple_lora_receiver.py`
- Configures Pi Zero as LoRa receiver
- Listens for messages from ESP32
- Uses address 2, receives from address 1

## Configuration

Both devices must have matching LoRa settings:
- **Frequency**: 915MHz (US) - Change to 868MHz for Europe
- **Network ID**: 7
- **Addresses**: ESP32=1, Pi=2

## Usage

1. **Start the receiver** on Pi Zero:
   ```bash
   python3 simple_receiver.py
   ```

2. **Power up the ESP32** - it will automatically start transmitting

3. **Expected output** on Pi:
   ```
   LoRa configured - listening for messages...
   From 1: Hello from ESP32!
   From 1: Hello from ESP32!
   ```

## Troubleshooting

### No messages received
- Check wiring connections
- Verify both devices have same frequency/network settings
- Ensure Pi UART is properly enabled
- Check for other processes using `/dev/serial0`

### Poor signal quality
- Ensure antennas are properly connected
- Check for interference from other devices
- Verify 3.3V power supply is stable
- Try different locations/orientations

### Serial port errors on Pi
```bash
# Check if serial port exists
ls -l /dev/serial*

# Test basic communication
echo "AT" > /dev/serial0
```

## Signal Quality

The receiver shows signal strength indicators:
- **RSSI**: Received Signal Strength (-30 dBm is excellent, below -80 dBm is poor)
- **SNR**: Signal-to-Noise Ratio (positive values are good)

## Customization

### Change transmission frequency
```cpp
// ESP32 code
lora.println("AT+BAND=868000000");  // For Europe
```

### Modify message interval
```cpp
// ESP32 code
delay(10000);  // Send every 10 seconds instead of 5
```

### Add custom messages
```cpp
// ESP32 code
String message = "Sensor reading: " + String(analogRead(A0));
```

## Range Testing

Typical range depends on environment:
- **Open field**: 2-10 km
- **Urban environment**: 200m-2km
- **Indoor**: 50-200m

## Legal Considerations

- **US**: 915MHz ISM band, no license required
- **Europe**: Use 868MHz instead of 915MHz
- **Other regions**: Check local regulations

## License

This project is open source. Feel free to modify and distribute.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Support

For issues or questions:
- Check the troubleshooting section
- Review RYLR998 datasheet
- Open an issue on GitHub

---

**Note**: This is a basic implementation. For production use, consider adding error handling, encryption, and proper protocol design.
