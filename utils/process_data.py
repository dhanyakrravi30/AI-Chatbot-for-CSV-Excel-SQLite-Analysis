import os
import pandas as pd
import sqlite3

def load_file(uploaded_file):
    """Load CSV, Excel, or SQLite file and save temporarily."""
    file_extension = uploaded_file.name.split(".")[-1].lower()
    temp_file_path = f"temp_data.{file_extension}"


    uploaded_file.seek(0)
    with open(temp_file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    df = None  

    if file_extension == "csv":
        df = pd.read_csv(temp_file_path)
    elif file_extension == "xlsx":
        df = pd.read_excel(temp_file_path, engine="openpyxl")
    elif file_extension == "db":
        
        pass
    else:
        raise ValueError("Unsupported file format! Please upload a CSV, XLSX, or DB file.")

    return df, temp_file_path, file_extension  
