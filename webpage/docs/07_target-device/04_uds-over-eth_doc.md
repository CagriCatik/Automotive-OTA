# UDS over Ethernet: DoIP Protocol Architecture and Implementation

Diagnostics over IP (DoIP) represents a significant advancement in vehicle diagnostic communication, transitioning from traditional CAN-based systems to IP-based networks. Defined by ISO 13400, DoIP enables robust communication between external diagnostic tools and in-vehicle ECUs using standard Ethernet and IP protocols. This architectural shift provides substantial benefits including higher data throughput capabilities and support for remote connectivity, making it particularly valuable for diagnostic operations, firmware flashing, telematics applications, and advanced driver assistance systems.

The fundamental advantage of DoIP over CAN-based diagnostics lies in its significantly faster data transfer rates. This enhanced bandwidth makes DoIP exceptionally well-suited for programming operations that require large data uploads, as well as for modern vehicle architectures featuring centralized or high-performance ECUs. The protocol leverages existing IP infrastructure while maintaining the diagnostic semantics established by UDS (Unified Diagnostic Services, ISO 14229), creating a bridge between traditional automotive diagnostics and modern networking technologies.

## DoIP Message Encapsulation Architecture

The DoIP protocol implements a layered encapsulation structure that integrates seamlessly with standard Ethernet networking. At the physical and data link layers, DoIP utilizes conventional Ethernet frames, which include the standard Ethernet header for source and destination MAC addressing, followed by an IP header for network layer routing. The transport layer employs either TCP or UDP protocols depending on the specific message type and communication requirements. The actual DoIP payload resides at the application layer, with error detection handled through the standard Ethernet CRC mechanism.

```kroki-mermaid {display-width=600px display-align=center}
graph TD
    A["Ethernet Frame"] --> B["Ethernet Header"]
    A --> C["IP Header"]
    A --> D["TCP/UDP Header"]
    A --> E["DoIP Payload"]
    E --> F["Generic DoIP Header"]
    E --> G["DoIP Message Content"]
    G --> H["UDS Diagnostic Data"]
    
    style A fill:#e1f5fe
    style E fill:#f3e5f5
    style H fill:#fff3e0
```

This encapsulation structure ensures that DoIP messages can coexist with other network traffic while maintaining clear protocol boundaries. The use of standard networking layers allows DoIP to leverage existing network infrastructure and tools, including packet capture and analysis utilities such as Wireshark. When examining captured packets, the hierarchical structure becomes evident, with each layer's headers providing specific routing and protocol information.

## Generic DoIP Header Structure

Every DoIP message begins with a generic header that provides essential protocol information and ensures proper message interpretation. This header follows a fixed structure consisting of several critical fields that facilitate protocol versioning, message type identification, and payload length specification. The generic header serves as the foundation for all DoIP communication, enabling both diagnostic tools and vehicle ECUs to properly parse and process incoming messages.

The protocol version field occupies one byte and indicates the specific version of the DoIP protocol being used. Current implementations typically utilize version 0x02, representing the standardized version of the protocol. Complementing this is the inverse protocol version field, also one byte in length, which contains the bitwise inverse of the protocol version. This redundancy serves as a validation mechanism, allowing receivers to verify correct packet formatting and detect potential transmission errors or protocol mismatches.

The payload type field spans two bytes and defines how the subsequent payload should be interpreted by the receiving entity. This field is crucial as it determines the semantic meaning and processing requirements for the message content. Following this, the payload length field occupies four bytes and specifies the exact length of the payload in bytes, excluding the generic header itself. This length information enables proper payload extraction and boundary detection, preventing parsing errors and ensuring message integrity.

```kroki-mermaid {display-width=700px display-align=center}
graph LR
    A["Generic DoIP Header"] --> B["Protocol Version (1 byte)"]
    A --> C["Inverse Protocol Version (1 byte)"]
    A --> D["Payload Type (2 bytes)"]
    A --> E["Payload Length (4 bytes)"]
    A --> F["DoIP Payload (variable)"]
    
    B --> G["0x02 (current version)"]
    C --> H["Bitwise inverse of version"]
    D --> I["Message type identifier"]
    E --> J["Payload byte count"]
    F --> K["Actual message content"]
    
    style A fill:#e8f5e9
    style F fill:#fff8e1
```

## Payload Types and Message Semantics

The payload type field within the generic DoIP header serves as a discriminator that defines the semantic meaning and processing requirements for each message. ISO 13400 defines a comprehensive set of payload types that cover the full spectrum of diagnostic communication scenarios, from initial vehicle identification to ongoing diagnostic message exchange. Each payload type corresponds to a specific message format and expected response pattern, enabling standardized communication between diagnostic tools and vehicle ECUs.

Vehicle identification messages form the foundation of DoIP communication establishment. The vehicle identification request (0x0001) allows diagnostic tools to discover available vehicles on the network, while specialized requests using EID (0x0002) or VIN (0x0003) provide more targeted identification capabilities. The vehicle announcement message (0x0004) enables vehicles to proactively announce their presence on the network, facilitating automatic discovery by diagnostic tools.

Routing activation messages manage the establishment of diagnostic communication paths. The routing activation request (0x0005) initiates the process of establishing a diagnostic session with a specific ECU, while the corresponding response (0x0006) confirms successful routing activation or provides error information if activation fails. This mechanism ensures that diagnostic communication is properly authorized and routed through the vehicle's network infrastructure.

