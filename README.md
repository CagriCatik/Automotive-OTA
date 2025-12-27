# Automotive OTA Update

This repository serves as a comprehensive resource for understanding, simulating, and implementing secure Firmware-Over-The-Air (FOTA) systems for Software Defined Vehicles (SDV).

It combines a **high-fidelity technical simulation** with **extensive educational documentation**.

## Project Structure

This project is divided into two main components:

- **[`simulator/`](simulator/)**: A working prototype of an OTA system.
    - **Features**: A/B Dual-Bank updates, Delta compression (`bsdiff`), Simulated CAN Bus (UDP Multicast), Ed25519 Security, and a Head Unit UI.
    - **Tech Stack**: Python, Flask, Docker, Python-CAN.
- **[`webpage/`](webpage/)**: The source code for the project's documentation website.
    - **Content**: Covers OTA fundamentals, Vehicle Architecture, Backend/Cloud infrastructure, Security (Uptane/Theupdateframework), and Regulatory compliance (UN R155/R156).
    - **Tech Stack**: MkDocs, Material for MkDocs.

---

## Getting Started

### 1. Running the Simulation
Experience the update process yourself using the Docker-based simulation.

**Prerequisites**: [Docker Desktop](https://www.docker.com/products/docker-desktop/)

```bash
cd simulator
docker compose up --build
```

- **Dashboard**: Open [http://localhost:8080](http://localhost:8080) to control the vehicle and trigger updates.
- **Details**: See [`simulator/README.md`](simulator/README.md) for deeper architectural details and testing guides.

### 2. Viewing the Documentation
To view the full theoretical documentation locally:

**Prerequisites**: Python 3.x

```bash
# Install dependencies
pip install -r requirements-docs.txt

# Serve the documentation site
mkdocs serve
```

- **Access**: Open [http://localhost:8000](http://localhost:8000) to browse the documentation.

---

## Documentation Overview

The documentation (in `webpage/`) is structured to guide you from basics to advanced topics:

- **Fundamentals**: SOTA vs FOTA, Market Analysis.
- **Architecture**: Vehicle State, ECUs, Gateways.
- **Backend**: Cloud Providers, Campaign Management.
- **Protocols**: UDS, MQTT, HTTP, CAN.
- **Security**: Threat Analysis, Defense Layers, Compliance.
