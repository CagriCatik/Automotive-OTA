# UDS-Based ECU Flashing Sequence in Automotive OTA Updates

## System Architecture and Overview

In modern automotive architectures, the Telematic Control Unit (TCU) functions as a diagnostic tester to execute flashing operations on downstream Electronic Control Units (ECUs) through the vehicle gateway. This architecture enables secure Over-The-Air (OTA) updates by leveraging the standardized Unified Diagnostic Services (UDS) protocol defined in ISO 14229. The TCU initiates and controls the entire flashing sequence, ensuring that software updates are applied safely and reliably to target ECUs while maintaining vehicle system integrity throughout the process.

The flashing operation begins with version verification, where the TCU reads the current software version from the target ECU using the Read Data By Identifier service (0x22). This version information is compared against update details received from the backend infrastructure, typically delivered via MQTT messaging. When a version mismatch indicates an available update, the TCU proceeds with the comprehensive flashing sequence designed to safely replace the ECU's software while preventing corruption or system instability.

## UDS Flashing Sequence Flow

The UDS flashing sequence follows a meticulously ordered process that ensures secure and reliable software updates. The sequence begins with establishing proper diagnostic communication and progresses through security validation, memory preparation, data transfer, and system restoration. Each step must complete successfully before proceeding to the next, with built-in error handling mechanisms that abort the process if critical conditions are not met.

```kroki-mermaid {display-width=400px display-align=center}
graph TD
    _1_Start["Start Flashing"] --> _2_VersionCheck["Read Software Version (0x22)"]
    _2_VersionCheck -- "Update Required?" --> _3_Decision{"Version Check"}
    _3_Decision -- "Yes" --> _4_ExtendedSession["Extended Diagnostic Session (0x10 03)"]
    _3_Decision -- "No" --> _31_End["Process Complete"]
    _4_ExtendedSession --> _5_Preconditions["Verify Preconditions (Routine Control)"]
    _5_Preconditions -- "Preconditions OK?" --> _6_Decision2{"Precondition Check"}
    _6_Decision2 -- "Fail" --> _32_Abort["Abort Flashing"]
    _6_Decision2 -- "Pass" --> _7_DisableDTC["Disable DTC Logging (0x85)"]
    _7_DisableDTC --> _8_DisableComm["Disable Communication (0x28)"]
    _8_DisableComm --> _9_ProgrammingSession["Programming Session (0x10)"]
    _9_ProgrammingSession --> _10_Security["Security Access (0x27)"]
    _10_Security -- "Seed-Key Exchange" --> _11_Decision3{"Security Valid"}
    _11_Decision3 -- "Fail" --> _32_Abort
    _11_Decision3 -- "Pass" --> _12_Fingerprint["Write Fingerprint (Optional)"]
    _12_Fingerprint --> _13_EraseMemory["Erase Memory (Routine Control)"]
    _13_EraseMemory --> _14_RequestDownload["Request Download (0x34)"]
    _14_RequestDownload --> _15_TransferData["Transfer Data Blocks (0x36)"]
    _15_TransferData --> _16_TransferExit["Request Transfer Exit (0x37)"]
    _16_TransferExit --> _17_Verify["Verify Memory (Routine Control)"]
    _17_Verify --> _18_Reset["ECU Reset (0x11)"]
    _18_Reset --> _19_EnableComm["Enable Communication (0x28)"]
    _19_EnableComm --> _20_EnableDTC["Enable DTC Logging (0x85)"]
    _20_EnableDTC --> _21_DefaultSession["Default Session (0x10 01)"]
    _21_DefaultSession --> _31_End
```

## Detailed UDS Service Implementation

The flashing sequence utilizes multiple UDS services, each serving specific functions in the update process. The Diagnostic Session Control service (0x10) manages the ECU's operational state, transitioning from the default session to an extended diagnostic session (sub-function 0x03) for preliminary operations, and subsequently to a programming session for memory modification capabilities. The specific session types and sub-functions may vary based on OEM implementation requirements, but the fundamental purpose remains consistent: establishing the appropriate operational context for secure programming.

Routine Control services play a critical role in validating system readiness and executing memory operations. Before flashing begins, routine control requests verify essential preconditions including battery voltage levels, ECU operational state, and other safety-related parameters. The ECU responds with negative response codes (NRC) if any precondition fails, immediately terminating the flashing process to prevent potential system damage. After successful precondition validation, routine control services are employed again for memory erasure and post-transfer verification operations.

