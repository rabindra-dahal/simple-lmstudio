# ui_chat.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtGui import QColor  # 🚀 CRITICAL FOR FLASH OVERRIDES
from PyQt6.QtCore import Qt

class ChatPanel(QWidget):
    """Manages the dialogue interface canvas utilizing a high-performance Chromium view core."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_layout()

    def init_layout(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # --- Top Navigation Header Bar Panel ---
        self.header_widget = QWidget()
        header_layout = QHBoxLayout(self.header_widget)
        header_layout.setContentsMargins(24, 12, 24, 12)
        
        meta_layout = QVBoxLayout()
        self.model_tag = QLabel("Active Model: None Detected")
        self.model_tag.setStyleSheet("font-size: 14px; font-weight: 600; font-family: 'Segoe UI';")
        
        self.status_subtext = QLabel("Local AI Studio — 100% Offline Pure CPU")
        self.status_subtext.setStyleSheet("font-size: 11px; font-weight: 500;")
        
        meta_layout.addWidget(self.model_tag)
        meta_layout.addWidget(self.status_subtext)
        header_layout.addLayout(meta_layout)
        header_layout.addStretch()
        main_layout.addWidget(self.header_widget)
        
        # --- THE CHROMIUM WEB VIEW COMPONENT CANVAS ---
        self.chat_history = QWebEngineView()
        
        # 🚀 THE NATIVE BLINK KILL SWITCH:
        # Forcefully sets the underlying C++ rendering engine base canvas background color
        # to dark obsidian before any webpage content can build.
        # self.chat_history.page().setBackgroundColor(QColor("#131314"))
        self.chat_history.page().setBackgroundColor(QColor.fromString("#131314"))
        
        main_layout.addWidget(self.chat_history)
        
        # --- Bottom Message Input Bar Row ---
        self.footer_widget = QWidget()
        footer_layout = QHBoxLayout(self.footer_widget)
        footer_layout.setContentsMargins(24, 12, 24, 24)
        footer_layout.setSpacing(12)
        
        self.input_container = QWidget()
        input_container_layout = QHBoxLayout(self.input_container)
        input_container_layout.setContentsMargins(20, 2, 20, 2)
        
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Message your local model...")
        input_container_layout.addWidget(self.input_field)
        footer_layout.addWidget(self.input_container)
        
        # Bottom side-by-side action buttons
        self.stop_overlay_btn = QPushButton("🛑 Stop")
        self.stop_overlay_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.stop_overlay_btn.setVisible(False)
        
        self.send_btn = QPushButton("Send")
        self.send_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        
        footer_layout.addWidget(self.stop_overlay_btn)
        footer_layout.addWidget(self.send_btn)
        main_layout.addWidget(self.footer_widget)
