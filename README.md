# ⚡ nulti-Server GitHub Toolkit with LLM Integration


This project connects a Streamlit frontend with an LLM client and an MCP-server using FastAPI. It provides a seamless interface to interact with various GitHub management tools via natural language.

---

## Features

- **GitHub Repository Management:** Create, delete, and list repositories.
- **Issue Tracking:** Create issues, get details, close individual or all issues.
- **Pull Request Handling:** Create, list, get details, comment on, and close pull requests.
- **Branch Management:** List branches and find the default branch.
- **Natural Language Interface:** Communicate with the backend tools via a Streamlit UI using conversational prompts.
- **Modular Architecture:** Separate servers for the LLM client, backend tools (MCP-servers), and frontend UI for easy maintenance and scaling.

##  Getting Started !

### 1. Clone the Repository

```bash
git clone https://github.com/mayarsamer/github-mcp.git
cd github-mcp
```
---

### 2. Install Dependencies with uv
#### This project uses the uv package manager instead of pip. It will automatically create and manage a virtual environment for you.

1. Install uv:
```bash
pip install uv
```
2. Sync all dependencies using the lockfile

```bash
uv sync --locked
```
3. Activate the Virtual Environment

```bash
source .venv/bin/activate
```
---

### 3. Export Required Environment Variables
Before starting the servers, export your API keys in your terminal session:

```bash
export GITHUB_TOKEN=your_github_token
export GOOGLE_API_KEY=your_google_api_key
```
---

### 4. Make the Startup Script Executable
If not already done:

```bash
sudo chmod +x start_servers.sh
```
---

### 5. Start All Servers
Now launch all the servers (FastAPI, LLM client, and Streamlit):

```bash
./start_servers.sh
```
