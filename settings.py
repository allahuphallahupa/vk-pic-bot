from dotenv import load_dotenv
import os
path = os.path.join('venv', '.env')
if os.path.exists(path):
    load_dotenv(dotenv_path=os.path.join('venv', '.env'))