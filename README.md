````markdown
# AGELA

## Autonomous Exploit Generation by LLM Agents

AGELA is a multi-agent cybersecurity framework designed to automate key stages of web application security assessment using Large Language Models (LLMs).

Instead of relying on a single LLM, AGELA divides the security assessment workflow into specialized agents. Each agent performs a specific task such as target authorization, reconnaissance, vulnerability knowledge retrieval, attack planning, exploit generation, memory management, validation, and security reporting.

AGELA is designed for authorized penetration testing, cybersecurity education, academic research, controlled laboratories, and deliberately vulnerable applications.

---

## Project Overview

Web application security assessment normally requires multiple tools, manual analysis, vulnerability knowledge, exploit development, validation, and report preparation.

AGELA explores how a coordinated group of specialized LLM agents can automate and connect these stages into a single security assessment pipeline.

The framework follows the workflow:

```text
                    ┌──────────────────────┐
                    │      Target URL      │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Guardrail Agent    │
                    │ Authorization Check  │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │  Supervisor Agent    │
                    │   Task Coordination  │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │     Recon Agent      │
                    │ Application Analysis │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Knowledge Agent    │
                    │ Vulnerability Data   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    Routing Agent     │
                    │   Attack Planning    │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │     Memory Agent     │
                    │ Previous Exploits    │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    Exploit Agent     │
                    │ Payload Generation   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Validation Agent   │
                    │ Verify & Deduplicate │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │     Report Agent     │
                    │ JSON + Markdown      │
                    └──────────────────────┘
````

AGELA also maintains persistent memory of previous exploit attempts so that information from earlier assessments can be retrieved and used during later assessments.

---

## Research Objective

The primary objective of AGELA is to develop and evaluate a multi-agent LLM framework capable of supporting automated web application security assessment.

The project focuses on:

* Automated reconnaissance
* LLM-assisted security analysis
* Vulnerability knowledge retrieval
* Automated attack route planning
* Exploit payload generation
* Exploit result validation
* Persistent exploit memory
* Target authorization and safety controls
* Automated security report generation

---

## Key Features

| Feature              | Description                                                  |
| -------------------- | ------------------------------------------------------------ |
| Target Authorization | Verifies that the target is explicitly authorized            |
| Reconnaissance       | Discovers application forms, inputs, links, and technologies |
| Knowledge Retrieval  | Retrieves relevant vulnerability patterns                    |
| Attack Routing       | Determines suitable attack categories and routes             |
| Exploit Memory       | Retrieves and stores previous exploit information            |
| LLM Reasoning        | Uses local LLMs for analysis and decision support            |
| Exploit Generation   | Generates and tests security payloads                        |
| Validation           | Verifies successful exploit results                          |
| Deduplication        | Groups multiple payloads into unique vulnerability findings  |
| Automated Reporting  | Generates JSON and Markdown reports                          |

---

## System Architecture

AGELA uses a coordinated multi-agent architecture in which specialized agents perform different stages of the security assessment.

<p align="center">
  <img src="docs/agela-architecture.png" alt="AGELA System Architecture" width="100%">
</p>

The architecture connects the authorized target, security agents, local LLM reasoning, vulnerability knowledge, persistent memory, exploit validation, and automated reporting.

---

## Multi-Agent Architecture

AGELA consists of nine specialized agents.

| Agent            | Role                | Main Responsibility                                    |
| ---------------- | ------------------- | ------------------------------------------------------ |
| Guardrail Agent  | Security Control    | Verifies target authorization                          |
| Supervisor Agent | Coordinator         | Coordinates the overall assessment                     |
| Recon Agent      | Reconnaissance      | Identifies application technologies and attack surface |
| Knowledge Agent  | Knowledge Retrieval | Retrieves relevant vulnerability patterns              |
| Routing Agent    | Attack Planning     | Determines suitable attack routes                      |
| Memory Agent     | Persistent Memory   | Retrieves and stores previous exploit information      |
| Exploit Agent    | Exploitation        | Generates and tests exploit payloads                   |
| Validation Agent | Verification        | Validates results and removes duplicate findings       |
| Report Agent     | Reporting           | Generates final JSON and Markdown reports              |

---

## Agent Workflow

### 1. Guardrail Agent

The Guardrail Agent provides the first security control in the pipeline.

It checks whether the supplied target exists in the authorized target configuration.

```text
Target URL
    │
    ▼
Guardrail Agent
    │
    ├── Authorized ──► Continue
    │
    └── Unauthorized ► Stop
