# ui_sidebar.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QSlider, QPushButton, QProgressBar, QFileDialog
from PyQt6.QtCore import Qt, pyqtSignal
from ui.theme_manager import ThemeManager

class SidebarPanel(QWidget):
    """Left control tray managing local model assets, parameter controls, and file export triggers."""
    directory_changed = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(260)
        self.init_layout()

    def init_layout(self):
        sidebar_layout = QVBoxLayout(self)
        sidebar_layout.setContentsMargins(16, 20, 16, 20)
        sidebar_layout.setSpacing(20)

        # Storage Engine Sections
        self.dir_label = QLabel("MODEL STORAGE TARGET")
        self.change_dir_btn = QPushButton("📁 Change Directory")
        self.change_dir_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.change_dir_btn.clicked.connect(self.select_directory_dialog)
        
        sidebar_layout.addWidget(self.dir_label)
        sidebar_layout.addWidget(self.change_dir_btn)

        self.theme_label = QLabel("INTERFACE APPEARANCE")
        self.toggle_theme_btn = QPushButton("🌓 Switch to Light Mode")
        self.toggle_theme_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        
        sidebar_layout.addWidget(self.theme_label)
        sidebar_layout.addWidget(self.toggle_theme_btn)

        self.model_label = QLabel("SELECT LOCAL AI ENGINE")
        self.model_selector = QComboBox()
        self.model_selector.setCursor(Qt.CursorShape.PointingHandCursor)
        
        sidebar_layout.addWidget(self.model_label)
        sidebar_layout.addWidget(self.model_selector)

        temp_header = QHBoxLayout()
        self.temp_label = QLabel("CREATIVITY (TEMP)")
        self.temp_value_label = QLabel("0.70")
        temp_header.addWidget(self.temp_label)
        temp_header.addStretch()
        temp_header.addWidget(self.temp_value_label)

        self.temp_slider = QSlider(Qt.Orientation.Horizontal)
        self.temp_slider.setMinimum(0)
        self.temp_slider.setMaximum(150)
        self.temp_slider.setValue(70)
        self.temp_slider.setCursor(Qt.CursorShape.SplitHCursor)
        self.temp_slider.valueChanged.connect(self.update_temp_text_readout)

        sidebar_layout.addLayout(temp_header)
        sidebar_layout.addWidget(self.temp_slider)

        ram_header = QHBoxLayout()
        self.ram_title_label = QLabel("SYSTEM RAM MONITOR")
        self.ram_percentage_label = QLabel("0.0%")
        ram_header.addWidget(self.ram_title_label)
        ram_header.addStretch()
        ram_header.addWidget(self.ram_percentage_label)

        self.ram_bar = QProgressBar()
        self.ram_bar.setTextVisible(False)
        self.ram_bar.setFixedHeight(8)

        sidebar_layout.addLayout(ram_header)
        sidebar_layout.addWidget(self.ram_bar)

        sidebar_layout.addStretch()

        # --- UTILITY CONTROLS LAYER ---
        util_section = QWidget()
        util_layout = QVBoxLayout(util_section)
        util_layout.setContentsMargins(0, 0, 0, 0)
        util_layout.setSpacing(10)

        # 🚀 NEW ACTION TRIGGER: The Markdown Export Button
        self.export_chat_btn = QPushButton("📝 Export Chat (.md)")
        self.export_chat_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        
        self.clear_history_btn = QPushButton("🗑️ Clear Local Logs")
        self.clear_history_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        
        util_layout.addWidget(self.export_chat_btn)
        util_layout.addWidget(self.clear_history_btn)
        sidebar_layout.addWidget(util_section)

        self.apply_theme_colors("dark")

    def apply_theme_colors(self, mode: str):
        """THE SIDEBAR METRICS RECOLOR MATRIX: Repaints labels and values instantly without text highlights."""
        c = ThemeManager.get_styles(mode)
        self.setStyleSheet(ThemeManager.get_sidebar_stylesheet(mode))
        
        headers = [self.dir_label, self.theme_label, self.model_label, self.temp_label, self.ram_title_label]
        for header in headers:
            header.setStyleSheet(f"color: {c['text_muted']}; font-size: 11px; font-weight: 700; background: transparent; border: none;")
            
        self.temp_value_label.setStyleSheet(f"color: {c['accent_cyan']}; font-size: 12px; font-weight: 700; background: transparent;")
        self.ram_percentage_label.setStyleSheet(f"color: {c['text_main']}; font-size: 11px; font-weight: 700; background: transparent;")
        
        self.toggle_theme_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {c['input_bg']}; color: {c['accent_cyan']}; 
                font-size: 12px; font-weight: 600; border: 1px solid {c['accent_cyan']};
            }}
            QPushButton:hover {{ background-color: {c['accent_cyan']}; color: {c['window_bg']}; }}
        """)
        
        # Style the Markdown Export Button to look sleek and distinct
        self.export_chat_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {c['input_bg']}; color: {c['text_main']};
                font-size: 12px; font-weight: 600; border: 1px solid {c['border']};
            }}
            QPushButton:hover {{ background-color: #0b57d0; color: white; border: 1px solid #0b57d0; }}
        """)
        
        self.clear_history_btn.setStyleSheet(f"""
            QPushButton {{ background-color: transparent; color: #da373c; font-size: 12px; font-weight: 600; border: 1px solid #da373c; }}
            QPushButton:hover {{ background-color: #da373c; color: #ffffff; }}
        """)

    def update_temp_text_readout(self, value):
        self.temp_value_label.setText(f"{value / 100.0:.2f}")

    def update_ram_tracker(self, percentage: float):
        self.ram_percentage_label.setText(f"{percentage:.1f}%")
        self.ram_bar.setValue(int(percentage))

    def select_directory_dialog(self):
        selected_dir = QFileDialog.getExistingDirectory(self, "Select GGUF Model Workspace Directory", "")
        if selected_dir:
            self.directory_changed.emit(selected_dir)
