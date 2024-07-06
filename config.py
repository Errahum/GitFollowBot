import os
from typing import Optional


class Config:
    def __init__(self, env_file: str = '.env'):
        self.env_file = env_file
        self.github = {
            "api_key": self._get_env_var("github_follow_unfollow")
        }

    def _get_env_var(self, var_name: str, default: Optional[str] = None) -> str:
        value = os.getenv(var_name, default)
        if value is None:
            raise ValueError(
                f"La variable d'environnement {var_name} est manquante et aucune valeur par défaut n'a été fournie.")
        return value

    def get_api_key(self) -> str:
        return self.github["api_key"]
