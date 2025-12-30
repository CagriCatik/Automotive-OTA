# UN Regulation No. 156: Software Update Management System Framework

## Introduction to OTA Updates and Regulatory Context

Modern connected vehicles rely extensively on software systems spanning powertrain control, braking mechanisms, infotainment platforms, and connectivity modules. These software components evolve continuously, necessitating periodic updates to enhance functionality, address security vulnerabilities, and improve performance. Unlike traditional vehicle maintenance performed at service stations, contemporary vehicles support Over-The-Air (OTA) update capabilities, enabling wireless delivery of software modifications directly to vehicle electronic control units (ECUs).

The OTA infrastructure comprises backend systems maintained by Original Equipment Manufacturers (OEMs), commonly referred to as OTA servers or cloud platforms. These backend systems manage the distribution of software updates, which may include application software, firmware revisions, or security patches. Updates are targeted to specific vehicle models or variants and delivered securely through telematics units or in-vehicle gateways to the appropriate ECUs. The entire process, from backend preparation to vehicle installation, constitutes an OTA update cycle.

However, OTA capabilities introduce significant risks that must be systematically managed. Update installations may fail mid-process, malicious actors could attempt to inject unauthorized software, or safety-critical systems might be compromised if updates occur under unsafe operational conditions. These risks necessitate a comprehensive regulatory framework to ensure safety and cybersecurity throughout the software update lifecycle.

## UN Regulation No. 156 Overview

UN Regulation No. 156, issued under UNECE WP.29, establishes a global regulatory framework specifically addressing software updates and the Software Update Management System (SUMS). This regulation serves as a comprehensive rulebook ensuring safety and cybersecurity during software updates for connected vehicles. The regulation does not prescribe specific technical implementations but requires manufacturers to demonstrate that risks are properly identified, assessed, and managed through documented processes and technical controls.

The regulatory timeline shows progressive enforcement beginning around 2021 in regions including Europe, Japan, and China. Starting from 2024, compliance with UNR 156 became mandatory for new vehicle type approvals in contracting regions, with progressive requirements extending to all newly produced vehicles. This regulatory mandate means that OTA functionality, behavior, and update processes must receive approval from regulatory authorities before vehicles can be placed on the market.

The regulation groups requirements into three major areas that collectively define the compliance framework. The first area addresses manufacturer requirements, focusing on organizational processes for secure software update management. The second area covers vehicle requirements, specifying technical capabilities that vehicle electronics and ECUs must possess to support secure OTA updates. The third area encompasses software identification requirements, standardizing how software versions and identifiers are defined, recorded, and verified throughout the vehicle lifecycle.

```kroki-mermaid {display-width=900px display-align=center}
graph LR
    A["UN Regulation No. 156"] --> B["Manufacturer Requirements"]
    A --> C["Vehicle Requirements"]
    A --> D["Software Identification Requirements"]
    
    B --> B1["Organizational Processes"]
    B --> B2["Software Records Management"]
    B --> B3["Update Procedures"]
    
    C --> C1["ECU Technical Capabilities"]
    C --> C2["Security Controls"]
    C --> C3["Update Preconditions"]
    
    D --> D1["RxSWIN Implementation"]
    D --> D2["Version Traceability"]
    D --> D3["Verification Processes"]
```

## OTA Update Architecture and Components

The OTA update ecosystem consists of multiple interconnected components working in coordination to deliver software updates securely and reliably. The backend infrastructure maintained by OEMs serves as the central hub for update management, hosting software packages, managing update campaigns, and monitoring deployment status. This backend system communicates with vehicles through network connections, leveraging telematics control units or dedicated in-vehicle gateways as communication interfaces.

Within the vehicle, multiple ECUs form the target destinations for software updates. These ECUs vary in complexity and criticality, ranging from non-safety-critical infotainment systems to safety-critical controllers for braking, steering, and powertrain operations. The OTA architecture must accommodate this diversity while maintaining security and reliability across all update operations.

