# app_controller.py
import os
import sys

# 🚀 SYSTEM DRIVER LAYER INTERLOCK
os.environ["VK_ICD_FILENAMES"] = ""      
os.environ["DISABLE_VULKAN"] = "1"        
os.environ["GGML_VULKAN_DISABLE"] = "1"   

from PyQt6.QtCore import QObject, QTimer, QUrl, pyqtSlot
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QApplication  # 🚀 IMPORT APPLICATION LEVEL REGISTERS
from PyQt6.QtWebChannel import QWebChannel
from ui.chat_renderer import ChatRenderer
from utils.model_service import ModelService
from utils.clipboard_manager import ClipboardManager

class AppController(QObject):
    """Refactored coordinator focused strictly on responsive Chromium WebEngine text loops."""
    def __init__(self, main_window):
        super().__init__()
        self.win = main_window   
        
        self.model_service = ModelService()
        self.clipboard_manager = ClipboardManager()
        self.win.models_dir = self.model_service.load_initial_directory()
        
        self.worker = None
        self.current_prompt = ""           
        self.current_assistant_html = ""
        self.current_theme = "dark"  
        
        self.chat_history_elements = []  
        self.active_message_id = 0
        self.active_message_running = False  
        
        # Setup Javascript-to-Python direct bridge layer interlock channels
        self.web_channel = QWebChannel()
        self.web_channel.registerObject("pyBackend", self)
        self.win.chat_panel.chat_history.page().setWebChannel(self.web_channel)
        
        # Connect visual layout slots
        self.win.chat_panel.stop_overlay_btn.clicked.connect(self.stop_generation)
        self.win.sidebar.toggle_theme_btn.clicked.connect(self.toggle_application_theme)
        
        if hasattr(self.win.sidebar, 'clear_history_btn'):
            self.win.sidebar.clear_history_btn.clicked.connect(self.clear_logs_database)

    @pyqtSlot(int)
    def executeNativeCopy(self, msg_id: int):
        """Processes full dialogue text card copies into Windows OS system registers smoothly [INDEX]."""
        mock_url_path = f"copy://{msg_id}"
        if self.clipboard_manager.copy_to_clipboard(mock_url_path):
            old_title = self.win.chat_panel.model_tag.text()
            self.win.chat_panel.model_tag.setText("📋 Full Response Copied to Clipboard!")
            QTimer.singleShot(2000, lambda: self.win.chat_panel.model_tag.setText(old_title))

    @pyqtSlot(str)
    def executeDirectTextCopy(self, text_content: str):
        """🚀 THE CODE PILL DIRECT OVERRIDE: Captures isolated raw code content instantly without text headers!"""
        clipboard = QApplication.clipboard()
        clipboard.clear(mode=clipboard.Mode.Clipboard)
        clipboard.setText(text_content.strip(), mode=clipboard.Mode.Clipboard)
        
        # Flash a unique confirmation layout message on the top header title tag
        old_title = self.win.chat_panel.model_tag.text()
        self.win.chat_panel.model_tag.setText("💻 Source Code Block Copied Successfully!")
        QTimer.singleShot(2000, lambda: self.win.chat_panel.model_tag.setText(old_title))

    def scan_models_directory(self):
        active_path = self.model_service.scan_directory(self.win.sidebar.model_selector, self.win.models_dir)
        self.win.active_model_path = active_path
        self.win.chat_panel.model_tag.setText(
            f"Active Model: {self.win.sidebar.model_selector.currentText()}" if active_path else "Active Model: None Detected"
        )

    def handle_model_changed(self, index):
        path = self.win.sidebar.model_selector.itemData(index)
        if path:
            self.win.active_model_path = path
            self.win.chat_panel.model_tag.setText(f"Active Model: {self.win.sidebar.model_selector.itemText(index)}")
            self.model_service.storage.save_model(self.win.active_model_path)
        else:
            self.win.active_model_path = ""

    def load_persistent_settings(self):
        verified_path = self.model_service.verify_and_apply_history(self.win.sidebar.model_selector)
        if verified_path:
            self.win.active_model_path = verified_path
            self.win.chat_panel.model_tag.setText(f"Active Model: {self.win.sidebar.model_selector.currentText()}")

    def execute_prompt_generation(self):
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
        self.active_message_running = False 
        
        self.win.canvas_service.redraw_entire_chat_canvas(self, streaming_text="")
        
        from engine_logic import InferenceWorker
        temp_val = self.win.sidebar.temp_slider.value() / 100.0
        self.worker = InferenceWorker(self.win.active_model_path, prompt, temp_val)
        self.worker.token_received.connect(self.handle_stream_token)
        self.worker.finished.connect(self.generation_cycle_complete)
        self.worker.start()

    def handle_stream_token(self, token):
        self.current_assistant_html += token
        self.win.canvas_service.redraw_entire_chat_canvas(self, streaming_text=self.current_assistant_html)

    def stop_generation(self):
        if self.worker and self.worker.isRunning():
            self.worker.requestInterruption()
            self.current_assistant_html += " *[Response Stopped by User]*"
            self.finalize_response_element()

    def finalize_response_element(self):
        self.active_message_running = False  
        self.chat_history_elements.append({"role": "assistant", "text": self.current_assistant_html})
        self.clipboard_manager.store_response(self.current_assistant_html)
        
        self.win.canvas_service.redraw_entire_chat_canvas(self, streaming_text=self.current_assistant_html, is_final_pass=True)
        
        from utils.history_logger import HistoryLogger
        model_name = self.win.sidebar.model_selector.currentText()
        temp_val = self.win.sidebar.temp_slider.value() / 100.0
        HistoryLogger.log_exchange(model_name, self.current_prompt, self.current_assistant_html, temp_val)

    def toggle_application_theme(self):
        self.current_theme = "light" if self.current_theme == "dark" else "dark"
        self.win.sidebar.toggle_theme_btn.setText(
            "🌓 Switch to Dark Mode" if self.current_theme == "light" else "🌓 Switch to Light Mode"
        )
        
        from ui.theme_manager import ThemeManager
        c = ThemeManager.get_styles(self.current_theme)
        self.win.chat_panel.chat_history.page().setBackgroundColor(QColor.fromString(c['window_bg']))
        
        self.active_message_running = False
        self.win.canvas_service.apply_global_theme_repaint(self)

    def clear_logs_database(self):
        if os.path.exists("chat_history.json"):
            try:
                os.remove("chat_history.json")
                self.clipboard_manager.clear_store()
                self.chat_history_elements.clear()
                self.active_message_running = False
                self.win.canvas_service.redraw_entire_chat_canvas(self)
            except Exception as e:
                print(f"Error removing logs: {str(e)}")

    def toggle_ui_state(self, enabled: bool):
        self.win.chat_panel.send_btn.setEnabled(enabled)
        self.win.chat_panel.input_field.setEnabled(enabled)
        self.win.sidebar.model_selector.setEnabled(enabled)
        self.win.chat_panel.stop_overlay_btn.setVisible(not enabled)

    def generation_cycle_complete(self):
        if self.worker and not self.worker.isInterruptionRequested():
            self.finalize_response_element()
        self.toggle_ui_state(True)
        self.win.chat_panel.input_field.setFocus()
        if self.worker:
            self.worker.quit()
            self.worker.wait()
            self.worker = None

    def save_exit_state(self):
        self.model_service.save_state(self.win.models_dir, self.win.active_model_path)
        if self.worker and self.worker.isRunning():
            self.worker.quit()
            self.worker.wait()
