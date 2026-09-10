import json
from core.base_agent import BaseAgent
from core.config import SCOPE_FILE


class GuardrailAgent(BaseAgent):
    """
    Guardrail Agent — FIRST agent in the pipeline.
    Checks if the target URL is in the authorized scope.
    If not authorized, pipeline stops completely.
    """

    def __init__(self, model: str = "mistral"):
        super().__init__(name="GuardrailAgent", model=model)

    def load_scope(self) -> list:
        """Load authorized targets from scope.json"""
        try:
            with open(SCOPE_FILE, "r") as f:
                data = json.load(f)
                return data.get("authorized_targets", [])
        except FileNotFoundError:
            self.log("ERROR: scope.json not found!")
            return []
        except json.JSONDecodeError:
            self.log("ERROR: scope.json is not valid JSON!")
            return []

    def is_authorized(self, target_url: str, authorized_targets: list) -> bool:
        """Check if target URL matches any authorized target"""
        for authorized in authorized_targets:
            if target_url.startswith(authorized):
                return True
        return False

    def run(self, context: dict) -> dict:
        target_url = context["target_url"]
        self.log(f"Checking authorization for: {target_url}")

        # Load authorized targets
        authorized_targets = self.load_scope()

        if not authorized_targets:
            self.log("No authorized targets found in scope.json")
            context["authorized"] = False
            return context

        # Check if target is authorized
        if self.is_authorized(target_url, authorized_targets):
            self.log(f"✓ Target AUTHORIZED: {target_url}")
            context["authorized"]     = True
            context["auth_timestamp"] = __import__("datetime").datetime.now().isoformat()
        else:
            self.log(f"✗ Target NOT AUTHORIZED: {target_url}")
            self.log(f"  Authorized targets: {authorized_targets}")
            context["authorized"] = False

        return context