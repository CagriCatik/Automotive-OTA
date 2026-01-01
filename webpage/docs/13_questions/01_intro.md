# Introduction

## Vehicle Architecture and Communication

### **1. What is the need for Zonal architecture?**

Answer: All of the above

Explanation:
Zonal architecture is necessary for multiple reasons:

* Managing increasing vehicle complexity -- Modern vehicles have numerous ECUs performing various tasks, and a zonal architecture helps optimize their management.
* Reducing vehicle architecture constraints -- By grouping ECUs into zones, it simplifies wiring, reduces weight, and enhances modularity.
* Efficient OTA (Over-the-Air) updates -- Centralized computing using HPCs enables scalable and reliable software updates.

Therefore, the correct answer is All of the above.

### **2. Which is the most widely used communication medium between HPC and gateway?**

Answer: Automotive Ethernet

Explanation:
Automotive Ethernet is the dominant backbone for HPC-gateway communication because it provides:

* High bandwidth required for OTA payloads and sensor data
* Low latency and deterministic behavior
* Native support for IP-based and service-oriented architectures

CAN and FlexRay are insufficient for HPC-level data throughput and scalability.


### **3. Is Zonal architecture designed only for OTA?**

Answer: False

Explanation:
Zonal architecture is a foundational enabler for software-defined vehicles, not an OTA-only concept. It supports:

* ECU consolidation
* Wiring harness reduction
* Centralized diagnostics
* Power and energy optimization
* Service-oriented communication models

OTA is a major beneficiary, but not the primary or sole purpose.

## OTA Concepts and Deployment Strategy

### **4. What is the meaning of campaign in OTA?**

Answer: Deploy software updates to group of vehicle variants (set of different ECUs)

Explanation:
An OTA campaign defines the controlled rollout of software updates across a selected vehicle population. It specifies:

* Target vehicle variants
* Target ECUs and software versions
* Rollout rules such as staged or phased deployment

Campaigns ensure safe, traceable, and manageable OTA delivery.


### **5. What is the purpose of a Mobile App when HMI already exists?**

Answer: All the above

Explanation:
A mobile application complements in-vehicle HMI by enabling:

* Remote update triggering without entering the vehicle
* Centralized control of update actions such as pause, resume, or scheduling
* Real-time notifications and status visibility

This is especially important for EVs during charging scenarios and unattended updates.


## OTA Communication Protocols

### **6. What is the use of MQTT and HTTPS in OTA?**

Answer:
MQTT -- used for controlling the updates
HTTPS -- used to send the actual data (software binaries)

Explanation:
MQTT is lightweight and event-driven, making it ideal for update orchestration, status reporting, and command control.
HTTPS is optimized for secure and reliable transfer of large firmware images, ensuring data integrity and encryption.


## Diagnostics and Flashing Mechanisms


### **7. What is the purpose of a UDS tester?**

Answer: Both A and B

Explanation:
In the UDS protocol (ISO 14229):

* The tester initiates diagnostic services, including flashing software from the TCU or gateway to the target ECU
* Communication follows a strict client-server model where the tester is the client and the ECU is the server

Both aspects define the tester's role.


### **8. What is the purpose of having Dual Bank Flash?**

Answer: Both A and B are correct

Explanation:
Dual-bank flashing provides:

* Ability to download new software while the vehicle is operational
* Reduced downtime and flashing risk

One memory bank runs the active software while the other receives the update. This approach improves safety and availability but consumes additional flash memory.


### **9. What happens if flashing fails in an ECU?**

Answer: Retry of flashing will happen

Explanation:
OTA-capable ECUs implement recovery mechanisms such as:

* Flash retry
* Rollback to last valid software
* Bootloader-controlled recovery

Permanent ECU lockout is considered a design failure in OTA architectures.


## OTA Security


### **10. Is security testing important for any OTA architecture?**

Answer: Highly Required

Explanation:
OTA introduces a permanent external attack surface even after vehicle production. Without security testing, attackers could:

* Inject malicious firmware
* Compromise safety-critical ECUs
* Violate regulatory compliance

Standards such as ISO 21434 and UNECE R155 mandate security validation of OTA interfaces, authentication mechanisms, encryption, and rollback protection.
