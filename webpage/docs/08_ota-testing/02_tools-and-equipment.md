# Tools & Equipment

Automotive OTA testing requires specialized hardware to simulate the vehicle environment and stress-test the protocols.

## Test Benches (HIL)

### 1. Vector CANoe & VT System

The industry standard for automotive testing.

- **CANoe:** Simulates the "Missing Nodes". If you are testing the TCU, CANoe simulates the Engine, Brakes, and Dashboard so the TCU thinks it's in a real car.
- **VT System:** Modular hardware for electrical simulation.
  - **VT7001 (Power):** Controls `KL30` (Battery) and `KL15` (Ignition). Used to simulate power failures.
  - **VT2004 (IO):** Simulates buttons (User Consent) and sensors.

### 2. Raspberry Pi / Linux Gateway

For DoIP generic testing, a simple Linux box with a CAN hat (e.g., PEAK-System) can act as a lightweight tester.

## Software Tools

### 1. CAPL (Communication Access Programming Language)

Scripting language used in CANoe.

```c
// CAPL Example: Simulate a Diagnostic Response
on message 0x7E0 {
  if (this.byte(0) == 0x02 && this.byte(1) == 0x10 && this.byte(2) == 0x03) {
    // Tester requested Extended Session
    message 0x7E8 response;
    response.byte(0) = 0x06; // PCI Length
    response.byte(1) = 0x50; // Positive Response
    response.byte(2) = 0x03; // Sub-function
    response.byte(3) = 0x00; // P2 Max (High)
    response.byte(4) = 0x32; // P2 Max (Low) = 50ms
    output(response);
  }
}
```

### 2. Wireshark (DoIP Analysis)

Essential for debugging Ethernet.

- **Filter:** `tcp.port == 13400`
- **Dissector:** Wireshark has a built-in "DoIP" dissector. You can see the Vehicle Announcement and Routing Activation packets clearly.

### 3. ODX-e / OTX

- **ODX (Open Diagnostic Data Exchange):** XML format that describes the ECU's diagnostic capabilities (DIDs, Routines).
- **OTX (Open Test Sequence Exchange):** XML format for defining the flash sequence logic.

## Automation Frameworks

### Robot Framework

A keyword-driven Python framework popular in automotive.

```robot
*** Test Cases ***
Verify OTA Rollback on Power Fail
    [Documentation]    Simulate power cut during flash write
    Connect To Bench
    Start OTA Update    v2.0
    Wait Until Progress    50%
    Cut Power For    5s
    Restore Power
    Wait For Boot
    Check Software Version    v1.0    # Should be rolled back
```
