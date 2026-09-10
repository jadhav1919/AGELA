# AGELA

## Autonomous Exploit Generation by LLM Agents

AGELA is a multi-agent cybersecurity framework designed to automate key stages of web application security assessment using Large Language Models (LLMs).

Instead of relying on a single LLM, AGELA divides the security assessment workflow into specialized agents. Each agent performs a specific task such as target authorization, reconnaissance, vulnerability knowledge retrieval, attack planning, exploit generation, memory management, validation, and security reporting.


## Project Overview

Web application security assessment normally requires multiple tools, manual analysis, vulnerability knowledge, exploit development, validation, and report preparation.

AGELA explores how a coordinated group of specialized LLM agents can automate and connect these stages into a single security assessment pipeline.

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

## System Architecture



