# models_manager.py
import os

class ModelsManager:
    """Manages file storage, local caches, and discovery of GGUF model paths."""
    
    @staticmethod
    def discover_gguf_models(directory_path: str) -> list:
        """
        Scans a targeted folder, builds the directory path if it is missing,
        and extracts an array of active files matching the .gguf file signature.
        """
        if not os.path.exists(directory_path):
            try:
                os.makedirs(directory_path)
            except Exception:
                return []
                
        return [f for f in os.listdir(directory_path) if f.endswith('.gguf')]