```kroki-mermaid {display-width=900px display-align=center}
graph LR
    Backend["OEM Backend/Cloud Platform"] -- "Secure Update Package" --> Telematics["Telematics Control Unit"]
    Telematics -- "Distribute to ECUs" --> ECU1["Safety-Critical ECU<br>(ABS, EPS, etc.)"]
    Telematics -- "Distribute to ECUs" --> ECU2["Powertrain ECU"]
    Telematics -- "Distribute to ECUs" --> ECU3["Infotainment ECU"]
    Telematics -- "Distribute to ECUs" --> ECU4["Gateway ECU"]
    
    ECU1 -- "Status/Feedback" --> Telematics
    ECU2 -- "Status/Feedback" --> Telematics
    ECU3 -- "Status/Feedback" --> Telematics
    ECU4 -- "Status/Feedback" --> Telematics
    Telematics -- "Deployment Status" --> Backend
```

The update process follows a structured flow beginning with preparation at the backend level, where software packages are created, tested, and validated for compatibility with target vehicle configurations. Updates are then packaged with security controls and metadata, including version information, compatibility requirements, and installation instructions. The backend system manages update campaigns, determining which vehicles should receive specific updates based on factors such as vehicle model, current software versions, geographic location, or specific hardware configurations.

## Software Update Management System (SUMS)

Section 7.1 of UN Regulation No. 156 specifically addresses the Software Update Management System at the manufacturer level. SUMS represents the comprehensive framework through which OEMs manage the entire software update lifecycle, from initial development through deployment and post-update verification. The regulation requires that SUMS include robust processes for securely recording software versions and hardware component relationships, ensuring complete traceability throughout the vehicle lifecycle.

A critical aspect of SUMS involves compatibility verification prior to update initiation. OEMs must implement systematic processes to ensure that software updates are compatible with target vehicle configurations, preventing widespread failures across vehicle fleets. This compatibility assessment must consider hardware variations, existing software versions, and potential interactions between different vehicle systems. The regulation specifically addresses how type-approved components are handled when software functionality is added or removed, requiring that such modifications be properly documented and managed within the SUMS framework.

```kroki-mermaid {display-width=600px display-align=center}
graph TD
    Start_Node["Update Campaign Initiation"] --> Compatibility["Compatibility Verification"]
    Compatibility --> Check{"Compatible?"}
    Check -- "Yes" --> Security["Security Validation"]
    Check -- "No" --> Campaign_Abort["Campaign Abort"]
    Security --> Preconditions["Verify Preconditions<br>(Safe State, Power, etc.)"]
    Preconditions --> Deploy["Deploy to Target Vehicles"]
    Deploy --> Monitor["Monitor Installation"]
    Monitor --> Success{"Successful?"}
    Success -- "Yes" --> Verify["Post-Update Verification"]
    Success -- "No" --> Recovery["Recovery Procedures"]
    Verify --> Process_Complete["Update Complete"]
    Recovery --> Process_Complete
```

The regulation mandates that update preconditions be clearly defined and systematically verified before installation commences. These preconditions include requirements for safe vehicle states, stable power supply conditions, and controlled environments necessary for critical updates. For instance, safety-critical system updates may require the vehicle to be stationary with parking brake engaged, while infotainment updates might permit installation during normal operation with appropriate safeguards.

SUMS must also address post-update requirements, particularly for safety-related systems. If updates require subsequent actions such as calibration of safety systems like Electronic Power Steering (EPS) or Anti-lock Braking Systems (ABS), these procedures must be documented, validated, and properly managed within the update process. The regulation emphasizes that such post-update activities must be traceable and verifiable to ensure continued vehicle safety and compliance.

## Software Identification and RxSWIN

UN Regulation No. 156 establishes standardized requirements for software identification to ensure traceability and prevent unauthorized modifications. The regulation introduces the Regulation Software Identification Number (RxSWIN) as a unique identifier representing the software version of electronic control systems relevant for type approval. RxSWIN serves as a critical component in maintaining software traceability throughout the vehicle lifecycle, enabling regulatory authorities to verify that approved software versions are deployed and that unauthorized changes are prevented.

The software identification requirements extend beyond simple version numbering to encompass comprehensive metadata about software components, their relationships to hardware, and their relevance to vehicle safety and emissions systems. Each software component must be uniquely identifiable, with clear documentation of its functionality, safety relevance, and compatibility requirements. This information must be maintained throughout the vehicle's operational life and made available for regulatory inspection as needed.

