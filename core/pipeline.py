import json
import datetime
from colorama import Fore, Style, init

init(autoreset=True)


class Pipeline:
    """
    AGELA Pipeline — runs all agents in sequence.
    Each agent receives the full context and adds its results.
    """

    def __init__(self, target_url: str, model: str = "mistral"):
        self.target_url = target_url
        self.model      = model
        self.agents     = []
        self.context    = {
            "target_url":  target_url,
            "model":       model,
            "pipeline_id": datetime.datetime.now().strftime("%Y%m%d_%H%M%S"),
            "start_time":  datetime.datetime.now().isoformat(),
            "authorized":  False,
            "recon":       {},
            "knowledge":   {},
            "routing":     {},
            "memory":      {},
            "exploits":    [],
            "validated":   [],
            "report":      {},
            "logs":        []
        }

    def add_agent(self, agent):
        """Add an agent to the pipeline."""
        self.agents.append(agent)

    def run(self):
        """Run all agents in sequence."""
        print(Fore.CYAN + "\n" + "="*60)
        print(Fore.CYAN + "  AGELA — Autonomous Exploit Generation by LLM Agents")
        print(Fore.CYAN + "="*60)
        print(Fore.YELLOW + f"  Target : {self.target_url}")
        print(Fore.YELLOW + f"  Model  : {self.model}")
        print(Fore.YELLOW + f"  ID     : {self.context['pipeline_id']}")
        print(Fore.CYAN + "="*60 + "\n")

        for agent in self.agents:
            print(Fore.BLUE + f"\n▶ Running: {agent.name}")
            print("-" * 40)

            try:
                self.context = agent.run(self.context)

                # Stop pipeline if guardrail blocks the target
                if agent.name == "GuardrailAgent" and not self.context["authorized"]:
                    print(Fore.RED + "\n✗ Target not in authorized scope. Pipeline stopped.")
                    return self.context

            except Exception as e:
                print(Fore.RED + f"✗ Agent {agent.name} failed: {str(e)}")
                self.context["logs"].append({
                    "agent": agent.name,
                    "error": str(e)
                })

        print(Fore.GREEN + "\n" + "="*60)
        print(Fore.GREEN + "  ✓ AGELA Pipeline Complete")
        print(Fore.GREEN + "="*60 + "\n")

        return self.context