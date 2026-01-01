# Target Device and Flashing Questions

This section explores the architecture of the Electronic Control Units (ECUs) being updated, focusing on memory layouts and fail-safe strategies.

```kroki-mermaid {display-width=700px display-align=center}
graph TD
    subgraph "Single-Bank Architecture"
        SB_F[Single Flash Region]
        SB_F --- SB_App[Active Application]
    end

    subgraph "Dual-Bank Architecture"
        DB_F[Flash Memory]
        DB_F --- BankA[Bank A: Active]
        DB_F --- BankB[Bank B: Inactive/Download]
    end

    SB_App -.->|Update Requires| Offline[Vehicle Offline]
    BankB -.->|Update Allows| Background[Background Programming]
```

---

## ECU Memory Architectures

### **1. What is the difference between Single-Bank and Dual-Bank flash memory?**

**Answer:** Single-bank has one memory region for the app, while dual-bank splits memory into two independent partitions (A and B).

**Explanation:**
*   **Single-Bank:** Cheaper but requires the vehicle to be non-operational during the entire erase-and-program cycle.
*   **Dual-Bank:** Allows the vehicle to run the current app (Bank A) while the new version is downloaded and programmed into Bank B in the background.

### **2. Why is an external backup flash often used for Single-Bank ECUs?**

**Answer:** To provide a recovery path if the flashing process is interrupted or the new software is corrupted.

**Explanation:**
Since a single-bank ECU must erase its only application to install a new one, it first copies the working software to an external storage (via SPI/I2C). If the update fails, the bootloader can restore the old version from this backup.

### **3. Explain the "A/B Switch" mechanism in Dual-Bank systems.**

**Answer:** It is the process of changing the execution pointer from the old software bank to the newly updated bank.

**Explanation:**
After Bank B is fully programmed and verified, the ECU performs a reset or a pointer jump. The bootloader then treats Bank B as the "Active" bank. This switch is fast and minimizes vehicle downtime.

---

## Fail-Safe and Rollback

### **4. What is the primary goal of a "Fail-Safe" strategy in OTA?**

**Answer:** To ensure the vehicle never remains in an inconsistent or unsafe state due to a failed update.

**Explanation:**
A fail-safe strategy detects errors (power loss, corruption) and triggers an immediate response—either a retry or a full rollback—to return the ECU to a known-working software version.

### **5. Why must dependent ECUs be rolled back together?**

**Answer:** To maintain functional consistency across the vehicle network.

**Explanation:**
If an update improves communication between the Engine ECU and the Transmission ECU, both must have the new software. If the Engine update succeeds but the Transmission fails, leaving them in mixed versions could cause severe vehicle issues. A "Unified Rollback" restores both to their previous compatible state.

### **6. What role does the Bootloader play in recovery?**

**Answer:** The bootloader is the first code to run; it verifies the application's integrity and decides whether to boot the new software or enter a recovery mode.

**Explanation:**
If the application flash is empty or corrupted, the bootloader prevents the ECU from attempting to run it and instead waits for a re-flashing command or restores a backup, preventing the device from being "bricked."

### **7. What is the main disadvantage of a single-bank ECU architecture?**

**Answer:** Extended vehicle downtime and higher risk during the update process.

**Explanation:**
Because the application must be erased before the new one is written, the ECU is completely non-functional during the update. Any failure during this window requires a slow restoration from backup.

### **8. How does a dual-bank ECU architecture support "background" updates?**

**Answer:** By allowing the processor to continue executing code from the active bank while the flash controller programs the inactive bank.

**Explanation:**
The hardware isolation between Bank A and Bank B means that the vehicle can remain drivable while the bulk of the update data is being written to memory, only requiring a brief pause to switch banks.

### **9. Why is a "Rollback" procedure across multiple ECUs necessary?**

**Answer:** To prevent system-wide incompatibility when one component of a multi-ECU update campaign fails.

**Explanation:**
In modern vehicles, ECUs are tightly coupled. A rollback ensures that if a campaign targeting five ECUs fails on the last one, all five are reverted to their previous state to ensure they can still "talk" to each other correctly.
