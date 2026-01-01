# OTA Architecture Questions

This section explores the structural components of an OTA system, focusing on vehicle state management, backend functional blocks, and the evolution of vehicle electronic architectures.

```kroki-mermaid {display-width=700px display-align=center}
graph TD
    subgraph OEM_Backend["OEM Backend"]
        UM[Update Management]
        DM[Device Management]
        CM[Campaign Management]
    end

    subgraph Vehicle["Vehicle Domain"]
        TCU[Telematics Control Unit / Gateway]
        OM[OTA Manager]
        E1[Target ECU 1]
        E2[Target ECU 2]
    end

    UM --- CM
    DM --- CM
    CM -- "Instructions (MQTT)" --> TCU
    TCU -- "Status (MQTT)" --> CM
    TCU -- "Package (HTTPS)" --- UM
    TCU --- OM
    OM --- E1
    OM --- E2
```

---

## Vehicle State and Preconditions

### **1. What is the primary difference between Drivable and Non-Drivable updates?**

**Answer:** Drivable updates can be installed while the vehicle is in operation (often in the background), whereas Non-Drivable updates require the vehicle to be stationary and non-operable.

**Explanation:**

- **Drivable updates** typically involve infotainment bug fixes or app updates that do not affect safety-critical systems. They can often be installed in the background or with minimal user intervention.
- **Non-Drivable updates** affect safety-critical systems (e.g., powertrain, engine control) and require strict safety conditions, such as the vehicle being parked, engine off, and battery sufficiently charged, as the update process might disable critical functions temporarily.

### **2. What are the critical preconditions that must be checked before a Non-Drivable update?**

**Answer:** Vehicle not running, stable power supply/sufficient battery, and healthy ECU status (no active faults).

**Explanation:**

Before initiating a non-drivable update, the system must validate:

- **Vehicle State:** The vehicle must be stationary and the engine/motor switched off.
- **Power:** The battery must have sufficient charge (SoC) and voltage stability to last through the update process, which can take 15-30 minutes or more.
- **ECU Health:** Diagnostic checks ensure the target ECUs are essentially healthy and capable of accepting the update, preventing bricking due to pre-existing hardware faults.

---

## OTA System Components

### **3. What are the three main functional blocks of the OEM Backend in an OTA architecture?**

**Answer:** Update Management, Device Management, and Campaign Management.

**Explanation:**

- **Update Management:** Handles software version control, package creation, and validation.
- **Device Management:** Maintains the inventory of vehicle hardware, ECU configurations, and software compatibility maps.
- **Campaign Management:** Orchestrates the deployment of updates to specific groups (fleets) of vehicles, managing scheduling and rollout phases.

### **4. How does the TCU (Telematics Control Unit) function in the OTA process?**

**Answer:** The TCU acts as the central gateway and coordinator for OTA operations within the vehicle.

**Explanation:**
The TCU receives update instructions from the OEM backend, downloads the data payloads (via HTTPS), and then coordinates the distribution of these updates to the target ECUs using internal vehicle networks (CAN, Ethernet) and diagnostic protocols (UDS). It also reports status back to the backend.

---

## Vehicle Architecture Evolution

### **5. Describe the progression of vehicle architecture from Decentralized to Zonal.**

**Answer:** Decentralized -> Domain-Based -> Zonal Architecture.

**Explanation:**

- **Decentralized:** Unstructured network of independent ECUs added as needed, leading to complex wiring and maintenance issues.
- **Domain-Based:** ECUs grouped by function (e.g., Powertrain, Infotainment) under a Domain Controller, improving modularity.
- **Zonal Architecture:** ECUs grouped by physical location (Zones) connected to Zonal Gateways and central High Performance Computers (HPCs), significantly reducing wiring harness weight and enabling centralized software management.

### **6. What is the role of High Performance Computers (HPCs) in modern Zonal Architectures?**

**Answer:** HPCs serve as the centralized "brain" of the vehicle, executing complex, compute-intensive workloads.

**Explanation:**
Unlike traditional microcontrollers that handle specific low-level tasks, HPCs use powerful microprocessors to handle data-heavy applications like ADAS perception, sensor fusion, and autonomous driving decision-making. In a Zonal architecture, they connect to Zonal Gateways via high-speed Ethernet to process aggregated data from the vehicle's zones.

---

## Backend-to-Vehicle Interaction

### **7. What role does the "OTA Manager" logical component play?**

**Answer:** The OTA Manager orchestrates vehicle-side activities, ensuring proper sequencing and validation of update steps.

**Explanation:**
While the TCU provides connectivity, the OTA Manager is the logic core that validates update packages, manages the update execution sequence (e.g., updating ECU A before ECU B), and handles error conditions or rollbacks if something goes wrong during the process.

### **8. Why is HTTPS used alongside MQTT in OTA architectures?**

**Answer:** MQTT is used for lightweight control signaling, while HTTPS is used for secure and efficient transfer of large software packages.

**Explanation:**

- **MQTT** is ideal for real-time status reporting and update triggers because it uses minimal bandwidth.
- **HTTPS** is better suited for bulk data transfer, providing high reliability and security for large binary files.

### **9. What is the difference between Single Bank and Dual Bank updates for the TCU?**

**Answer:** Single-bank updates require the system to be offline during flashing, while dual-bank updates allow the system to remain operational while the update is downloaded to an inactive partition.

**Explanation:**

- **Single-bank:** Simplier but riskier; if the update fails, the device might become inoperable.
- **Dual-bank:** Enables seamless updates and provides a safe rollback path by keeping the previous software version in one bank while updating the other.

