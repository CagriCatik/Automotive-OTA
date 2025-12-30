# Introduction

## Why OTA security matters in vehicles

Automotive software complexity has grown sharply (more ECUs, more code, more connectivity, more backend services). OTA updates are now a primary way to patch vulnerabilities and ship features, but they also create a large, distributed attack surface: backend repositories, distribution infrastructure, cellular/Wi-Fi links, and in-vehicle update clients.

Regulatory and industry guidance explicitly treats the "update process" as a security-critical function. UNECE WP.29 threat/mitigation material includes threats such as compromise of OTA update procedures (fabricated firmware) and denial-of-service against update servers or networks, and calls for secure software update procedures and key protection. ([UNECE][1])

A practical and widely cited OTA security model for automotive is Uptane. Uptane documents attacker capabilities (intercept/modify traffic; compromise repositories; compromise ECUs) and enumerates update-related threats in categories like reading updates, denying installation, replaying old bundles, and more. ([Uptane][2])

---

## Core attack classes in OTA (high-level)

The transcript lists four fundamental OTA attack categories. These map cleanly to common OTA threat models (including Uptane) and to typical firmware/OTA security literature.

### 1) Eavesdrop attack (confidentiality breach)

Goal: Passively read OTA traffic to extract sensitive or proprietary information from an update or its metadata.

Uptane explicitly describes an "Eavesdrop attack" as reading sensitive/confidential information from an update intended to be encrypted for a specific ECU. ([Uptane][2])

What is at risk:

* Proprietary firmware logic and IP
* Embedded secrets accidentally present in images
* Update structure that helps attackers craft later attacks

### 2) Denial of Service (DoS) against updates (availability loss)

Goal: Prevent installation of updates (or make it impractically slow), leaving vehicles unpatched and potentially unsafe.

Uptane lists multiple "deny installation" strategies including blocking traffic, slowing retrieval, replaying old bundles, blocking selected updates, and DoS against update infrastructure. ([Uptane][2])
UNECE WP.29 material includes "Denial of Service attack against update server or network" as an update-process threat. ([UNECE][1])

What is at risk:

* Delayed security patches (extended vulnerability window)
* Fleet fragmentation (some vehicles updated, others stuck)
* Operational disruption if update is mandatory for functions/features

### 3) Rollback (downgrade) of software version (integrity/safety regression)

Goal: Force the ECU to install an older, vulnerable firmware version to re-enable known exploits.

Firmware rollback protection is a common requirement in secure update systems; without it, attackers can reintroduce old vulnerabilities by downgrading. This is discussed in OTA security guidance and research on FOTA/downgrade attacks. ([MDPI][3])

What is at risk:

* Re-exposure of fixed CVEs
* Safety/function regressions if old logic returns
* Bypassing security posture improvements shipped in newer releases

### 4) Malicious software injection via OTA (authenticity failure)

Goal: Deliver and install attacker-controlled firmware by compromising repositories, credentials/keys, or update transport.

Automotive OTA threat discussions commonly include malicious update injection (compromise servers or intercept communications to distribute malware) and update tampering. ([Hermes Solution - 헤르메스솔루션][4])
UNECE WP.29 update-process threats include fabrication of firmware / compromise of OTA update procedures, and emphasizes secure update procedures and cryptographic key protection. ([UNECE][1])

What is at risk:

* Remote code execution inside ECUs
* Persistence and lateral movement across in-vehicle networks
* Safety-critical function manipulation

---

## How these attacks relate (the "chain" view)

These attacks are not isolated:

* Eavesdropping can reveal update structure and operational details that make later active attacks easier. Uptane explicitly separates "read updates" threats from "deny installation" threats, indicating distinct attacker goals and capabilities. ([Uptane][2])
* DoS extends the time window during which known vulnerabilities remain exploitable by blocking patches. ([Uptane][2])
* Rollback and malicious injection both target integrity/authenticity, often exploiting weak version enforcement, weak key management, or repository compromise. ([MDPI][3])

---

## What follows in a complete OTA security section

A structured OTA security chapter typically progresses from:

1. Threats (this section): eavesdrop, DoS, rollback, malicious injection
2. Security objectives: confidentiality, integrity, authenticity, availability, non-repudiation/auditability
3. Controls mapped to objectives:

   * Encryption and secure transport (confidentiality)
   * Signatures, hashes, signed metadata (integrity/authenticity)
   * Anti-rollback policies (integrity over time)
   * Resilience controls and infrastructure hardening (availability)
4. Formal frameworks/regulatory alignment (e.g., Uptane; UNECE R155/R156 update-process mitigations)

Uptane is specifically useful as it provides a concrete threat model and enumerated attacks aligned with OTA realities. ([Uptane][2])

[1]: https://unece.org/sites/default/files/2022-05/ECE_TRANS_WP.29_2022_60E.pdf?utm_source=chatgpt.com "United Nations"
[2]: https://uptane.org/papers/uptane-standard.1.1.0.pdf?utm_source=chatgpt.com "Uptane Standard for Design and Implementation"
[3]: https://www.mdpi.com/2079-9292/14/10/2034?utm_source=chatgpt.com "Threat Classification and Vulnerability Analysis on 5G Firmware Over-the-Air Updates for Mobile and Automotive Platforms"
[4]: https://www.hermessol.com/2025/04/28/blog_250404/?utm_source=chatgpt.com "ISO 21434: Connected Car OTA Security - Hermes Solution"
