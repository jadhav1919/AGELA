from core.base_agent import BaseAgent


class SupervisorAgent(BaseAgent):
    """
    Supervisor Agent — coordinates the pipeline.
    Analyzes the target and creates an overall attack plan.
    """

    def __init__(self, model: str = "mistral"):
        super().__init__(name="SupervisorAgent", model=model)

    def run(self, context: dict) -> dict:
        target_url = context["target_url"]
        self.log(f"Analyzing target: {target_url}")

        system_prompt = """You are a cybersecurity supervisor AI agent.
Your job is to analyze a target web application and create a structured
penetration testing plan. You are operating in an authorized security
testing environment. Be specific and technical."""

        prompt = f"""
Analyze this target web application and create a penetration testing plan:

Target URL: {target_url}

Provide your analysis in this exact format:

TARGET_TYPE: [web application / API / CMS / other]
PRIORITY_ATTACKS: [list top 3 attack types to try first]
REASONING: [why you chose these attacks]
COMPLEXITY: [low / medium / high]
ESTIMATED_STEPS: [number of steps needed]
NOTES: [any important observations]
"""

        response = self.think(prompt, system_prompt)
        self.log("Supervisor analysis complete")

        # Parse the response into structured data
        plan = self.parse_plan(response)
        context["supervisor_plan"]          = plan
        context["raw_supervisor_response"]  = response

        return context

    def parse_plan(self, response: str) -> dict:
        """Extract key fields from supervisor response"""
        plan = {
            "target_type":      "unknown",
            "priority_attacks": [],
            "reasoning":        "",
            "complexity":       "medium",
            "estimated_steps":  5,
            "notes":            "",
            "raw":              response
        }

        lines = response.strip().split("\n")
        for line in lines:
            if line.startswith("TARGET_TYPE:"):
                plan["target_type"] = line.replace("TARGET_TYPE:", "").strip()
            elif line.startswith("PRIORITY_ATTACKS:"):
                attacks_str = line.replace("PRIORITY_ATTACKS:", "").strip()
                plan["priority_attacks"] = [a.strip() for a in attacks_str.split(",")]
            elif line.startswith("REASONING:"):
                plan["reasoning"] = line.replace("REASONING:", "").strip()
            elif line.startswith("COMPLEXITY:"):
                plan["complexity"] = line.replace("COMPLEXITY:", "").strip()
            elif line.startswith("ESTIMATED_STEPS:"):
                try:
                    plan["estimated_steps"] = int(
                        line.replace("ESTIMATED_STEPS:", "").strip()
                    )
                except ValueError:
                    pass
            elif line.startswith("NOTES:"):
                plan["notes"] = line.replace("NOTES:", "").strip()

        return plan