# OTA Security Questions (Attacks)

## Attack Surface & Definitions

### **1. What are the three main components of the OTA attack surface?**

Answer: The **OEM Backend**, the **Communication Channel** (Network), and the **Vehicle** (TCU/ECUs).

### **2. Which element of the CIA Triad does an "Eavesdropping" attack target?**

Answer: **Confidentiality.**

Explanation:
Eavesdropping is a *passive* attack where the adversary intercepts traffic to steal intellectual property (firmware algorithms) or secrets (keys/passwords), but does not modify the data.

## Specific Attack Vectors

### **3. Why is a Denial of Service (DoS) attack dangerous in the context of OTA, even if it doesn't modify the software?**

Answer: It targets **Availability**, preventing the vehicle from receiving critical security patches.

Explanation:
By blocking or jamming the update signal, an attacker keeps the vehicle running vulnerable, outdated software, extending the window of opportunity for other exploits.

### **4. Describe a "Rollback Attack" and why it is a significant threat.**

Answer: An attack where the vehicle is tricked into installing an older, legitimate (signed) firmware version.

Explanation:
It is dangerous because it re-introduces known vulnerabilities that were fixed in newer versions. Attackers downgrade the software to a version they know how to exploit.

### **5. What is the goal of a "Malicious Injection" attack?**

Answer: To compromise **Authenticity and Integrity** by inserting unauthorized code into the vehicle.

Explanation:
The attacker intercepts the OTA process and replaces the legitimate firmware with a malicious version. If successful, this can grant full remote control over the vehicle or disable safety systems.

## Frameworks

### **6. How does the Uptane framework categorize OTA threats?**

Answer: It categorizes them by attacker goals, such as "Read Updates" (Eavesdropping), "Deny Installation" (DoS), and "Deny Functionality" (Bricking/Malware).
