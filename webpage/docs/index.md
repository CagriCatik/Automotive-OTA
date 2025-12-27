# Over-the-Air

**Fundamentals**

- [Introduction](01_introduction/01_intro.md)
    - [Definition](01_introduction/02_definition.md)
    - [Importance](01_introduction/03_importance.md)
    - [SOTA vs FOTA](01_introduction/04_sota-fota.md)
    - [Challenges](01_introduction/05_challenges.md)
    - [OTA Services](01_introduction/06_ota_services.md)
    - [Market Analysis](01_introduction/07_market-analysis.md)
    - [How OTA Works](01_introduction/08_how-ota.md)

**Architecture**

- [Core Architecture](02_core_architecture/02_architecture.md)
    - [Vehicle State](02_core_architecture/01_vehicle_state.md)
    - [Architecture](02_core_architecture/02_architecture.md)
    - [Vehicle Architecture](02_core_architecture/03_vehicle_architecture.md)
- [OTA Backend](03_ota-backend/01_oem-backend.md)
    - [Cloud Providers](03_ota-backend/02_cloud-providers.md)
    - [Campaign Management](03_ota-backend/03_campaign-management.md)
- [User Experience](04_user-experience/01_hmi.md)
    - [HMI](04_user-experience/01_hmi.md)
    - [OEM App](04_user-experience/02_oem-app.md)

**Vehicle And TCU**

- [OEM Backend and TCU](05_oem-backend-tcu/01_mqtt.md)
    - [MQTT](05_oem-backend-tcu/01_mqtt.md)
    - [MQTT Connectivity](05_oem-backend-tcu/02_mqtt-connectivity.md)
    - [HTTPS](05_oem-backend-tcu/03_https.md)
- [TCU](06_tcu/01_ota-manager.md)
    - [OTA Manager](06_tcu/01_ota-manager.md)
    - [UDS Tester](06_tcu/02_uds-tester.md)

**Target Device**

- [Diagnostics And Transport](07_target-device/01_uds-can-eth.md)
    - [UDS on CAN/ETH](07_target-device/01_uds-can-eth.md)
    - [UDS on CAN](07_target-device/03_uds-can.md)
    - [DoIP](07_target-device/04_doip.md)
    - [DoIP External](07_target-device/05_doip-external.md)
- [Platform](07_target-device/02_autosar.md)
    - [AUTOSAR](07_target-device/02_autosar.md)
    - [Bootloader](07_target-device/06_bootloader.md)
    - [Memory](07_target-device/07_target-device-memory.md)
    - [Fail-Safe Strategy](07_target-device/08_fail-safe-strategy.md)

**Testing And Security**

- OTA Testing
    - [Intro](08_ota-testing/01_intro.md)
    - [Methods](08_ota-testing/02_methods.md)
    - [Tool Chain](08_ota-testing/03_tool-chain.md)
- Use Cases
    - [Intro](09_usecase/01_intro.md)
    - [Remote Diagnostics](09_usecase/02_remote-diagnostics.md)
- Attacks
    - [Intro](11_possible-attacks-ota/01_intro.md)
    - [Eavesdropping](11_possible-attacks-ota/02_eavesdrop.md)
    - [Denial of Service](11_possible-attacks-ota/03_denial.md)
    - [Rollback](11_possible-attacks-ota/04_rollback.md)
    - [Injection](11_possible-attacks-ota/05_injection.md)
- Measures
    - [Protection Eavesdropping](12_possible-measures/01_protection-eavesdrop.md)
    - [Protection DoS](12_possible-measures/02_protection-dos.md)
    - [Protection Rollback](12_possible-measures/03_protection-rollback.md)

**Standards And SDV**

- [SDV](13_sdv/01_intro.md)
    - [Intro](13_sdv/01_intro.md)
    - [High Level Arch](13_sdv/02_high-level-architecture.md)
    - [Market Players](13_sdv/03_market-players.md)
    - [Level 1](13_sdv/04_level1.md)
    - [Level 2](13_sdv/06_level2.md)
    - [Level 3](13_sdv/07_level3.md)
    - [Level 4](13_sdv/08_level4.md)
    - [Level 5](13_sdv/09_level5.md)
- [UNECE R156](14_unece-r156/01_sums.md)
    - [SUMS](14_unece-r156/01_sums.md)
    - [Rollback](14_unece-r156/02_rollback.md)

**Questions**

- [Intro](15_questions/01_intro.md)
