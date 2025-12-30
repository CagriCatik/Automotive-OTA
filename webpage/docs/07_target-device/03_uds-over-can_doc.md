# UDS over CAN for Target Device OTA Updates

## Introduction to UDS over CAN in OTA Context

Unified Diagnostic Services (UDS) over Controller Area Network (CAN) forms the foundation of Over-The-Air (OTA) update mechanisms for automotive target devices. The protocol enables reliable transmission of diagnostic commands, firmware images, and configuration data to electronic control units (ECUs) within the vehicle network. The inherent limitation of classical CAN frames to eight bytes of payload necessitates a transport layer protocol to handle larger data transfers typical in OTA operations. The CAN Transport Protocol (CAN-TP) addresses this limitation by implementing a segmentation and reassembly mechanism that allows for the transfer of data packets far exceeding the native CAN frame capacity.

## CAN Transport Protocol Architecture

The CAN-TP operates as a transport layer protocol situated between the application layer (UDS) and the data link layer (CAN). Its primary responsibility is to manage the segmentation of large application messages into smaller CAN frames and ensure their reliable delivery to the target device. The protocol establishes a virtual communication channel that abstracts away the complexity of frame management, allowing the UDS application layer to operate with a simplified message-based interface. This architecture is particularly crucial for OTA operations where firmware images can span several megabytes and must be transferred reliably across the vehicle network.

The target device implements both sender and receiver roles depending on the OTA operation phase. During firmware upload, the target device acts as a receiver, acknowledging incoming segments and managing flow control to prevent buffer overflow. Conversely, during status reporting or log retrieval, the target device becomes the sender, transmitting diagnostic data back to the central OTA management system.

```kroki-mermaid {display-width=400px display-align=center}
graph TD
    A["UDS Application Layer"] --> B["CAN Transport Protocol"]
    B --> C["CAN Data Link Layer"]
    C --> D["Physical Layer"]
    
    subgraph "Target Device Components"
        E["OTA Manager"] --> F["UDS Handler"]
        F --> G["CAN-TP Module"]
        G --> H["CAN Controller"]
    end
    
    I["OTA Server"] -- "Diagnostic Commands" --> E
    H -- "CAN Frames" --> C
```

## Frame Types and Protocol Mechanics

The CAN-TP protocol defines three primary frame types that facilitate the segmented data transfer process. Each frame type serves a specific function in the communication sequence and contains a structured payload that conveys both protocol control information and application data.

The First Frame initiates a multi-frame transmission sequence. Its first byte contains the value 0x10, which the receiver interprets as the start of a segmented message. The second byte encodes the total length of the application payload, allowing the receiver to allocate appropriate buffer space. The remaining six bytes of the First Frame contain the initial portion of the application data. In the provided trace example, the First Frame payload begins with 0x10 0x12, indicating the start of an 18-byte message containing a UDS Transfer Data request (service ID 0x36).

Flow Control frames manage the data transmission rate and prevent receiver buffer overflow. These frames are always sent by the receiver and begin with the nibble 0x3 in their first byte. The second byte contains the flow status, where 0x00 indicates permission to continue transmission (Continue To Send), 0x01 signals wait (Wait), and 0x02 indicates overflow or abort conditions. The third and fourth bytes specify the block size and separation time parameters, respectively. A block size of zero indicates no restriction on the number of consecutive frames that may be sent before requiring another flow control acknowledgment, while a separation time of zero permits immediate transmission without delay.

Consecutive Frames carry the bulk of the segmented data payload. Each frame begins with a byte where the high nibble is set to 0x2, indicating a Consecutive Frame, and the low nibble contains the sequence number that increments from 1 to 15 before wrapping back to 0. This sequence number enables the receiver to detect missing frames and ensure proper reassembly of the original message. The remaining seven bytes of each Consecutive Frame contain application data, maximizing the utilization of the CAN frame's payload capacity.

## Data Transfer Process and Flow Control

The segmented data transfer process follows a well-defined sequence that ensures reliable communication between the OTA server and the target device. The process begins when the sender determines that the application data exceeds the single-frame capacity of the CAN protocol. The sender then constructs a First Frame containing the total message length and the initial data segment, transmitting it to the receiver.

