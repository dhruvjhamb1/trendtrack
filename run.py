import subprocess
import sys
import os
from database.astra_connector import AstraDB
from dotenv import load_dotenv

def import_csv_data():
    print("Importing engagement data from CSV...")
    load_dotenv()
    db = AstraDB()
    db.import_csv_data()

def run_flask():
    print("Starting Flask server...")
    subprocess.run([sys.executable, "app.py"])

if __name__ == "__main__":
    # Import CSV data first
    import_csv_data()
    
    # Then run Flask application
    run_flask() 