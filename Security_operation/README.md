# DARKTRACE-X Security_Operation

## Overview

DARKTRACE-X is a Security Operations Center (SOC) project designed to simulate, collect, normalize, and analyze security telemetry from different attack scenarios.

The project provides a controlled cybersecurity environment for demonstrating attack detection, security event collection, network monitoring, threat intelligence correlation, and security alert analysis.

## Project Objectives

* Simulate common cybersecurity attack scenarios in a controlled environment.
* Collect authentication, network, process, packet, and security alert telemetry.
* Detect suspicious activities using Suricata and Wazuh.
* Normalize security events into a common structure.
* Correlate security events with assets, vulnerabilities, and threat intelligence.
* Replay attack scenarios for repeatable SOC testing.
* Provide a foundation for AI-assisted security alert analysis.

## Architecture

```text
Attack Simulation
       |
       v
Telemetry Generation
       |
       +------------------+
       |                  |
       v                  v
    Suricata            Wazuh
       |                  |
       +--------+---------+
                |
                v
        Alert Collection
                |
                v
           Normalization
                |
                v
       Threat Intelligence
                |
                v
       Security Analysis
                |
                v
        AI Alert Analyzer
```

## Project Components

### attacks

Contains controlled attack simulations used to generate security events.

Included scenarios:

* SSH brute-force simulation
* Successful SSH authentication
* Port scanning
* Web attack simulation
* Delayed compromise simulation

### collectors

Contains components for collecting different types of security telemetry.

* Authentication events
* Network events
* Packet metadata
* Process events
* Security alerts

### firewall

Contains firewall simulation and firewall rule data.

### intelligence

Contains simulated security intelligence used for correlation.

* Asset information
* Threat intelligence indicators
* Vulnerability information

### normalizer

Converts different security events into a common normalized format for analysis.

### replay

Provides repeatable attack-scenario replay functionality for testing the SOC pipeline.

### scripts

Contains project utility scripts for:

* Demo data generation
* Environment health checking
* Environment reset
* SOC startup

### suricata

Contains Suricata configuration and custom detection rules.

### telemetry

Contains controlled sample security telemetry including:

* Authentication logs
* Network events
* Packet metadata
* Process events
* Server logs

### wazuh

Contains project-level Wazuh configuration placeholders and custom rule/decoder locations.

The live Wazuh Manager configuration is maintained separately on the SOC infrastructure and is not committed with sensitive machine-specific configuration.

## Attack Scenarios

The project supports repeatable scenarios such as:

```text
Port Scan
    |
    v
Network Detection
    |
    v
Security Alert
```

```text
SSH Brute Force
    |
    v
Authentication Events
    |
    v
Detection
    |
    v
Alert Normalization
```

```text
Web Attack
    |
    v
Web Server Events
    |
    v
Detection
    |
    v
Security Analysis
```

```text
Delayed Compromise
    |
    v
Initial Activity
    |
    v
Follow-up Activity
    |
    v
Correlation
    |
    v
Incident Analysis
```

## Technologies

* Linux
* Python
* Wazuh
* Suricata
* Git
* GitHub
* JSON
* Security telemetry
* Threat intelligence
* MITRE ATT&CK mapping

## Security Approach

This project is intended for controlled cybersecurity testing and educational SOC development.

All attack simulations and telemetry are designed to operate within an authorized laboratory environment.

## Repository Structure

```text
soc/
├── attacks/
├── collectors/
├── firewall/
├── intelligence/
├── normalizer/
├── replay/
├── scripts/
├── suricata/
├── telemetry/
├── wazuh/
└── README.md
```

## Future Integration

The SOC component is designed to integrate with the broader DARKTRACE-X platform.

The planned pipeline is:

```text
Wazuh / Suricata
       |
       v
Alert Collection
       |
       v
Normalization
       |
       v
Backend
       |
       v
AI Alert Analyzer
       |
       v
Investigation
       |
       v
Response / Approval
       |
       v
Audit
```

## Status

SOC telemetry generation, attack simulation, normalization, Suricata rules, replay scenarios, threat intelligence data, and supporting scripts are implemented for controlled testing.

The component can be integrated with the project's backend, AI analyzer, and frontend dashboard.
