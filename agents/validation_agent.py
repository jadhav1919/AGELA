from core.base_agent import BaseAgent


class ValidationAgent(BaseAgent):
    """
    Validation Agent — confirms which exploits succeeded.
    Assigns severity ratings to confirmed vulnerabilities.
    Deduplicates multiple successful payloads for the same
    vulnerability type and URL.
    Stores confirmed exploits back into Memory Agent.
    """

    def __init__(self, model: str = "mistral"):
        super().__init__(
            name="ValidationAgent",
            model=model
        )

        self.severity_map = {
            "SQL Injection":     "Critical",
            "Command Injection": "Critical",
            "XSS Stored":        "High",
            "XSS Reflected":     "Medium",
            "CSRF":              "Medium",
            "File Upload":       "High",
            "File Inclusion":    "High",
            "IDOR":              "High"
        }

    def assign_severity(self, attack_type: str) -> str:
        """Assign severity to a vulnerability type."""

        for key in self.severity_map:

            if key.lower() in attack_type.lower():
                return self.severity_map[key]

        return "Medium"

    def _get_cvss_score(self, severity: str) -> float:

        scores = {
            "Critical": 9.5,
            "High": 7.5,
            "Medium": 5.0,
            "Low": 2.5
        }

        return scores.get(
            severity,
            5.0
        )

    def _get_evidence(self, exploit: dict) -> str:

        if exploit.get("error_detected"):
            return "SQL error message detected in response"

        if exploit.get("reflected"):
            return "XSS payload reflected in HTTP response"

        if exploit.get("detected"):
            return "Command output detected in response"

        if exploit.get("data_returned"):
            return "Unexpected application data returned in response"

        return "Vulnerability indicator detected"

    def run(self, context: dict) -> dict:

        self.log("Validating exploit results")

        exploits = context.get(
            "exploits",
            []
        )

        tech_stack = context.get(
            "recon",
            {}
        ).get(
            "tech_stack",
            {}
        )

        memory_agent = context.get(
            "_memory_agent"
        )

        successful = [
            exploit
            for exploit in exploits
            if exploit.get("success")
        ]

        self.log(
            f"Successful exploits to validate: "
            f"{len(successful)}"
        )

        # --------------------------------------------------
        # Deduplicate vulnerabilities
        # Key = vulnerability type + target URL
        # --------------------------------------------------

        grouped = {}

        for exploit in successful:

            attack_type = exploit.get(
                "attack_type",
                "Unknown"
            )

            url = exploit.get(
                "url",
                ""
            )

            key = (
                attack_type.lower().strip(),
                url.lower().strip()
            )

            if key not in grouped:
                grouped[key] = []

            grouped[key].append(
                exploit
            )

        validated = []

        # --------------------------------------------------
        # Create one finding per vulnerability
        # --------------------------------------------------

        for key, exploit_group in grouped.items():

            first_exploit = exploit_group[0]

            attack_type = first_exploit.get(
                "attack_type",
                "Unknown"
            )

            url = first_exploit.get(
                "url",
                ""
            )

            severity = self.assign_severity(
                attack_type
            )

            successful_payloads = [
                exploit.get(
                    "payload",
                    ""
                )
                for exploit in exploit_group
            ]

            evidence_items = [
                self._get_evidence(exploit)
                for exploit in exploit_group
            ]

            # Remove duplicate evidence descriptions
            evidence_items = list(
                dict.fromkeys(evidence_items)
            )

            validated_exploit = {
                "attack_type": attack_type,
                "url": url,
                "payload": first_exploit.get(
                    "payload",
                    ""
                ),
                "successful_payloads":
                    successful_payloads,
                "successful_payload_count":
                    len(successful_payloads),
                "severity": severity,
                "confirmed": True,
                "cvss_score":
                    self._get_cvss_score(
                        severity
                    ),
                "evidence":
                    "; ".join(evidence_items)
            }

            validated.append(
                validated_exploit
            )

            self.log(
                f"✓ Confirmed: "
                f"{attack_type} "
                f"[{severity}] "
                f"({len(successful_payloads)} "
                f"successful payloads)"
            )

            # Store each successful payload in memory.
            # They remain separate historical attempts,
            # even though the final report groups them.
            if memory_agent:

                for exploit in exploit_group:

                    memory_agent.store_exploit({
                        "target": exploit.get(
                            "url",
                            ""
                        ),
                        "attack_type":
                            attack_type,
                        "payload": exploit.get(
                            "payload",
                            ""
                        ),
                        "tech_stack":
                            tech_stack,
                        "success": True
                    })

        # --------------------------------------------------
        # Ask LLM to summarize findings
        # --------------------------------------------------

        if validated:

            system_prompt = (
                "You are a security analyst "
                "writing a validation report."
            )

            prompt = f"""
Summarize these confirmed vulnerabilities
for a security report:

{validated}

Important:
- Each entry represents one unique vulnerability.
- Multiple successful payloads for the same
  vulnerability are evidence, not separate vulnerabilities.
- Do not inflate the vulnerability count.

For each vulnerability write:
- What it is (1 sentence)
- Why it is dangerous (1 sentence)
- Severity
- Number of successful payloads
"""

            summary = self.think(
                prompt,
                system_prompt
            )

        else:

            summary = (
                "No vulnerabilities confirmed "
                "in this scan."
            )

        context["validated"] = validated

        context["validation_summary"] = summary

        self.log(
            f"Validation complete: "
            f"{len(validated)} confirmed "
            f"unique vulnerabilities"
        )

        return context