from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

api_key = os.getenv('GEMINI_API_KEY')  # Get the API key from environment variables
if not api_key:
    raise ValueError("It is not set in the environment variable")