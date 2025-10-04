import os
from typing import List

# Telegram Bot Configuration
API_ID: int = int(os.getenv("API_ID", "13828860")
API_HASH: str = os.getenv("API_HASH", "bbcd5f94dcd9f8a5eedc5de7397b4127")
BOT_TOKEN: str = os.getenv("BOT_TOKEN", "7419820448:AAHQLtA814ta5kXQduBopHC6oxBTHka2FJQ")

# Admin User IDs (comma-separated in env)
ADMIN_IDS: List[int] = [
    int(uid.strip()) 
    for uid in os.getenv("ADMIN_IDS", "").split(",") 
    if uid.strip()
]

# Validate configuration
def validate_config():
    """Validate that all required config values are set"""
    errors = []
    
    if API_ID == 0:
        errors.append("API_ID is not set")
    
    if not API_HASH:
        errors.append("API_HASH is not set")
    
    if not BOT_TOKEN:
        errors.append("BOT_TOKEN is not set")
    
    if not ADMIN_IDS:
        errors.append("ADMIN_IDS is not set")
    
    if errors:
        error_msg = "Configuration errors:\n" + "\n".join(f"- {e}" for e in errors)
        raise ValueError(error_msg)

# Run validation on import
try:
    validate_config()
    print("✅ Configuration validated successfully")
except ValueError as e:
    print(f"❌ Configuration error:\n{e}")
    print("\nPlease set the following environment variables:")
    print("- API_ID: Your Telegram API ID")
    print("- API_HASH: Your Telegram API Hash")
    print("- BOT_TOKEN: Your Manager Bot Token")
    print("- ADMIN_IDS: Comma-separated user IDs (e.g., 123456,789012)")
    exit(1)
