# AGELA

## Autonomous Exploit Generation by LLM Agents

AGELA is a multi-agent cybersecurity framework designed to automate key stages of web application security assessment using Large Language Models (LLMs).

Instead of relying on a single LLM, AGELA divides the security assessment workflow into specialized agents. Each agent performs a specific task such as target authorization, reconnaissance, vulnerability knowledge retrieval, attack planning, exploit generation, memory management, validation, and security reporting.


## Project Overview

Web application security assessment normally requires multiple tools, manual analysis, vulnerability knowledge, exploit development, validation, and report preparation.

AGELA explores how a coordinated group of specialized LLM agents can automate and connect these stages into a single security assessment pipeline.

## Multi-Agent Architecture

### AGELA consists of nine specialized agents.
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


### Experimental Environment

AGELA was evaluated in a controlled local cybersecurity laboratory environment.

#### Target Application
DVWA
Damn Vulnerable Web Application
### Target URL
http://localhost/vulnerabilities/sqli/
### Environment
Application : DVWA
Web Server  : Apache
Database    : MySQL
Location    : Localhost
Purpose     : Controlled security testing

##### DVWA was selected because it is intentionally vulnerable and provides a controlled environment for evaluating security-testing techniques.

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
├── docs/
│   ├── agela-architecture.png
│   ├── agela-execution.png
│   └── agela-report.png
│
├── knowledge/
│
├── reports/
│
├── tests/
│
├── debug.py
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```


## Installation

## 1. Clone the Repository
git clone https://github.com/jadhav1919/AGELA.git
cd AGELA
## 2. Create a Virtual Environment
python -m venv venv
## 3. Activate the Virtual Environment

Windows PowerShell:
```bash

.\venv\Scripts\Activate.ps1
```

Windows Command Prompt:
```bash
venv\Scripts\activate
```
## 4. Install Dependencies
python -m pip install -r requirements.txt


## Ollama Setup

AGELA uses Ollama as its local LLM backend.

Make sure Ollama is installed and running before starting AGELA.

Default model:

mistral

Additional supported models:

codellama:13b
llama3.1:8b

AGELA expects the local Ollama service at:

http://localhost:11434



## Running AGELA

For the controlled local DVWA environment:

```bash
python main.py "http://localhost/vulnerabilities/sqli/"
```

To specify a model:
```bash

python main.py "http://localhost/vulnerabilities/sqli/" mistral
```

General command format:
```bash

python main.py <target-url> <model>
```

The model argument is optional.


## Limitations

AGELA is currently a research prototype.

Current limitations include:

Testing is primarily focused on controlled web applications.
LLM-generated reasoning may require human verification.
Vulnerability confirmation depends on available response-based evidence.
Severity values are framework-configured rather than formal CVSS calculations.
Some vulnerability classes require additional specialized detection and validation logic.
Automated findings should be reviewed before being treated as definitive security conclusions.
The current implementation is not intended to replace professional penetration-testing tools or human security expertise.

# Author

Jadhav Sai

B.Tech — Computer Science and Engineering

Cybersecurity Research Project

GitHub: https://github.com/jadhav1919


