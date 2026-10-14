# app_controller.py
import os
import sys

# 🚀 SYSTEM DRIVER LAYER INTERLOCK
# Completely blocks the Intel graphics driver from allocating a heavy Vulkan RAM heap.
os.environ["VK_ICD_FILENAMES"] = ""      
os.environ["DISABLE_VULKAN"] = "1"        
os.environ["GGML_VULKAN_DISABLE"] = "1"   

from PyQt6.QtCore import QObject, QTimer
from engine_logic import InferenceWorker
from ui.chat_renderer import ChatRenderer
from utils.model_service import ModelService
from utils.clipboard_manager import ClipboardManager

class AppController(QObject):
    """
    Lightweight runtime orchestrator refactored to prevent system overflow crashes.
    Delegates parsing matrices and preference storage arrays to modular sub-services.
    """
    def __init__(self, main_window):
        super().__init__()
        self.win = main_window   
        
        # Instantiate standalone modular sub-services matching our blueprint architecture
        self.model_service = ModelService()
        self.clipboard_manager = ClipboardManager()
        
        self.win.models_dir = self.model_service.load_initial_directory()
        self.worker = None
        self.current_prompt = ""           
        self.current_assistant_html = ""
        self.current_theme = "dark"  
        
        # Unified tracking matrices
        self.chat_history_elements = []  
        self.active_message_id = 0
        
        # Connect visual layout slots
        self.win.chat_panel.stop_overlay_btn.clicked.connect(self.stop_generation)
        self.win.chat_panel.chat_history.anchorClicked.connect(self.handle_anchor_navigation)
        self.win.sidebar.toggle_theme_btn.clicked.connect(self.toggle_application_theme)
        
        if hasattr(self.win.sidebar, 'clear_history_btn'):
            self.win.sidebar.clear_history_btn.clicked.connect(self.clear_logs_database)

    def scan_models_directory(self):
        """Delegates folder scanning routines straight to the ModelService module."""
        active_path = self.model_service.scan_directory(self.win.sidebar.model_selector, self.win.models_dir)
        self.win.active_model_path = active_path
        self.win.chat_panel.model_tag.setText(
            f"Active Model: {self.win.sidebar.model_selector.currentText()}" if active_path else "Active Model: None Detected"
        )

    def handle_model_changed(self, index):
        """Swaps active model tracking paths when user updates selection boxes."""
        path = self.win.sidebar.model_selector.itemData(index)
        if path:
            self.win.active_model_path = path
            self.win.chat_panel.model_tag.setText(f"Active Model: {self.win.sidebar.model_selector.itemText(index)}")
            self.model_service.storage.save_model(self.win.active_model_path)
        else:
            self.win.active_model_path = ""

    def load_persistent_settings(self):
        """Loads previous model states verified by service layers to exist on disk."""
        verified_path = self.model_service.verify_and_apply_history(self.win.sidebar.model_selector)
        if verified_path:
            self.win.active_model_path = verified_path
            self.win.chat_panel.model_tag.setText(f"Active Model: {self.win.sidebar.model_selector.currentText()}")

    def execute_prompt_generation(self):
        """Spawns non-blocking asynchronous background computational structures on prompt submission."""
        if not self.win.active_model_path or (self.worker and self.worker.isRunning()):
            return
        prompt = self.win.chat_panel.input_field.text().strip()
        if not prompt:
            return
            
        self.current_prompt = prompt  
        self.chat_history_elements.append({"role": "user", "text": prompt})
        self.current_assistant_html = ""
        self.win.chat_panel.input_field.clear()
        self.toggle_ui_state(False)
        
        self.active_message_id = self.clipboard_manager.get_next_index_id()
        self.win.canvas_service.redraw_entire_chat_canvas(self, streaming_text="")
        
        temp_val = self.win.sidebar.temp_slider.value() / 100.0
        self.worker = InferenceWorker(self.win.active_model_path, prompt, temp_val)
        self.worker.token_received.connect(self.handle_stream_token)
        self.worker.finished.connect(self.generation_cycle_complete)
        self.worker.start()

    def handle_stream_token(self, token):
        """Streams raw text fragments directly inside the active response bubble tracking frames."""
        self.current_assistant_html += token
        self.win.canvas_service.redraw_entire_chat_canvas(self, streaming_text=self.current_assistant_html)

    def stop_generation(self):
        """🛑 ABORT SWITCH: Commands the background thread loop to break instantly."""
        if self.worker and self.worker.isRunning():
            self.worker.requestInterruption()
            self.current_assistant_html += " *[Response Stopped by User]*"
            self.finalize_response_element()

    def finalize_response_element(self):
        """Appends the final, completed message block to the history array lists."""
        self.chat_history_elements.append({"role": "assistant", "text": self.current_assistant_html})
        self.clipboard_manager.store_response(self.current_assistant_html)
        self.win.canvas_service.redraw_entire_chat_canvas(self)
        
        from utils.history_logger import HistoryLogger
        model_name = self.win.sidebar.model_selector.currentText()
        temp_val = self.win.sidebar.temp_slider.value() / 100.0
        HistoryLogger.log_exchange(model_name, self.current_prompt, self.current_assistant_html, temp_val)

    def handle_anchor_navigation(self, url):
        """Delegates clipboard copy routines straight to the ClipboardManager module."""
        if self.clipboard_manager.copy_to_clipboard(url.toString()):
            old_title = self.win.chat_panel.model_tag.text()
            self.win.chat_panel.model_tag.setText("📋 Response Text Successfully Copied to Clipboard!")
            QTimer.singleShot(2000, lambda: self.win.chat_panel.model_tag.setText(old_title))

    def toggle_application_theme(self):
        """🚀 THE CONVERSION MACHINE: Delegates window color re-painting to the canvas sub-service."""
        self.current_theme = "light" if self.current_theme == "dark" else "dark"
        self.win.sidebar.toggle_theme_btn.setText(
            "🌓 Switch to Dark Mode" if self.current_theme == "light" else "🌓 Switch to Light Mode"
        )
        self.win.canvas_service.apply_global_theme_repaint(self)

    def clear_logs_database(self):
        """Wipes the local history JSON array file clean on demand."""
        if os.path.exists("chat_history.json"):
            try:
                os.remove("chat_history.json")
                self.clipboard_manager.clear_store()
                self.chat_history_elements.clear()
                self.win.chat_panel.chat_history.clear()
                self.win.canvas_service.redraw_entire_chat_canvas(self)
            except Exception as e:
                print(f"Error removing logs: {str(e)}")

    def toggle_ui_state(self, enabled: bool):
        """Locks input states and handles floating stop overlay visibility dynamics."""
        self.win.chat_panel.send_btn.setEnabled(enabled)
        self.win.chat_panel.input_field.setEnabled(enabled)
        self.win.sidebar.model_selector.setEnabled(enabled)
        self.win.chat_panel.stop_overlay_btn.setVisible(not enabled)

    def generation_cycle_complete(self):
        """Cleans up active thread structures safely upon completion."""
        if self.worker and not self.worker.isInterruptionRequested():
            self.finalize_response_element()
        self.toggle_ui_state(True)
        self.win.chat_panel.input_field.setFocus()
        if self.worker:
            self.worker.quit()
            self.worker.wait()
            self.worker = None

    def save_exit_state(self):
        """Preserves workspace folder logs and preference paths cleanly upon application window exit."""
        self.model_service.save_state(self.win.models_dir, self.win.active_model_path)
        if self.worker and self.worker.isRunning():
            self.worker.quit()
            self.worker.wait()
