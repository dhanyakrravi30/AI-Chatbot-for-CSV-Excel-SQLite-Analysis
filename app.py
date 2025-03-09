import os
import streamlit as st
from dotenv import load_dotenv
from utils.process_data import load_file
from utils.query_agent import get_ai_response

load_dotenv(dotenv_path=".env", override=True)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    st.error("🚨 GOOGLE_API_KEY is missing! Set it in the .env file.")
    st.stop()

st.set_page_config(page_title="AI Data Chatbot - CSV, Excel & SQLite")
st.title("📊 AI Data Chatbot (CSV, Excel & SQLite)")

uploaded_file = st.file_uploader("📁 Upload a CSV, Excel, or SQLite (.db) File", type=["csv", "xlsx", "db"])

if uploaded_file:
    try:
        df, temp_file_path, file_type = load_file(uploaded_file)  

        
        if file_type in ["csv", "xlsx"]:
            st.write("### 🔍 Preview of Uploaded Data:")
            st.dataframe(df.head())  

        user_question = st.text_input("💬 Ask a question about your file:")

        if user_question:
            with st.spinner("🤖 Thinking..."):
                response = get_ai_response(temp_file_path, user_question, file_type)  # Pass file type
                st.write("### 🤖 AI Response:")
                st.success(response)

    except UnicodeDecodeError as e:
        st.error(f"❌ Encoding Error: {e}. Try uploading a properly formatted UTF-8 file.")
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
