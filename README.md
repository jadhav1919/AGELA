\# AGELA

\## Autonomous Exploit Generation by LLM Agents



AGELA is a multi-agent cybersecurity framework that uses Large Language Models (LLMs) to support automated security assessment and exploit generation in authorized environments.



The framework combines reconnaissance, vulnerability knowledge retrieval, attack routing, memory, exploit generation, validation, guardrails, supervision, and automated security reporting.



\---



\## Objectives



\- Automate parts of the web application security assessment process.

\- Use LLM agents for reconnaissance and exploit generation.

\- Validate generated exploit results.

\- Maintain memory of previous exploit attempts.

\- Generate structured security reports.

\- Enforce authorized-target restrictions through a guardrail agent.



\---



\## Architecture



AGELA consists of multiple specialized agents:



1\. \*\*Guardrail Agent\*\* — checks whether the target is authorized.

2\. \*\*Supervisor Agent\*\* — analyzes the target and coordinates the assessment.

3\. \*\*Recon Agent\*\* — performs reconnaissance and identifies application technologies.

4\. \*\*Knowledge Agent\*\* — retrieves relevant vulnerability knowledge.

5\. \*\*Routing Agent\*\* — determines the attack route.

6\. \*\*Memory Agent\*\* — retrieves and stores information from previous exploit attempts.

7\. \*\*Exploit Agent\*\* — generates and tests exploit payloads.

8\. \*\*Validation Agent\*\* — validates successful exploit results and removes duplicate findings.

9\. \*\*Report Agent\*\* — generates JSON and Markdown security reports.



\---



\## Technology Stack



\- Python

\- Ollama

\- Large Language Models

\- ChromaDB

\- HTTP-based web testing

\- JSON

\- Markdown



\---



\## Tested Models



AGELA was evaluated using:



\- Mistral

\- Code Llama 13B

\- Llama 3.1 8B



\---



\## Authorized Testing



AGELA is intended only for security testing of systems for which explicit authorization has been obtained.



The current research implementation was tested against \*\*DVWA (Damn Vulnerable Web Application)\*\* running in a local controlled environment.



Example authorized target:



```text

http://localhost/vulnerabilities/sqli/

