from dotenv import load_dotenv
import os

def Env(filename: str):
    def decorator(cls):
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Environment file {filename} not found.")
        load_dotenv(dotenv_path=filename, override=True)
        return cls
    return decorator
