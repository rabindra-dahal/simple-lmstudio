# settings_storage.py
import os
from PyQt6.QtCore import QSettings

class SettingsStorage:
    """Interfaces with platform-native registries to store directory paths and loaded files."""
    def __init__(self):
        self.settings = QSettings("MyLocalAIStudio", "ModelSessionLog")

    def get_last_directory(self) -> str:
        """Retrieves the last active folder path or defaults to the standard models folder."""
        return self.settings.value("last_models_directory", os.path.abspath("./models"), type=str)

    def save_directory(self, path: str):
        """Persistently caches a targeted model folder selection."""
        self.settings.setValue("last_models_directory", path)

    def get_last_model(self) -> str:
        """Retrieves the file location footprint of the last active GGUF model."""
        return self.settings.value("last_selected_model_path", "", type=str)

    def save_model(self, path: str):
        """Persistently caches the chosen active model path blueprint."""
        self.settings.setValue("last_selected_model_path", path)
