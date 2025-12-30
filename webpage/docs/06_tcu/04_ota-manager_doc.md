# OTA Manager Technical Documentation

## System Architecture Overview

The OTA Manager serves as the central coordinator for all Over-The-Air update activities within the vehicle architecture. In the discussed implementation, the OTA Manager resides on the gateway ECU, specifically the Telematics Control Unit (TCU). This strategic placement enables the TCU to manage all OTA operations while serving as the communication hub between various vehicle ECUs and the OEM backend. The OTA Manager interfaces with multiple systems including the infotainment or HMI system for user notifications, the backend infrastructure via MQTT and HTTPS protocols, and downstream ECUs through Unified Diagnostic Services (UDS) communication.

```kroki-mermaid {display-width=900px display-align=center}
graph LR
    Backend["OEM Backend"] -- "MQTT Notifications" --> TCU["Telematics Control Unit<br>(OTA Manager)"]
    Backend -- "HTTPS Downloads" --> TCU
    TCU -- "User Notifications" --> HMI["Infotainment/HMI"]
    TCU -- "UDS Commands" --> ECU1["Target ECU 1"]
    TCU -- "UDS Commands" --> ECU2["Target ECU 2"]
    TCU -- "UDS Commands" --> ECUN["Target ECU N"]
    HMI -- "User Approval" --> TCU
```

## Core Responsibilities

The OTA Manager encompasses a comprehensive set of responsibilities that ensure secure and reliable software updates. These responsibilities begin with update availability evaluation, where the system continuously monitors MQTT topics published by the backend to determine if updates exist for specific target ECUs. Upon detecting available updates, the OTA Manager orchestrates the complete update lifecycle, from initial user notification through final status reporting. The manager maintains strict control over each phase, ensuring that all preconditions are met before proceeding to subsequent steps. This centralized approach provides consistency and reliability across all update operations while maintaining detailed visibility into the process state at all times.

## Update Process Flow

The update process follows a meticulously defined sequence that ensures data integrity and system stability. The process begins when the OTA Manager evaluates update availability based on backend notifications. If an update is available and the user provides approval, the system initiates pre-download validation to verify all required preconditions. Upon successful validation, the OTA Manager requests the update package from the backend using HTTPS, downloading both the binary payload and associated metadata including package size, version details, and integrity verification parameters.

```kroki-mermaid {display-width=600px display-align=center}
graph TD
    Start_Node["Start Update Process"] --> Check["Evaluate Update Availability"]
    Check -- "Update Available" --> Notify["Notify User via HMI"]
    Notify -- "User Approval" --> PreValidate["Pre-download Validation"]
    PreValidate -- "Conditions Met" --> Request["Request Update Package"]
    Request --> Download["Download Binary and Metadata"]
    Download --> PostValidate["Post-download Validation"]
    PostValidate -- "Valid" --> Decompress["Decompress if Needed"]
    Decompress --> Integrity["Verify Data Integrity"]
    Integrity -- "Valid" --> Compatibility["ECU Compatibility Check"]
    Compatibility -- "Compatible" --> Flash["Initiate UDS Flashing"]
    Flash --> Monitor["Monitor Progress"]
    Monitor -- "Success" --> Report["Report Success to Backend"]
    Monitor -- "Failure" --> Failure_Handler["Execute Failure Handling"]
    Failure_Handler --> Report
    PreValidate -- "Conditions Not Met" --> Process_Abort["Abort Process"]
    PostValidate -- "Invalid" --> Process_Abort
    Integrity -- "Invalid" --> Process_Abort
    Compatibility -- "Incompatible" --> Process_Abort
```

## Validation and Verification Procedures

The OTA Manager implements multiple layers of validation to ensure update safety and reliability. Pre-download validation examines vehicle state conditions including power availability, network connectivity, and system readiness. The system verifies the current ECU software version against metadata provided by the backend to prevent inappropriate updates. During post-download validation, the OTA Manager performs comprehensive integrity checks using cryptographic hashes or message authentication codes. If the binary is compressed, it is decompressed on the TCU before verification. Any anomaly detected during validation, such as checksum mismatch or corrupted data, results in immediate process termination and failure reporting to the OEM backend.

## ECU Compatibility Verification

While the backend performs initial compatibility validation, the vehicle-side OTA Manager conducts independent verification to ensure target ECU readiness. This verification includes checking ECU identity parameters, confirming sufficient memory availability for the update, validating communication protocol compatibility, and assessing the ECU's readiness state for update operations. This dual-layer verification approach provides additional safety assurance by confirming compatibility at both the backend and vehicle levels before initiating potentially risky flashing operations.

## Flashing and Monitoring

In the gateway-based architecture, the TCU functions as a UDS Tester to communicate with downstream ECUs. The OTA Manager triggers the diagnostic flashing sequence using standardized UDS protocols to transfer and install the software update on the target ECU. During the flashing process, the OTA Manager maintains continuous monitoring of update progress and system state, tracking parameters such as data transfer rates, flash memory programming status, and ECU response times. This real-time monitoring enables immediate detection of anomalies or interruptions that could compromise update integrity.

## Error Handling and Recovery

The OTA Manager implements comprehensive error handling strategies to address various failure scenarios. If interruptions occur during the update process, such as power loss, communication failure, or violation of preconditions, the OTA Manager executes predefined failure handling procedures. These procedures may include attempting to resume the interrupted process, rolling back to a previous software version if the ECU supports this capability, or safely aborting the update to maintain system stability. The specific response strategy depends on the nature and timing of the failure, the capabilities of the target ECU, and the current state of the update process.

```kroki-mermaid {display-width=800px display-align=center}
stateDiagram-v2
    [*] --> Idle
    Idle --> Evaluating: "Update Notification"
    Evaluating --> Idle: "No Update"
    Evaluating --> PendingApproval: "Update Available"
    PendingApproval --> Idle: "User Rejects"
    PendingApproval --> PreValidation: "User Approves"
    PreValidation --> Downloading: "Preconditions Met"
    PreValidation --> Error: "Preconditions Failed"
    Downloading --> PostValidation: "Download Complete"
    Downloading --> Error: "Download Failed"
    PostValidation --> Compatibility: "Validation Passed"
    PostValidation --> Error: "Validation Failed"
    Compatibility --> Flashing: "Compatible"
    Compatibility --> Error: "Incompatible"
    Flashing --> Monitoring: "Flash Initiated"
    Flashing --> Error: "Flash Failed"
    Monitoring --> Complete: "Success"
    Monitoring --> Error: "Interruption"
    Error --> Idle: "Recovery Complete"
    Complete --> Idle: "Process Reset"
```

## Status Reporting

Upon completion of the update process, whether successful or unsuccessful, the OTA Manager generates comprehensive status reports for transmission to the OEM backend. For successful updates, the report includes confirmation that the update was received, validated, and successfully flashed on the target ECU. For failed updates, the report contains detailed error information including the failure point, error codes, and any relevant diagnostic data. This bidirectional communication ensures that the OEM backend maintains accurate visibility into the update status across the vehicle fleet, enabling fleet management, analytics, and support operations.

The OTA Manager represents a critical component in the vehicle OTA ecosystem, providing the necessary coordination, validation, and control mechanisms to ensure safe, reliable, and efficient software updates across all vehicle electronic control units. Its comprehensive responsibility set encompasses the complete update lifecycle from initial notification through final status reporting, maintaining system integrity and user trust throughout the process.