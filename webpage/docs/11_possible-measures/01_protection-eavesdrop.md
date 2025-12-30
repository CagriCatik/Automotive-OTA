# OTA Security: Protection Against Eavesdropping

This document outlines the defense strategies required to mitigate **eavesdropping attacks** (passive interception) in Over-the-Air (OTA) update systems. The primary goal is to preserve the **confidentiality** of the update data (firmware, configuration files, and metadata) as it traverses untrusted public networks (e.g., cellular, Wi-Fi) from the backend server to the vehicle.

## Core Defense Strategies

The defense against eavesdropping relies on a **Defense in Depth** approach, layering security at both the transport and application levels.

### 1. Transport Layer Security (TLS)
The first line of defense is securing the communication channel itself.
- **Encryption**: All OTA traffic should be encapsulated within a secure tunnel using **TLS 1.2** or **TLS 1.3**. This encrypts the entire communication stream, rendering intercepted packets unreadable to an attacker.
- **Authentication**: Usage of **HTTPS** ensures the client (vehicle) is talking to the legitimate server.
- **Mutual TLS (mTLS)**: For higher security, mTLS should be enforced. This requires both the server and the client (vehicle) to present valid x.509 certificates, preventing "Man-in-the-Middle" scenarios that could facilitate eavesdropping.

### 2. Application Layer Payload Encryption
Relying solely on TLS is often insufficient for automotive standards (e.g., UN R156, ISO 21434). If the TLS termination point is an edge node or if the content is cached by a Content Delivery Network (CDN), the firmware could be exposed in plaintext.
- **End-to-End Encryption**: The firmware binary itself is encrypted by the OEM backend before it ever enters the distribution network.
- **Symmetric Encryption**: Typically, large firmware binaries are encrypted using a symmetric algorithm (e.g., **AES-256-GCM** or **ChaCha20-Poly1305**) because symmetric decryption is computationally efficient for the ECU.
- **Key Distribution**: The symmetric key is then encrypted (wrapped) using the target ECU’s public key (Asymmetric Encryption) or derived via a secure key exchange protocol (e.g., ECDH).

### 3. Secure Key Storage
Confidentiality is only as strong as the protection of the decryption keys.
- **Hardware Security Modules (HSM)**: Private keys used for decryption must be stored in tamper-resistant hardware (HSM, TPM, or SHE) within the ECU.
- **Key Isolation**: Decryption should occur inside the secure environment to prevent the plaintext firmware or the keys from leaking into the rich OS memory.

---

## Visualizing the Protection

### Encrypted Channel vs. Encrypted Payload

The following diagram illustrates the concept of Layered Security. Even if the Transport Layer (TLS) is compromised or terminated at a CDN, the Application Layer encryption ensures the data remains confidential.

```kroki-mermaid {display-width=600px display-align=center}
graph TD
    classDef secure fill:#e1f5fe,stroke:#01579b,stroke-width:2px;
    classDef compromise fill:#ffebee,stroke:#b71c1c,stroke-width:2px;
    classDef component fill:#fff3e0,stroke:#e65100,stroke-width:2px;

    Cloud[OEM OTA Cloud]:::component
    CDN[Content Delivery Network]:::component
    Vehicle[Vehicle Gateway / ECU]:::component
    Attacker[Attacker / Eavesdropper]:::compromise

    Cloud --|1. Encrypted Binary (AES-256)|--> CloudOut[Protected Payload]
    CloudOut --|2. HTTPS / TLS Tunnel|--> CDN
    CDN --|3. HTTPS / TLS Tunnel|--> Vehicle

    %% Attack Vector
    CDN -.->|TLS Termination| Attacker
    Attacker --|Observes Traffic|--> Result{Inspection Result}

    Result --|If TLS Only|--> Clear[PLAINTEXT EXPOSED<br/>Attacker has firmware]:::compromise
    Result --|If Payload Encrypted|--> Encrypted[CIPHERTEXT ONLY<br/>Attacker has blobs]:::secure

    style CloudOut fill:#e8f5e9,stroke:#1b5e20
```

### Secure OTA Download Sequence

 This sequence diagram demonstrates a secure update flow using a Hybrid Encryption scheme (Envelope Encryption), which is standard best practice for OTA.

1.  **Preparation**: Backend generates a random symmetric key ($K_{sym}$), encrypts the firmware, and then encrypts $K_{sym}$ with the ECU's Public Key ($K_{pub}$).
2.  **Transmission**: The package is sent over TLS.
3.  **Reception**: ECU uses its Private Key ($K_{priv}$) to decrypt the symmetric key, then uses the symmetric key to decrypt the firmware.

```kroki-mermaid {display-width=600px display-align=center}
sequenceDiagram
    participant Cloud as OEM OTA Cloud
    participant Net as Public Network (TLS)
    participant ECU as Target ECU (HSM)

    Note over Cloud: **1. Preparation**
    Cloud->>Cloud: Generate Random Key (K_sym)
    Cloud->>Cloud: Encrypt Firmware: E(Firmware, K_sym)
    Cloud->>Cloud: Encrypt Key: E(K_sym, ECU_Public_Key)
    
    Note over Cloud, ECU: **2. Transmission**
    Cloud->>Net: Send [Encrypted_Firmware + Encrypted_Key]
    Net-->>ECU: Receive Package (via TLS Tunnel)
    
    Note over ECU: **3. Decryption (Secure World)**
    ECU->>ECU: Load ECU_Private_Key (from HSM)
    ECU->>ECU: Decrypt K_sym = D(Encrypted_Key, ECU_Private_Key)
    ECU->>ECU: Decrypt Firmware = D(Encrypted_Firmware, K_sym)
    
    alt Decryption Success
        ECU-->>Cloud: Ack: Ready for Installation
    else Decryption Fail
        ECU-->>Cloud: Error: Integrity/Auth Failure
    end
```

## Summary of Recommendations

| Layer | Mechanism | Algorithm / Standard | Protection Goal |
| :--- | :--- | :--- | :--- |
| **Transport** | **mTLS** (Mutual TLS) | TLS 1.3 | Secures the "pipe". prevents man-in-the-middle and passive sniffing on the wire. |
| **Application** | **Hybrid Encryption** | AES-256 (Data) + RSA/ECC (Keys) | Secures the "data". Protects IP even if the pipe is broken or trusted intermediates (CDNs) are used. |
| **Hardware** | **Secure Storage** | HSM / TPM / SHE | Protects the "keys". Ensures physical extraction of secrets is infeasible. |
