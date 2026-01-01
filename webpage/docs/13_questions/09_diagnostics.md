# OTA Diagnostics Questions (UDS & DoIP)

## UDS over CAN (Protocol Details)

### **1. Why is a Transport Protocol (CAN-TP) required for OTA updates over CAN?**

Answer: To enable the transmission of large data payloads (like firmware) over the CAN bus, which has a native limit of only 8 bytes per frame.

Explanation:
CAN-TP handles **Segmentation and Reassembly**. It breaks down a large message (e.g., 1MB firmware chunk) into multiple small CAN frames on the sender side and reassembles them on the receiver side.

### **2. Explain the function of the "Flow Control" frame in CAN-TP.**

Answer: It allows the receiver to tell the sender to pause or adjust the transmission speed to prevent buffer overflow.

Explanation:
After receiving a "First Frame" (start of a large message), the receiver sends a "Flow Control" frame (0x30) containing:
*   **Block Size (BS):** How many frames to send before waiting for another acknowledgement.
*   **Separation Time (STmin):** Minimum time delay between frames.

### **3. What are the three main frame types in a segmented CAN-TP transfer?**

Answer:
1.  **First Frame (0x10):** Announces the total message length.
2.  **Flow Control (0x30):** Receiver acknowledges and sets parameters.
3.  **Consecutive Frame (0x21, 0x22...):** Carries the actual data payload.

## UDS over Ethernet (DoIP)

### **4. What is the primary advantage of DoIP (Diagnostics over IP) compared to UDS over CAN for OTA?**

Answer: **Bandwidth.** DoIP offers drastically higher speeds (100 Mbps or 1 Gbps) compared to CAN (500 kbps - 1 Mbps), reducing flashing time from hours to minutes.

Explanation:
For modern vehicles with large software images (Infotainment, ADAS), CAN is too slow. DoIP uses standard Ethernet physical layers and TCP/IP to transfer data rapidly.

### **5. In DoIP, which transport protocols are used for Vehicle Discovery versus Diagnostic Data?**

Answer:
*   **Vehicle Discovery:** Uses **UDP** (Broadcast, lightweight, connectionless).
*   **Diagnostic Data:** Uses **TCP** (Reliable, connection-oriented, ensures packet delivery).

### **6. Which UDS Service is typically used to read stored fault codes (DTCs)?**

Answer: Service **0x19** (ReadDTCInformation).

Explanation:
The diagnostic tester sends `0x19 0x02` (Read DTCs by Status Mask) to query the ECU for any stored error codes, which is essential for the "Remote Diagnostics" use case.
