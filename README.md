<h1 align="center">Automotive OTA</h1>

<p align="center">
  <img alt="Status" src="https://img.shields.io/badge/status-active-success" />
  <img alt="License" src="https://img.shields.io/badge/license-MIT-blue" />
  <img alt="Python" src="https://img.shields.io/badge/python-3.10%2B-blue" />
  <img alt="Docker" src="https://img.shields.io/badge/docker-required-2496ED" />
  <img alt="SDV" src="https://img.shields.io/badge/domain-Software%20Defined%20Vehicle-orange" />
  <img alt="Security" src="https://img.shields.io/badge/security-Uptane%20%7C%20Ed25519-critical" />
  <img alt="MkDocs" src="https://img.shields.io/badge/docs-MkDocs-526CFE" />
  <img alt="PDF" src="https://img.shields.io/badge/output-PDF-informational" />
  <img alt="GitHub Actions" src="https://img.shields.io/badge/CI-GitHub%20Actions-2088FF" />
  <img alt="GitHub Workflow" src="https://img.shields.io/badge/workflows-enabled-brightgreen" />
  <img alt="GitHub Pages" src="https://img.shields.io/badge/deploy-GitHub%20Pages-222222" />
</p>

<p align="center">
A high-fidelity Over-The-Air simulation and knowledge base for Software Defined Vehicles.
</p>

This repository combines:

- A **working OTA system prototype** that models real-world automotive update flows.
- A **deep technical documentation site** covering architecture, security, and regulation.

The goal is precision over abstraction: this project favors realistic constraints, explicit tradeoffs, and standards-aligned design.

---

## What This Project Is (and Is Not)

**This is**:

- A realistic OTA update simulation inspired by production automotive systems.
- A reference implementation for A/B updates, delta delivery, and cryptographic verification.
- A structured learning resource for OTA, SDV architecture, and compliance.

**This is not**:

- A production-ready OTA backend.
- A vendor-specific implementation.
- A simplified demo that ignores safety or security edge cases.

---

## Repository Structure

```bash
.
├── simulator/        # Executable OTA system simulation
│   ├── backend       # OTA server and campaign logic
│   ├── vehicle       # ECU, gateway, and update agent simulation
│   └── ui            # Head Unit dashboard
│
├── webpage/          # Documentation website source
│   ├── docs          # Markdown-based technical content
│   └── mkdocs.yml    # Site configuration
│
└── README.md

```

### Simulator

A containerized OTA system prototype.

**Core features**

- A/B dual-bank firmware updates
- Delta compression using `bsdiff`
- Cryptographic signing and verification (Ed25519)
- Simulated CAN bus via UDP multicast
- Campaign-based update orchestration
- Head Unit dashboard for observability and control

**Technology**

- Python, Flask
- Docker / Docker Compose
- python-can
- Cryptography libraries

## Webpage

A full documentation site explaining the theory behind the simulation.

**Coverage**

- OTA fundamentals (SOTA vs FOTA)
- Vehicle and ECU architecture
- OTA backend and cloud design
- Update protocols (UDS, MQTT, HTTP, CAN)
- Security models (Uptane, TUF, threat analysis)
- Regulatory compliance (UN R155, UN R156)

**Technology**

- MkDocs
- Material for MkDocs

---

## Getting Started

### Run the OTA Simulation

**Requirements**

- Docker Desktop

```bash
cd simulator
docker compose up --build
```

**Access**

* OTA Dashboard: [http://localhost:8080](http://localhost:8080)

From the dashboard you can:

* Inspect vehicle state
* Trigger firmware campaigns
* Observe update phases and failures

For architecture details, failure modes, and testing scenarios, see:

```
simulator/README.md
```

---

### View the Documentation Locally

**Requirements**

* Python 3.10+

```bash
pip install -r requirements-docs.txt
mkdocs serve
```

**Access**

* Documentation site: [http://localhost:8000](http://localhost:8000)

---

## Design Principles

* **Safety-first updates**: No in-place flashing, always recoverable.
* **Explicit trust chains**: No implicit security assumptions.
* **Standards-aligned**: Uptane, TUF, UDS, and ISO concepts where applicable.
* **Observable systems**: Update state is inspectable at every step.
* **Educational clarity**: Every abstraction exists for a reason.

---

## Regulatory Context

The system and documentation explicitly reference:

* UN Regulation No. 155 (Cybersecurity)
* UN Regulation No. 156 (OTA Updates)

These are treated as engineering constraints, not paperwork.

---

## Intended Audience

* Automotive software engineers
* Embedded and backend developers entering SDV
* Security engineers studying OTA threat models
* Technical leads evaluating OTA architecture tradeoffs
