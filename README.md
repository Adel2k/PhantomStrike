# ⚠️ PhantomStrike ⚠️

> **DISCLAIMER**  
This tool is created **strictly for educational, academic, and research purposes**. It must **never be deployed outside legal, controlled test environments** such as CTFs, isolated sandboxes, or ethical hacking labs. **Unauthorized use is illegal.**  

**Authors:** Adeline Eminian, Andranik Adyan  
**Date:** April 12, 2025  
**Classification:** Educational | Red Team | Blue Team | Research Use Only

---

## 📖 Overview

**PhantomStrike** is a cross-platform payload delivery framework designed to test system defenses against advanced persistent threat (APT)-style techniques. It simulates real-world attack vectors using vulnerability scanning, reverse shells, anti-forensics, and obfuscation methods — deployed through a Trojanized game or application.

---

## 🚀 Features

- 🔥 Cross-platform support: **Windows, Linux, macOS**
- 🛠️ Vulnerability scanning module targeting open ports, services, and kernel CVEs
- 🐚 Reverse shell capability
- 🎮 Game-based obfuscation and dual-thread payload delivery
- 🎭 Anti-forensics techniques to minimize forensic artifacts
- 📦 Obfuscation methods:
  - String encryption
  - Binary packing
  - Variable name obfuscation
  - Anti-VM and sandbox detection

---

## 🖥️ System Architecture

```mermaid
graph TD
    A[Game/App Launch] --> B[Payload Activation]
    B --> C[Emigrate]
    C --> D[OS & Service Detection]
    D --> E[Vulnerability Scan]
    E --> F[Data Exfiltration to Server]