```

This prevents the framework from automatically proceeding against targets that have not been explicitly authorized.

---

### 2. Supervisor Agent

The Supervisor Agent analyzes the target and coordinates the overall security assessment.

It uses LLM reasoning to analyze the assessment context and provide high-level guidance to the remaining agents.

---

### 3. Recon Agent

The Recon Agent performs reconnaissance against the authorized target.

It can identify:

* HTTP response status
* Forms
* Input fields
* Links
* Application technologies
* Web server information
* Database information where detectable

Example experimental detection:

```text
CMS       : DVWA
Framework : Apache
Database  : MySQL
```

---

### 4. Knowledge Agent

The Knowledge Agent retrieves vulnerability knowledge based on the target technology and application context.

The knowledge layer provides vulnerability patterns and attack information that can be used by later stages.

Experimental result:

```text
17 vulnerability patterns retrieved
```

---

### 5. Routing Agent

The Routing Agent determines which attack categories should be considered.

For the local DVWA experiment, the base route included:

```text
SQL Injection
Command Injection
XSS Reflected
```

The routing stage expanded this into:

```text
7 planned attacks
```

---

### 6. Memory Agent

The Memory Agent provides persistent memory across assessments.

It retrieves previous exploit attempts and stores newly validated exploit results.

Example experimental result:

```text
SQL Injection     → 3 previous exploits
Command Injection → 3 previous exploits
XSS Reflected     → 3 previous exploits

Total retrieved   → 9 memories
```

The memory system uses ChromaDB for persistent storage.

---

### 7. Exploit Agent

The Exploit Agent generates and tests payloads against the authorized target.

The current research implementation evaluates attack categories including:

```text
SQL Injection
Command Injection
XSS
```

Experimental result:

```text
Total exploit attempts : 13
Successful exploits    : 6
```

The successful results are passed to the Validation Agent.

---

### 8. Validation Agent

The Validation Agent verifies successful exploit results and performs vulnerability deduplication.

For example:

```text
Payload 1 → SQL Injection
Payload 2 → SQL Injection
Payload 3 → SQL Injection
Payload 4 → SQL Injection
```

Instead of reporting four separate vulnerabilities, AGELA groups them into:

```text
One SQL Injection finding
```

Experimental result:

```text
Successful exploit results : 6
Unique confirmed findings  : 2
```

Confirmed findings:

```text
1. SQL Injection
2. XSS Reflected
```

---

### 9. Report Agent

The Report Agent generates the final security assessment report.

Supported report formats:

```text
JSON
Markdown
```

The reports contain information such as:

* Executive summary
* Risk assessment
* Severity breakdown
* Confirmed vulnerabilities
* Payload information
* Evidence
* Successful payload count
* Remediation recommendations

---

## LLM Integration

AGELA uses Ollama as the local LLM backend.

The current configuration supports:

```text
mistral
codellama:13b
llama3.1:8b
```

The default model is:

```text
mistral
```

The LLM is used by multiple agents for tasks including:

```text
Target Analysis
      ↓
Reconnaissance Interpretation
      ↓
Knowledge Analysis
      ↓
Attack Route Planning
      ↓
Exploit Reasoning
      ↓
Validation Analysis
      ↓
