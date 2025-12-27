# Security Threats (STRIDE)

OTA updates are the most critical attack vector in a modern vehicle. If an attacker controls the update server, they control the fleet. We analyze threats using the **STRIDE** model.

## 1. Spoofing

**Attack:** An attacker impersonates the OEM Server.

- **Scenario:** A "Man-in-the-Middle" (MitM) sets up a fake cell tower (IMSI Catcher). The vehicle connects to `update.oem.com` which resolves to the attacker's IP.
- **Impact:** The attacker sends malicious firmware to the car.

## 2. Tampering

**Attack:** Altering the firmware binary *in transit* or *at rest*.

- **Scenario:** The firmware is stored on a CDN (Content Delivery Network). The attacker hacks the CDN and injects a backdoor into the `engine_ctrl.bin` file.
- **Impact:** The vehicle downloads the modified binary. If the signature check isn't robust, the code runs.

## 3. Repudiation

**Attack:** Denying that an action took place.

- **Scenario:** A user claims, "I never authorized this update that bricked my car."
- **Impact:** Legal liability. Without non-repudiation (logs signed by the user's private key), the OEM cannot prove the user consented.

## 4. Information Disclosure

**Attack:** Eavesdropping on the update channel.

- **Scenario:** An attacker captures the update traffic.
- **Impact:**
  - **Privacy:** They see the VIN and location data.
  - **IP Theft:** They reverse-engineer the firmware to find 0-day vulnerabilities.

## 5. Denial of Service (DoS)

**Attack:** Preventing the vehicle from updating or operating.

- **Scenario 1 (Network):** Jamming the cellular signal (GSM Jammer).
- **Scenario 2 (Battery Drain):** Constantly waking up the TCU with "Hello" packets so it never sleeps, draining the 12V battery.
- **Scenario 3 (Infinite Loop):** Sending a bad update that causes the ECU to bootloop.

## 6. Elevation of Privilege

**Attack:** Gaining higher access rights than authorized.

- **Scenario:** An attacker exploits a buffer overflow in the Gateway's "Unzip" function.
- **Impact:** They gain Root access on the Gateway, allowing them to send CAN messages to the Brakes or Steering.

## Specific OTA Attacks

### The "Endless Rollback" Attack

The attacker triggers a failure condition (e.g., pulling a fuse) exactly when the update finishes. The system rolls back. They repeat this ad infinitum to prevent a security patch from installing.

### The "Mix-and-Match" Attack

The attacker takes a valid **Engine v1.0** (signed) and a valid **Transmission v2.0** (signed) and tells the car to install them together.

- **Problem:** These two versions are incompatible. The engine expects torque data in Nm, the transmission sends it in lb-ft.
- **Result:** Physical damage to the gearbox.
- **Defense:** **Uptane** (Director repository) ensures coherent sets.
