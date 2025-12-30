# Features on Demand (FoD)

The automotive industry is shifting from a hardware-sales model to a **Software-as-a-Service (SaaS)** model. Vehicles are shipped with "dormant" hardware that can be activated OTA.

## The Business Model

1. **Try Before You Buy:** User gets a 1-month trial of "Full Self Driving" or "Premium Sound".
2. **Subscription:** Monthly fee for "Live Traffic" or "Connectivity".
3. **Micro-transactions:** "Weekend Power Boost" for a track day.

### Implementation Examples

- **Tesla:** Acceleration Boost (Unlocks more current from inverter).
- **BMW:** Heated Seats (Subscription).
- **Polestar:** Performance Upgrade (KW increase).

## Technical Implementation

### 1. Entitlement Management

The vehicle has a secure **Keystore** in the Gateway or HSM.

- **Certificate:** The OEM Cloud generates a signed "Feature Certificate" (e.g., `FeatureID: HEATED_SEATS, Expiry: 2025-12-31`).
- **Installation:** The OTA Manager installs this certificate into the secure storage.

### 2. Feature Activation

The target ECU (e.g., Seat Module) checks the keystore on boot.

```python
if (VerifyCertificate("HEATED_SEATS") == VALID) {
    ActivateHeater();
} else {
    ShowDisplay("Subscription Expired");
}
```

### 3. Anti-Tamper

Hackers will try to spoof these certificates.

- **Root of Trust:** Certificates must be signed by the OEM Root CA.
- **Hardware Binding:** The certificate is bound to the specific VIN and ECU Serial Number. You cannot copy a certificate from one car to another.

## Software-Defined Vehicle (SDV)

This separates the hardware lifecycle from the software lifecycle.

- **Hardware:** 5-7 year cycle.
- **Software:** Weekly/Monthly cycle.
The car gets *better* over time (like a smartphone), increasing residual value and customer loyalty.
