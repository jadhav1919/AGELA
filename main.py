import sys
from core.pipeline import Pipeline
from core.config   import DEFAULT_MODEL

# Import all agents
from agents.guardrail_agent   import GuardrailAgent
from agents.supervisor_agent  import SupervisorAgent
from agents.recon_agent       import ReconAgent
from agents.knowledge_agent   import KnowledgeAgent
from agents.routing_agent     import RoutingAgent
from agents.memory_agent      import MemoryAgent
from agents.exploit_agent     import ExploitAgent
from agents.validation_agent  import ValidationAgent
from agents.report_agent      import ReportAgent


def main():
    # Get target from command line or use default
    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        target = "http://127.0.0.1"

    model = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_MODEL

    # Build the pipeline
    pipeline = Pipeline(target_url=target, model=model)

    # Add all 8 agents in order
    pipeline.add_agent(GuardrailAgent(model=model))
    pipeline.add_agent(SupervisorAgent(model=model))
    pipeline.add_agent(ReconAgent(model=model))
    pipeline.add_agent(KnowledgeAgent(model=model))
    pipeline.add_agent(RoutingAgent(model=model))
    pipeline.add_agent(MemoryAgent(model=model))
    pipeline.add_agent(ExploitAgent(model=model))
    pipeline.add_agent(ValidationAgent(model=model))
    pipeline.add_agent(ReportAgent(model=model))

    # Run everything
    result = pipeline.run()

    # Show report location
    if result.get("report", {}).get("file"):
        print(f"Report saved to: {result['report']['file']}")


if __name__ == "__main__":
    main()