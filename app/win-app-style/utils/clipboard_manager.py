# clipboard_manager.py
import re
from PyQt6.QtWidgets import QApplication

class ClipboardManager:
    """
    Decoupled helper class focused entirely on text tracking arrays
    and native Windows OS clipboard binding operations.
    """
    def __init__(self):
        # 🚀 THE SECURE TEXT BUFFER ARRAY: Keeps plain text safe from memory drops
        self.history_text_store = []

    def store_response(self, response_text: str):
        """Appends a completed assistant response string securely inside the text cache list."""
        self.history_text_store.append(response_text)

    def get_next_index_id(self) -> int:
        """Returns the tracking index ID identifier value for the next response bubble."""
        return len(self.history_text_store)

    def clear_store(self):
        """Resets the history text cache pool completely."""
        self.history_text_store.clear()

    def copy_to_clipboard(self, url_string: str) -> bool:
        """
        Parses custom copy:// integer indexing paths, extracts plain-text,
        and binds it directly onto the native Windows system clipboard register.
        """
        if not url_string.startswith("copy://"):
            return False
            
        try:
            # Clean up the string using a regular expression to grab only the final digits,
            # completely bypassing any local loopback hostnames like '0.0.0.0/'
            match = re.search(r'(\d+)$', url_string)
            if not match:
                return False
                
            msg_index = int(match.group(1))
            
            if 0 <= msg_index < len(self.history_text_store):
                # Pull the clean text out of our persistent history array list
                raw_chat_text = self.history_text_store[msg_index]
                
                # Direct access to the native Windows OS system clipboard register
                clipboard = QApplication.clipboard()
                clipboard.clear(mode=clipboard.Mode.Clipboard)
                clipboard.setText(raw_chat_text, mode=clipboard.Mode.Clipboard)
                return True
        except Exception as e:
            print(f"[Clipboard Manager Error: {str(e)}]")
            
        return False
