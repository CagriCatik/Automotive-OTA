# Software Defined Vehicle Level 1: Technical Documentation

## Introduction to SDV Level Classification

The automotive industry is experiencing a transformation similar to what occurred with Advanced Driver Assistance Systems (ADAS) a decade ago. When ADAS features first emerged, manufacturers described their capabilities inconsistently, leading to confusion in the market. This inconsistency necessitated the formal definition of ADAS levels, creating a standardized framework from no automation to fully automated driving. The same situation now exists with Software-Defined Vehicles (SDVs), where OEMs require a structured classification system to describe how software-driven their vehicles are, what capabilities they support, and what limitations exist at each stage.

## SDV Level 1 Definition and Characteristics

Software-Defined Vehicle Level 1 represents the foundational transition from a traditional vehicle to a minimally connected one. The defining characteristic of this level is the introduction of basic internet connectivity, enabling the vehicle to communicate with cloud services and user devices. However, software control at this stage remains significantly limited. SDV Level 1 vehicles can execute a small set of non-critical features remotely, but they lack the sophisticated software management capabilities of higher levels.

The remote capabilities typically include climate control activation, remote engine start or stop, vehicle locking and unlocking, and basic vehicle status reporting through a smartphone application. These features provide convenience to users but do not fundamentally alter the vehicle's operational software. A critical limitation of SDV Level 1 is the absence of over-the-air (OTA) update capabilities for Electronic Control Units (ECUs). Firmware and core ECU software updates still require physical service intervention at authorized service centers. The remote functionality is restricted to predefined commands and status queries rather than dynamic software modification or feature deployment.

## System Architecture

The architecture of SDV Level 1 consists of three primary components working in concert to enable basic connectivity and remote control features. The first component is a smartphone application that serves as the user interface, allowing customers to send commands and receive vehicle status information. The second component is a cloud backend that acts as a mediator, handling authentication, command routing, and data processing between the user's device and the vehicle. The third component consists of one or more vehicle ECUs, typically the infotainment system or telematics unit, which receive and execute the limited set of commands from the cloud backend.

```kroki-mermaid {display-width=600px display-align=center}
graph TD
    Smartphone_App["Smartphone Application"] -- "Encrypted Commands" --> Cloud_Backend["Cloud Backend"]
    Cloud_Backend -- "Authenticated Commands" --> Vehicle_ECU["Vehicle ECU/Telematics"]
    Vehicle_ECU -- "Status Reports" --> Cloud_Backend
    Cloud_Backend -- "Status Data" --> Smartphone_App
    Service_Center["Service Center"] -- "Physical Updates" --> Vehicle_ECU
```

The communication flow follows a structured pattern where commands originate from the smartphone application, traverse through the cloud backend for processing and authentication, and finally reach the vehicle's designated ECU for execution. The vehicle then responds with status information, which follows the reverse path back to the user's application. This architecture ensures that all remote interactions are properly mediated and logged, providing a foundation for security and accountability.

## Capabilities and Limitations

SDV Level 1 vehicles support a specific set of remote functions designed to enhance user convenience without compromising vehicle safety or critical systems. These capabilities include vehicle identification through unique identifiers, real-time location tracking, geofencing to monitor vehicle movement within predefined boundaries, basic health reports covering non-critical systems, and remote control of selected comfort functions. Many OEMs have already implemented such solutions through platforms like Hyundai BlueLink, BMW ConnectedDrive, and Tesla's early mobile application features.

Despite these connected features, the vehicle software in SDV Level 1 remains essentially static. The system cannot add new features, upgrade ECU software, or deploy security patches remotely. Functionality is fixed at the time of production and can only be modified through physical service visits. This limitation means that the vehicle's capabilities evolve slowly, tied to the service cycle rather than continuous software improvement. The remote features, while convenient, do not represent true software upgradability but rather remote access to pre-existing functions.

## Security Considerations

Security remains paramount even at this foundational SDV level. The communication channels between the smartphone, cloud backend, and vehicle must be protected through multiple layers of security measures. Encryption protocols ensure that data transmitted between components remains confidential and cannot be intercepted or modified by unauthorized parties. Software integrity checks verify that commands and updates originate from legitimate sources and have not been tampered with during transmission. Additionally, appropriate firewall mechanisms must be implemented to prevent unauthorized access to vehicle systems and to isolate critical safety systems from connected components.

Although the attack surface in SDV Level 1 is smaller compared to higher levels, the potential consequences of security breaches remain significant. Unauthorized access to remote control features could pose safety risks if malicious actors gain control of vehicle functions, or privacy risks through access to location data and vehicle status information. Therefore, robust security implementation is not optional but essential for maintaining user trust and vehicle safety.

## Communication Flow and Data Exchange

The interaction between system components follows a well-defined sequence that ensures reliable and secure operation. When a user initiates a remote command through the smartphone application, the request is first authenticated and encrypted before transmission to the cloud backend. The cloud backend validates the user's credentials, checks the vehicle's current state, and forwards the command to the appropriate vehicle ECU. The vehicle ECU executes the command if conditions permit and returns a status confirmation through the same path.

```kroki-mermaid {display-width=600px display-align=center}
sequenceDiagram
    participant User
    participant Smartphone_App as "Smartphone App"
    participant Cloud_Backend as "Cloud Backend"
    participant Vehicle_ECU as "Vehicle ECU"

    User->>Smartphone_App: Initiates Remote Command
    Smartphone_App->>Cloud_Backend: Encrypted Command Request
    Cloud_Backend->>Cloud_Backend: Authenticate User
    Cloud_Backend->>Vehicle_ECU: Forward Validated Command
    Vehicle_ECU->>Vehicle_ECU: Execute Command
    Vehicle_ECU->>Cloud_Backend: Status Response
    Cloud_Backend->>Smartphone_App: Processed Status
    Smartphone_App->>User: Display Confirmation
```

This sequence ensures that every remote interaction is properly logged, authenticated, and validated before execution. The cloud backend maintains session state and command history, enabling audit trails and providing diagnostic information if issues arise. The vehicle ECU operates within strict parameters, rejecting commands that could affect safety systems or exceed its operational capabilities.

## Evolution Path and Future Considerations

SDV Level 1 serves as a crucial foundation for the evolution toward more advanced software-defined vehicles. While current capabilities are limited, the architecture establishes the basic connectivity infrastructure necessary for future enhancements. The experience gained in managing cloud services, mobile applications, and vehicle connectivity at this level provides valuable insights for implementing more sophisticated features in subsequent SDV levels.

The transition to higher SDV levels will require significant architectural enhancements, particularly in the areas of over-the-air update capabilities, expanded ECU programmability, and more sophisticated security frameworks. However, the fundamental patterns established in SDV Level 1—secure communication, mediated access, and clear separation between convenience features and safety-critical systems—will continue to inform the development of more advanced software-defined vehicle architectures.