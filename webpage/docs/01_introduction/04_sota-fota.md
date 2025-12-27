# SOTA vs. FOTA

In the realm of embedded systems and connected devices, remote updates are pivotal for maintaining and enhancing functionality. Two primary methods facilitate these updates: **Software Over-the-Air (SOTA)** and **Firmware Over-the-Air (FOTA)**. While both enable wireless updates, they target different layers of a device's software architecture. This chapter delineates the distinctions between SOTA and FOTA, explores their unique applications, and delves into the technical considerations essential for their effective implementation in automotive systems.

## What is SOTA?

**Software Over-the-Air (SOTA)** refers to the wireless delivery of software updates, configuration settings, or other data to devices such as smartphones, tablets, set-top boxes, and vehicles. In the automotive context, SOTA primarily targets non-critical software components, enhancing functionalities without directly interacting with the vehicle's core hardware operations. SOTA updates can encompass:

- **Operating System Updates**: Enhancements or patches to the vehicle's infotainment system or other onboard operating systems.
- **Application Updates**: Introduction of new features or bug fixes for installed applications, such as navigation, media, or connectivity services.
- **Configuration Settings**: Adjustments to device parameters or network settings to optimize performance or user preferences.

The primary advantage of SOTA updates is the elimination of manual interventions, allowing devices to stay current with minimal user effort. This method is widely used in mobile devices and is increasingly prevalent in automotive systems to update infotainment applications and other non-critical software components.

*Example: SOTA Update for Infotainment System*

```python
import requests
import hashlib
import cryptography

def perform_sota_update(app_name, version):
    update_url = f"https://updates.automanufacturer.com/apps/{app_name}/{version}"
    response = requests.get(update_url, verify='ca_cert.pem')

    if response.status_code == 200:
        update_data = response.content
        signature = response.headers.get('Signature')

        if verify_signature(update_data, signature):
            with open(f"/apps/{app_name}.bin", "wb") as f:
                f.write(update_data)
            reboot_application(app_name)
            log_update_status(f"SOTA Update for {app_name} v{version} Successful")
        else:
            log_update_status(f"SOTA Update for {app_name} v{version} Failed: Signature Mismatch")
    else:
        log_update_status(f"SOTA Update for {app_name} v{version} Failed: HTTP {response.status_code}")

def verify_signature(data, signature):
    # Implement cryptographic signature verification
    pass

def reboot_application(app_name):
    # Implement application reboot logic
    pass

def log_update_status(message):
    print(message)
```

## What is FOTA?

**Firmware Over-the-Air (FOTA)** specifically pertains to the remote updating of a device's firmware—the low-level software that directly interacts with hardware components. Firmware is crucial for the basic operation of devices and includes:

- **Bootloaders**: Programs that initialize hardware during the booting process.
- **System Firmware**: Core functionalities that control hardware operations, such as engine control units (ECUs), braking systems, and advanced driver-assistance systems (ADAS).

FOTA updates are essential for addressing hardware-level issues, enhancing performance, or patching security vulnerabilities. Given the critical nature of firmware, FOTA processes are designed with stringent safeguards to ensure update integrity and device stability.

*Example: FOTA Update Handler for ECU*

```c
#include "ecu.h"
#include "crypto.h"
#include "storage.h"

// Apply firmware update to ECU
bool apply_ecu_firmware_update(uint8_t *firmware_data, size_t firmware_size) {
    // Verify firmware signature
    if (!verify_signature(firmware_data, firmware_size, PUBLIC_KEY)) {
        log_error("Firmware signature verification failed.");
        return false;
    }

    // Write firmware to temporary storage
    if (!storage_write("temp_firmware.bin", firmware_data, firmware_size)) {
        log_error("Failed to write firmware to storage.");
        return false;
    }

    // Validate firmware integrity
    if (!validate_firmware("temp_firmware.bin")) {
        log_error("Firmware validation failed.");
        return false;
    }

    // Replace old firmware with new firmware
    if (!storage_replace("current_firmware.bin", "temp_firmware.bin")) {
        log_error("Failed to replace firmware.");
        return false;
    }

    // Reboot ECU to apply new firmware
    reboot_ecu();

    log_info("ECU firmware updated successfully.");
    return true;
}
```

## Key Differences Between SOTA and FOTA

| Feature               | SOTA (Software Over-the-Air)                  | FOTA (Firmware Over-the-Air)                   |
|-----------------------|-----------------------------------------------|------------------------------------------------|
| **Target Layer**      | Operating systems, applications, configurations | Low-level firmware and bootloaders             |
| **Update Type**       | OS updates, app enhancements, settings adjustments | Core firmware patches, bootloader updates      |
| **Storage**           | Stored in file systems or application memory    | Stored in non-volatile memory (e.g., flash ROM)|
| **Impact on Device**  | May require a reboot depending on the update    | Typically requires a reboot to apply new firmware|
| **Update Size**       | Varies; can be large for OS updates             | Generally smaller, focused on essential firmware components |
| **Failure Handling**  | Can often revert to previous versions; less critical | Requires robust fail-safes to prevent device bricking |

## Technical Considerations

Implementing SOTA and FOTA updates requires addressing distinct technical challenges to ensure seamless, secure, and reliable update processes. The following sections explore the key technical considerations for each method.

### 1. Update Delivery Mechanism

Both SOTA and FOTA rely on secure and efficient delivery methods to transmit update packages from the cloud backend to the vehicle's internal systems.

