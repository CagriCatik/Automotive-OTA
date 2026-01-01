# OTA Use Cases Questions

## Smart Maintenance & Remote Diagnostics

### **1. How does "Remote Diagnostics" shift the vehicle maintenance paradigm?**

Answer: It moves from a "Reactive" model (wait for breakdown/warning light) to a "Proactive/Predictive" model.

Explanation:
Instead of waiting for a driver to report an issue, the vehicle continuously sends telemetry to the cloud. The cloud analyzes this data to detect anomalies (e.g., battery health degradation, starter motor voltage drop) *before* a failure occurs, allowing the OEM to notify the customer to schedule service proactively.

### **2. What is the role of the "Digital Twin" in predictive maintenance?**

Answer: It provides a virtual cloud-based replica of the vehicle's state for simulation and analysis.

Explanation:
The Digital Twin mirrors the physical vehicle's status (telemetry, software versions, component health). Machine Learning algorithms run on this digital twin in the cloud to simulate stress tests or predict wear and tear without affecting the physical vehicle's operation.

## Features on Demand (FoD)

### **3. What is "Features on Demand" (FoD) and what business models does it enable?**

Answer: FoD allows enabling software-locked hardware capabilities via OTA updates. Business models include:
*   **Subscriptions:** Monthly fee for features like Live Traffic or Heated Seats.
*   **One-Time Purchase:** Permanently unlocking a feature (e.g., Full Self-Driving).
*   **Micro-transactions/Temporary:** "Weekend mode" or temporary performance boosts.

### **4. From a technical security perspective, how is a paid feature enabled on a specific vehicle?**

Answer: By installing a digitally signed **"Entitlement Certificate"** into the vehicle's Secure Keystore (HSM).

Explanation:
When a user buys a feature, the OEM backend generates a license certificate containing the feature ID (e.g., `HEATED_SEATS`) and the specific VIN, signed with the OEM's private key. The OTA Manager downloads this certificate to the vehicle's HSM. Validating the signature ensures that features cannot be cracked or enabled without payment.

## Remote Commands

### **5. Describe the security flow for a Remote Command (e.g., "Unlock Door") from a mobile app.**

Answer: Mobile App authentication (OAuth2) + End-to-End Command Signing.

Explanation:
1.  **User Auth:** The user logs in via the App using OAuth2/OpenID Connect to get a secure token.
2.  **Command Auth:** The command sent to the vehicle is digitally signed by the backend. The vehicle's TCU verifies this signature before executing the command (e.g., unlocking doors) to prevent unauthorized replay or man-in-the-middle attacks.
