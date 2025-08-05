# 🧠 Multi-Server AI Tool Interface

This project connects a Streamlit frontend with an LLM client and an MCP-server using FastAPI. It provides a seamless interface to interact with various GitHub management tools via natural language.

---

##  Getting Started !

### 1. Clone the Repository

```bash
git clone https://github.com/mayarsamer/github-mcp.git
cd github-mcp
```

### 2. Activate the Virtual Environment
If you’re using a virtual environment (recommended), activate it:

```bash
source venv/bin/activate
```

### 3. Export Required Environment Variables
Before starting the servers, export your API keys in your terminal session:

```bash
export GITHUB_TOKEN=your_github_token
export GOOGLE_API_KEY=your_google_api_key
```


### 4. Make the Startup Script Executable
If not already done:

```bash
sudo chmod +x start_servers.sh
```


### 5. Start All Servers
Now launch all the servers (FastAPI, LLM client, and Streamlit):

```bash
./start_servers.sh
```