Vehicles must implement technical controls to prevent unauthorized software modifications while supporting restoration mechanisms where required by the regulation. These controls include cryptographic verification of software authenticity and integrity, secure boot processes, and runtime integrity monitoring. The regulation requires that vehicles enforce defined prerequisites for safe software updates, ensuring that modifications cannot occur under conditions that might compromise vehicle safety or security.

## Vehicle Requirements and Technical Controls

The vehicle requirements section of UN Regulation No. 156 specifies technical capabilities that must be implemented to support secure OTA updates. Electronic control units must possess the ability to verify software authenticity and integrity before installation, using cryptographic mechanisms to ensure that only authorized software from legitimate sources can be installed. This verification process must occur automatically and transparently, with clear error handling and reporting mechanisms for failed verifications.

Vehicles must implement robust security controls to protect against unauthorized software modifications, including protection against rollback attacks where malicious actors attempt to install older, potentially vulnerable software versions. The regulation requires that vehicles maintain secure records of installed software versions, enabling detection of unauthorized changes and supporting forensic analysis when security incidents occur. These records must be protected against tampering and made available for regulatory compliance verification.

The technical requirements also address update reliability and failure handling. Vehicles must implement mechanisms to detect update failures, maintain system stability during interrupted updates, and recover gracefully from failed installation attempts. For safety-critical systems, additional safeguards must be implemented to ensure that update failures cannot compromise vehicle safety, including fallback mechanisms and safe state transitions.

## Compliance and Type Approval Process

Compliance with UN Regulation No. 156 is demonstrated through a comprehensive type approval process where regulatory authorities review evidence submitted by manufacturers. This evidence must demonstrate compliance with safety and cybersecurity requirements at both the backend SUMS level and the vehicle implementation level. The approval process involves detailed documentation of organizational processes, technical implementations, and security controls, along with evidence of testing and validation activities.

The regulation includes approximately thirty individual requirements that collectively define compliance expectations. These requirements cover aspects such as risk assessment methodologies, security control implementation, update process management, and incident response procedures. Manufacturers must provide detailed evidence addressing each requirement, demonstrating how their systems and processes meet the specified criteria.

Type approval is not a permanent status but subject to renewal and ongoing compliance verification. The regulation includes provisions for vehicle modifications after type approval, defining conditions for conformity, non-conformity, and circumstances requiring approval updates or extensions. Manufacturers must maintain continuous compliance monitoring and report significant changes that might affect the approved status of their OTA systems.

The regulation also specifies consequences for non-compliance, including potential penalties and requirements for remediation. These provisions ensure that manufacturers maintain ongoing compliance throughout the vehicle lifecycle and address any identified deficiencies promptly and effectively.

## Applicability and Scope

UN Regulation No. 156 applies to vehicles used for the transport of passengers and goods, including trailers, across specified vehicle categories defined by UNECE. The regulation covers vehicle categories such as M (passenger vehicles), N (goods vehicles), O (trailers), and other specified categories. For example, category M1 refers to passenger vehicles, M2 to buses, and category T to agricultural and forestry tractors.

The applicability of UNR 156 is conditional on vehicles supporting OTA update capabilities. If a vehicle within the specified categories supports OTA updates, the requirements of UNR 156 must be fulfilled. This conditional applicability ensures that the regulation focuses on vehicles and systems where OTA functionality presents potential safety and cybersecurity risks.

The regulation includes annexes covering declarations of compliance, approval forms, and approval marks. These documents standardize the format for manufacturer declarations, specify required information for approval submissions, and define the format for approval marks that must be displayed on compliant vehicles. The annexes also address procedures for approval extensions, refusals, and certification formats, providing a comprehensive framework for regulatory compliance management.

In summary, UN Regulation No. 156 establishes a comprehensive regulatory framework for OTA software updates in vehicles, requiring manufacturers to implement robust processes and technical controls to ensure safety and security throughout the update lifecycle. The regulation's requirements span organizational processes, vehicle technical capabilities, and software identification standards, collectively ensuring that OTA updates can be performed safely and securely in modern connected vehicles.