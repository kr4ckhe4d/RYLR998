import serial
import time
import sys

LORA_PORT = "/dev/serial0"
AT_END = "\r\n"

def send_at_command(ser, command):
    print(f"Configuring: {command}")
    ser.write((command + AT_END).encode('utf-8'))
    time.sleep(1.0)  # Increased delay for better response reading
    
    responses = []
    # Read all available responses
    while ser.in_waiting > 0:
        response = ser.readline().decode('utf-8').strip()
        if response:  # Only print non-empty responses
            responses.append(response)
            print(f"Response: {response}")
    
    if not responses:
        print("No response received - this might indicate a problem!")
    
    return responses

def test_basic_communication(ser):
    """Test basic AT communication"""
    print("\n--- Testing Basic Communication ---")
    send_at_command(ser, "AT")
    
    # Get module version
    send_at_command(ser, "AT+VER")
    
    # Get current parameters
    send_at_command(ser, "AT+PARAMETER?")
    send_at_command(ser, "AT+BAND?")
    send_at_command(ser, "AT+NETWORKID?")
    send_at_command(ser, "AT+ADDRESS?")

try:
    print("Opening LoRa serial port...")
    lora_serial = serial.Serial(LORA_PORT, 115200, timeout=2.0)
    print("LoRa serial port opened successfully.")
    
    # Test basic communication first
    test_basic_communication(lora_serial)
    
    print("\n--- Configuring LoRa Module ---")
    
    # Configure the LoRa Module - ensure these match the transmitter exactly
    send_at_command(lora_serial, "AT+BAND=915000000")
    send_at_command(lora_serial, "AT+NETWORKID=7")
    send_at_command(lora_serial, "AT+ADDRESS=2")
    
    # Optional: Set the same parameters as transmitter
    send_at_command(lora_serial, "AT+PARAMETER=12,4,1,7")
    
    print("\n--- Final Configuration Check ---")
    send_at_command(lora_serial, "AT+PARAMETER?")
    send_at_command(lora_serial, "AT+BAND?")
    send_at_command(lora_serial, "AT+NETWORKID?")
    send_at_command(lora_serial, "AT+ADDRESS?")
    
    print("\n--- LoRa Receiver Listening ---")
    print("Waiting for messages from ESP32 (address 1)...")
    print("Press Ctrl+C to stop\n")
    
    message_count = 0
    last_heartbeat = time.time()
    
    while True:
        current_time = time.time()
        
        # Show heartbeat every 30 seconds to confirm program is running
        if current_time - last_heartbeat > 30:
            print(f"[{time.strftime('%H:%M:%S')}] Still listening... (received {message_count} messages)")
            last_heartbeat = current_time
        
        if lora_serial.in_waiting > 0:
            try:
                # Read the incoming line from the LoRa module
                line = lora_serial.readline().decode('utf-8').strip()
                
                if line:  # Only process non-empty lines
                    print(f"[{time.strftime('%H:%M:%S')}] Raw data: {line}")
                    
                    # A received message starts with "+RCV="
                    if line.startswith("+RCV="):
                        message_count += 1
                        print(f"*** MESSAGE {message_count} RECEIVED ***")
                        print(f"Full message: {line}")
                        
                        # Parse the message: +RCV=[Address],[Length],[Data],[RSSI],[SNR]
                        try:
                            parts = line[5:].split(',')  # Remove "+RCV=" and split
                            if len(parts) >= 5:
                                sender_addr = parts[0]
                                msg_length = parts[1]
                                message_data = parts[2]
                                rssi = parts[3]
                                snr = parts[4]
                                
                                print(f"  From Address: {sender_addr}")
                                print(f"  Message: '{message_data}'")
                                print(f"  RSSI: {rssi} dBm")
                                print(f"  SNR: {snr} dB")
                                print(f"  Message Length: {msg_length}")
                            else:
                                print(f"  Unexpected message format: {line}")
                        except Exception as e:
                            print(f"  Error parsing message: {e}")
                        
                        print("*" * 50)
                        
                    elif line.startswith("+OK") or line.startswith("+ERR"):
                        print(f"Module status: {line}")
                    else:
                        print(f"Unknown response: {line}")
                        
            except UnicodeDecodeError as e:
                print(f"Unicode decode error: {e}")
            except Exception as e:
                print(f"Error reading from serial: {e}")
        
        time.sleep(0.1)  # Small delay to prevent high CPU usage

except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    print("\nTroubleshooting tips:")
    print("1. Check if Pi Zero UART is enabled in raspi-config")
    print("2. Verify wiring connections")
    print("3. Try a different USB-to-serial adapter if using one")
    print("4. Check if another process is using the serial port")
    
except KeyboardInterrupt:
    print("\nProgram stopped by user.")
    
except Exception as e:
    print(f"Unexpected error: {e}")
    
finally:
    if 'lora_serial' in locals() and lora_serial.is_open:
        lora_serial.close()
        print("LoRa serial port closed.")
