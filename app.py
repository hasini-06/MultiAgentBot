import streamlit as st
from agents import MasterAgent

st.set_page_config(page_title="Multi-Agent Chatbot", layout="centered")

st.title("🤖 Multi-Agent Conversational Assistant")

if "history" not in st.session_state:
    st.session_state["history"] = []

agent = MasterAgent()

query = st.chat_input("Type your query...")

if query:
    response = agent.route(query)
    st.session_state["history"].append(("🧑", query))
    st.session_state["history"].append(("🤖", response))

# Display conversation
for role, text in st.session_state["history"]:
    st.markdown(f"**{role}:** {text}")

# Clear chat
if st.button("Clear Chat"):
    st.session_state["history"] = []

# Export chat
if st.button("Export Chat"):
    with open("conversation.txt", "w", encoding="utf-8") as f:
        for role, text in st.session_state["history"]:
            f.write(f"{role}: {text}\n")
    st.success("Conversation exported as conversation.txt ✅")
