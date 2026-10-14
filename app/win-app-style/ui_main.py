# ui_main.py
import os
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout
from PyQt6.QtCore import QTimer
from ui.ui_sidebar import SidebarPanel
from ui.ui_chat import ChatPanel
from app_controller import AppController
from canvas_service import CanvasService


class LocalAIStudio(QMainWindow):
    """Primary interface container window orchestrating theme-aware layout placement."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Local AI Development Studio")
        self.resize(1100, 720)
        self.setMinimumSize(850, 550)
        
        self.models_dir = os.path.abspath("./models")
        self.active_model_path = ""
        
        self.init_ui_canvas()
        self.canvas_service = CanvasService()
        
        # Instantiate the coordinator logic backend
        self.controller = AppController(self)
        
        # Execution wiring connections
        self.sidebar.change_dir_btn.clicked.connect(self.trigger_folder_explorer)
        self.sidebar.directory_changed.connect(self.update_workspace_directory)
        self.chat_panel.send_btn.clicked.connect(self.controller.execute_prompt_generation)
        self.chat_panel.input_field.returnPressed.connect(self.controller.execute_prompt_generation)
        
        self.controller.scan_models_directory()
        self.controller.load_persistent_settings()
        
        # Telemetry cycle: Query backend RAM stats dynamically every 1.5 seconds
        self.telemetry_timer = QTimer(self)
        self.telemetry_timer.timeout.connect(self.update_telemetry_readout)
        self.telemetry_timer.start(1500)
        # 🚀 FORCE DARK PRESET INITIALIZATION AT INITIAL APPS LAUNCH STAGE
        self.canvas_service.apply_global_theme_repaint(self.controller)


    def init_ui_canvas(self):
        """Builds sub-layout frameworks side-by-side inside a horizontal matrix."""
        # 🚀 TRACK WITH AN EXPLICIT POINTER HANDLE
        self.central_canvas = QWidget()
        self.setCentralWidget(self.central_canvas)
        
        layout = QHBoxLayout(self.central_canvas)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        self.sidebar = SidebarPanel(self)
        self.chat_panel = ChatPanel(self)
        
        layout.addWidget(self.sidebar)
        layout.addWidget(self.chat_panel)

    def trigger_folder_explorer(self):
        self.sidebar.select_directory_dialog()

    def update_workspace_directory(self, new_path: str):
        self.models_dir = new_path
        self.controller.scan_models_directory()

    def update_telemetry_readout(self):
        """Live refresh matching native psutil indicators."""
        if hasattr(self, 'sidebar') and hasattr(self.sidebar, 'update_ram_tracker'):
            from engine_logic import SystemBackend
            current_ram_usage = SystemBackend.get_ram_usage()
            self.sidebar.update_ram_tracker(current_ram_usage)

    def closeEvent(self, event):
        self.telemetry_timer.stop()
        self.controller.save_exit_state()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    from PyQt6.QtGui import QFont
    app.setFont(QFont("Segoe UI", 10))
    
    studio = LocalAIStudio()
    studio.show()
    sys.exit(app.exec())
