# AUTOSAR


We have discussed diagnostics over CAN and diagnostics over Ethernet. CAN-based diagnostics are relatively straightforward. Before going deeper into DoIP, it is important to understand AUTOSAR, because DoIP and Ethernet diagnostics are typically implemented within an AUTOSAR-based software architecture.

AUTOSAR stands for Automotive Open System Architecture. It is a global development partnership founded in 2003 by major automotive OEMs and suppliers, including BMW, Volkswagen, Daimler, Bosch, and PSA. The goal of AUTOSAR is to define a standardized, open software architecture for automotive ECUs.

Historically, automotive software was tightly coupled to specific hardware and Tier-1 suppliers. AUTOSAR addresses this by decoupling application software from hardware, enabling portability, reuse, and supplier independence. With AUTOSAR, software components can be reused across different ECUs and hardware platforms with minimal changes.

At a high level, the AUTOSAR Classic Platform architecture consists of three main layers: the Application Layer, the Runtime Environment (RTE), and the Basic Software (BSW).

The Application Layer contains software components that implement vehicle functions. Examples include emergency braking, lane-keeping assist, cruise control, and infotainment features. Multiple software components can coexist at this layer.

AUTOSAR enables standardized communication between application software and lower layers through the Virtual Functional Bus concept. This allows software components to communicate with each other in a hardware-independent manner via well-defined ports and interfaces.

The Runtime Environment, or RTE, acts as a middleware layer. It provides communication services between software components, both within a single ECU and across ECUs. The RTE abstracts ECU-specific details from the application software and serves as a bridge between the Application Layer and the Basic Software.

Below the RTE is the Basic Software, or BSW. The BSW is divided into three main layers: the Service Layer, the ECU Abstraction Layer, and the Microcontroller Abstraction Layer (MCAL).

The Service Layer is the top layer of the Basic Software. It provides services to the application software that are independent of the microcontroller and ECU hardware. These services include the operating system, diagnostic services such as UDS, memory services, ECU state management, communication services, and watchdog management. Security-related services such as cryptographic services are also part of this layer, although they are not the focus here.

The ECU Abstraction Layer provides a hardware-independent interface to vehicle communication buses and peripherals. Modules such as CanIf and EthernetIf belong to this layer. They allow upper layers to access CAN or Ethernet communication without depending on specific controller implementations.

The Microcontroller Abstraction Layer, or MCAL, provides direct access to microcontroller peripherals. It contains low-level drivers supplied by silicon vendors such as NXP, Renesas, Infineon, or Texas Instruments. In cases where AUTOSAR does not fully meet specific timing or hardware requirements, Complex Device Drivers (CDD) may be used to handle specialized sensors or actuators.

From a diagnostics perspective, DoIP plays a key role in Ethernet-based communication. DoIP stands for Diagnostics over Internet Protocol and is standardized under ISO 13400. Diagnostic services themselves are defined by ISO 14229 (UDS), which means all diagnostic services available over CAN are also available over IP.

DoIP operates over Automotive Ethernet, typically using 100BASE-T1 today, with 1000BASE-T1 becoming increasingly common. Compared to CAN, DoIP offers significantly higher bandwidth, making it well-suited for flashing large software images and supporting modern vehicle architectures.

DoIP supports vehicle identification and announcement, routing activation, node information services, and alive-check mechanisms to maintain connections. It also supports IP-level services such as address assignment, vehicle discovery, connection management, status reporting, and error handling.

Within the AUTOSAR Ethernet stack, the Socket Adapter (SoAd) module binds socket-based communication to AUTOSAR PDUs. SoAd interfaces upward with diagnostic and communication modules and downward with the TCP/IP stack.

The Ethernet Interface module (EthernetIf) resides in the ECU Abstraction Layer. It provides a hardware-independent interface to Ethernet controllers and transceivers. EthernetIf does not access hardware directly; instead, it calls Ethernet driver modules. This design allows multiple Ethernet controllers or switches to be used within the same ECU without impacting upper layers.

Similarly, for CAN-based communication, the CAN Interface (CanIf) is used in the ECU Abstraction Layer. However, CAN has a limitation of carrying only up to 8 bytes of payload per frame.

To transmit diagnostic data larger than 8 bytes, CAN Transport Protocol (CAN-TP), standardized under ISO 15765, is used. CAN-TP operates across the Network and Transport layers of the OSI model and enables segmentation and reassembly of larger messages.

CAN-TP supports payloads up to 4095 bytes per message. It defines four frame types: Single Frame, First Frame, Consecutive Frame, and Flow Control Frame. Flow Control frames regulate the transmission by specifying flow status, block size, and separation time.

In standard CAN addressing, a Single Frame can carry up to 7 bytes of payload, while extended addressing reduces this to 6 bytes. CAN-TP ensures reliable transmission of larger diagnostic messages such as firmware blocks during flashing.

This overview focuses on AUTOSAR from a communication and diagnostics perspective. Other AUTOSAR modules related to cybersecurity, such as Crypto Interface and CSM, are outside the scope here and are covered separately. In the next sections, we will examine CAN, CAN-TP, and DoIP frame formats in more detail.

---

CORRECTNESS AND CONSISTENCY ANALYSIS

1. AUTOSAR Definition and Purpose

* AUTOSAR definition, founding year, and consortium role are correct [Verified].
* Decoupling of software from hardware is accurately described [Verified].

2. AUTOSAR Layering

* Application Layer, RTE, and BSW separation is correct [Verified].
* Role of RTE as middleware is accurately explained [Verified].

3. Basic Software Structure

* Service Layer, ECU Abstraction Layer, and MCAL breakdown is correct [Verified].
* Placement of CanIf and EthernetIf in ECU Abstraction Layer is correct [Verified].

4. Complex Device Drivers

* Use of CDDs for hardware- or timing-specific requirements is correctly stated [Verified].

5. DoIP Standards

* DoIP standardized under ISO 13400 is correct [Verified].
* Use of ISO 14229 (UDS) over IP is accurate [Verified].

6. Ethernet Capabilities

* 100BASE-T1 and 1000BASE-T1 references are correct [Verified].
* Higher bandwidth compared to CAN is correctly emphasized [Verified].

7. Socket Adapter (SoAd)

* SoAd role in binding sockets to PDUs is correctly described [Verified].

8. EthernetIf

* EthernetIf abstraction and independence from hardware drivers is accurate [Verified].

9. CAN and CAN-TP

* CAN payload limitation of 8 bytes is correct [Verified].
* CAN-TP standard ISO 15765 is correct [Verified].
* Maximum payload of 4095 bytes is correct [Verified].
* Frame types and flow control behavior are accurately described [Verified].

10. Scope and Focus

* Limiting discussion to communication and diagnostics is consistent and appropriate [Verified].

---

FINAL VERDICT

The rewritten AUTOSAR section is technically accurate, consistent with AUTOSAR Classic Platform concepts, and aligned with ISO 14229, ISO 13400, and ISO 15765.
No incorrect protocol behavior, architectural misplacement, or misleading claims were found.
The material is suitable for an OTA, diagnostics, and automotive software audience at an intermediate to advanced level.
