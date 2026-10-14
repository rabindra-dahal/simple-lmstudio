# model_service.py
import os
from engine_logic import SystemBackend
from .settings_storage import SettingsStorage

class ModelService:
    """
    Decoupled utility orchestrating file discovery and active preference logs.
    Lightens the layout structural weight of your main application controller.
    """
    def __init__(self):
        self.storage = SettingsStorage()

    def load_initial_directory(self) -> str:
        """Retrieves the previous folder location workspace directory."""
        return self.storage.get_last_directory()

    def scan_directory(self, selector_widget, target_dir: str) -> str:
        """
        Scans a targeted system path to extract valid local GGUF models.
        Populates selection menus and returns the initial model file path marker.
        """
        selector_widget.blockSignals(True)
        selector_widget.clear()
        
        files = SystemBackend.discover_gguf_models(target_dir)
        active_path = ""
        
        if files:
            for file in files:
                full_path = os.path.join(target_dir, file)
                selector_widget.addItem(file, full_path)
            selector_widget.blockSignals(False)
            
            # Default to tracking index 0 data path
            active_path = selector_widget.itemData(0) or ""
        else:
            selector_widget.addItem("No models found!", "")
            selector_widget.blockSignals(False)
            
        return active_path

    def verify_and_apply_history(self, selector_widget) -> str:
        """Validates if the last used session model still exists physically on disk."""
        saved_model_path = self.storage.get_last_model()
        if saved_model_path and os.path.exists(saved_model_path):
            index = selector_widget.findData(saved_model_path)
            if index != -1:
                selector_widget.setCurrentIndex(index)
                return saved_model_path
        return ""

    def save_state(self, directory_path: str, model_path: str):
        """Preserves system preference strings upon application exit."""
        self.storage.save_directory(directory_path)
        if model_path:
            self.storage.save_model(model_path)
