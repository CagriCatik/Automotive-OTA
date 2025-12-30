# Target Device

So far, we have discussed the OTA infrastructure, communication protocols, backend systems, and gateway ECUs. Now we will focus on the target devices -- the ECUs that are actually being updated over the air.

While communication protocols and OEM backend platforms have evolved significantly, the target ECU hardware has also had to evolve. OTA updates impose strict requirements on memory layout, update time, safety, and reliability.

A vehicle cannot always wait for long update cycles, and at the same time, certain ECUs cannot be reprogrammed while they are actively controlling critical functions. To address these constraints, different memory architectures are used in ECUs.

From an OTA perspective, target ECUs can be broadly classified into two categories:

* Single-bank ECUs
* Dual-bank ECUs

Let us first look at single-bank ECUs.

In a single-bank ECU, the bootloader and application software reside in a single flash memory region. When the TCU initiates an OTA update, the ECU must first meet strict preconditions. For example, if the ECU controls a safety-critical function such as engine management, the vehicle must not be in a running or driving state.

If the ECU is operating while the update is triggered, the TCU will immediately abort the update process. Even if the user approves the update, flashing will not proceed until all preconditions are satisfied.

Once preconditions are met, the ECU may back up the existing software, typically to an external flash memory using interfaces such as SPI or I2C. The existing application is then erased, and the new software is programmed into the same flash region.

After programming is complete, the ECU is reset and begins execution of the new software. The update status is then reported back to the TCU and OEM backend.

Single-bank ECUs are cost-effective because they require only one application flash region. However, they have significant drawbacks:

* Updates take longer because erase and program operations are sequential.
* The vehicle must be in a safe, non-operational state.
* If a failure occurs during flashing, the ECU may become temporarily unusable until recovery is performed.

To overcome these limitations, dual-bank ECUs are increasingly used.

In a dual-bank ECU, flash memory is divided into two independent regions, commonly referred to as Bank A and Bank B. One bank contains the currently executing application, while the other bank is reserved for updates.

When an OTA update is triggered, the new software is downloaded and programmed into the inactive bank while the active bank continues to run the existing software. This allows certain updates to be performed even while the vehicle is operational, depending on ECU criticality and OEM policy.

Once the new software is fully programmed and verified in the inactive bank, the TCU instructs the ECU to switch the execution pointer to the updated bank. This switch may occur immediately, at the next ignition cycle, or under other OEM-defined conditions.

After the switch, the previously active bank can either be erased, updated later, or retained as a fallback option. This behavior is entirely dependent on OEM design decisions.

Dual-bank ECUs provide several advantages:

* Faster and safer OTA updates
* Reduced dependency on strict vehicle preconditions
* Rollback capability in case of update failure

However, these benefits come at the cost of increased flash memory requirements and higher ECU cost.

In summary, single-bank ECUs offer a lower-cost solution but require strict update conditions and carry higher risk during flashing. Dual-bank ECUs provide improved safety, flexibility, and reliability for OTA updates, at the expense of additional hardware cost.

OEMs select the appropriate memory strategy based on ECU criticality, cost targets, and OTA requirements.

---

TECHNICAL AND FACTUAL ANALYSIS

1. ECU Classification

* Classification into single-bank and dual-bank ECUs is accurate and widely used [Verified].

2. Preconditions for Single-Bank ECUs

* Requirement that safety-critical ECUs must not be updated while running is correct [Verified].
* Dependence on ignition state, battery level, and vehicle status is accurately described [Verified].

3. Backup and Flashing Behavior

* Use of external flash for backup via SPI or I2C is plausible and commonly implemented [Verified].
* Sequential erase and program behavior in single-bank ECUs is correct [Verified].

4. Failure Risk in Single-Bank Designs

* Risk of ECU unavailability if flashing fails is accurately stated [Verified].

5. Dual-Bank Architecture

* Parallel execution and update using Bank A and Bank B is correctly described [Verified].
* Execution switch after verification is accurate [Verified].
* OEM-dependent switching strategy is correctly noted [Verified].

6. OTA Advantages of Dual-Bank ECUs

* Faster updates, rollback capability, and improved safety are correctly identified [Verified].

7. Cost Tradeoff

* Increased flash memory and higher cost for dual-bank ECUs is accurate [Verified].

8. No Incorrect Claims

* No claim that all ECUs can be updated while driving [Verified].
* No claim that preconditions are entirely eliminated for dual-bank ECUs [Verified].

---

FINAL VERDICT

The rewritten explanation accurately describes target ECU memory architectures used for OTA updates.
All technical claims align with real-world automotive ECU designs and OTA best practices.
The comparison between single-bank and dual-bank ECUs is correct, balanced, and technically sound.
