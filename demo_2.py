import streamlit as st
from src.helper_1 import read_documents_from_folder, chat_with_llm

# Streamlit page configuration
st.set_page_config(
    page_title="DocGenie",
    page_icon="🤖",
    layout="wide"
)

# Hardcoded folder path for documents
FOLDER_PATH = r"/Users/anushraypingale/Desktop/DocGenie/backend_docs"

# Extract text from all supported files in the folder
file_content = read_documents_from_folder(FOLDER_PATH)

if not file_content:
    st.error("⚠️ No valid content extracted. Check the folder.")
    st.stop()

# UI Header
st.markdown(
    """
    <h1 style="display: flex; align-items: center;">
        🤖 DocGenie
    </h1>
    """,
    unsafe_allow_html=True
)

# Initialize session state for AI response
if "llm_response" not in st.session_state:
    st.session_state["llm_response"] = ""

# Suggested Queries Section
st.markdown("<h3 style='font-size:24px;'>💡 Suggested Queries</h3>", unsafe_allow_html=True)

# Predefined questions
predefined_questions = [
    "What are the key points of the documents?",
    "Summarize the documents in bullet points.",
    "What are the main requirements mentioned?",
    "Are there any limitations or constraints?",
]

# Display predefined questions as buttons in columns
for i in range(0, len(predefined_questions), 2):
    cols = st.columns(2)
    for j in range(2):
        if i + j < len(predefined_questions):
            with cols[j]:
                if st.button(f"🔹 {predefined_questions[i + j]}", key=f"btn_{i+j}"):
                    st.session_state["query"] = predefined_questions[i + j]

# Query Input Box
query = st.text_input("", placeholder="Enter a query", key="query")

# Get Response Button
if st.button("💬 Get Response"):
    if not query:
        st.error("⚠️ Please enter a question to proceed!")
    else:
        with st.spinner("⏳ Generating response..."):
            llm_response = chat_with_llm(query, file_content)
            st.session_state["llm_response"] = llm_response if llm_response else "⚠️ No valid response from AI."

# Display AI Response
st.write(st.session_state["llm_response"])
