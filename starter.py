import subprocess
import os

# Make sure we are in the root folder
root_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(root_dir)

print("Starting FastAPI backend...")
subprocess.Popen([
    "uvicorn",
    "app:app",    # <filename>:<FastAPI_instance>
    "--reload",
    "--port", "8000"
])

print("Starting Streamlit UI...")
subprocess.Popen([
    "streamlit",
    "run",
    "ui/app.py"   # path to Streamlit app
])

input("Press Enter to exit...")