The Security Access service (0x27) implements the seed-key authentication mechanism required to unlock programming capabilities. The ECU generates a random seed value, which the TCU must process using a proprietary algorithm to calculate and return the corresponding key. This exchange ensures that only authorized testers can modify ECU software. The specific algorithm implementation varies by OEM and remains confidential to maintain system security. Successful authentication grants the TCU temporary programming access necessary for the subsequent memory operations.

## Memory Operations and Data Transfer

Memory management during flashing follows a strict sequence to ensure data integrity. The process begins with memory erasure, where the target memory regions are cleared using routine control services. This step is essential to prevent data corruption and ensure clean installation of the new software. The memory erase operation must complete successfully before any data transfer can commence.

The Request Download service (0x34) initiates the data transfer phase by specifying critical parameters including the target memory address, total data size, and data format. These parameters must be precisely calculated to prevent memory corruption or overflow. The ECU validates these parameters and responds with acceptance or rejection based on memory availability and format compatibility. Once accepted, the Transfer Data service (0x36) manages the actual data transmission, breaking the software image into manageable blocks according to protocol specifications. The ECU acknowledges each received block, ensuring reliable delivery before the next block is transmitted.

```kroki-mermaid {display-width=700px display-align=center}
sequenceDiagram
    participant TCU as TCU (Tester)
    participant ECU as Target ECU
    
    TCU->>ECU: 0x22 Read Data By Identifier
    ECU-->>TCU: Software Version Response
    
    TCU->>ECU: 0x10 Diagnostic Session Control (Extended)
    ECU-->>TCU: Positive Response
    
    TCU->>ECU: Routine Control (Check Preconditions)
    ECU-->>TCU: Preconditions OK
    
    TCU->>ECU: 0x85 Control DTC Setting (Disable)
    ECU-->>TCU: Positive Response
    
    TCU->>ECU: 0x28 Communication Control (Disable)
    ECU-->>TCU: Positive Response
    
    TCU->>ECU: 0x10 Diagnostic Session Control (Programming)
    ECU-->>TCU: Positive Response
    
    TCU->>ECU: 0x27 Security Access (Request Seed)
    ECU-->>TCU: Seed Value
    TCU->>ECU: 0x27 Security Access (Send Key)
    ECU-->>TCU: Access Granted
    
    TCU->>ECU: Routine Control (Erase Memory)
    ECU-->>TCU: Erase Complete
    
    TCU->>ECU: 0x34 Request Download (Address, Size)
    ECU-->>TCU: Download Accepted
    
    loop Data Transfer
        TCU->>ECU: 0x36 Transfer Data (Block)
        ECU-->>TCU: Block Acknowledged
    end
    
    TCU->>ECU: 0x37 Request Transfer Exit
    ECU-->>TCU: Transfer Complete
    
    TCU->>ECU: Routine Control (Verify Memory)
    ECU-->>TCU: Verification OK
    
    TCU->>ECU: 0x11 ECU Reset
    ECU-->>TCU: Reset Acknowledged
    
    Note over ECU: ECU Reboots with New Software
    
    TCU->>ECU: 0x28 Communication Control (Enable)
    ECU-->>TCU: Positive Response
    
    TCU->>ECU: 0x85 Control DTC Setting (Enable)
    ECU-->>TCU: Positive Response
    
    TCU->>ECU: 0x10 Diagnostic Session Control (Default)
    ECU-->>TCU: Positive Response
```

After all data blocks are successfully transferred, the Request Transfer Exit service (0x37) signals the completion of data transmission. The ECU then performs internal verification routines, typically triggered through additional routine control requests, to validate the integrity of the newly written software. These checks may include checksum verification, signature validation, and other integrity assessments specific to the OEM's implementation requirements.

## System Restoration and Post-Flashing Operations

Following successful software installation, the system undergoes a carefully orchestrated restoration process to return to normal operation. The ECU Reset service (0x11) is typically issued to reboot the ECU, allowing it to initialize with the newly installed software. This reset ensures that all system components properly initialize with the updated code and that any cached data from the previous version is cleared.

The restoration sequence systematically re-enables all functions that were disabled during flashing to ensure the ECU resumes standard operational behavior. The Communication Control service (0x28) is used to re-enable diagnostic and network communications that were previously disabled to isolate the ECU during programming. Similarly, the Control DTC Setting service (0x85) re-enables diagnostic trouble code logging, which was suspended to prevent fault code generation during the temporary ECU unavailability period.

Finally, the Diagnostic Session Control service returns the ECU to its default diagnostic session, completing the flashing process. At this point, the update is considered successful, and the ECU operates with the new software version while maintaining full diagnostic and communication capabilities. The entire sequence, from initial version check through final restoration, ensures that OTA updates are applied safely and reliably while maintaining system integrity throughout the process.