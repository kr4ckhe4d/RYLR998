import serial
import time

# Open serial connection to LoRa module
lora = serial.Serial("/dev/serial0", 115200, timeout=1)

# Configure LoRa module (must match ESP32 settings)
def setup_lora():
    lora.write(b"AT+BAND=915000000\r\n")
    time.sleep(0.5)
    
    lora.write(b"AT+NETWORKID=7\r\n")
    time.sleep(0.5)
    
    lora.write(b"AT+ADDRESS=2\r\n")  # Pi is address 2
    time.sleep(0.5)
    
    print("LoRa configured - listening for messages...")

# Main program
setup_lora()

while True:
    # Check if we received data
    if lora.in_waiting > 0:
        message = lora.readline().decode().strip()
        
        # Look for received messages (they start with "+RCV=")
        if message.startswith("+RCV="):
            # Extract just the message part
            # Format: +RCV=address,length,message,rssi,snr
            parts = message.split(',')
            sender = parts[0][5:]  # Remove "+RCV=" from first part
            actual_message = parts[2]  # The message is the 3rd part
            
            print(f"From {sender}: {actual_message}")
    
    time.sleep(0.1)
