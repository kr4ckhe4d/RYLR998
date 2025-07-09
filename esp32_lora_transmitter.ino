// ESP32 WROVER-E LoRa Transmitter using RYLR998 Module
// Hardware Serial2 is used for LoRa communication

HardwareSerial loraSerial(2);

// Pin definitions for ESP32 WROVER-E
// Using GPIO pins that are available and not used for PSRAM/Flash
#define LORA_RX_PIN 21  // Connect to RYLR998 TX
#define LORA_TX_PIN 22  // Connect to RYLR998 RX
#define LORA_RST_PIN 19  // Optional: Connect to RYLR998 RST pin

void setup() {
  // Initialize USB serial for debugging
  Serial.begin(115200);
  while (!Serial) {
    delay(10); // Wait for serial port to connect
  }
  Serial.println("ESP32 WROVER-E LoRa Transmitter Starting...");

  // Optional: Hardware reset of LoRa module
  #ifdef LORA_RST_PIN
    pinMode(LORA_RST_PIN, OUTPUT);
    digitalWrite(LORA_RST_PIN, LOW);
    delay(100);
    digitalWrite(LORA_RST_PIN, HIGH);
    delay(1000);
  #endif

  // Initialize hardware serial for LoRa module
  // ESP32 WROVER-E: Using GPIO 21/22 which are available and safe to use
  loraSerial.begin(115200, SERIAL_8N1, LORA_RX_PIN, LORA_TX_PIN);
  delay(1000);

  // Test communication with LoRa module
  Serial.println("Testing LoRa module communication...");
  loraSerial.println("AT");
  delay(500);
  
  // Read response
  if (loraSerial.available()) {
    String response = loraSerial.readString();
    Serial.print("LoRa Response: ");
    Serial.println(response);
  }

  // Configure LoRa module
  Serial.println("Configuring LoRa module...");
  
  // Set frequency band (915MHz for US, change to 868000000 for EU)
  // Check your local regulations!
  sendATCommand("AT+BAND=915000000");
  
  // Set network ID (0-15) to avoid interference
  sendATCommand("AT+NETWORKID=7");
  
  // Set this module's address
  sendATCommand("AT+ADDRESS=1");
  
  // Optional: Set transmission power (5-22 dBm)
  sendATCommand("AT+PARAMETER=12,4,1,7");  // SF=12, BW=4(500kHz), CR=1(4/5), Preamble=7
  
  Serial.println("LoRa Module configured successfully!");
  Serial.println("Starting transmission loop...");
}

void loop() {
  // Message to send
  String message = "Hello from ESP32 WROVER-E!";
  
  // Send message to address 2
  sendMessage(2, message);
  
  // Check for any incoming messages
  checkForMessages();
  
  // Wait 10 seconds before next transmission
  delay(10000);
}

void sendATCommand(String command) {
  Serial.println("Sending: " + command);
  loraSerial.println(command);
  delay(500);
  
  // Read and display response
  if (loraSerial.available()) {
    String response = loraSerial.readString();
    response.trim();
    Serial.println("Response: " + response);
  }
}

void sendMessage(int address, String message) {
  // AT command format: AT+SEND=[Address],[Payload Length],[Payload]
  String atCommand = "AT+SEND=" + String(address) + "," + String(message.length()) + "," + message;
  
  Serial.println("Transmitting to address " + String(address) + ": " + message);
  loraSerial.println(atCommand);
  
  delay(1000); // Wait for transmission to complete
  
  // Check for transmission confirmation
  if (loraSerial.available()) {
    String response = loraSerial.readString();
    response.trim();
    if (response.indexOf("+OK") >= 0) {
      Serial.println("Message sent successfully!");
    } else {
      Serial.println("Transmission failed: " + response);
    }
  }
}

void checkForMessages() {
  // Check if there are any incoming messages
  if (loraSerial.available()) {
    String incoming = loraSerial.readString();
    incoming.trim();
    
    // Parse incoming message format: +RCV=[Address],[Length],[Data],[RSSI],[SNR]
    if (incoming.startsWith("+RCV=")) {
      Serial.println("Received message: " + incoming);
      
      // Extract message components
      int firstComma = incoming.indexOf(',');
      int secondComma = incoming.indexOf(',', firstComma + 1);
      int thirdComma = incoming.indexOf(',', secondComma + 1);
      int fourthComma = incoming.indexOf(',', thirdComma + 1);
      
      if (firstComma > 0 && secondComma > 0 && thirdComma > 0) {
        String senderAddress = incoming.substring(5, firstComma);
        String messageLength = incoming.substring(firstComma + 1, secondComma);
        String messageData = incoming.substring(secondComma + 1, thirdComma);
        String rssi = incoming.substring(thirdComma + 1, fourthComma);
        String snr = incoming.substring(fourthComma + 1);
        
        Serial.println("From: " + senderAddress);
        Serial.println("Message: " + messageData);
        Serial.println("RSSI: " + rssi + " dBm");
        Serial.println("SNR: " + snr + " dB");
      }
    }
  }
}

// Optional: Function to put ESP32 into deep sleep to save power
void enterDeepSleep(int seconds) {
  Serial.println("Entering deep sleep for " + String(seconds) + " seconds...");
  Serial.flush();
  esp_sleep_enable_timer_wakeup(seconds * 1000000ULL); // Convert to microseconds
  esp_deep_sleep_start();
}
