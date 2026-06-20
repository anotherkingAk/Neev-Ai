# Neev AI IDE 

Neev AI IDE is a developer-first, sovereign, and local-first development environment engineered to integrate the user interface foundation of OpenCode with the persistent, self-evolving memory engine of the Hermes Agent.

## 🚀 The Architecture
Traditional AI code editors suffer from "closed-tab amnesia" and rapid context degradation. Neev introduces a persistent background daemon that actively maps developer intent, architectural guards, and localized code memory into a secure, structured engram database via the Model Context Protocol (MCP).

### Core Features (V0.1 Core Bridge)
* **Persistent Engram Layer:** A centralized SQLite database that keeps your AI context completely synchronized across sessions without costly re-prompting.
* **Model Context Protocol (MCP):** Native standard-input/output (stdio) routing that allows external agents to securely read and write contextual memories without messing with core IDE files.
* **Security & Secret Scrubbing:** Proactive regex validation built directly into the data path to prevent API keys and sensitive environment variables from leaking into plaintext logs or memory files.

## 🛠️ Quick Start
To integrate this memory server into your existing MCP-compliant IDE or agent framework:

```bash
# Clone the repository
git clone https://github.com/anotherkingAk/Neev-Ai.git
cd Neev-Ai

# Install dependencies
pip install -r requirements.txt

# Run the MCP server
python neev_memory_mcp.py
