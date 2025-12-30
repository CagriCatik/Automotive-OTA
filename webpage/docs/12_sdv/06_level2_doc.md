# Software-Defined Vehicle Level 2

## Introduction

Software-Defined Vehicle Level 2 represents a significant evolution in vehicle connectivity and software management capabilities. This level builds upon the foundational connectivity features introduced in Level 1 by introducing seamless over-the-air (OTA) software updates managed directly by the Original Equipment Manufacturer (OEM). The integration of OTA functionality at the production stage, typically through the infotainment system or telematics control unit, marks a fundamental shift in how vehicle software is maintained and updated throughout the vehicle lifecycle.

## Core Capabilities and Architecture

At SDV Level 2, vehicles maintain all basic remote functionalities accessible via smartphone applications, including remote locking, climate control, and vehicle status monitoring. The architectural enhancement at this level centers on the OEM's ability to push software updates remotely without requiring physical access to the vehicle. This capability fundamentally transforms the traditional update mechanism and significantly reduces vehicle recall costs by enabling remote resolution of software issues that would previously necessitate dealership visits.

The scope of OTA updates at Level 2 is specifically limited to static or non-safety-critical domains within the vehicle architecture. Typical update targets include infotainment systems, telematics units, and multimedia and connectivity-related Electronic Control Units (ECUs). These ECUs function as gateways or service platforms but do not directly control safety-critical vehicle functions. Other ECUs within the vehicle, particularly those without direct internet connectivity, are not updated independently at this stage. Updates may indirectly influence these systems only through predefined interfaces, if such influence is designed into the system architecture.

## System Architecture and Components

The SDV Level 2 architecture requires a fully functional OEM cloud backend that serves as the central hub for all OTA operations. This backend infrastructure encompasses multiple critical responsibilities including software file storage and versioning, access control and authentication, OTA campaign management, and comprehensive update scheduling, monitoring, and reporting capabilities. The cloud infrastructure establishes the OEM as the central trust anchor for software distribution, ensuring end-to-end control over the update process.

```kroki-mermaid
graph TD
    OEM_Cloud["OEM Cloud Backend"] -- "Encrypted Software Package" --> Telematics_Unit["Telematics Control Unit"]
    Telematics_Unit -- "Update Distribution" --> Infotainment_System["Infotainment System"]
    Infotainment_System -- "Interface Communication" --> Other_ECUs["Non-Safety-Critical ECUs"]
    Mobile_App["OEM Mobile Application"] -- "User Interaction" --> OEM_Cloud
    OEM_Cloud -- "Campaign Management" --> Update_Server["Update Management Server"]
    Update_Server -- "Version Control" --> Software_Repository["Software Repository"]
    Telematics_Unit -- "Status Reporting" --> OEM_Cloud
```

All OTA operations are strictly controlled by the OEM, with third-party systems having no direct access to the OEM OTA infrastructure. The mobile application used by customers for vehicle interaction is owned and managed by the OEM, ensuring complete end-to-end control and security throughout the update process. This centralized approach prevents unauthorized access and maintains the integrity of the software distribution chain.

## OTA Update Process Flow

The OTA update process at SDV Level 2 follows a structured workflow designed to ensure security, reliability, and proper validation. The process begins when the OEM initiates an update campaign through the cloud backend, targeting specific vehicles or vehicle populations based on various criteria such as current software version, hardware configuration, or geographic location.

```kroki-mermaid
graph TD
    _1_Start["Update Campaign Initiated"] -- "Target Selection" --> _2_Validation["Vehicle Eligibility Check"]
    _2_Validation -- "Authorized Vehicle" --> _3_Download["Secure Package Download"]
    _3_Download -- "Integrity Verification" --> _4_Installation["Package Installation"]
    _4_Installation -- "Success" --> _5_Activation["Software Activation"]
    _4_Installation -- "Failure" --> _6_Rollback["Rollback to Previous Version"]
    _5_Activation -- "Confirmation" --> _7_Report["Status Report to OEM"]
    _6_Rollback -- "Error Report" --> _7_Report
    _7_Report -- "Process Complete" --> _8_Process_End["Update Complete"]
```

During the download phase, the vehicle's telematics unit or infotainment system retrieves the encrypted software package from the OEM cloud. The package undergoes rigorous authentication and integrity verification before installation. The installation process includes validation checks to ensure compatibility with the target ECU and sufficient system resources. Upon successful installation, the new software version is activated, and the vehicle reports the update status back to the OEM cloud for record-keeping and campaign tracking.

## Security Requirements and Mechanisms

Security requirements increase significantly at SDV Level 2 due to the critical nature of remote software updates. OTA software packages must be encrypted, authenticated, and integrity-protected throughout the distribution process. Secure download mechanisms ensure that packages are transmitted safely over networks, while validation procedures verify the authenticity and integrity of received packages before installation.

Rollback mechanisms are mandatory at this level to ensure that a vehicle can safely revert to a previous software version if an update fails or causes system instability. This fallback capability is essential for maintaining vehicle operability and preventing situations where failed updates render vehicle systems inoperable. The rollback process must be automated and reliable, requiring minimal user intervention while maintaining system security.

Access control represents another critical security dimension at SDV Level 2. Only authorized OEM systems and credentials are permitted to initiate or manage OTA updates. The OEM cloud infrastructure implements robust authentication and authorization mechanisms to prevent unauthorized access to the OTA system. Role-based access control ensures that different stakeholders have appropriate levels of system access based on their responsibilities and requirements.

## Limitations and Scope

While SDV Level 2 introduces significant capabilities for remote software management, it operates within well-defined boundaries. The OTA functionality is limited to non-safety-critical domains, ensuring that vehicle safety systems remain unaffected by remote update processes. This limitation is intentional, as safety-critical systems require additional validation, redundancy, and certification processes that are not addressed at this level.

The update process does not enable independent updates for all vehicle ECUs, particularly those without direct internet connectivity. The architecture maintains a hierarchical approach where certain ECUs serve as update distributors or gateways, while others remain isolated from direct OTA access. This design choice reflects both technical constraints and safety considerations inherent in vehicle system design.

## Foundation for Higher Levels

SDV Level 2 establishes the foundational infrastructure and processes necessary for more advanced software-defined vehicle capabilities. The OEM cloud backend, secure update mechanisms, and established OTA workflows provide the building blocks for future expansion into full-vehicle updates and safety-critical domain management. The security frameworks, access control systems, and rollback mechanisms developed at this level serve as templates for enhanced capabilities in subsequent SDV levels.

The experience gained from managing OTA updates for infotainment and telematics systems provides valuable insights into the challenges and requirements for expanding OTA capabilities to other vehicle domains. The centralized OEM control model ensures consistent security and quality standards while maintaining the flexibility needed for future evolution toward more comprehensive software-defined vehicle architectures.

In summary, SDV Level 2 represents the first true step toward a software-upgradable vehicle by introducing OEM-controlled OTA updates for selected vehicle domains. While it does not yet enable full-vehicle or safety-critical software updates, it establishes the essential infrastructure, security frameworks, and operational processes that form the foundation for higher SDV levels and the eventual realization of fully software-defined vehicles.
