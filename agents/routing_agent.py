from core.base_agent import BaseAgent


class RoutingAgent(BaseAgent):
    """
    Routing Agent — decides attack strategy based on target fingerprint.
    Maps detected tech stack to most effective attack order.
    Novel contribution of AGELA framework.
    """

    def __init__(self, model: str = "mistral"):
        super().__init__(name="RoutingAgent", model=model)

        self.routing_matrix = {
            "DVWA": [
                "SQL Injection",
                "Command Injection",
                "XSS Reflected",
                "XSS Stored",
                "CSRF",
                "File Upload",
                "File Inclusion"
            ],
            "WordPress": [
                "User Enumeration",
                "XML-RPC Brute Force",
                "Plugin SQL Injection",
                "XSS in Comments",
                "CSRF"
            ],
            "PHP": [
                "SQL Injection",
                "XSS",
                "CSRF",
                "File Upload",
                "Local File Inclusion"
            ],
            "Apache": [
                "Directory Traversal",
                "XSS",
                "SQL Injection",
                "CSRF"
            ],
            "generic": [
                "SQL Injection",
                "XSS",
                "CSRF",
                "IDOR",
                "Access Control Bypass"
            ]
        }

    def get_attack_route(self, tech_stack: dict) -> list:
        """Select attack order based on detected tech stack"""
        cms = tech_stack.get("cms", "unknown")
        if cms in self.routing_matrix:
            self.log(f"Using routing matrix for: {cms}")
            return self.routing_matrix[cms]

        language = tech_stack.get("language", "unknown")
        if language in self.routing_matrix:
            self.log(f"Using routing matrix for: {language}")
            return self.routing_matrix[language]

        framework = tech_stack.get("framework", "unknown")
        if framework in self.routing_matrix:
            self.log(f"Using routing matrix for: {framework}")
            return self.routing_matrix[framework]

        self.log("Using generic routing matrix")
        return self.routing_matrix["generic"]

    def run(self, context: dict) -> dict:
        self.log("Determining optimal attack route")

        tech_stack  = context.get("recon", {}).get("tech_stack", {})
        forms       = context.get("recon", {}).get("forms", [])
        knowledge   = context.get("knowledge", {}).get("prioritized", "")

        attack_route = self.get_attack_route(tech_stack)
        self.log(f"Base attack route: {attack_route[:3]}")

        system_prompt = """You are an expert penetration tester.
Given reconnaissance data and vulnerability knowledge, create a
precise ordered attack plan with specific payloads to try."""

        prompt = f"""
Create a precise attack plan for this target:

Tech Stack: {tech_stack}
Forms available: {len(forms)}
Form details: {forms[:2]}
Base attack route: {attack_route}
Vulnerability knowledge: {knowledge[:500]}

For each attack specify:
- ATTACK: [name]
- TARGET: [which form/parameter]
- PAYLOAD_TYPE: [what kind of payload]
- EXPECTED_RESULT: [what success looks like]

List top 4 attacks only.
"""

        refined_plan = self.think(prompt, system_prompt)

        context["routing"] = {
            "attack_route":    attack_route,
            "refined_plan":    refined_plan,
            "tech_stack_used": tech_stack,
            "total_attacks":   len(attack_route)
        }

        self.log(f"Routing complete — {len(attack_route)} attacks planned")
        return context