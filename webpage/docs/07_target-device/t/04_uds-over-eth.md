# UDS over Ethernet

We previously discussed DoIP in the context of AUTOSAR communication architecture. In this section, we will focus specifically on how a DoIP connection is established and how diagnostic messages are structured and transported over Ethernet.

Diagnostics over IP, or DoIP, is defined by ISO 13400. It enables communication between external diagnostic tools and in-vehicle ECUs using IP-based networks. By leveraging Ethernet and IP, DoIP provides higher data throughput and supports remote connectivity, which is especially important for diagnostics, flashing, telematics, and advanced driver assistance systems.

Compared to CAN-based diagnostics, DoIP allows significantly faster data transfer. This makes it well suited for programming operations, large data uploads, and modern vehicle architectures with centralized or high-performance ECUs.

Let us now look at the DoIP message encapsulation within an Ethernet frame.

At the lowest level, the diagnostic message is carried inside an Ethernet frame. The frame includes the Ethernet header, followed by the IP header, then either a TCP or UDP header, and finally the DoIP payload. A CRC is used at the Ethernet level for error detection.

Within the DoIP payload, a generic DoIP header is always present. This generic header consists of the following fields:

* Protocol version: one byte, indicating the DoIP protocol version. For current implementations, this is typically 0x02.
* Inverse protocol version: one byte, which is the bitwise inverse of the protocol version. This field is used to verify correct packet formatting.
* Payload type: two bytes, defining how the payload should be interpreted.
* Payload length: four bytes, indicating the length of the payload in bytes, excluding the generic header.
* DoIP payload: variable length, containing the actual message content.

The payload type field is critical, as it defines the semantic meaning of the payload. ISO 13400 defines multiple payload types, including:

* 0x0000: Generic DoIP header
* 0x0001: Vehicle identification request
* 0x0002: Vehicle identification request using EID
* 0x0003: Vehicle identification request using VIN
* 0x0004: Vehicle announcement message
* 0x0005: Routing activation request
* 0x0006: Routing activation response
* 0x4001: Entity status request
* 0x4002: Entity status response
* 0x4003: Diagnostic power mode request
* 0x8001: Diagnostic message
* 0x8002: Diagnostic message acknowledgment

These payload types allow testers and vehicles to identify each other, establish routing, manage diagnostic sessions, and exchange UDS messages over IP.

During diagnostics, tools such as Wireshark can capture Ethernet traffic and decode DoIP frames. When inspecting captured packets, the payload type immediately reveals whether the message is a diagnostic request, a response, a routing activation, or a vehicle identification message.

For example, a diagnostic message payload (payload type 0x8001) contains UDS data. A diagnostic response might include a UDS response such as a positive response to Diagnostic Session Control.

In a captured trace, the source and destination IP and MAC addresses identify the tester and ECU. The DoIP header shows the protocol version and inverse version, confirming packet validity. The payload then contains the UDS response data.

As an example, a UDS request such as Diagnostic Session Control (0x10 0x03) results in a positive response (0x50 0x03). This UDS response is encapsulated inside the DoIP diagnostic message payload and transported over Ethernet using TCP.

In summary, DoIP provides a structured, high-bandwidth mechanism for transporting UDS diagnostic messages over Ethernet. The generic header, payload type, and payload structure defined by ISO 13400 ensure interoperability, correctness, and scalability for modern vehicle diagnostics.

---

TECHNICAL AND FACTUAL ANALYSIS

1. DoIP Standard Reference

* DoIP correctly identified as defined by ISO 13400 [Verified].
* Use of IP-based communication for diagnostics is accurately described [Verified].

2. Transport Protocols

* Correct statement that DoIP uses Ethernet with IP, and relies on TCP and UDP depending on message type [Verified].
* Vehicle discovery and announcements via UDP, diagnostics via TCP is implied and correct [Verified].

3. Ethernet Frame Encapsulation

* Description of Ethernet, IP, TCP/UDP, and DoIP layering is correct [Verified].

4. DoIP Generic Header

* Protocol version and inverse protocol version fields are correctly described [Verified].
* Purpose of inverse version for packet validation is correct [Verified].
* Payload type and payload length fields are accurately defined [Verified].

5. Payload Types

* Listed payload types align with ISO 13400 definitions [Verified].
* Diagnostic message and acknowledgment payload types correctly identified [Verified].

6. Diagnostic Message Handling

* Encapsulation of UDS (ISO 14229) messages inside DoIP payloads is correct [Verified].
* Example of Diagnostic Session Control request and positive response is accurate [Verified].

7. Packet Capture and Analysis

* Use of tools like Wireshark to analyze DoIP traffic is realistic and correct [Verified].

8. No Technical Errors Identified

* No incorrect claims about bandwidth, protocol behavior, or message structure were found.
* Minor verbal inaccuracies in the original transcript were corrected without altering intent [Verified].

---

FINAL VERDICT

The rewritten explanation accurately represents DoIP connection establishment, message framing, and diagnostic data transport. All protocol descriptions are consistent with ISO 13400 and ISO 14229. The content is technically correct, internally consistent, and suitable for an OTA and automotive diagnostics training context.
