# AGELA Configuration File
# All settings for the framework in one place

# Ollama settings
OLLAMA_BASE_URL = "http://localhost:11434"
DEFAULT_MODEL   = "mistral"

# Models available for paper comparison
AVAILABLE_MODELS = [
    "mistral",
    "codellama:13b",
    "llama3.1:8b",
]

# ChromaDB settings
CHROMA_DB_PATH = "./data/chroma_db"

# Reports output folder
REPORTS_PATH = "./reports"

# Scope file path
SCOPE_FILE = "./data/scope.json"

# Agent timeouts — higher because we run on CPU
AGENT_TIMEOUT    = 300
MAX_EXPLOIT_ATTEMPTS = 5

# Memory toggle — for experiment 2 in paper
MEMORY_ENABLED   = True

# CPU optimization for Intel UHD 770
OLLAMA_NUM_THREADS = 8