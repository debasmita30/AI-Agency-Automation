import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASE_URL = "sqlite:///" + os.path.join(BASE_DIR, "data", "leads.db")

AIRTABLE_KEY = os.getenv("AIRTABLE_KEY")

AIRTABLE_BASE = os.getenv("AIRTABLE_BASE")

N8N_WEBHOOK = os.getenv("N8N_WEBHOOK")

GOOGLE_SHEET = os.getenv("GOOGLE_SHEET")