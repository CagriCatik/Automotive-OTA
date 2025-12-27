# Compliance & Security (UN R156)

OTA updates are no longer just a technical feature; they are a regulated process. In the UNECE region (Europe, Japan, etc.), vehicles **cannot be sold** without Type Approval regarding Software Updates.

## UN Regulation No. 156 (SUMS)

**UN R156** mandates that the OEM must implement a **Software Update Management System (SUMS)**.

### Key Requirements

1. **RXSWIN (Regulation X Software Identification Number):**
    - A unique ID representing the approved software configuration of the vehicle (typically related to emissions, braking, steering).
    - The vehicle must store the RXSWIN and ensure the running software matches it.
    - If an update changes the RXSWIN, the OEM must apply for a Type Approval Extension *before* deploying the update.
2. **Safety & User Info:**
    - The user must be informed about the update purpose.
    - The update must not be performable if it impacts safety (e.g., while driving).
3. **Audit Trail:**
    - Every update attempt (success or failure) must be logged and traceable for years.

## UN Regulation No. 155 (CSMS)

**UN R155** focuses on Cybersecurity. OTA is a primary attack vector.

### Threat Analysis & Risk Assessment (TARA)

Before deploying OTA, the OEM must conduct a TARA (as per **ISO 21434**).

- **Threat:** "Attacker spoofs backend and sends malicious firmware."
- **Mitigation:** "Implement TLS 1.3 pinned certificates + ECDSA Signature verification in OTA Manager."

## ISO 24089 (Road Vehicles – Software Update Engineering)

This ISO standard provides the "How-To" for complying with UN R156. It defines the organizational processes:

- **Campaign Management:** How to select vehicles.
- **Compatibility Check:** Ensuring HW/SW compatibility.
- **Rollout Strategy:** Staged rollout (Alpha -> Beta -> 10% -> 100%).

## Conclusion

Testing is not just about "Does it work?". It is about "Can we prove to the auditor that it is safe?".
OTA developers must work closely with the Homologation department to ensure every bit sent to a car is legally accounted for.
