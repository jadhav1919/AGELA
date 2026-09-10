import os
import json
import datetime
import chromadb
from core.base_agent import BaseAgent
from core.config import CHROMA_DB_PATH, MEMORY_ENABLED


class MemoryAgent(BaseAgent):
    """
    Memory Agent — stores and retrieves past exploit results.
    Uses ChromaDB as local vector database.
    AGELA gets smarter with every run.
    Novel contribution of AGELA framework.
    """

    def __init__(self, model: str = "mistral"):
        super().__init__(name="MemoryAgent", model=model)
        self.client     = None
        self.collection = None
        self._init_db()

    def _init_db(self):
        """Initialize ChromaDB local database"""
        try:
            os.makedirs(CHROMA_DB_PATH, exist_ok=True)
            self.client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
            self.collection = self.client.get_or_create_collection(
                name="agela_exploits",
                metadata={"description": "AGELA successful exploit memory"}
            )
            self.log(f"ChromaDB initialized at {CHROMA_DB_PATH}")
            self.log(f"Memory contains {self.collection.count()} past exploits")
        except Exception as e:
            self.log(f"ChromaDB init failed: {str(e)}")
            self.client     = None
            self.collection = None

    def search_memory(self, tech_stack: dict, attack_type: str) -> list:
        """Search for past successful exploits matching current target"""
        if not self.collection or self.collection.count() == 0:
            return []

        try:
            query   = f"{tech_stack} {attack_type}"
            results = self.collection.query(
                query_texts=[query],
                n_results=min(3, self.collection.count())
            )

            memories = []
            if results and results["documents"]:
                for i, doc in enumerate(results["documents"][0]):
                    memories.append({
                        "past_exploit": doc,
                        "metadata":     results["metadatas"][0][i]
                            if results["metadatas"] else {}
                    })
            return memories

        except Exception as e:
            self.log(f"Memory search failed: {str(e)}")
            return []

    def store_exploit(self, exploit_data: dict):
        """Store a successful exploit in memory for future use"""
        if not self.collection:
            return

        try:
            doc_id   = f"exploit_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
            document = json.dumps({
                "target":      exploit_data.get("target", ""),
                "attack_type": exploit_data.get("attack_type", ""),
                "payload":     exploit_data.get("payload", ""),
                "success":     exploit_data.get("success", False)
            })

            self.collection.add(
                documents=[document],
                metadatas=[{
                    "tech_stack":  str(exploit_data.get("tech_stack", {})),
                    "attack_type": exploit_data.get("attack_type", ""),
                    "timestamp":   datetime.datetime.now().isoformat(),
                    "success":     str(exploit_data.get("success", False))
                }],
                ids=[doc_id]
            )
            self.log(f"Stored exploit in memory: {doc_id}")

        except Exception as e:
            self.log(f"Failed to store exploit: {str(e)}")

    def run(self, context: dict) -> dict:
        # Check if memory is enabled (for experiment 2)
        if not MEMORY_ENABLED:
            self.log("Memory disabled for experiment")
            context["memory"] = {
                "past_exploits":  [],
                "memory_count":   0,
                "db_initialized": False
            }
            return context

        self.log("Searching memory for past exploits")

        tech_stack   = context.get("recon", {}).get("tech_stack", {})
        attack_route = context.get("routing", {}).get("attack_route", [])

        all_memories = []
        for attack_type in attack_route[:3]:
            memories = self.search_memory(tech_stack, attack_type)
            if memories:
                self.log(f"Found {len(memories)} past exploits for: {attack_type}")
                all_memories.extend(memories)

        if all_memories:
            self.log(f"Total memories retrieved: {len(all_memories)}")
        else:
            self.log("No past exploits found — fresh start")

        context["memory"] = {
            "past_exploits":  all_memories,
            "memory_count":   self.collection.count() if self.collection else 0,
            "db_initialized": self.collection is not None
        }

        # Store reference for validation agent to use later
        context["_memory_agent"] = self

        return context