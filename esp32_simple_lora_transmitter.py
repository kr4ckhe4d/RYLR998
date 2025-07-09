// Simple ESP32 WROVER-E LoRa Transmitter

HardwareSerial lora(2);  // Use Serial2 for LoRa

void setup() {
  // Start serial for debugging
  Serial.begin(115200);
  Serial.println("ESP32 LoRa Transmitter Starting...");
  
  // Start LoRa serial (RX=21, TX=22)
  lora.begin(115200, SERIAL_8N1, 21, 22);
  delay(1000);
  
  // Configure LoRa module (must match Pi settings)
  lora.println("AT+BAND=915000000");
  delay(500);
  
  lora.println("AT+NETWORKID=7");
  delay(500);
  
  lora.println("AT+ADDRESS=1");  // ESP32 is address 1
  delay(500);
  
  Serial.println("LoRa configured - starting transmission...");
}

void loop() {
  String message = "Hello from ESP32!";
  
  // Send to address 2 (Pi Zero)
  // Format: AT+SEND=address,length,message
  String command = "AT+SEND=2," + String(message.length()) + "," + message;
  
  Serial.println("Sending: " + message);
  lora.println(command);
  
  delay(5000);  // Wait 5 seconds before next message
}
