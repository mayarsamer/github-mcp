import streamlit as st
import requests
from typing import Dict, Any

st.set_page_config(page_title="AI Chat Interface", layout="centered")

FASTAPI_URL = "http://localhost:8000"

ASK_ENDPOINT = f"{FASTAPI_URL}/ask"

def send_message_to_api(prompt: str) -> Dict[str, Any]:
    """
    Send a message to the FastAPI server and return the response.
    """
    try:
        payload = {"prompt": prompt}
        response = requests.post(
            ASK_ENDPOINT,
            json=payload,
            timeout=15
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        return {"error": "Request timed out. Please try again."}
    except requests.exceptions.ConnectionError:
        return {"error": "Could not connect to the server. Is it running?"}
    except requests.exceptions.HTTPError:
        if response.status_code == 504:
            return {"error": "The AI service timed out. Please try again."}
        return {"error": f"HTTP error {response.status_code}: {response.text}"}
    except Exception as e:
        return {"error": str(e)}

def main():
    st.title("🤖 AI Chat Interface")
    st.markdown("Ask me anything — powered by Gemini and MCP tools.")

    user_input = st.text_area("Enter your prompt:", height=150)

    if st.button("Submit"):
        if not user_input.strip():
            st.warning("Please enter a prompt.")
            return

        with st.spinner("Sending your message..."):
            result = send_message_to_api(user_input)

        if "error" in result:
            st.error(result["error"])
        else:
            st.success("Response:")
            st.write(result["response"])

if __name__ == "__main__":
    main()
