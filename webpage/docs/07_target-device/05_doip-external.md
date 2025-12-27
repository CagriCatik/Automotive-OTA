# DoIP - Connection to External Tester

Diagnostics over Internet Protocol (DoIP) is a communication protocol standardized under ISO 13400, designed to facilitate diagnostic communication between vehicle Electronic Control Units (ECUs) and external diagnostic testers over Ethernet networks. DoIP enhances the efficiency and speed of diagnostic operations by leveraging the high bandwidth and flexibility of IP-based networks. This documentation delves into the intricacies of establishing and managing DoIP connections to external testers within an AUTOSAR framework, providing advanced users with comprehensive technical insights and practical code implementations.

## AUTOSAR Layer Architecture for DoIP

Understanding the AUTOSAR (AUTomotive Open System ARchitecture) layered architecture is crucial for implementing DoIP effectively. The architecture delineates clear separation of concerns, enabling modular and scalable development. Below is a detailed examination of the relevant layers and their interactions in the context of DoIP.

### AUTOSAR Layer Composition

1. **Application Layer**: Houses the diagnostic services and application-specific functionalities.
2. **Runtime Environment (RTE)**: Facilitates communication between the application layer and the underlying services.
3. **Basic Software (BSW)**: Comprises various modules that provide essential services, including communication stacks and hardware abstraction.
4. **Microcontroller Abstraction Layer (MCAL)**: Interfaces directly with the hardware, providing low-level drivers.

### DoIP Integration within AUTOSAR

Within the AUTOSAR architecture, DoIP is integrated primarily within the BSW. The key components involved in DoIP communication include:

- **Kante Module**: Acts as an interface between the DoIP protocol and the rest of the AUTOSAR stack.
- **Pre-Router**: Manages routing of diagnostic messages across different communication channels.
- **CAN Driver and CAN Transport Protocol (CAN TP)**: Facilitate communication over the Controller Area Network (CAN) bus.
- **Socket Adapter**: Bridges DoIP communication with socket-based networking.
- **Frame Types Module**: Defines and manages different frame formats used in DoIP.
- **Ethernet Interface and Driver**: Handle physical and data link layer operations over Ethernet.

The interaction between these components ensures seamless data transmission between the ECUs and external diagnostic testers.

## DoIP Communication Stack

The DoIP communication stack leverages both UDP and TCP protocols to establish and manage diagnostic sessions. Understanding the roles and functionalities of these protocols within the stack is essential for advanced diagnostics and troubleshooting.

### Layered Communication Flow

1. **DoIP Module**: Initiates communication and manages protocol-specific operations.
2. **Socket Adapter**: Facilitates the use of standard socket APIs for network communication.
3. **Frame Types Module**: Handles the construction and parsing of DoIP-specific frame structures.
4. **Ethernet Interface**: Manages the physical Ethernet connection, including MAC addressing and frame transmission.
5. **Ethernet Driver**: Provides low-level access to the Ethernet hardware, ensuring efficient data transfer.

This layered approach ensures modularity and flexibility, allowing each component to be developed and maintained independently.

## Connection Establishment Process

Establishing a DoIP connection between an external tester and an ECU involves a series of well-defined steps. This process ensures secure and reliable communication, enabling effective diagnostic operations.

### Step 1: Vehicle Discovery and Announcement via UDP

The initial phase involves the external tester broadcasting a discovery request to identify available vehicles on the network.

```c
// UDP discovery request example
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <arpa/inet.h>

#define DISCOVERY_PORT 13400
#define DISCOVERY_MESSAGE "VehicleDiscoveryRequest"

int main() {
    int sockfd;
    struct sockaddr_in servaddr;
    
    // Create UDP socket
    sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    
    memset(&servaddr, 0, sizeof(servaddr));
    
    servaddr.sin_family = AF_INET;
    servaddr.sin_port = htons(DISCOVERY_PORT);
    servaddr.sin_addr.s_addr = inet_addr("255.255.255.255"); // Broadcast address
    
    // Send discovery message
    sendto(sockfd, DISCOVERY_MESSAGE, strlen(DISCOVERY_MESSAGE), 0, 
           (struct sockaddr*)&servaddr, sizeof(servaddr));
    
    close(sockfd);
    return 0;
}
```

