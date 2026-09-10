from core.base_agent import BaseAgent


class KnowledgeAgent(BaseAgent):
    """
    Knowledge Agent — retrieves relevant vulnerability knowledge.
    Uses local built-in knowledge base of CVEs and OWASP Top 10.
    No internet required — all knowledge is built in.
    """

    def __init__(self, model: str = "mistral"):
        super().__init__(name="KnowledgeAgent", model=model)

        self.knowledge_base = {
            "PHP": [
                "SQL Injection via unsanitized GET/POST parameters",
                "Remote Code Execution via file upload vulnerabilities",
                "Local File Inclusion (LFI) via path traversal",
                "XSS via unsanitized output in HTML context",
                "CSRF on forms without token validation",
                "Session fixation and session hijacking"
            ],
            "WordPress": [
                "Plugin vulnerabilities — check outdated plugins",
                "XML-RPC brute force and enumeration",
                "User enumeration via /wp-json/wp/v2/users",
                "SQL Injection in vulnerable plugins",
                "File upload bypass in vulnerable themes"
            ],
            "DVWA": [
                "SQL Injection — login and search forms",
                "Blind SQL Injection — boolean and time-based",
                "Reflected XSS — name and search parameters",
                "Stored XSS — comment and message fields",
                "CSRF — change password form",
                "Command Injection — ping utility",
                "File Inclusion — LFI and RFI",
                "File Upload — unrestricted file upload"
            ],
            "Apache": [
                "Directory traversal",
                "Server-side includes injection",
                "HTTP verb tampering"
            ],
            "generic": [
                "SQL Injection on all input fields",
                "Cross-Site Scripting (XSS) on all output",
                "CSRF on all state-changing forms",
                "Insecure Direct Object Reference (IDOR)",
                "Security misconfiguration",
                "Broken access control"
            ]
        }

    def get_relevant_knowledge(self, tech_stack: dict) -> list:
        """Get vulnerabilities relevant to detected tech stack"""
        vulnerabilities = []

        for tech_type, tech_value in tech_stack.items():
            if tech_value in self.knowledge_base:
                vulnerabilities.extend(self.knowledge_base[tech_value])
                self.log(f"Found knowledge for: {tech_value}")

        vulnerabilities.extend(self.knowledge_base["generic"])

        # Remove duplicates
        seen        = set()
        unique_vulns = []
        for v in vulnerabilities:
            if v not in seen:
                seen.add(v)
                unique_vulns.append(v)

        return unique_vulns

    def run(self, context: dict) -> dict:
        self.log("Retrieving vulnerability knowledge")

        tech_stack = context.get("recon", {}).get("tech_stack", {})
        forms      = context.get("recon", {}).get("forms", [])

        vulnerabilities = self.get_relevant_knowledge(tech_stack)
        self.log(f"Retrieved {len(vulnerabilities)} vulnerability patterns")

        system_prompt = """You are a cybersecurity expert with deep knowledge
of web application vulnerabilities. Given reconnaissance data and a list
of potential vulnerabilities, create a prioritized attack plan."""

        prompt = f"""
Given this information about the target:

Tech stack detected: {tech_stack}
Forms found: {len(forms)}
Form inputs: {[inp for form in forms for inp in form.get('inputs', [])]}

And these potential vulnerabilities:
{chr(10).join(f"- {v}" for v in vulnerabilities)}

Create a prioritized list of the TOP 5 vulnerabilities to test first.
For each one, explain WHY it is likely to succeed on this target.

Format:
1. [VULNERABILITY NAME] — [reason it will likely work]
2. [VULNERABILITY NAME] — [reason it will likely work]
3. [VULNERABILITY NAME] — [reason it will likely work]
4. [VULNERABILITY NAME] — [reason it will likely work]
5. [VULNERABILITY NAME] — [reason it will likely work]
"""

        prioritized = self.think(prompt, system_prompt)

        context["knowledge"] = {
            "all_vulnerabilities": vulnerabilities,
            "prioritized":         prioritized,
            "tech_stack_used":     tech_stack
        }

        self.log("Knowledge retrieval complete")
        return context