import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("7995816359:AAESeFlM6x7wiFh5Lhv_iua8v7-hOs1ihqc")
ADMIN_USER_ID = int(os.getenv("6959589442"))

# Dictionary to store task configurations (task name -> settings)
tasks = {}