**Key Characteristics of UDP in DoIP:**

- **Connectionless**: No persistent connection is established; ideal for initial discovery.
- **Non-reliable**: No guarantee of message delivery, ordering, or duplication protection.
- **Use Case**: Primarily used for broadcasting discovery and announcement messages.

### Step 2: Vehicle Identification Message Handling

Upon receiving a discovery request, the ECU evaluates the identification message to determine whether to respond based on predefined criteria such as MAC address or Vehicle Identification Number (VIN).

```c
// Vehicle identification response example
#include <stdio.h>
#include <string.h>
#include <arpa/inet.h>

#define IDENTIFICATION_PORT 13400
#define RESPONSE_MESSAGE "VehicleDiscoveryResponse"
#define VALID_MAC "00:1A:2B:3C:4D:5E"
#define VALID_VIN "1HGCM82633A004352"

int main() {
    int sockfd;
    struct sockaddr_in cliaddr;
    char buffer[1024];
    socklen_t len = sizeof(cliaddr);
    
    // Create UDP socket
    sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    
    // Bind to discovery port
    struct sockaddr_in servaddr;
    memset(&servaddr, 0, sizeof(servaddr));
    
    servaddr.sin_family = AF_INET;
    servaddr.sin_addr.s_addr = INADDR_ANY;
    servaddr.sin_port = htons(IDENTIFICATION_PORT);
    
    bind(sockfd, (struct sockaddr*)&servaddr, sizeof(servaddr));
    
    // Receive discovery request
    recvfrom(sockfd, buffer, sizeof(buffer), 0, (struct sockaddr*)&cliaddr, &len);
    
    // Parse and validate identification message
    // Assume buffer contains JSON with ID type and value
    // Example: {"id_type":"MAC","id_value":"00:1A:2B:3C:4D:5E"}
    // Pseudocode for parsing and validation
    
    char id_type[10];
    char id_value[30];
    // Parse JSON (implementation omitted for brevity)
    
    if ((strcmp(id_type, "MAC") == 0 && strcmp(id_value, VALID_MAC) == 0) ||
        (strcmp(id_type, "VIN") == 0 && strcmp(id_value, VALID_VIN) == 0)) {
        // Send response
        sendto(sockfd, RESPONSE_MESSAGE, strlen(RESPONSE_MESSAGE), 0, 
               (struct sockaddr*)&cliaddr, len);
    }
    
    close(sockfd);
    return 0;
}
```

**Identification Criteria:**

- **MAC Address or VIN**: The ECU compares the received ID against its stored MAC address or VIN based on configuration.
- **Response Logic**: A response is sent only if the received ID matches the ECU's stored ID; otherwise, no response is issued, effectively closing the connection attempt.

### Step 3: Routing Activation Request via TCP

After successful discovery and identification, the external tester initiates a reliable connection using TCP to activate routing for subsequent diagnostic communication.

```c
// TCP routing activation example
#include <stdio.h>
#include <string.h>
#include <arpa/inet.h>
#include <unistd.h>

#define ROUTING_PORT 13400
#define ACTIVATION_REQUEST "RoutingActivationRequest"

int main() {
    int sockfd;
    struct sockaddr_in servaddr;
    
    // Create TCP socket
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    
    memset(&servaddr, 0, sizeof(servaddr));
    
    servaddr.sin_family = AF_INET;
    servaddr.sin_port = htons(ROUTING_PORT);
    servaddr.sin_addr.s_addr = inet_addr("192.168.1.100"); // ECU IP address
    
    // Connect to ECU
    connect(sockfd, (struct sockaddr*)&servaddr, sizeof(servaddr));
    
    // Send routing activation request
    send(sockfd, ACTIVATION_REQUEST, strlen(ACTIVATION_REQUEST), 0);
    
    // Receive activation response
    char buffer[1024];
    int n = recv(sockfd, buffer, sizeof(buffer), 0);
    buffer[n] = '\0';
    printf("Received: %s\n", buffer);
    
    // Proceed with diagnostic communication if activation is successful
    
    close(sockfd);
    return 0;
}
```

**Key Characteristics of TCP in DoIP:**

