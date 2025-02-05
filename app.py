import streamlit as st
import google.generativeai as genai
import os

# Configure Gemini
genai.configure(api_key="AIzaSyDzboVyiU1vAuXkfzF6C5XsUMj1E2M1eDM")

# Initialize the model
model = genai.GenerativeModel('gemini-1.5-pro-latest')

# Initialize session state
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])
if "file_texts" not in st.session_state:
    st.session_state.file_texts = ""

st.title("📚 Lecture Files Chat Assistant")
st.markdown("Automatically loads all lecture files from the project folder!")

# Function to read text from all .txt files in the repository folder
def read_all_txt_files(folder_path):
    combined_text = ""
    try:
        for filename in os.listdir(folder_path):
            if filename.endswith(".txt"):  # Process only text files
                file_path = os.path.join(folder_path, filename)
                with open(file_path, "r", encoding="utf-8") as file:
                    combined_text += f"\n\n--- {filename} ---\n" + file.read()
        return combined_text
    except Exception as e:
        st.error(f"Error reading files: {e}")
        return ""

# Read all text files in the current folder
FOLDER_PATH = "."  # Set to current directory
st.session_state.file_texts = read_all_txt_files(FOLDER_PATH)

# Display the extracted content
if st.session_state.file_texts:
    st.subheader("Loaded Lecture Notes")
    st.text_area("Extracted Text", st.session_state.file_texts[:1000] + "...", height=200)

# Chat interface
for message in st.session_state.chat.history:
    with st.chat_message(message.role):
        st.markdown(message.parts[0].text if message.parts else "")

user_input = st.chat_input("Ask something about your lecture files...")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)

    # Construct query with file contents
    full_query = f"Lecture Notes:\n{st.session_state.file_texts}\n\nUser Question: {user_input}"
    
    # Generate response
    try:
        response = st.session_state.chat.send_message(full_query)
        assistant_reply = response.text  # FIX: Extract text properly

        with st.chat_message("assistant"):
            st.markdown(assistant_reply)
    except Exception as e:
        st.error(f"🚨 Error generating response: {str(e)}")

# Styling
st.markdown("""
<style>
    .stChatInput textarea {
        min-height: 100px !important;
    }
    .stDownloadButton button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)
