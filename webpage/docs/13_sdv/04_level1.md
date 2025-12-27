# Software Defined Vehicle Level 1

As the automotive industry transitions towards Software Defined Vehicles (SDVs), it becomes imperative to establish standardized levels that categorize the progression and capabilities of these technologically advanced vehicles. This classification mirrors the historical approach taken with Advanced Driver Assistance Systems (ADAS), where defining levels from basic assistance to full automation provided clarity and uniformity across manufacturers and stakeholders. Similarly, categorizing SDV levels facilitates a structured understanding of the evolution, implementation, and capabilities of software-centric vehicle functionalities.

## Importance of Categorizing SDV Levels

### Historical Context: ADAS Levels

Approximately fifteen years ago, ADAS emerged as a significant advancement in vehicle safety and automation. Early ADAS implementations varied widely across manufacturers, each offering different definitions and feature sets. This lack of standardization led to confusion and hindered the broader adoption of these technologies. To address this, the automotive industry adopted a tiered classification system, delineating ADAS capabilities from Level 0 (no assistance) to Level 5 (full automation). This structured approach enabled manufacturers, regulators, and consumers to have a common framework for understanding and evaluating ADAS functionalities.

### Parallel Necessity for SDV Levels

In the wake of ADAS, the emergence of SDVs brings forth a similar need for standardized levels. As manufacturers increasingly integrate software-driven features into vehicles, categorizing these advancements ensures:

1. **Consistency:** Establishes uniform benchmarks for SDV capabilities across different manufacturers.
2. **Clarity:** Provides a clear progression path for consumers and industry stakeholders to understand the evolution of vehicle software functionalities.
3. **Regulatory Alignment:** Aids in the formulation of regulations and safety standards tailored to each SDV level.
4. **Development Roadmap:** Guides manufacturers in the phased development and implementation of SDV features.

## SDV Levels Overview

The categorization of SDV levels typically ranges from Level 0 to Level 5, analogous to the ADAS framework. Each level represents a distinct stage in the software integration and automation capabilities of the vehicle.

### Level 0: No SDV Functionality

- **Description:** Vehicles operate without any software-defined functionalities. All controls and features are managed manually without any digital assistance or connectivity.
- **Features:** Traditional mechanical controls, no internet connectivity, no remote features.

### Level 1: Basic SDV Integration

#### Transitioning from Traditional Vehicles to SDV Level 1

Level 1 SDV marks the initial stage of integrating software-defined functionalities into traditional vehicle architectures. This level focuses on establishing basic internet connectivity and enabling rudimentary remote controls without extensive over-the-air (OTA) update capabilities.

#### Key Features of SDV Level 1

1. **Basic Internet Connectivity:**
   - Establishes a foundational link between the vehicle and external networks.
   - Enables communication between the vehicle and smartphones or remote devices.

2. **Remote Control of Essential Features:**
   - **Climate Control Activation:** Users can remotely activate or deactivate climate control systems.
   - **Engine Start/Stop:** Allows remote initiation or termination of the vehicle's engine.
   - **Basic Security Features:** Remote locking/unlocking and vehicle tracking.

3. **Limited Remote Interactions:**
   - Only essential and non-critical controls are managed remotely.
   - No comprehensive OTA update capabilities for Electronic Control Units (ECUs).

4. **Third-Party Application Integration:**
   - Applications developed by third parties can interact with vehicle systems to perform specific actions.
   - Examples include remote activation of climate control via smartphone apps.

#### Example Implementations

- **Hyundai Bluelink:**
  - **Features:** Vehicle identification, "Find My Vehicle," geofencing, vehicle status monitoring, and health reporting.
  - **Functionality:** Allows users to perform basic remote operations such as locating the vehicle, monitoring its status, and receiving health reports.

- **Tesla Mobile Application:**
  - **Features:** Remote climate control, vehicle location tracking, and basic vehicle status updates.
  - **Functionality:** Users can activate air conditioning remotely, locate their vehicle on a map, and monitor essential vehicle metrics.

- **BMW Connected Apps:**
  - **Features:** Remote start/stop, climate control, vehicle status monitoring, and basic security functions.
  - **Functionality:** Enables users to control specific vehicle functions remotely through dedicated BMW applications.

#### Technical Considerations for SDV Level 1

Implementing Level 1 SDV functionalities necessitates robust security measures to safeguard against unauthorized access and ensure data integrity. Key security elements include:

1. **Encryption:**
   - **Purpose:** Protects data transmission between the vehicle and external devices.
   - **Implementation:** Utilizes advanced encryption standards (AES) to secure communication channels.
   ```python
   from Crypto.Cipher import AES
   import base64

   def encrypt_data(data, key):
       cipher = AES.new(key, AES.MODE_EAX)
       nonce = cipher.nonce
       ciphertext, tag = cipher.encrypt_and_digest(data.encode('utf-8'))
       return base64.b64encode(nonce + ciphertext).decode('utf-8')

   # Example usage
   encrypted = encrypt_data("Activate Climate Control", "ThisIsASecretKey")
   print(encrypted)
   ```

2. **Software Integrity:**
   - **Purpose:** Ensures that the software interacting with vehicle systems remains unaltered and free from malicious code.
   - **Implementation:** Incorporates integrity checks and validation mechanisms to verify software authenticity.
   ```bash
   # Example: Shell commands for verifying software integrity
   sha256sum /vehicle/system/update_v1.0.bin
   # Compare the output with the expected hash value
   ```

