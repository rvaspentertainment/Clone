import json
import os
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

class Storage:
    def __init__(self, storage_file: str = "bots_data.json"):
        self.storage_file = storage_file
        self.data = self._load_data()
    
    def _load_data(self) -> Dict:
        """Load data from JSON file"""
        try:
            if os.path.exists(self.storage_file):
                with open(self.storage_file, 'r') as f:
                    data = json.load(f)
                    logger.info(f"Loaded {len(data.get('bots', {}))} bots from storage")
                    return data
            else:
                logger.info("No existing storage file, starting fresh")
                return {"bots": {}}
        except Exception as e:
            logger.error(f"Error loading storage: {str(e)}")
            return {"bots": {}}
    
    def _save_data(self):
        """Save data to JSON file"""
        try:
            with open(self.storage_file, 'w') as f:
                json.dump(self.data, f, indent=2)
            logger.info("Data saved to storage")
        except Exception as e:
            logger.error(f"Error saving storage: {str(e)}")
    
    def save_bot(self, bot_id: str, bot_info: Dict):
        """Save bot information"""
        try:
            # Don't save process object (can't serialize)
            save_info = {
                "bot_token": bot_info["bot_token"],
                "repo_url": bot_info["repo_url"],
                "bot_dir": bot_info["bot_dir"],
                "started_at": bot_info["started_at"],
                "log_file": bot_info["log_file"]
            }
            
            self.data["bots"][bot_id] = save_info
            self._save_data()
            logger.info(f"Bot {bot_id} saved to storage")
        except Exception as e:
            logger.error(f"Error saving bot {bot_id}: {str(e)}")
    
    def remove_bot(self, bot_id: str):
        """Remove bot from storage"""
        try:
            if bot_id in self.data["bots"]:
                del self.data["bots"][bot_id]
                self._save_data()
                logger.info(f"Bot {bot_id} removed from storage")
        except Exception as e:
            logger.error(f"Error removing bot {bot_id}: {str(e)}")
    
    def get_bot(self, bot_id: str) -> Optional[Dict]:
        """Get bot information"""
        return self.data["bots"].get(bot_id)
    
    def get_all_bots(self) -> Dict:
        """Get all bots"""
        return self.data["bots"]
    
    def clear_all(self):
        """Clear all data"""
        try:
            self.data = {"bots": {}}
            self._save_data()
            logger.info("All data cleared")
        except Exception as e:
            logger.error(f"Error clearing data: {str(e)}")
