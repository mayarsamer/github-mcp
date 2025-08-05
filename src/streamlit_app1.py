import streamlit as st
import requests
from typing import Dict, Any

st.set_page_config(page_title="GitHub AI Assistant", layout="centered")

FASTAPI_URL = "http://LLM_client:8000"
ASK_ENDPOINT = f"{FASTAPI_URL}/ask"

TOOL_GUIDE = {
    "Repository Management": {
        "description": "Manage your GitHub repositories.",
        "requirements": [
            "Action (create/delete/list)",
            "Repository name (required for create/delete)"
        ]
    },
    "Issue Tracking": {
        "description": "Work with GitHub issues.",
        "requirements": [
            "Action (create/get/close/close all)",
            "Repository name",
            "Issue title/body/number depending on the action"
        ]
    },
    "Pull Request Management": {
        "description": "Handle pull requests.",
        "requirements": [
            "Action (create/get/list/recently updated prs/list comments on pr/close)",
            "Repository name",
            "Base and head branches (for creating PRs)",
            "PR number (for closing or getting details)"
        ]
    },
    "Branch Management": {
        "description": "Work with branches in a repository.",
        "requirements": [
            "Action (list/get default)",
            "Repository name"
        ]
    },
    "GitHub Analysis": {
        "description": "Analyze repository performance and activity.",
        "requirements": [
            "Repository name",
            "Timeframe (for top contributors)",
            "Metrics of interest (commits, issues, PRs)"
        ]
    }
}

def send_message_to_api(prompt: str) -> Dict[str, Any]:
    try:
        response = requests.post(
            ASK_ENDPOINT,
            json={"prompt": prompt},
            timeout=15
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        return {"error": "⏱️ Request timed out. Please try again."}
    except requests.exceptions.ConnectionError:
        return {"error": "🔌 Could not connect to the server."}
    except requests.exceptions.HTTPError:
        if response.status_code == 504:
            return {"error": "🧠 AI service timed out. Try again."}
        return {"error": f"❌ HTTP error: {response.text}"}
    except Exception as e:
        return {"error": f"⚠️ Unexpected error: {str(e)}"}

def main():
    st.markdown("<h1 style='text-align: center;'>🚀 GitHub AI Assistant</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Choose a tool and get prompt suggestions tailored for it</p>", unsafe_allow_html=True)
    st.markdown("---")

    # === Tool Selection ===
    selected_tool = st.selectbox("🔧 Select a tool you want to use:", list(TOOL_GUIDE.keys()))

    if selected_tool:
        guide = TOOL_GUIDE[selected_tool]
        st.markdown(f"### 🧠 Tool Description\n{guide['description']}")
        st.markdown("#### 📌 Required in your prompt:")
        for req in guide["requirements"]:
            st.markdown(f"- {req}")

    st.markdown("---")
    st.subheader("💬 Your Prompt")
    user_input = st.text_area("Write your command:", height=150, placeholder="e.g., Create a new repo called 'test-ai-repo'")

    if st.button("🚀 Run"):
        if not user_input.strip():
            st.warning("Please enter a prompt.")
        else:
            with st.spinner("Thinking..."):
                result = send_message_to_api(user_input)

            if "error" in result:
                st.error(result["error"])
            else:
                st.success("✅ Response:")
                st.write(result["response"])

if __name__ == "__main__":
    main()
