# utils/export_service.py
import os
from datetime import datetime
from PyQt6.QtWidgets import QFileDialog

class ExportService:
    """
    Decoupled utility class that compiles chat history matrices into clear Markdown structure logs.
    Bypasses token limit overflows by taking layout generation completely out of the controller.
    """
    @staticmethod
    def compile_and_save_md(parent_window, history_elements: list, current_model: str) -> bool:
        """Assembles conversation text blocks and spawns a native Windows save file prompt."""
        if not history_elements:
            return False

        timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        md_document = f"# Local AI Studio Conversation Log\n"
        md_document += f"- **Export Timestamp:** {timestamp_str}\n"
        md_document += f"- **Active Model Engine:** {current_model}\n"
        md_document += f"--- \n\n"

        for element in history_elements:
            if element["role"] == "user":
                md_document += f"### 👤 USER\n{element['text']}\n\n"
            elif element["role"] == "assistant":
                md_document += f"### 🤖 LOCAL ASSISTANT\n{element['text']}\n\n"
                md_document += f"---\n\n"

        file_path, _ = QFileDialog.getSaveFileName(
            parent_window, "Export Conversation History Log", "ai_studio_session.md", "Markdown Documents (*.md)"
        )
        
        if file_path:
            with open(file_path, "w", encoding="utf-8") as md_file:
                md_file.write(md_document)
            return True
            
        return False