- **Reliable Connection**: Ensures ordered and error-checked delivery of messages.
- **Persistent Connection**: Maintains an open channel for ongoing diagnostic operations, such as flashing or DTC (Diagnostic Trouble Code) activities.
- **Use Case**: Utilized for routing activation and sustained diagnostic communication following successful discovery.

### Step 4: Diagnostic Communication

Once the routing is activated, the external tester can send diagnostic requests over the established TCP connection. The ECU processes these requests and responds accordingly.

```c
// Diagnostic request example over TCP
#include <stdio.h>
#include <string.h>
#include <arpa/inet.h>
#include <unistd.h>

#define DIAGNOSTIC_PORT 13400
#define DIAGNOSTIC_REQUEST "ReadDTCRequest"

int main() {
    int sockfd;
    struct sockaddr_in servaddr;
    
    // Create TCP socket
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    
    memset(&servaddr, 0, sizeof(servaddr));
    
    servaddr.sin_family = AF_INET;
    servaddr.sin_port = htons(DIAGNOSTIC_PORT);
    servaddr.sin_addr.s_addr = inet_addr("192.168.1.100"); // ECU IP address
    
    // Connect to ECU
    connect(sockfd, (struct sockaddr*)&servaddr, sizeof(servaddr));
    
    // Send diagnostic request
    send(sockfd, DIAGNOSTIC_REQUEST, strlen(DIAGNOSTIC_REQUEST), 0);
    
    // Receive diagnostic response
    char buffer[1024];
    int n = recv(sockfd, buffer, sizeof(buffer), 0);
    buffer[n] = '\0';
    printf("Received DTCs: %s\n", buffer);
    
    close(sockfd);
    return 0;
}
```

**Diagnostic Operations:**

- **Request Types**: Includes standard diagnostic services such as reading DTCs, ECU reprogramming, and sensor calibration.
- **Response Handling**: ECUs respond with either positive acknowledgments or negative responses based on the validity and feasibility of the requested operation.

## Connection Termination

After completing the diagnostic session, the TCP connection must be gracefully terminated to release resources and ensure network stability.

```c
// Connection termination example
#include <stdio.h>
#include <string.h>
#include <arpa/inet.h>
#include <unistd.h>

#define TERMINATION_MESSAGE "TerminateConnection"

int main() {
    int sockfd;
    struct sockaddr_in servaddr;
    
    // Create TCP socket
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    
    memset(&servaddr, 0, sizeof(servaddr));
    
    servaddr.sin_family = AF_INET;
    servaddr.sin_port = htons(13400);
    servaddr.sin_addr.s_addr = inet_addr("192.168.1.100"); // ECU IP address
    
    // Connect to ECU
    connect(sockfd, (struct sockaddr*)&servaddr, sizeof(servaddr));
    
    // Send termination message
    send(sockfd, TERMINATION_MESSAGE, strlen(TERMINATION_MESSAGE), 0);
    
    // Optionally receive acknowledgment
    char buffer[1024];
    int n = recv(sockfd, buffer, sizeof(buffer), 0);
    if (n > 0) {
        buffer[n] = '\0';
        printf("Termination Acknowledged: %s\n", buffer);
    }
    
    // Close socket
    close(sockfd);
    return 0;
}
```

**Termination Process:**

- **Initiation**: Typically initiated by the ECU upon completion of diagnostic activities, but can also be requested by the external tester.
- **Graceful Shutdown**: Ensures all pending communications are completed before closing the connection.
- **Resource Release**: Frees up network and system resources, allowing for future diagnostic sessions without conflicts.

## Summary of Communication Flow

1. **Discovery**: External tester broadcasts a UDP discovery request.
2. **Identification**: ECU validates the request and responds if identifiers match.
3. **Activation**: External tester establishes a TCP connection and sends a routing activation request.
4. **Diagnostic Session**: Ongoing diagnostic requests and responses are managed over the TCP connection.
5. **Termination**: The session is gracefully closed, terminating the TCP connection.

## Conclusion

Establishing a DoIP connection to an external tester within an AUTOSAR framework involves meticulous coordination across multiple layers and protocols. By leveraging UDP for initial discovery and TCP for reliable, persistent communication, DoIP ensures efficient and secure diagnostic operations. The provided code snippets offer practical implementations for each stage of the connection process, serving as a valuable reference for advanced users aiming to develop or enhance DoIP-based diagnostic solutions.