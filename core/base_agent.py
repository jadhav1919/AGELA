import ollama
import json
import datetime
from core.config import DEFAULT_MODEL, AGENT_TIMEOUT


class BaseAgent:
    """
    Base class for all AGELA agents.
    Every agent inherits from this class.
    """

    def __init__(self, name: str, model: str = DEFAULT_MODEL):
        self.name       = name
        self.model      = model
        self.logs       = []
        self.created_at = datetime.datetime.now().isoformat()

    def think(self, prompt: str, system_prompt: str = "") -> str:
        """
        Send a prompt to the local Ollama LLM and get a response.
        This is how every agent thinks.
        """
        try:
            messages = []

            if system_prompt:
                messages.append({
                    "role":    "system",
                    "content": system_prompt
                })

            messages.append({
                "role":    "user",
                "content": prompt
            })

            response = ollama.chat(
                model    = self.model,
                messages = messages
            )

            result = response["message"]["content"]
            self.log(f"LLM response received ({len(result)} chars)")
            return result

        except Exception as e:
            self.log(f"ERROR in think(): {str(e)}")
            return f"ERROR: {str(e)}"

    def log(self, message: str):
        """
        Log a message with timestamp and agent name.
        """
        entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "agent":     self.name,
            "message":   message
        }
        self.logs.append(entry)
        print(f"[{self.name}] {message}")

    def run(self, context: dict) -> dict:
        """
        Every agent must implement this method.
        Receives pipeline context, returns updated context.
        """
        raise NotImplementedError(
            f"Agent '{self.name}' must implement the run() method."
        )