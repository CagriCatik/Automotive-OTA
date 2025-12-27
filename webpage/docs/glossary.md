# Glossary

## A

### Active Bank

The bank of flash memory that is currently in use and running the active firmware. In a dual-bank system, the active bank is the one that is executing the current version of the firmware.

## B

### Bootloader

The software component responsible for managing the ECU's firmware updates and ensuring the system's reliability and security. It is responsible for loading the active firmware into memory and executing it, as well as handling the update process and recovery from failures.

## C

### Campaign

A group of vehicles that are scheduled to receive an OTA update. Each campaign is defined by a set of parameters, such as the target vehicle model, the update content, and the update schedule.    

## D

### Device

An ECU that is part of a vehicle and is responsible for executing the firmware and handling the communication with the backend.    

### Dual-Bank

An ECU firmware update strategy in which two separate flash memory regions are maintained: one active bank running the current firmware and one inactive bank used for staging an update. The new firmware is written and validated in the inactive bank before switching execution to it. If the new firmware fails to boot or pass health checks, the ECU can revert to the previous bank. This approach increases reliability and update safety at the cost of additional memory and more complex bootloader logic.

## E

### ECU

An Electronic Control Unit (ECU) is a specialized computer system that controls various functions of a vehicle, such as engine management, transmission control, and safety systems. ECUs are typically embedded systems that use specialized hardware and software to perform their functions. They are often responsible for executing firmware and handling communication with other ECUs and the vehicle's network.

## F

### Flash Memory

A non-volatile memory (NVM) that stores data persistently, even when the power is off. Flash memory is commonly used in embedded systems to store firmware, configuration data, and other critical information.

### Firmware

A set of instructions and data that control the behavior of an ECU. Firmware is typically stored in flash memory and is executed by the ECU's processor.

## G

### Gateway

A device that acts as an intermediary between two or more networks, allowing communication between them. In the context of vehicle networks, a gateway is typically used to connect different communication protocols and networks, such as CAN and Ethernet.

## H

### Health Checks

A set of tests that verify the integrity and functionality of the firmware. Health checks are typically performed at boot time and during runtime to ensure that the firmware is operating correctly.

## I

### ISO 26262

The International Organization for Standardization (ISO) 26262 is an international standard for functional safety of electrical and electronic systems in production automobiles. It provides guidelines for the development, production, and maintenance of safe automotive systems.

## J

### J1939

J1939 is a communication protocol used in heavy-duty trucks and agricultural equipment. It is a message-based protocol that allows devices to exchange data and control information over a network.

## K



## L



## M

### Message

A unit of data that is transmitted over a communication channel. In the context of vehicle networks, messages are typically used to exchange data and control information between devices.

## N

### Network

A communication system that allows devices to exchange data and information over a physical or wireless medium. In the context of vehicle networks, a network is typically used to connect different communication protocols and networks, such as CAN and Ethernet.

## O

### OTA

Over-the-Air (OTA) is a technology that allows devices to receive and install software updates wirelessly, without the need for physical access to the device.

## P

### Protocol

A set of rules and procedures that define how devices communicate with each other. In the context of vehicle networks, protocols are typically used to define the format and structure of messages and the rules for their exchange.

## Q

### QoS

Quality of Service (QoS) is a set of parameters that define the quality of a communication service. In the context of vehicle networks, QoS is typically used to define the priority and reliability of messages and the rules for their exchange.

## R

### Remote Diagnostics

Remote diagnostics is a feature that allows a vehicle to be diagnosed and monitored remotely. It is typically used to identify and resolve issues with the vehicle's systems and components, as well as to monitor the vehicle's performance and health.

## S

### Single-Bank

An ECU firmware update strategy in which a single flash memory region is used to store the active firmware. During an OTA update, the existing firmware is erased and overwritten in place. If the update process is interrupted or validation fails, the ECU may become unbootable, as no fallback firmware is available. This approach minimizes memory usage and hardware cost but provides limited fault tolerance.


## T

### Target Device

The device that is being updated. In the context of OTA updates, the target device is typically an ECU that is part of a vehicle and is responsible for executing the firmware and handling the communication with the backend.

## U

### Update

An update is a set of instructions and data that are used to modify the behavior of an ECU. Updates are typically stored in flash memory and are executed by the ECU's processor.

## V


## W

## X

## Y

## Z