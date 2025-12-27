# Defense in Depth

To protect against the threats outlined in STRIDE, we employ a multi-layered security architecture.

## 1. Transport Layer Security (mTLS)

**Defense against:** Spoofing, Information Disclosure.

- **Mutual TLS (mTLS):** The Server has a certificate, AND the **Vehicle** has a certificate (Factory PKI).
- **Pinning:** The vehicle "pins" the OEM's Root CA. It will reject certificates from any other CA (even valid ones like Let's Encrypt), preventing MitM via compromised CAs.

## 2. Supply Chain Security (Uptane)

**Defense against:** Mix-and-Match, Compromised Backend.
OTA is unique because even the **OEM Server** is untrusted. If an insider at the OEM goes rogue, they could sign malicious firmware.
**Uptane** (IEEE-ISTO 6100) solves this by separating duties:

- **Image Repository:** Stores the binaries (Signed by Developers).
- **Director Repository:** Instructs the vehicle *what* to install (Signed by Release Managers).
- **Time Server:** Prevents "Freeze Attacks" (replay of old updates).
The vehicle validates signatures from *both* repositories.

## 3. On-Device Security

### Secure Boot (Hardware Root of Trust)

**Defense:** Validation of the bootloader.

1. **ROM Code:** Verifies the Bootloader signature.
2. **Bootloader:** Verifies the Kernel signature.
3. **Kernel:** Verifies the Filesystem (dm-verity).
If any check fails, the ECU refuses to boot.

### Hardware Security Module (HSM)

Top-tier ECUs have a dedicated HSM core (e.g., Infineon Aurix).

- **Key Storage:** Private keys never leave the HSM.
- **Crypto Acceleration:** AES-256 and ECC verification happens in hardware, preventing side-channel attacks (Power Analysis).

## 4. Anti-Rollback (Hardware Enforced)

**Defense against:** Downgrade Attacks.
When an update to v2.0 is successful, the HSM blows a microscopic fuse (eFuse).

- If anyone tries to flash v1.0 later, the HSM checks the fuse: "Fuse 2 is blown, but v1.0 expects Fuse 1. Reject."

## 5. Gateway Firewall

**Defense:** Network Segmentation.
The Gateway (central router) filters traffic.

- **Rule:** "Only the OTA Manager process can talk to `update.oem.com`."
- **Rule:** "The Infotainment unit cannot send CAN messages to the Engine."
