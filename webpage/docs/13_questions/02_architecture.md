# OTA Architecture Questions

## Vehicle State and Preconditions

### **1. What is the primary difference between Drivable and Non-Drivable updates?**

Answer: Drivable updates can be installed while the vehicle is in operation (often in the background), whereas Non-Drivable updates require the vehicle to be stationary and non-operable.

Explanation:
**Drivable updates** typically involve infotainment bug fixes or app updates that do not affect safety-critical systems. They can often be installed in the background or with minimal user intervention.
**Non-Drivable updates** affect safety-critical systems (e.g., powertrain, engine control) and require strict safety conditions, such as the vehicle being parked, engine off, and battery sufficiently charged, as the update process might disable critical functions temporarily.

### **2. What are the critical preconditions that must be checked before a Non-Drivable update?**

Answer: Vehicle not running, stable power supply/sufficient battery, and healthy ECU status (no active faults).

Explanation:
Before initiating a non-drivable update, the system must validate:
*   **Vehicle State:** The vehicle must be stationary and the engine/motor switched off.
*   **Power:** The battery must have sufficient charge (SoC) and voltage stability to last through the update process, which can take 15-30 minutes or more.
*   **ECU Health:** Diagnostic checks ensure the target ECUs are essentially healthy and capable of accepting the update, preventing bricking due to pre-existing hardware faults.

## OTA System Components

### **3. What are the three main functional blocks of the OEM Backend in an OTA architecture?**

Answer: Update Management, Device Management, and Campaign Management.

Explanation:
*   **Update Management:** Handles software version control, package creation, and validation.
*   **Device Management:** Maintains the inventory of vehicle hardware, ECU configurations, and software compatibility maps.
*   **Campaign Management:** Orchestrates the deployment of updates to specific groups (fleets) of vehicles, managing scheduling and rollout phases.

### **4. How does the TCU (Telematics Control Unit) function in the OTA process?**

Answer: The TCU acts as the central gateway and coordinator for OTA operations within the vehicle.

Explanation:
The TCU receives update instructions from the OEM backend, downloads the data payloads (via HTTPS), and then coordinates the distribution of these updates to the target ECUs using internal vehicle networks (CAN, Ethernet) and diagnostic protocols (UDS). It also reports status back to the backend.

## Vehicle Architecture Evolution

### **5. Describe the progression of vehicle architecture from Decentralized to Zonal.**

Answer: Decentralized -> Domain-Based -> Zonal Architecture.

Explanation:
*   **Decentralized:** Unstructured network of independent ECUs added as needed, leading to complex wiring and maintenance issues.
*   **Domain-Based:** ECUs grouped by function (e.g., Powertrain, Infotainment) under a Domain Controller, improving modularity.
*   **Zonal Architecture:** ECUs grouped by physical location (Zones) connected to Zonal Gateways and central High Performance Computers (HPCs), significantly reducing wiring harness weight and enabling centralized software management.

### **6. What is the role of High Performance Computers (HPCs) in modern Zonal Architectures?**

Answer: HPCs serve as the centralized "brain" of the vehicle, executing complex, compute-intensive workloads.

Explanation:
Unlike traditional microcontrollers that handle specific low-level tasks, HPCs use powerful microprocessors to handle data-heavy applications like ADAS perception, sensor fusion, and autonomous driving decision-making. In a Zonal architecture, they connect to Zonal Gateways via high-speed Ethernet to process aggregated data from the vehicle's zones.
