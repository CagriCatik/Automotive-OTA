# OTA Connectivity Questions (MQTT & HTTPS)

## Protocols

### **1. Why are two different protocols (MQTT and HTTPS) used in the OTA architecture?**

Answer: MQTT is used for lightweight control/signaling, while HTTPS is used for heavy payload transmission.

Explanation:
*   **MQTT:** Optimized for low bandwidth, unstable networks, and real-time connectivity (Pub-Sub). It handles command messages, status updates, and telemetry.
*   **HTTPS:** Optimized for reliable, secure transfer of large files (firmware images). It supports resumable downloads and standard encryption.

### **2. Explain the difference between QoS 0, QoS 1, and QoS 2 in MQTT.**

Answer:
*   **QoS 0 (At most once):** Fire-and-forget. The message is sent, and no distinct acknowledgment is expected. Fastest, but messages can be lost.
*   **QoS 1 (At least once):** Guarantees delivery. The sender stores the message until it receives a PUBACK. Common for OTA control messages. May result in duplicates.
*   **QoS 2 (Exactly once):** Guarantee delivery without duplicates. Slower due to 4-step handshake. High overhead.

## Connectivity Architecture

### **3. What is a "Digital Twin" or "Shadow State" in the context of vehicle connectivity?**

Answer: A cloud-based replica of the vehicle's state that allows applications to interact with the vehicle even when it is offline.

Explanation:
The cloud maintains a "Shadow" of the vehicle. If a command (e.g., "Unlock Door") is sent while the vehicle is offline (e.g., in a tunnel), it updates the Shadow data. When the vehicle comes back online, it synchronizes with the Shadow to execute the pending commands.

### **4. How does the architecture handle "Intermittent Connectivity" for OTA?**

Answer: Through MQTT Queuing and Resumable HTTPS Downloads.

Explanation:
*   **MQTT:** If the vehicle disconnects, the Broker (with `CleanSession=False`) queues messages (QoS > 0) and delivers them when the vehicle reconnects.
*   **HTTPS:** Using HTTP Range requests, the vehicle can resume a file download from the last received byte after a network drop, preventing the need to restart large downloads.

##  Telemetry

### **5. What is "Edge Processing" in telemetry streaming, and why is it important?**

Answer: Processing and filtering sensor data locally on the TCU before sending it to the cloud.

Explanation:
Vehicles generate terabytes of data. Streaming raw data is cost-prohibitive over cellular networks. Edge processing filters this data (e.g., "only send data if battery temp > 40°C") to reduce bandwidth usage and cloud storage costs.