Report Generation
```

Using Ollama allows the current implementation to perform LLM-based processing locally.

---

## Technology Stack

| Technology     | Purpose                              |
| -------------- | ------------------------------------ |
| Python         | Core framework implementation        |
| Ollama         | Local LLM runtime                    |
| Mistral        | Default LLM                          |
| Code Llama 13B | Supported LLM                        |
| Llama 3.1 8B   | Supported LLM                        |
| ChromaDB       | Knowledge and memory storage         |
| HTTP Requests  | Web application interaction          |
| JSON           | Configuration and structured reports |
| Markdown       | Human-readable security reports      |

---

## Experimental Environment

AGELA was evaluated in a controlled local cybersecurity laboratory environment.

### Target Application

```text
DVWA
Damn Vulnerable Web Application
```

### Target URL

```text
http://localhost/vulnerabilities/sqli/
```

### Environment

```text
Application : DVWA
Web Server  : Apache
Database    : MySQL
Location    : Localhost
Purpose     : Controlled security testing
```

DVWA was selected because it is intentionally vulnerable and provides a controlled environment for evaluating security-testing techniques.

---

## Experimental Results

The following execution demonstrates a complete AGELA pipeline run against the authorized local DVWA environment.

### AGELA Pipeline Execution

<p align="center">
  <img src="docs/agela-execution.png" alt="AGELA Pipeline Execution" width="100%">
</p>

The screenshot shows the complete execution flow from target authorization through reconnaissance, knowledge retrieval, attack routing, memory retrieval, exploit testing, validation, and report generation.

---

## Experimental Summary

| Metric                              |                Result |
| ----------------------------------- | --------------------: |
| Target Authorization                |            Successful |
| Reconnaissance                      |            Successful |
| Technology Detection                | DVWA / Apache / MySQL |
| Vulnerability Patterns Retrieved    |                    17 |
| Attack Routes Planned               |                     7 |
| Previous Exploit Memories Retrieved |                     9 |
| Exploit Attempts                    |                    13 |
| Successful Exploits                 |                     6 |
| Unique Confirmed Vulnerabilities    |                     2 |

---

## Confirmed Vulnerabilities

The experimental run identified two unique vulnerability categories.

| Vulnerability | AGELA Severity | Successful Payloads |
| ------------- | -------------- | ------------------: |
| SQL Injection | Critical       |                   4 |
| XSS Reflected | Medium         |                   2 |

Multiple successful payloads against the same vulnerability and URL are grouped by the Validation Agent.

This prevents the final report from counting every successful payload as a separate vulnerability.

---

## Generated Security Report

AGELA automatically generates a structured security assessment report.

### Report Preview

<p align="center">
  <img src="docs/agela-report.png" alt="AGELA Generated Security Report" width="100%">
</p>

The generated report provides a human-readable view of the assessment results.

Reports are stored in:

```text
reports/
```

Available formats:

```text
JSON
Markdown
```

Example:

```text
AGELA_Report_YYYYMMDD_HHMMSS.json
AGELA_Report_YYYYMMDD_HHMMSS.md
```

---

## Report Contents

Each generated report can contain:

```text
Report ID
Pipeline ID
Target
Generation Time
Technology Stack
Executive Summary
Risk Assessment
Severity Breakdown
Confirmed Vulnerabilities
Payload Information
Evidence
Successful Payload Count
Remediation Recommendations
```

---

## Severity Methodology

AGELA currently uses framework-configured AGELA Severity Scores.

These values are intended for research and experimental comparison.

They are not official CVSS calculations.

Example:

```text
SQL Injection
Severity    : Critical
AGELA Score : 9.5
CVE         : Not assigned / Not applicable
```

```text
XSS Reflected
Severity    : Medium
AGELA Score : 5.0
CVE         : Not assigned / Not applicable
```

AGELA does not automatically invent CVE identifiers.

When a vulnerability does not have a verified CVE associated with it, the report states:

```text
CVE: Not assigned / Not applicable
```

---

## Target Authorization

AGELA uses an explicit target scope configuration.

The scope file is:

```text
data/scope.json
```

Example:

```json
{
  "authorized_targets": [
    "http://localhost",
    "http://127.0.0.1"
  ],
  "notes": "Only add targets you have explicit written authorization to test."
}
```

The Guardrail Agent checks the target before the security assessment proceeds.

Only targets for which explicit authorization exists should be added to the scope configuration.

---

## Project Structure

```text
AGELA/
│
├── agents/
│   ├── __init__.py
│   ├── exploit_agent.py
│   ├── guardrail_agent.py
│   ├── knowledge_agent.py
│   ├── memory_agent.py
│   ├── recon_agent.py
│   ├── report_agent.py
│   ├── routing_agent.py
│   ├── supervisor_agent.py
│   └── validation_agent.py
│
├── core/
│   ├── __init__.py
│   ├── base_agent.py
│   ├── config.py
│   └── pipeline.py
│
├── data/
│   └── scope.json
│
├── knowledge/
│
├── reports/
│
├── tests/
│
├── docs/
│   ├── agela-architecture.png
│   ├── agela-execution.png
│   └── agela-report.png
│
├── debug.py
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/jadhav1919/AGELA.git
cd AGELA
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Windows Command Prompt:

```cmd
venv\Scripts\activate
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

---

## Ollama Setup

AGELA uses Ollama as its local LLM backend.

Make sure Ollama is installed and running before starting AGELA.

Default model:

```text
mistral
```

Additional configured models:

```text
codellama:13b
llama3.1:8b
```

AGELA expects the local Ollama service at:

```text
http://localhost:11434
```

---

## Configuration

The main configuration file is:

```text
core/config.py
```

Important configuration values include:

```text
OLLAMA_BASE_URL
DEFAULT_MODEL
AVAILABLE_MODELS
CHROMA_DB_PATH
REPORTS_PATH
SCOPE_FILE
AGENT_TIMEOUT
MAX_EXPLOIT_ATTEMPTS
MEMORY_ENABLED
OLLAMA_NUM_THREADS
```

---

## Running AGELA

For a controlled local DVWA environment:

```bash
python main.py "http://localhost/vulnerabilities/sqli/"
```

To specify a model:

```bash
python main.py "http://localhost/vulnerabilities/sqli/" mistral
```

General command format:

```text
python main.py <target-url> <model>
```

The model argument is optional.

---

## Output

After execution, AGELA generates reports under:

```text
reports/
```

Example:

```text
reports/
├── AGELA_Report_YYYYMMDD_HHMMSS.json
└── AGELA_Report_YYYYMMDD_HHMMSS.md
```

The JSON report provides structured data.

The Markdown report provides a human-readable security assessment.

---

## Memory System

AGELA uses ChromaDB to maintain persistent exploit memory.

The memory workflow is:

```text
Previous Assessment
        │
        ▼