Upon receiving the First Frame, the target device analyzes the total length parameter and prepares its receive buffers accordingly. The device then responds with a Flow Control frame that communicates its readiness to receive data and specifies the transmission parameters. The block size parameter in the Flow Control frame determines how many Consecutive Frames the sender may transmit before pausing for another flow control acknowledgment. This mechanism enables the receiver to manage its buffer utilization and prevent overflow during high-speed transfers.

The sender then begins transmitting Consecutive Frames, each carrying up to seven bytes of application data. The sequence number in each frame allows the receiver to track the order of segments and detect any missing frames. The separation time parameter specified in the Flow Control frame governs the minimum interval between consecutive frame transmissions, preventing the sender from overwhelming the receiver's processing capabilities.

```kroki-mermaid {display-width=400px display-align=center}
sequenceDiagram
    participant S as OTA Server
    participant T as Target Device
    
    S->>T: First Frame (0x10)
    Note over S,T: Announces multi-frame message<br/>with total length
    
    T->>S: Flow Control (0x30)
    Note over T,S: Grants permission to send<br/>with block size and timing
    
    loop Consecutive Frames
        S->>T: Consecutive Frame (0x21)
        Note over S,T: Carries 7 bytes of data<br/>with sequence number
        
        S->>T: Consecutive Frame (0x22)
        Note over S,T: Continues data transfer<br/>with incremented sequence
        
        alt Block size reached
            T->>S: Flow Control (0x30)
            Note over T,S: Acknowledges block and<br/>authorizes continuation
        end
    end
    
    Note over S,T: Complete message reassembled<br/>at target device
```

## Protocol Analysis with Real Trace Example

The provided CAN trace demonstrates a complete CAN-TP transaction involving the transfer of a UDS diagnostic message. The initial frame contains the payload 10 12 36 01 01 31 47 31, where the first byte 0x10 identifies it as a First Frame. The second byte 0x12 indicates that the complete application message spans 18 bytes, necessitating segmentation across multiple CAN frames. The third byte 0x36 represents the UDS service identifier for Transfer Data, which is commonly used in OTA operations to send firmware chunks or configuration data to the target device.

The target device responds with a Flow Control frame containing 30 00 00 00 00 00 00 00. The first byte 0x30 identifies this as a Flow Control frame, while the second byte 0x00 indicates the Continue To Send status, granting the sender permission to proceed with data transmission. The zero values for block size and separation time in bytes three and four, respectively, indicate that the sender may transmit consecutive frames without restriction and without enforced delays. This configuration is typical when the target device has sufficient buffer space and processing capability to handle high-speed data transfers.

Following the Flow Control acknowledgment, the sender begins transmitting Consecutive Frames starting with sequence number 1 (0x21). Each subsequent frame increments the sequence number, allowing the receiver to track the order of segments and detect any potential gaps in the transmission. The receiver reassembles the complete UDS message by concatenating the data payloads from the First Frame and all subsequent Consecutive Frames in the correct order based on their sequence numbers.

## Implementation Considerations for Target Devices

Target devices implementing OTA update capabilities must carefully manage several critical aspects of the CAN-TP implementation to ensure reliable operation. Buffer management represents a primary concern, as the device must allocate sufficient memory to store incoming segments while processing them and writing to non-volatile storage. The implementation should employ circular buffers or double-buffering techniques to enable continuous data reception while processing previously received segments.

Flow control implementation requires careful tuning of block size and separation time parameters based on the target device's processing capabilities and storage write speeds. Devices with slower flash memory may need to request smaller block sizes or longer separation times to prevent buffer overflow during firmware writes. Conversely, devices with ample processing power and fast storage can maximize throughput by allowing larger block sizes and minimal separation delays.

Error handling and recovery mechanisms are essential for robust OTA operations. The target device should implement timeout detection for missing frames and request retransmission of lost segments. Additionally, the device should validate checksums and digital signatures on received firmware chunks before writing them to memory, ensuring the integrity and authenticity of the OTA update package.

The segmentation and reassembly process must maintain strict synchronization between the sender and receiver, particularly during critical OTA operations such as bootloader updates. Any corruption or loss of segments during the transfer could render the target device inoperable, necessitating robust error detection and recovery procedures throughout the update process.