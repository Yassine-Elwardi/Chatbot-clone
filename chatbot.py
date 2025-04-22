
import streamlit as st
from openai import OpenAI
from datetime import datetime

st.title("Chatbot-Clone")

# Available models
models = ["deepseek/deepseek-chat-v3-0324:free","deepseek/deepseek-chat-v3-0324","deepseek/deepseek-r1-zero:free","deepseek/deepseek-r1-distill-qwen-32b:free"]

# Initialize session state for model and messages
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = models
if "messages" not in st.session_state:
    st.session_state.messages = []
if "history_sessions" not in st.session_state:
    st.session_state.history_sessions = []
if "selected_session" not in st.session_state:
    st.session_state.selected_session = None

# Function to create a new session
def create_new_session():
    if st.session_state.messages:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        session_data = {
            "timestamp": timestamp,
            "messages": st.session_state.messages.copy()
        }
        st.session_state.history_sessions.append(session_data)
        st.session_state.messages = []
        st.session_state.selected_session = None

# Sidebar for model selection and history
with st.sidebar:
    _left, mid, _right = st.columns(3)
    with mid:
        st.image("robot.gif",use_container_width=True,width=200)
    
    st.subheader("Model Selection :")
    st.session_state["openai_model"] = st.selectbox(
        "Select a model",
        options=models,
        
    )
    deepseek_api_key = st.text_input("Deepseek API Key :", key="chatbot_api_key", type="password")
    "[Get a Deepseek API key for free : ](https://openrouter.ai)"
    "[View the source code](https://github.com/Yassine-Elwardi/Chatbot-clone)"

    st.header("Settings & History")

    if st.button("New Chat", type="primary"):
        create_new_session()
        st.rerun()
    
    st.subheader("Chat History")

      # Display history sessions as clickable links
    for i, session in enumerate(st.session_state.history_sessions):
        # Create a unique key for each button
        if st.button(f"{session['timestamp']} - {session['messages'][0]['content'][:30]}...", 
                    key=f"session_{i}"):
            st.session_state.selected_session = i
            st.session_state.messages = st.session_state.history_sessions[i]["messages"].copy()
            st.rerun()
    
    # Display current session if selected
    if st.session_state.selected_session is not None:
        st.write(f"Viewing session from {st.session_state.history_sessions[st.session_state.selected_session]['timestamp']}")
        if st.button("Back to Current Chat"):
            st.session_state.selected_session = None
            st.session_state.messages = []
            st.rerun()

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
    

# User input
if prompt:= st.chat_input("Type here....."):

    if not deepseek_api_key:
        st.error("Please enter your Deepseek API Key in the sidebar.")
        st.stop()
    # Initialize OpenAI client
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=deepseek_api_key,
    )
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get and display AI response
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    
    # Add AI response to history
    st.session_state.messages.append({"role": "assistant", "content": response})


            
    
