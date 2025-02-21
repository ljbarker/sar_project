import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API keys
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# Deployment settings
DEPLOYMENT_NAME = os.getenv("DEPLOYMENT_NAME", "default_deployment")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Agent configuration
DEFAULT_MODEL = "gemini-2.0-flash"
DEFAULT_TEMPERATURE = 0.7
DEFAULT_TIMEOUT = 600

# File paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
