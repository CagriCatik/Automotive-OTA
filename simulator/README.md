# Automotive OTA Simulation Platform

> A high-fidelity, production-grade simulation of an Over-The-Air (OTA) software update system for Software Defined Vehicles (SDV).

## Overview

This project simulates a complete end-to-end OTA architecture, mirroring the complexity of real-world automotive systems. It is designed to demonstrate:

* **Separation of Concerns**: Distinct Control Plane, Data Plane, and Event Plane.
* **Automotive Constraints**: Simulation of low-speed CAN bus networks, binary delta patching, and resource-constrained ECUs.
* **Safety & Security**: Implementation of The Update Framework (TUF) principles, including manifest signing, artifact verification, and A/B partition rollback.

## 🏗️ System Architecture

The system is divided into two primary contexts: the **Cloud Infrastructure** and the **Vehicle Edge**.

```mermaid
graph TD
    subgraph "Cloud Infrastructure"
        BE[Backend Orchestrator]
        CP["Control Plane (gRPC)"]
        AS["Artifact Server (HTTP)"]
        MQ[MQTT Broker]
  
        BE -->|Publish Campaign| CP
        BE -->|Upload Artifacts| AS
        BE -->|Notify| MQ
    end

    subgraph "Vehicle Edge"
        GW[Gateway / OTA Agent]
        HMI[Head Unit UI]
  
        subgraph "CAN Bus Network"
            ECU1[ECU: Engine]
            ECU2[ECU: ADAS]
        end
  
        GW -->|Poll/Job| CP
        GW -->|Download| AS
        MQ -.->|Wake Up| GW
  
        GW -->|"Diagnostics (UDS)"| ECU1
        GW -->|"Diagnostics (UDS)"| ECU2
        HMI -- User Approval --> GW
    end

    style BE fill:#e1f5fe,stroke:#01579b
    style CP fill:#e1f5fe,stroke:#01579b
    style AS fill:#e1f5fe,stroke:#01579b
    style GW fill:#fff3e0,stroke:#e65100
    style ECU1 fill:#e8f5e9,stroke:#2e7d32
    style ECU2 fill:#e8f5e9,stroke:#2e7d32

```

### Component Deep Dive

| Component                 | Tech Stack    | Responsibility                                                                                                                           |
| :------------------------ | :------------ | :--------------------------------------------------------------------------------------------------------------------------------------- |
| **Backend**         | Python        | Orchestrates campaigns, generates `bsdiff4` binary deltas, signs manifests using Ed25519 keys.                                         |
| **Control Plane**   | gRPC (Python) | The authoritative source of truth. Handles job creation, state tracking, and policy enforcement (e.g., "Is vehicle allowed to update?"). |
| **Gateway**         | Python, Flask | The Master OTA Agent. It bridges the internet (HTTP/gRPC) and the internal vehicle network (CAN). Manages the update state machine.      |
| **Artifact Server** | HTTP          | A simple CDN simulation hosting encrypted/signed firmware binaries and delta patches.                                                    |
| **ECUs**            | Python        | Simulated target devices with Dual-Bank (A/B) storage. They receive binary streams over virtual CAN and simulate flashing/booting.       |

---

## 🔄 OTA Workflow

The following sequence diagram illustrates the "Happy Path" of a successful firmware update.

```mermaid
sequenceDiagram
    autonumber
    participant BE as Backend
    participant CP as Control Plane
    participant MQ as MQTT Broker
    participant GW as Gateway
    participant ECU as Target ECU

    Note over BE, CP: 1. Campaign Started
    BE->>CP: Register Manifest & Campaign
    BE->>MQ: Publish "Update Available"
  
    Note over GW: 2. Notification
    MQ-->>GW: Wake Up / Notify
    GW->>CP: Create Job (CheckIn)
    CP-->>GW: Job Created (ID: job-123)
  
    Note over GW: 3. Confirmation
    GW->>CP: Get Manifest
    GW->>GW: Verify Ed25519 Signature
    GW->>CP: Update Status: WAITING_FOR_APPROVAL
  
    Note over GW: 4. User Consent
    GW->>GW: Wait for HMI Approval
  
    Note over GW: 5. Download
    GW->>CP: Update Status: DOWNLOADING
    GW->>BE: Download Artifact (HTTP)
    GW->>GW: Verify SHA256 Hash
  
    Note over GW, ECU: 6. Installation (CAN Bus)
    GW->>CP: Update Status: INSTALLING
    GW->>ECU: UDS Request Download
    GW->>ECU: Stream Binary Data
    ECU-->>GW: Transfer Complete
  
    Note over ECU: 7. Validation
    ECU->>ECU: Verify Signature
    ECU->>ECU: Switch Active Partition (A->B)
    ECU-->>GW: Reboot Success
  
    Note over GW: 8. Completion
    GW->>CP: Job Succeeded
```

---

## 🛡️ Security & Resilience

### Trust Chain

1. **Root of Trust**: The Backend holds the private signing keys.
2. **Manifest Signing**: Every update campaign generates a Manifest containing hashes of all artifacts, signed with the Backend's private key.
3. **Gateway Verification**: The Gateway has the public key pinned. It validates the Manifest signature before initiating *any* downloads.
4. **Artifact Integrity**: Downloaded files are hashed and compared against the verified Manifest.

### A/B Partitioning & Rollback

To prevent "bricking" vehicles, ECUs implement an A/B banking strategy:

* **Slot A**: Current Active Firmware.
* **Slot B**: Update Target.
* **Rollback**: If the simulated new firmware fails to "boot" (simulated via chaos testing flags), the ECU watchdog automatically swaps back to Slot A and reports failure.

---

## 🚀 Getting Started

### Prerequisites

* docker
* docker compose

### Running the Simulation

1. **Start Services**:
   ```bash
   docker compose up --build
   ```
2. **Access Dashboard**:
   Open [http://localhost:8080](http://localhost:8080) to view the Vehicle HMI.
   * Observe the "Update Available" notification.
   * Click "Install Now" to approve.
3. **Monitor Progress**:
   The Dashboard will show real-time progress as the Gateway downloads artifacts and streams them to the ECUs.

### Directory Structure

* `backend/`: Cloud services (Orchestrator, Signer).
* `control-plane/`: gRPC Server definition and implementation.
* `gateway/`: Vehicle-side logic (OTA Agent, HMI, CAN Bridge).
* `ecu/`: Simulated hardware targets.
* `traces/`: Shared volume for simulation logs (jsonl).
* `ota.proto`: Unified gRPC protocol definition.

## 🐛 Troubleshooting

**"Not in waiting state" Error**

* **Cause**: The Gateway failed to create a Job in the Control Plane, often due to a protocol mismatch.
* **Fix**: Ensure `ota.proto` is synchronized across all services and rebuild using `docker compose up --build`.

**Logs**

* Streaming structure logs are available in `traces/simulation_trace.jsonl`.
