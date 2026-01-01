# OTA Measures Questions (Mitigation)

## Confidentiality (Eavesdropping Protection)

### **1. Why is TLS (Transport Layer Security) alone often considered insufficient for protecting firmware confidentiality?**

Answer: TLS terminates at the CDN or edge server. If the CDN is compromised or untrusted, the firmware would be exposed in plaintext.

Explanation:
To achieve **Defense in Depth**, OEMs use **Application Layer Encryption** (Encrypted Payloads). The firmware is encrypted before it leaves the backend, so it remains opaque even to the CDN handling the download.

### **2. Describe the "Hybrid Encryption" scheme used for OTA updates.**

Answer: It combines Symmetric and Asymmetric encryption to balance speed and security.

Explanation:
1.  **Symmetric (e.g., AES-256):** Used to encrypt the large firmware binary because it is fast.
2.  **Asymmetric (e.g., RSA/ECC):** Used to encrypt the *Symmetric Key* itself, using the target ECU's Public Key. This encrypted key is sent along with the payload.

### **3. Where must the private decryption keys be stored within the vehicle?**

Answer: In a **Hardware Security Module (HSM)** or Secure Hardware Extension (SHE).

Explanation:
Storing keys in standard flash memory is risky. An HSM is tamper-resistant hardware that performs cryptographic operations internally, ensuring the private keys are never exposed to the main operating system.

## Integrity (Rollback Protection)

### **4. How does an ECU technically prevent a Rollback Attack?**

Answer: By comparing the version number in the **Signed Metadata** against a stored **Monotonic Counter**.

Explanation:
Before installing, the ECU verifies validity of the signature, then checks if `New_Version > Stored_Version`. If the new version is lower or equal, it rejects the update.

### **5. What is a "Monotonic Counter"?**

Answer: A hardware or secure software counter that can only be incremented (count up) and never decremented or reset.

Explanation:
This ensures that once a vehicle has updated to version 5, it is physically impossible to overwrite the counter back to version 4, thus permanently blocking installation of older firmware.

## Availability (DoS Protection)

### **6. What client-side strategy mitigates the impact of network congestion or DoS attempts?**

Answer: **Exponential Backoff.**

Explanation:
If a vehicle fails to connect to the update server, it should not retry immediately (which would worsen congestion). Instead, it waits progressively longer intervals (e.g., 1s, 2s, 4s, 8s) before retrying.
