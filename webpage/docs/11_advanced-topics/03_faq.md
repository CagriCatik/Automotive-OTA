# OTA Frequently Asked Questions (FAQ)

## Safety & Reliability

### Q: What happens if the 12V battery dies during an update?

**A:** This is the #1 Testing Scenario.

- **Dual Bank:** The active bank is untouched. The car reboots into the old version.
- **Single Bank:** The Bootloader checks a "flag". It sees the update was interrupted and stays in "Recovery Mode", waiting for a retry. The car will not start, but the ECU is not bricked.

### Q: What if the cellular connection drops (tunnel)?

**A:** OTA Protocols (HTTP Range Requests) support **Resume**. The download pauses and resumes exactly where it left off when signal returns. The *installation* only begins once 100% of the payload is verified (Signature Check).

### Q: Can I drive the car while it updates?

**A:** It depends.

- **SOTA (Maps, Apps):** Yes. Features update in the background.
- **FOTA (Engine, Brakes):** **NO.** The vehicle immobilizer is engaged. Using the brakes while the ABS module is resetting would be catastrophic. The screen will show a "countdown" and warn the user not to drive.

## Business & Legal

### Q: Who pays for the mobile data?

**A:** The OEM. They have bulk contracts with Telcos (AT&T, Verizon, Vodafone) for "IoT Sims". However, some OEMs require Home Wi-Fi for massive map updates to save cost.

### Q: Does OTA void my warranty?

**A:** Official OTA updates *maintain* the warranty. In fact, refusing a critical safety OTA might void your warranty (negligence).

### Q: Can hackers control my steering wheel?

**A:** Extremely difficult, but theoretically possible if the **Gateway** is compromised. This is why the Gateway Firewall isolates the Infotainment (Internet) from the Chassis CAN (Steering).

## Technical

### Q: Why do updates take so long (e.g., 45 mins)?

**A:** It's not the download speed; it's the **Bus Speed**.

- CAN Bus is slow (500 kbps).
- Flashing a 4MB binary over UDS on CAN takes minutes.
- Flashing 30 ECUs sequentially takes time.
- **Future:** Ethernet (DoIP) will reduce this to seconds.

### Q: Why does the fan run loud during an update?

**A:** To protect the battery. The ECUs are awake and consuming power (20-30 Amps). The DC-DC converter might be active, or the Head Unit requires cooling while processing the update files.
