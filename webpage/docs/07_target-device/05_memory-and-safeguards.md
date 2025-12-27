# Memory & Safeguards

OTA Updates are risky. If power fails during a write operation, the ECU can be "bricked". This section covers the hardware and software strategies used to prevent this.

## Memory Architectures

### 1. Single Bank (The Risk)

The ECU has only one application area.

- **Process:**
    1. Erase Application.
    2. Write New Application.
    3. Verify.
- **Risk:** If power fails at Step 2, the ECU has no valid software. It stays in Bootloader mode (if lucky) or creates a "Dead ECU" (if Bootloader is corrupted).
- **Use Case:** Cost-sensitive ECUs (Door Modules, Seat Modules).

### 2. Dual Bank (The Gold Standard)

The ECU has two partition slots (A and B).

- **Process:**
    1. Run from Slot A.
    2. Erase Slot B.
    3. Write New Application to Slot B.
    4. Verify Slot B.
    5. Update "Active Flag" to Slot B.
    6. Reboot.
- **Safeguard:** If flashing fails at Step 3, the ECU just reboots back into Slot A. No harm done.
- **Use Case:** Critical ECUs (Gateway, Engine, ADAS).

## Fail-Safe Strategies

### 1. The Bootloader (Last Line of Defense)

The **Bootloader** is a small, immutable piece of code that runs on startup.

- **Golden Rule:** The Bootloader is **never** erased/updated OTA (in most safety strategies).
- **Logic:**

    ```c
    void main() {
        if (IsValid(App_Slot_A)) {
            JumpTo(App_Slot_A);
        } else if (IsValid(App_Slot_B)) {
            JumpTo(App_Slot_B);
        } else {
            // Stay in Bootloader and wait for UDS Flash tools
            EnterProgrammingMode();
        }
    }
    ```

### 2. Watchdog Timers

During flashing, the standard OS is dead. A hardware **Watchdog Timer** will reset the ECU if not "kicked" every few milliseconds.

- **Strategy:** The Flash Driver implementation must efficiently kick the dog while writing to flash, or disable it (if safe) to prevent a reset loop during the critical erase phase.

### 3. A/B Swapping & Rollback

If the new firmware (Slot B) boots but crashes immediately (Boot Loop):

1. **Trial Counter:** The Bootloader increments a counter on every boot.
2. **Success Flag:** The Application must run for 2 minutes and write "OK" to NVM to reset the counter.
3. **Rollback:** If the counter hits 3 (3 failed boots), the Bootloader automatically switches the Active Flag back to Slot A.

## Delta Updates (Optimization)

Instead of sending the full 100MB binary, send only the 2MB difference.

1. **BSDIFF:** Standard algorithm to generate binary patches.
2. **In-Place Reconstruction:**
    - Read Old Block 1.
    - Apply Patch.
    - Write New Block 1 to Slot B.

!!! warning "Complexity"
    Delta updates require significantly more RAM on the ECU to apply the patch. Make sure the target device can handle the reconstruction overhead.

## Conclusion

Safety is not an accident; it is a design choice. While Dual Bank memory costs more silicon, it saves millions in warranty costs and tow trucks. For modern SDVs (Software Defined Vehicles), **A/B Partitioning** is non-negotiable.
