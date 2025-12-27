# Software Defined Vehicle (SDV) Architecture

The concept of the "Software Defined Vehicle" implies that the value of the vehicle is defined by its software, not its mechanicals. This transition happens in **5 Levels**.

## Level 1: E/E Adaptation

- **Architecture:** Distributed (CAN Bus hell). 100+ ECUs.
- **Software:** Hard-coded in ROM.
- **OTA:** None. Dealer update only via OBD-II port.
- **Example:** Cars from 2010.

## Level 2: Infotainment OTA (SOTA)

- **Architecture:** Distributed, but with a connected Head Unit.
- **OTA:** Maps and Apps update over Wi-Fi/LTE. No update to brakes/engine.
- **Example:** Early Ford Sync, Audi MMI.

## Level 3: Domain Centralization

- **Architecture:** Domain Controllers (Body, Powertrain, ADAS, Infotainment).
- **OTA:** FOTA (Firmware OTA) possible for nearly all domains.
- **Constraint:** Complexity. Wiring harness is heavy ($50kg$).
- **Example:** BMW iDrive 7, Volkswagen ID.4 (E3 1.1).

## Level 4: Zonal Architecture

- **Architecture:** Organized by **Location**, not function. "Front Left Zone Controller", "Rear Right Zone Controller".
- **Network:** Ethernet Backbone (10Gbps).
- **OTA:** Full vehicle update in <15 minutes.
- **Example:** Tesla Model 3, Rivian R1T.

## Level 5: Central Compute (Cloud Native)

- **Architecture:** One "Car Brain" (HPC) + Dumb Actuators.
- **Software:** Containerized (Docker/K8s on weels).
- **Feature:** **SOAFEE** (Scalable Open Architecture for Embedded Edge).
- **Vision:** The car is just an edge node in the cloud. You develop code in the cloud and deploy it to the car seamlessly.

### The Shift to Services

In L4 and L5, the OEM becomes a software company.

- **App Store:** 3rd party developers build apps for the car.
- **Data Monetization:** Insurers bid for driving data.
- **Hardware capabilities:** Hardware is over-provisioned (e.g., Lidar included but disabled) to be unlocked later.