Successful Exploit
        │
        ▼
Memory Storage
        │
        ▼
Future Assessment
        │
        ▼
Memory Retrieval
        │
        ▼
Additional Attack Context
```

This allows information from previous assessments to be retrieved during future assessments.

---

## Validation and Deduplication

The Validation Agent plays an important role in reducing duplicate findings.

For example:

```text
SQL Injection
    │
    ├── Successful Payload 1
    ├── Successful Payload 2
    ├── Successful Payload 3
    └── Successful Payload 4
                │
                ▼
       One Unique Finding
```

This allows the report to distinguish between:

```text
Successful Exploit Attempts
```

and:

```text
Unique Vulnerabilities
```

In the experimental run:

```text
Successful Exploits        : 6
Unique Vulnerabilities     : 2
```

---

## Research Contribution

AGELA explores the application of multi-agent LLM architectures to automated cybersecurity assessment.

The central approach is to divide the security-testing workflow into specialized cooperating agents rather than depending on one general-purpose agent.

The framework combines:

```text
Multi-Agent Coordination
          +
LLM Reasoning
          +
Security Knowledge
          +
Persistent Memory
          +
Exploit Generation
          +
Exploit Validation
          +
Authorization Controls
          +
Automated Reporting
```

This architecture provides a foundation for evaluating how specialized LLM agents can cooperate during cybersecurity workflows.

---

## Limitations

AGELA is currently a research prototype.

Current limitations include:

* Testing is primarily focused on controlled web applications.
* LLM-generated reasoning may require human verification.
* Vulnerability confirmation depends on available response-based evidence.
* Severity values are framework-configured rather than formal CVSS calculations.
* Some vulnerability classes require additional specialized detection and validation logic.
* Automated findings should be reviewed before being treated as definitive security conclusions.
* The current implementation is not intended to replace professional penetration-testing tools or human security expertise.

---

## Future Work

Potential future improvements include:

* Formal CVSS calculation
* Additional vulnerability classes
* Improved false-positive detection
* Advanced exploit validation
* Additional LLM model support
* Human-in-the-loop approval
* Improved agent coordination
* Expanded benchmark datasets
* Larger experimental evaluation
* Additional deliberately vulnerable applications
* Improved security report generation
* Production-oriented security controls

---

## Reproducibility

A basic experiment can be reproduced using the following workflow:

```text
1. Install Python
2. Clone the AGELA repository
3. Install project dependencies
4. Install and run Ollama
5. Download a supported LLM
6. Set up a local DVWA instance
7. Add the authorized local target to data/scope.json
8. Run AGELA
9. Review the generated JSON and Markdown reports
```

Example authorized laboratory target:

```text
http://localhost/vulnerabilities/sqli/
```

---

## Project Status

```text
Research Prototype
```

Current implementation status:

```text
[✓] Multi-Agent Architecture
[✓] Target Authorization
[✓] Reconnaissance
[✓] Knowledge Retrieval
[✓] Attack Routing
[✓] Exploit Memory
[✓] Exploit Generation
[✓] Validation
[✓] Vulnerability Deduplication
[✓] Automated Reporting
[✓] JSON Reports
[✓] Markdown Reports
[✓] Local DVWA Evaluation
[✓] Multiple LLM Model Support
```

---

## Ethical and Authorized Use

AGELA is intended only for:

```text
Authorized Penetration Testing
Cybersecurity Research
Academic Projects
Security Education
Controlled Laboratory Environments
Deliberately Vulnerable Applications
```

The framework must not be used against systems without explicit authorization.

The experimental evaluation described in this repository was performed against a local DVWA instance in a controlled environment.

---

## Disclaimer

AGELA is provided for authorized security research, cybersecurity education, academic experimentation, and controlled laboratory environments.

Do not use this framework to test systems without explicit permission.

The authors are not responsible for unauthorized, illegal, or malicious use of this software.

---

## Author

Jadhav Sai

B.Tech — Computer Science and Engineering

Cybersecurity Research Project

GitHub: [https://github.com/jadhav1919](https://github.com/jadhav1919)

```
```
