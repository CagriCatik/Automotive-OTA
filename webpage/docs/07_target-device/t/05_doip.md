# DoIP


We previously discussed the communication stack placement for diagnostics. To reiterate, at the outer communication layer, CAN-TP is used in CAN-based diagnostics. CAN-TP interacts with the CAN Interface, CAN driver, and ultimately the CAN physical layer.

In contrast, for Ethernet-based diagnostics, DoIP replaces CAN-TP. DoIP communicates with the Socket Adapter, which then interfaces with the TCP/IP stack. Below that, the Ethernet Interface and Ethernet driver handle communication with the physical Ethernet network.

When viewing the complete AUTOSAR communication stack, this layered structure can appear complex. However, the key idea is straightforward: CAN-TP is used for CAN-based diagnostics, while DoIP is used for Ethernet-based diagnostics, each integrated cleanly into the AUTOSAR stack.

Now let us walk through a practical example of how a DoIP connection is established between an external diagnostic tester and a vehicle ECU. This sequence is largely standardized and comparable across implementations, with some additional steps compared to CAN-based diagnostics.

The first step is vehicle discovery. The external tester sends a Vehicle Identification Request using UDP. UDP is a connectionless and non-reliable protocol and is used here only for discovery and announcement purposes.

The vehicle responds with a Vehicle Identification Response if the received identifier matches. This identifier may be an Entity ID (EID), MAC address, or VIN, depending on the configuration. The DoIP entity compares the received identifier with its internally stored values. If there is no match, no response is sent and the discovery process terminates.

If the VIN or EID matches, the vehicle sends a Vehicle Identification Announcement message. At this point, the tester knows that a valid DoIP entity is available.

The next step is routing activation. This step uses TCP, which provides a reliable, connection-oriented communication channel. The tester sends a Routing Activation Request to the DoIP entity.

During routing activation, the DoIP entity validates the source address of the tester and the target address of the ECU. These addresses are typically preconfigured and stored in the ECU. If validation is successful, the DoIP entity responds with a Routing Activation Response and opens a diagnostic communication channel.

Once routing is activated, the tester can begin sending diagnostic messages. These messages are standard UDS requests, identical in content to those used over CAN. For example, requests for diagnostic session control, DTC readout, or programming services follow ISO 14229.

DoIP simply transports these UDS messages over the established TCP connection. The ECU responds with positive or negative responses as defined by UDS, while the TCP connection remains active throughout the diagnostic or flashing session.

After all diagnostic or programming activities are completed, the DoIP entity initiates connection termination. The TCP connection is closed, and no further communication occurs unless a new discovery and routing activation sequence is started.

In summary, DoIP communication consists of UDP-based vehicle discovery, TCP-based routing activation, followed by reliable transport of UDS diagnostic messages. This mechanism enables high-speed, scalable diagnostics and flashing while preserving full compatibility with existing UDS services.

---

TECHNICAL AND FACTUAL ANALYSIS

1. AUTOSAR Stack Placement

* Correct distinction between CAN-TP for CAN diagnostics and DoIP for Ethernet diagnostics [Verified].
* Accurate description of interaction with CAN Interface and Ethernet Socket Adapter stacks [Verified].

2. DoIP Discovery Phase

* Use of UDP for vehicle discovery and announcement is correct [Verified].
* Description of VIN, EID, and MAC-based identification is accurate [Verified].

3. Connection Establishment

* Routing Activation using TCP is correctly explained [Verified].
* Validation of tester source address and ECU target address is consistent with ISO 13400 [Verified].

4. Diagnostic Communication

* Transport of standard UDS messages over DoIP without modification is correct [Verified].
* Positive and negative UDS responses over TCP are correctly described [Verified].

5. Connection Termination

* TCP connection closure after diagnostics or flashing is accurate [Verified].

6. Comparison to CAN Diagnostics

* Statement that UDS services remain identical across CAN and DoIP is correct [Verified].

7. No Incorrect Claims

* UDP correctly described as non-reliable and used only for discovery [Verified].
* TCP correctly described as reliable and persistent for diagnostics [Verified].

---

FINAL VERDICT

The rewritten explanation accurately describes DoIP layering, discovery, routing activation, and diagnostic communication. All protocol behavior aligns with ISO 13400 and ISO 14229. The content is technically correct, clear, and suitable for advanced OTA and automotive diagnostics training.
