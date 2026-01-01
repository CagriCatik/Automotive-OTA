# Connectivity and Protocols Questions

This section covers the communication protocols used for OTA updates, focusing on MQTT for control signaling and HTTPS for data transfer.

```kroki-mermaid {display-width=700px display-align=center}
graph LR
    subgraph "Control Plane (MQTT)"
        B[MQTT Broker]
        TCU_C[TCU Client]
        BE_C[Backend Client]
        BE_C -- "Publish Command" --> B
        B -- "Route to TCU" --> TCU_C
        TCU_C -- "Publish Status" --> B
        B -- "Route to Backend" --> BE_C
    end

    subgraph "Data Plane (HTTPS)"
        S[Cloud Storage / CDN]
        TCU_D[TCU Downloader]
        S -- "Binary Payload" --> TCU_D
    end
```

---

## MQTT for Control Signaling

### **1. Why is MQTT preferred over HTTPS for update orchestration?**

**Answer:** MQTT is lightweight, event-driven, and maintains a persistent connection, making it ideal for "push" notifications and real-time status reporting.

**Explanation:**
*   **Persistent Connection:** Allows the backend to instantly trigger a vehicle update without waiting for the vehicle to "poll" the server.
*   **Low Overhead:** Small packet headers save battery and data costs in mobile environments.
*   **Pub/Sub Model:** Decouples the backend from the vehicle, allowing for flexible fleet management.

### **2. Explain the purpose of MQTT Topics in an OTA context.**

**Answer:** Topics serve as hierarchical addresses used to route messages to specific vehicles or groups of vehicles.

**Explanation:**
Using a topic like `ota/fleet/model_y/vin_12345/command`, the backend can target a single vehicle. Using wildcards like `ota/fleet/model_y/+/command`, it could potentially target all Model Y vehicles.

---

## HTTPS for Data Transfer

### **3. Why is HTTPS used for transferring the actual software package?**

**Answer:** HTTPS is optimized for large, reliable, and secure file transfers.

**Explanation:**
*   **Reliability:** Built-in mechanisms for handling large data volumes and resuming interrupted downloads.
*   **Security:** Provides strong encryption (TLS) to protect the software binary from being intercepted or tampered with during transit.
*   **Universal Support:** CDNs (Content Delivery Networks) are highly optimized for serving HTTPS traffic at scale.

---

## QoS and Reliability

### **4. What does "QoS 1" mean in MQTT, and why is it used for OTA?**

**Answer:** QoS 1 ensures "At Least Once" delivery, meaning the message is guaranteed to arrive, though duplicates are possible.

**Explanation:**
For OTA updates, it is critical that a "Start Update" command reaches the vehicle. QoS 1 ensures this by requiring an acknowledgment from the receiver. If no acknowledgment is received, the sender retransmits the message.

### **5. Can MQTT be used for the actual binary download?**

**Answer:** Technically yes, but it is not recommended for large files.

**Explanation:**
MQTT is designed for small messages. Large binary payloads can block the broker and are less efficiently handled by MQTT's overhead compared to the streaming capabilities of HTTPS.

### **6. How does the TCU handle network switching (e.g., 4G to 5G) during a download?**

**Answer:** The TCU and the HTTPS protocol are designed to handle IP address changes and connection drops by using session resumption and range requests.

**Explanation:**
Modern OTA clients can pause a download when the connection is lost and resume from the exact byte where they left off once the connection is re-established, ensuring efficiency.

### **7. What are the three components of an MQTT message?**

**Answer:** A fixed header, a variable header, and a payload.

**Explanation:**
*   **Fixed Header:** Contains control info like message type and QoS flags.
*   **Variable Header:** Contains topic names and packet identifiers.
*   **Payload:** Carries the actual application data (e.g., JSON command or status).

### **8. Which MQTT QoS level is typically used for OTA control messaging and why?**

**Answer:** QoS 1 (At Least Once).

**Explanation:**
QoS 1 provides a good balance between reliability and overhead. It ensures that critical commands like "Start Update" or "Rollback" are delivered even in poor network conditions, without the high handshake overhead of QoS 2.

### **9. How are wildcards (+ and #) used in MQTT topic subscriptions?**

**Answer:** `+` is a single-level wildcard, and `#` is a multi-level wildcard.

**Explanation:**
*   `ota/+/status`: Subscribes to status updates from all vehicles.
*   `ota/vin123/#`: Subscribes to all topics related to a specific vehicle (commands, status, logs, etc.).
