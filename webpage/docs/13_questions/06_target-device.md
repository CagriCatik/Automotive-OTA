# Target Device & TCU Questions

## TCU & OTA Manager

### **1. What is the functioning of the TCU (Telematics Control Unit) in the OTA context?**

Answer: It acts as the vehicle's gateway, managing communication with the cloud (backend) and internal ECUs.

Explanation:
The TCU hosts the **OTA Manager**, which orchestrates the update process. It receives update packages from the cloud (via HTTPS), verifies them, and then directs the update to the target ECUs using diagnostic protocols (UDS). It also collects and uploads telemetry data to the cloud.

### **2. What validation steps does the OTA Manager perform before initiating an update on an ECU?**

Answer: Pre-download validation (conditions check), Post-download validation (integrity/checksum), and Compatibility verification.

Explanation:
1.  **Pre-download:** Checks vehicle state (battery, ignition, network).
2.  **Post-download:** Verifies that the downloaded file is not corrupt (integrity check, e.g., SHA-256).
3.  **Compatibility:** Confirms that the updated software version matches the target ECU's hardware and is allowed for installation.

## Target ECU Architecture

### **3. What is the difference between the Boot Manager and the Bootloader?**

Answer: The Boot Manager decides *which mode* to start in (Application vs Programming), while the Bootloader *executes* the programming process.

Explanation:
*   **Boot Manager:** Runs first at power-up. It checks flags to see if a programming session is requested. If yes, it jumps to the Bootloader. If no, it jumps to the Application.
*   **Bootloader:** Handles UDS services (download, erase, write) to update the software.

### **4. During a UDS programming session, which service is used to unlock the ECU security?**

Answer: Service 0x27 (Security Access).

Explanation:
Before any critical operations (like writing to flash memory) can occur, the tester (TCU) must unlock the ECU using a Seed-Key exchange via the Security Access service (0x27).

### **5. What is the role of the Flash Driver in the ECU update process?**

Answer: It provides the low-level hardware abstraction layer for writing data to the physical flash memory.

Explanation:
The Bootloader stays generic. To write to specific memory hardware, it calls functions in the Flash Driver, which handles the specific voltage and timing requirements to erase and program the flash sectors.

## Fail-Safe Strategy

### **6. Why is a "Rollback" mechanism critical, especially when updating multiple dependent ECUs?**

Answer: To prevent the vehicle from being left in an "inconsistent state" where dependent ECUs have mismatched software versions.

Explanation:
If updating ECU A succeeds but ECU B fails, and they depend on each other (e.g., Infotainment and Battery Management), the system is unstable. A rollback restores *both* to their previous known-good version to ensure the vehicle remains safe and functional.
