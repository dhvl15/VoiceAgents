"""Streamlit app for testing Google ADK agents via REST API."""

import os
import uuid

import requests
import streamlit as st

# Configuration
ADK_API_URL = os.getenv("ADK_API_URL", "http://localhost:8001")
AVAILABLE_AGENTS = ["starter_agent", "news_analyst", "research_coordinator", "medical_receptionist"]
USER_ID = "u_default"  # Single user


def create_session(app_name: str, user_id: str, session_id: str) -> dict:
    """Create a new session for the agent."""
    url = f"{ADK_API_URL}/apps/{app_name}/users/{user_id}/sessions/{session_id}"
    response = requests.post(url, json={}, timeout=10)
    response.raise_for_status()
    return response.json()


def run_agent(
    app_name: str, user_id: str, session_id: str, message: str
) -> dict:
    """Send a message to the agent and get the response."""
    url = f"{ADK_API_URL}/run"
    payload = {
        "appName": app_name,
        "userId": user_id,
        "sessionId": session_id,
        "newMessage": {
            "role": "user",
            "parts": [{"text": message}],
        },
    }
    response = requests.post(url, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()


def main():
    st.set_page_config(
        page_title="AI Agents Lab",
        page_icon="🤖",
        layout="wide",
    )

    st.title("🤖 AI Agents Lab")
    st.markdown("Test your Google ADK agents via REST API")

    # Sidebar configuration
    with st.sidebar:
        st.header("Configuration")
        api_url = st.text_input(
            "ADK API URL",
            value=ADK_API_URL,
            help="The URL where adk api_server is running",
        )
        os.environ["ADK_API_URL"] = api_url

        st.divider()
        st.header("Session Management")
        
        # Session list
        if "sessions" not in st.session_state:
            st.session_state.sessions = {}
        
        if st.button("New Session"):
            new_session_id = f"s_{uuid.uuid4().hex[:8]}"
            st.session_state.sessions[new_session_id] = {"messages": []}
            st.session_state.current_session = new_session_id
            st.rerun()
        
        # Select session
        session_list = list(st.session_state.sessions.keys())
        if session_list:
            if "current_session" not in st.session_state or st.session_state.current_session not in session_list:
                st.session_state.current_session = session_list[0]
            
            selected_session = st.selectbox(
                "Active Session",
                session_list,
                index=session_list.index(st.session_state.current_session),
                key="session_selector"
            )
            st.session_state.current_session = selected_session
            
            if st.button("Delete Current Session"):
                del st.session_state.sessions[selected_session]
                if st.session_state.sessions:
                    st.session_state.current_session = list(st.session_state.sessions.keys())[0]
                else:
                    st.session_state.current_session = None
                st.rerun()
        else:
            st.info("No sessions. Click 'New Session' to start.")

        st.divider()
        st.header("Instructions")
        st.markdown(
            """
            1. Start the ADK API server:
               ```bash
               cd google
               adk api_server --port 8001
               ```

            2. Create a new session or select an existing one.

            3. Select an agent and start chatting!
            """
        )

    # Agent selection
    col1, col2 = st.columns([1, 3])
    with col1:
        selected_agent = st.selectbox("Select Agent", AVAILABLE_AGENTS)

    # Check if session exists
    if not st.session_state.get("current_session"):
        st.warning("Please create a session in the sidebar to start chatting.")
        return

    current_session = st.session_state.current_session
    session_data = st.session_state.sessions[current_session]

    # Initialize ADK session if needed
    session_key = f"adk_session_{selected_agent}_{current_session}"
    if session_key not in st.session_state:
        try:
            create_session(selected_agent, USER_ID, current_session)
            st.session_state[session_key] = True
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to create session: {e}")
            st.error(
                "Make sure the ADK API server is running with: `adk api_server --port 8001`"
            )
            return

    # Chat interface
    # Display chat history
    for message in session_data["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Type your message..."):
        # Add user message to history
        session_data["messages"].append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get agent response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = run_agent(
                        selected_agent,
                        USER_ID,
                        current_session,
                        prompt,
                    )

                    # The /run endpoint returns a list of events directly
                    response_text = ""
                    events = response if isinstance(response, list) else response.get("events", [])
                    
                    for event in events:
                        if not isinstance(event, dict):
                            continue
                        # Try multiple possible structures
                        author = event.get("author", "")
                        if author != "user":
                            content = event.get("content", {})
                            if isinstance(content, dict):
                                parts = content.get("parts", [])
                                for part in parts:
                                    if isinstance(part, dict) and "text" in part:
                                        response_text += part["text"]
                            elif isinstance(content, str):
                                response_text += content

                    if not response_text:
                        # Fallback: show the raw response structure for debugging
                        response_text = f"Could not parse response. Raw: {response}"

                    st.markdown(response_text)
                    session_data["messages"].append(
                        {"role": "assistant", "content": response_text}
                    )

                    # Show raw response in expander for debugging
                    with st.expander("Raw API Response"):
                        st.json(response)

                except requests.exceptions.RequestException as e:
                    st.error(f"Error calling agent: {e}")
                    st.error(
                        "Make sure the ADK API server is running with: `adk api_server --port 8001`"
                    )

    # Clear chat button
    if st.button("Clear Chat"):
        session_data["messages"] = []
        st.rerun()


if __name__ == "__main__":
    main()