Entity status messages provide information about the availability and state of diagnostic entities. The entity status request (0x4001) allows tools to query the current status of specific ECUs or diagnostic gateways, with the corresponding response (0x4002) providing detailed status information including availability, active diagnostic sessions, and other relevant parameters. The diagnostic power mode request (0x4003) enables tools to determine the current power state of the vehicle, which can affect diagnostic operation availability.

Diagnostic message types (0x8001 and 0x8002) facilitate the actual exchange of UDS diagnostic data. The diagnostic message payload type (0x8001) carries UDS request messages from the diagnostic tool to the target ECU, while the diagnostic message acknowledgment (0x8002) provides confirmation of message receipt and processing. These payload types form the core of the diagnostic communication session, enabling the full range of UDS diagnostic services to be executed over the IP network.

## Diagnostic Message Exchange Process

The exchange of diagnostic messages over DoIP follows a structured process that begins with vehicle discovery and progresses through session establishment to ongoing diagnostic communication. This process ensures reliable communication while maintaining the security and integrity of the vehicle's diagnostic systems. The diagnostic tool typically initiates the process by broadcasting vehicle identification requests or listening for vehicle announcement messages to discover available targets.

Once a target vehicle is identified, the diagnostic tool initiates routing activation to establish a dedicated communication path with the desired ECU. This process involves exchanging routing activation requests and responses, which may include authentication and authorization steps depending on the vehicle's security configuration. Successful routing activation results in the establishment of a TCP connection between the diagnostic tool and the target ECU, providing a reliable transport layer for subsequent diagnostic message exchange.

```kroki-mermaid {display-width=600px display-align=center}
sequenceDiagram
    participant Tool as Diagnostic Tool
    participant Vehicle as Vehicle ECU
    
    Tool->>Vehicle: Vehicle Identification Request (0x0001)
    Vehicle-->>Tool: Vehicle Identification Response
    
    Tool->>Vehicle: Routing Activation Request (0x0005)
    Vehicle-->>Tool: Routing Activation Response (0x0006)
    
    Note over Tool,Vehicle: TCP Connection Established
    
    Tool->>Vehicle: Diagnostic Message (0x8001)<br/>UDS: 0x10 0x03 (Diagnostic Session Control)
    Vehicle-->>Tool: Diagnostic Message (0x8001)<br/>UDS: 0x50 0x03 (Positive Response)
    
    Tool->>Vehicle: Diagnostic Message Acknowledgment (0x8002)
```

During active diagnostic sessions, UDS messages are encapsulated within DoIP diagnostic message payloads. For example, a Diagnostic Session Control request (UDS service 0x10 with subfunction 0x03) is transmitted from the diagnostic tool to the ECU encapsulated within a DoIP message with payload type 0x8001. The ECU processes this request and generates a corresponding positive response (UDS service 0x50 with subfunction 0x03), which is then encapsulated in another DoIP diagnostic message and transmitted back to the tool. The diagnostic tool acknowledges receipt of the response using a DoIP diagnostic message acknowledgment (payload type 0x8002), completing the request-response cycle.

This encapsulation process maintains full compatibility with existing UDS diagnostic services while leveraging the high-bandwidth capabilities of Ethernet networks. The TCP transport layer ensures reliable delivery of diagnostic messages, while the DoIP header provides the necessary context and routing information for proper message processing. The entire communication process can be monitored and analyzed using standard network analysis tools, with the payload type field immediately revealing the purpose and content of each captured DoIP message.

## Network Analysis and Troubleshooting

The structured nature of DoIP communication facilitates comprehensive network analysis and troubleshooting using standard tools such as Wireshark. When capturing and analyzing DoIP traffic, each layer of the protocol stack provides valuable information for understanding the communication flow and diagnosing potential issues. The Ethernet and IP headers reveal the physical and network layer routing information, while the TCP or UDP headers indicate the transport protocol and port usage.

The DoIP generic header provides immediate insight into the protocol version and message type through its payload type field. This field serves as a primary discriminator for packet analysis, allowing engineers to quickly identify whether a captured packet represents a vehicle identification message, routing activation, diagnostic request, or other communication type. The payload length field enables verification of complete packet capture, while the protocol version and inverse version fields confirm proper packet formatting.

Within diagnostic message payloads, the encapsulated UDS data follows the standard UDS format, with service identifiers, subfunctions, and data parameters arranged according to ISO 14229 specifications. This standardization enables direct mapping between DoIP diagnostic messages and their corresponding UDS services, facilitating traceability and debugging of diagnostic communication issues. The source and destination IP and MAC addresses in captured packets clearly identify the communicating entities, while the TCP sequence numbers and acknowledgments provide insight into the reliability of the transport layer.

Through comprehensive packet analysis, engineers can verify the complete flow of diagnostic communication, from initial vehicle discovery through session establishment and ongoing diagnostic service execution. This capability is particularly valuable for diagnosing communication failures, identifying performance bottlenecks, and validating compliance with protocol specifications. The combination of structured DoIP headers and standard UDS content creates a highly analyzable communication protocol that supports both development and production diagnostic scenarios.