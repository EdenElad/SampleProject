# main.py
import json
import logging
from datetime import datetime
import sys
import logging


# --- הגדרות בסיסיות ---
CONFIG_PATH = "config.json"

# --- הגדרת לוגים ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("app.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout),  # <-- במקום StreamHandler()
    ],
)

# --- פונקציות עזר ---
def load_config(path: str) -> dict:
    """טוען את קובץ ההגדרות (config.json)."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            config = json.load(f)
        logging.info("Configuration loaded successfully.")
        return config
    except FileNotFoundError:
        logging.error(f"Configuration file not found: {path}")
        return {}
    except json.JSONDecodeError:
        logging.error("Error parsing configuration file.")
        return {}

def greet_user(name: str):
    """מדפיס ברכת שלום עם השעה הנוכחית."""
    current_time = datetime.now().strftime("%H:%M:%S")
    logging.info(f"Greeting user: {name}")
    print(f"Hello, {name}! The current time is {current_time}.")

# --- פונקציית main ---
def main():
    """נקודת הכניסה הראשית של התוכנית."""
    logging.info("Starting application...")
    config = load_config(CONFIG_PATH)

    # אם אין קובץ קונפיגורציה, ברירת מחדל
    user_name = config.get("user_name", "Guest")

    greet_user(user_name)
    logging.info("Application finished successfully.")

# --- הפעלת התוכנית רק אם זה הקובץ הראשי ---
if __name__ == "__main__":
    main()
