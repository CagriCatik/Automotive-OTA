# Bootloader

Welcome to this section. In this video, we will clarify who is actually responsible for programming an Electronic Control Unit.

In earlier sections, we stated that the Telematics Control Unit is responsible for flashing ECUs. That statement is correct at a system level, but it is important to understand the internal responsibility split in more detail.

From an architectural perspective, two main entities are involved in ECU programming:

* The external or gateway-side tester, typically the TCU
* The target ECU that is being programmed

Inside the TCU, a UDS tester component is responsible for sending diagnostic and programming requests over CAN or Ethernet. These requests are transported using CAN-TP or DoIP, depending on the vehicle architecture.

However, the actual act of programming memory does not happen in the TCU. It happens inside the target ECU.

Inside the ECU, the internal flash memory contains multiple software components. Among them, the most critical for programming are the bootloader, the boot manager, and the flash driver.

The bootloader is the primary component responsible for handling ECU programming. The boot manager is a logical part of the bootloader that decides whether the ECU should start in application mode or programming mode. This decision is made every time the ECU resets or powers up.

The flash driver is a low-level component that performs the actual erase and write operations on the flash memory. It provides hardware-specific APIs that the bootloader uses to modify memory.

At ECU startup or reset, execution always begins in the boot manager. Based on predefined conditions, the boot manager decides whether to hand control to the application software or to remain in the bootloader.

Now let us map this to a typical flashing sequence.

When the tester sends a Diagnostic Session Control request with sub-function 0x02 (programming session), the request reaches the ECU and is processed by the boot manager. The boot manager recognizes that a programming session has been requested and transfers control to the bootloader.

Subsequent programming-related UDS services are then handled by the bootloader.

For example:

* Security Access services (0x27) are processed by the bootloader to unlock programming permissions.
* Fingerprint writing using Write Data By Identifier (0x2E) is handled by the bootloader.
* Routine Control services used for memory erase are executed by the bootloader, which calls the flash driver APIs to erase the specified memory regions.

When a Request Download service is received, the bootloader validates the target memory address and size. This information defines where the new software will be stored.

During Transfer Data (0x36), the incoming data blocks are received by the bootloader. The bootloader forwards these blocks to the flash driver, which writes the data into flash memory sector by sector based on the provided start address and block size.

Once all data blocks have been transferred, the Request Transfer Exit service (0x37) signals completion of the download phase. The bootloader then verifies memory integrity, often using a checksum or hash via Routine Control.

After successful verification, an ECU Reset service is issued. Upon reset, control again starts in the boot manager. This time, since programming has completed and no programming session is active, the boot manager transfers execution to the application software.

In summary, while the TCU acts as the external tester that initiates and controls the flashing process, the actual programming of flash memory is performed entirely inside the target ECU by the bootloader using the flash driver.

The bootloader is the component that truly programs the ECU. The TCU only orchestrates the process through diagnostic communication.

In the next section, we will look more deeply into bootloader design and implementation details.

---

TECHNICAL AND FACTUAL ANALYSIS

1. Responsibility Split

* Statement that TCU acts as UDS tester and initiator is correct [Verified].
* Statement that actual flashing is performed inside the ECU is correct [Verified].

2. Bootloader Role

* Bootloader identified as the component responsible for erase and write operations via flash driver [Verified].
* Boot manager role in startup decision-making is correctly described [Verified].

3. Flash Driver

* Flash driver described as low-level memory programming component is accurate [Verified].

4. UDS Programming Flow

* Diagnostic Session Control 0x10 0x02 triggering programming mode is correct [Verified].
* Security Access, Request Download, Transfer Data, Transfer Exit mapping to bootloader handling is correct [Verified].

5. Reset Behavior

* Control returning to boot manager after reset is correct [Verified].
* Application execution after successful programming is accurate [Verified].

6. No Incorrect Claims

* No claim that TCU writes ECU flash directly [Verified].
* No confusion between tester responsibility and ECU internal responsibility [Verified].

---

FINAL VERDICT

The rewritten explanation correctly clarifies ECU programming responsibility.
All roles of the TCU, UDS tester, bootloader, boot manager, and flash driver are accurately described and aligned with ISO 14229 and real-world ECU implementations.
No technical inaccuracies were identified.
