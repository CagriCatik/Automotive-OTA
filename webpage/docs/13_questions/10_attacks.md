# Security Attacks and Vulnerabilities Questions

This section analyzes the different ways an OTA update system can be attacked, targeting its confidentiality, integrity, and availability.

```kroki-mermaid {display-width=700px display-align=center}
graph LR
    Attacker["Attacker"] -- "Intercept/Listen" --> Eavesdrop["Eavesdrop: Loss of Privacy/IP"]
    Attacker -- "Block Traffic" --> DoS["DoS: Prevent Safety Patches"]
    Attacker -- "Old Version" --> Rollback["Rollback: Re-enable Vulnerabilities"]
    Attacker -- "Malicious Code" --> Injection["Injection: Remote Control/Malware"]

    subgraph "Impact"
        ConfID["Confidentiality"] --- Eavesdrop
        Avail["Availability"] --- DoS
        Integ["Integrity"] --- Rollback
        Auth["Authenticity"] --- Injection
    end
```

---

## Common Attack Vectors

### **1. What is a Man-in-the-Middle (MITM) attack in OTA?**

**Answer:** An attack where the adversary inserts themselves between the OEM backend and the vehicle to intercept or modify the communication.

**Explanation:**
In a MITM scenario, the attacker can:
*   Read telemetry (Eavesdropping).
*   Block the update from reaching the car (DoS).
*   Deliver a modified (malicious) software package (Injection).

### **2. How does a "Rollback Attack" harm a vehicle?**

**Answer:** It forces an ECU to "downgrade" to an older software version that contains known, previously fixed security vulnerabilities.

**Explanation:**
Even if the current software is secure, an attacker might force the car back to a version from a year ago that they know how to exploit. This effectively nullifies the progress made by security patches.

---

## Denial and Eavesdropping

### **3. Why is a Denial of Service (DoS) attack against update servers dangerous?**

**Answer:** It prevents the OEM from deploying critical safety or security patches to the fleet during an active threat.

**Explanation:**
If an OEM discovers a zero-day exploit and tries to push a fix, a DoS attack on their servers can keep millions of vehicles vulnerable for days, giving hackers time to exploit the vehicles.

### **4. Can an attacker "Steal" software via OTA?**

**Answer:** Yes, via Eavesdropping.

**Explanation:**
By intercepting the download stream, an attacker can extract the binary files. They might then reverse-engineer the code to steal intellectual property or find new bugs to exploit later.

---

## Malicious Injection

### **5. What is "Firmware Tampering"?**

**Answer:** Modifying a legitimate firmware binary to include malicious code, like a backdoor or a virus, before it is installed on the vehicle.

**Explanation:**
The goal of tampering is to maintain a "normal" appearance so the system doesn't detect the change. Secure OTA systems use Digital Signatures to detect if even a single bit of the file has been altered.

### **6. How can an attacker bypass "User Consent"?**

**Answer:** By compromising the HMI or the mobile app, an attacker could simulate a user's "Accept" click or disable the prompt entirely, allowing for "silent" malicious updates.

**Explanation:**
Because the HMI is often part of the infotainment system (which has a larger attack surface), it is a prime target for bypassing the manual step of update authorization.

### **7. What is an "Eavesdrop" attack in the context of OTA, and why is it dangerous even if no code is modified?**

**Answer:** It is the passive interception of update traffic. It's dangerous because it allows attackers to steal proprietary logic (IP) and discover secrets or "keys" accidentally left in the firmware.

**Explanation:**
Knowledge is power. By reading the update, an attacker learns the vehicle's architecture and can perform "offline" reverse engineering to find vulnerabilities without alerting the OEM.

### **8. Explain the "Rollback Attack" and why it's a major threat to vehicle safety.**

**Answer:** A rollback attack tricks the ECU into re-installing old software. It's a threat because it re-opens security holes that were already closed, making the vehicle vulnerable to "old" hacks.

**Explanation:**
Attackers use this to bypass the latest security measures. If they can't break the new version, they just go back to an old version they *can* break.

### **9. How does an "Injection Attack" differ from a "Denial of Service" (DoS) attack?**

**Answer:** Injection is an attack on *Integrity* (changing the code), whereas DoS is an attack on *Availability* (stopping the service).

**Explanation:**
*   **DoS:** "You can't have the update."
*   **Injection:** "Here is a 'fake' update that gives me control of your car."
Injection is generally considered much more severe as it leads to total system compromise.
