# clipboard_manager.py
import urllib.parse
from PyQt6.QtWidgets import QApplication

class ClipboardManager:
    """
    Decoupled helper class focused entirely on native text tracking
    and native Windows OS clipboard binding operations.
    """
    def __init__(self):
        # Kept for architectural continuity across modular subsystems
        self.history_text_store = []

    def store_response(self, response_text: str):
        pass

    def get_next_index_id(self) -> int:
        return 0

    def clear_store(self):
        pass

    def copy_to_clipboard(self, url_string: str) -> bool:
        """
        Parses custom copy:// text stream blocks directly and binds them 
        instantly onto the native Windows system clipboard register layout.
        """
        if not url_string.startswith("copy://"):
            return False
            
        try:
            # 🚀 THE CRITICAL DECODING RESOLUTION:
            # Strip the routing scheme label string off the front
            encoded_text_block = url_string.replace("copy://", "")
            
            # Unquote the web tokens back into a beautiful, human-readable plain text string
            raw_decoded_chat_text = urllib.parse.unquote(encoded_text_block)
            
            # Interact directly with the native Windows system clipboard matrix register
            clipboard = QApplication.clipboard()
            clipboard.clear(mode=clipboard.Mode.Clipboard)
            clipboard.setText(raw_decoded_chat_text, mode=clipboard.Mode.Clipboard)
            return True
        except Exception as e:
            print(f"[Clipboard Manager Extraction Error: {str(e)}]")
            
        return False
