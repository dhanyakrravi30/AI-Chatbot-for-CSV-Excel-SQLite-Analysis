import os
import pandas as pd
import sqlite3
from dotenv import load_dotenv
from langchain_experimental.agents import create_csv_agent
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY is missing! Please check your .env file.")

def get_ai_response(file_path, query, file_type):
    """Handles CSV, XLSX & SQLite, queries AI, and returns a conversational response."""

    if file_type == "xlsx":

        df = pd.read_excel(file_path)
        temp_csv_path = file_path.replace(".xlsx", ".csv")
        df.to_csv(temp_csv_path, index=False)
        file_path = temp_csv_path  

    if file_type in ["csv", "xlsx"]:
        
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=GOOGLE_API_KEY)
        agent = create_csv_agent(llm, file_path, verbose=True, allow_dangerous_code=True)
        response = agent.run(query)

    elif file_type == "db":
        
        conn = sqlite3.connect(file_path)
        cursor = conn.cursor()

       
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]

        if not tables:
            return "The database is empty!"

        
        try:
            cursor.execute(f"SELECT * FROM {tables[0]} LIMIT 5;")  
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

            
            df = pd.DataFrame(rows, columns=columns)

            
            llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=GOOGLE_API_KEY)
            prompt = f"Based on the following data:\n\n{df.to_string(index=False)}\n\nAnswer in a friendly way: {query}"
            response = llm.invoke(prompt).content  

        except Exception as e:
            response = f"Sorry, I couldn't fetch data from the database. Error: {str(e)}"

        finally:
            conn.close()

    else:
        response = "Unsupported file format!"

    return response
