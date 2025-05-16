from dotenv import load_dotenv
import os

load_dotenv()

class Config():
    airtable_api_key = os.getenv("AIRTABLE_API_KEY")
    AIRTABLE_BASE_ID = os.getenv("BASE_ID")