3. **Firewalls:**
   - **Purpose:** Acts as a barrier to prevent unauthorized access to vehicle networks and systems.
   - **Implementation:** Deploys robust firewall configurations to filter incoming and outgoing traffic.
   ```yaml
   # Example: YAML configuration for firewall rules
   firewall:
     rules:
       - name: Allow_Remote_Climate_Control
         protocol: TCP
         port: 443
         action: allow
       - name: Block_Untrusted_Services
         protocol: any
         port: any
         action: block
   ```

#### Example Code Snippet: Remote Climate Control Activation

```javascript
// JavaScript code for activating climate control via a cloud API
const axios = require('axios');

async function activateClimateControl(vehicleId, temperature) {
    try {
        const response = await axios.post(`https://api.oem.com/vehicles/${vehicleId}/climate`, {
            temperature: temperature,
            mode: 'AUTO'
        }, {
            headers: {
                'Authorization': `Bearer YOUR_ACCESS_TOKEN`
            }
        });
        console.log('Climate control activated:', response.data);
    } catch (error) {
        console.error('Error activating climate control:', error);
    }
}

// Example usage
activateClimateControl('VEH12345', 22.5);
```

#### Infrastructure Components for SDV Level 1

1. **Smartphone Integration:**
   - Acts as the primary interface for users to interact with the vehicle remotely.
   - Hosts dedicated applications that facilitate remote control and monitoring.

2. **Cloud Setup:**
   - Serves as the intermediary between the smartphone applications and the vehicle's control units.
   - Manages data transmission, authentication, and execution of remote commands.

3. **Vehicle Control Units:**
   - **Infotainment Systems:** Interface with cloud services to receive and execute remote commands.
   - **Electronic Control Units (ECUs):** Handle specific vehicle functions such as climate control and engine management based on received commands.

#### Example Code Snippet: Smartphone Application Trigger Integration

```python
import requests

def trigger_vehicle_feature(vehicle_id, feature, action):
    api_url = f"https://api.oem.com/vehicles/{vehicle_id}/{feature}"
    payload = {'action': action}
    headers = {'Authorization': 'Bearer YOUR_ACCESS_TOKEN'}

    response = requests.post(api_url, json=payload, headers=headers)
    if response.status_code == 200:
        print(f"{feature.capitalize()} {action}d successfully.")
    else:
        print(f"Failed to {action} {feature}: {response.text}")

# Example usage
trigger_vehicle_feature('VEH12345', 'climate', 'activate')
```

## Security Considerations for SDV Level 1

Ensuring the security and integrity of SDV Level 1 functionalities is paramount. As vehicles become more connected and reliant on software, robust security measures are essential to prevent unauthorized access and potential system compromises.

### Encryption

- **Purpose:** Protects data transmitted between the vehicle and external devices, such as smartphones and cloud services.
- **Implementation:** Utilizes industry-standard encryption algorithms (e.g., AES) to secure data packets.
  
  ```python
  from Crypto.Cipher import AES
  import base64

  def encrypt_data(data, key):
      cipher = AES.new(key, AES.MODE_EAX)
      nonce = cipher.nonce
      ciphertext, tag = cipher.encrypt_and_digest(data.encode('utf-8'))
      return base64.b64encode(nonce + ciphertext).decode('utf-8')

  # Example usage
  encrypted = encrypt_data("Activate Climate Control", "ThisIsASecretKey")
  print(encrypted)
  ```

### Software Integrity

- **Purpose:** Ensures that the software controlling vehicle functionalities remains unaltered and secure from malicious interventions.
- **Implementation:** Implements integrity checks using hashing algorithms and digital signatures to verify software authenticity.

  ```bash
  # Example: Shell commands for verifying software integrity
  sha256sum /vehicle/system/update_v1.0.bin
  # Compare the output with the expected hash value
  ```

### Firewalls

- **Purpose:** Acts as a protective barrier to prevent unauthorized access and control over vehicle systems.
- **Implementation:** Configures firewall rules to allow only trusted connections and block potentially harmful traffic.

  ```yaml
  # Example: YAML configuration for firewall rules
  firewall:
    rules:
      - name: Allow_Remote_Climate_Control
        protocol: TCP
        port: 443
        action: allow
      - name: Block_Untrusted_Services
        protocol: any
        port: any
        action: block
  ```

## Summary of SDV Level 1

SDV Level 1 represents the foundational stage of software-defined functionalities in vehicles, transitioning from purely mechanical controls to basic software-driven interactions. By enabling essential remote controls and establishing internet connectivity, Level 1 SDVs enhance user convenience and vehicle interactivity. However, the absence of comprehensive OTA update capabilities limits the scope of software-driven enhancements. Ensuring robust security measures, including encryption, software integrity checks, and firewall protections, is crucial to safeguarding these early-stage SDV functionalities against potential cyber threats.

## Conclusion

Categorizing SDV levels is a critical step in structuring the evolution of software-defined functionalities within the automotive industry. Drawing parallels from the ADAS levels, SDV levels provide a standardized framework that facilitates consistent development, implementation, and evaluation of vehicle software capabilities. SDV Level 1, with its basic internet connectivity and remote control features, marks the beginning of this transformative journey. As manufacturers progress through higher SDV levels, they will unlock more advanced functionalities, enhanced automation, and comprehensive OTA update mechanisms, all while maintaining stringent security and safety standards. Establishing these levels not only aids in technological advancement but also ensures that the integration of software within vehicles is systematic, secure, and aligned with consumer expectations and regulatory requirements.