- **Protocols**: Utilization of HTTP(S) or MQTT for retrieving updates ensures reliable and scalable communication channels.
- **Data Efficiency**: Implementation of differential update techniques, such as binary delta encoding, minimizes data transmission by sending only the changes between software versions.
- **Security**: Application of digital signatures and hash verifications ensures the authenticity and integrity of update packages.

*Example: Secure Update Retrieval Using HTTPS*

```c
#include "network.h"
#include "crypto.h"

bool retrieve_update_package(const char *url, uint8_t *buffer, size_t buffer_size) {
    // Establish secure HTTPS connection
    if (!network_connect_secure(url, buffer, buffer_size)) {
        log_error("Secure connection failed.");
        return false;
    }

    // Verify digital signature of the update package
    if (!verify_signature(buffer, buffer_size, PUBLIC_KEY)) {
        log_error("Update package signature verification failed.");
        return false;
    }

    log_info("Update package retrieved and verified successfully.");
    return true;
}
```

### 2. Flashing Process

The process of applying updates differs significantly between SOTA and FOTA due to the layers they target.

- **SOTA Updates**:
  - Involve installing new applications or OS versions.
  - May not directly affect the device's core functionalities.
  - Can often be applied without interrupting critical operations.

- **FOTA Updates**:
  - Involve flashing the firmware, which directly interacts with hardware components.
  - Managed by a bootloader that ensures the process is atomic, meaning it either completes successfully or reverts to the previous state without partial updates.
  - Typically requires a system reboot to apply the new firmware.

*Example: Atomic Firmware Flashing Process*

```c
#include "bootloader.h"
#include "storage.h"

// Atomic firmware flashing
bool flash_firmware_atomic(uint8_t *firmware_data, size_t firmware_size) {
    // Write to inactive firmware slot
    if (!storage_write("firmware_slot_2.bin", firmware_data, firmware_size)) {
        log_error("Failed to write to inactive firmware slot.");
        return false;
    }

    // Verify firmware integrity
    if (!validate_firmware("firmware_slot_2.bin")) {
        log_error("Firmware integrity validation failed.");
        return false;
    }

    // Switch active firmware slot
    if (!bootloader_switch_slot(2)) {
        log_error("Failed to switch firmware slots.");
        return false;
    }

    // Reboot to apply new firmware
    reboot_system();

    log_info("Firmware flashed atomically and system rebooted successfully.");
    return true;
}
```

### 3. Rollback and Redundancy

Given the critical role of firmware in device operation, FOTA implementations often incorporate redundancy strategies to ensure reliability and facilitate safe rollbacks in case of update failures.

- **Dual Firmware Slots**: Maintain two firmware slots (e.g., slot A and slot B) allowing the system to switch between them in case an update fails.
- **Backup Storage**: Keep backup copies of previous firmware versions to enable quick recovery.
- **Automated Rollback Procedures**: Implement automated mechanisms that detect update failures and revert to a stable firmware version without user intervention.

*Example: Dual Firmware Slot Management*

```c
#define SLOT_ACTIVE 0
#define SLOT_BACKUP 1

bool switch_firmware_slot(int slot) {
    if (slot != SLOT_ACTIVE && slot != SLOT_BACKUP) {
        log_error("Invalid firmware slot.");
        return false;
    }

    // Update bootloader configuration to activate the selected slot
    if (!bootloader_set_active_slot(slot)) {
        log_error("Failed to set active firmware slot.");
        return false;
    }

    log_info("Firmware slot switched successfully.");
    return true;
}

bool detect_and_handle_update_failure() {
    if (bootloader_detect_failure()) {
        log_warning("Firmware update failure detected. Initiating rollback.");
        return switch_firmware_slot(SLOT_BACKUP);
    }
    return true;
}
```

### 4. Security Measures

Ensuring the security of both SOTA and FOTA updates is paramount to protect against unauthorized access, data breaches, and malicious updates. Key security measures include:

- **Encryption**: Use of end-to-end encryption protocols like TLS or AES-256 during transmission to protect data from interception and tampering.
- **Authentication**: Verification of updates through cryptographic signatures ensures that only authorized updates are applied.
- **Secure Boot**: Implementation of secure boot processes ensures that only authenticated firmware is executed during the device's startup process.

*Example: Secure Boot Verification*

```c
#include "secure_boot.h"
#include "crypto.h"

bool verify_secure_boot() {
    uint8_t bootloader_hash[HASH_SIZE];
    uint8_t expected_hash[HASH_SIZE] = { /* Precomputed hash values */ };

    // Compute hash of the bootloader
    compute_sha256("bootloader.bin", bootloader_hash);

    // Compare computed hash with expected hash
    if (memcmp(bootloader_hash, expected_hash, HASH_SIZE) != 0) {
        log_error("Bootloader integrity check failed.");
        return false;
    }

    log_info("Bootloader verified successfully.");
    return true;
}
```

## Conclusion

While both **SOTA and FOTA** enable remote updates, they serve distinct purposes within a device's architecture. **SOTA** focuses on higher-level software components such as operating systems and applications, facilitating continuous improvements and feature enhancements without directly interacting with hardware functionalities. In contrast, **FOTA** is dedicated to updating the foundational firmware essential for hardware operation, addressing critical performance and security aspects.

Understanding the differences between SOTA and FOTA is crucial for implementing effective and secure update strategies in modern connected vehicles. By leveraging both methods appropriately, automotive manufacturers can ensure that their vehicles remain up-to-date, secure, and capable of delivering an optimal user experience. Integrating robust delivery mechanisms, secure flashing processes, redundancy strategies, and comprehensive security measures will enable seamless and reliable OTA updates, thereby enhancing the overall reliability and longevity of automotive systems.