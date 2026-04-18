import logging
import json
import os

logger = logging.getLogger(__name__)

class ContextManager:
    def __init__(self, config):
        self.config = config
        self.history = [] # List of {"role": "user/assistant", "content": "..."}
        self.max_history = 10
        self.user_profile = {
            "name": "User",
            "city": "London" # Default, can be updated
        }
        self.profile_path = "user_profile.json"
        self._load_profile()

    def add_turn(self, role, content):
        """
        Adds a turn to the conversation history.
        """
        self.history.append({"role": role, "content": content})
        if len(self.history) > self.max_history:
            self.history.pop(0)

    def get_context(self):
        """
        Returns the formatted conversation history.
        """
        return self.history

    def update_profile(self, key, value):
        """
        Updates a user profile setting.
        """
        self.user_profile[key] = value
        self._save_profile()
        logger.info(f"Updated profile: {key} = {value}")

    def get_profile(self, key):
        return self.user_profile.get(key)

    def _save_profile(self):
        try:
            with open(self.profile_path, 'w') as f:
                json.dump(self.user_profile, f)
        except Exception as e:
            logger.error(f"Failed to save profile: {e}")

    def _load_profile(self):
        if os.path.exists(self.profile_path):
            try:
                with open(self.profile_path, 'r') as f:
                    self.user_profile = json.load(f)
            except Exception as e:
                logger.error(f"Failed to load profile: {e}")
