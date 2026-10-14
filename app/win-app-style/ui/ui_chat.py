# ui_chat.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextBrowser, QLineEdit, QPushButton, QGridLayout
from PyQt6.QtCore import Qt

class ChatPanel(QWidget):
    """Manages the dialogue interface canvas without hardcoded background conflicts."""
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
        
        self.status_subtext = QLabel("✨ Local Engine Active — 100% Offline Pure CPU")
        self.status_subtext.setStyleSheet("font-size: 11px; font-weight: 500;")
        
        meta_layout.addWidget(self.model_tag)
        meta_layout.addWidget(self.status_subtext)
        header_layout.addLayout(meta_layout)
        header_layout.addStretch()
        main_layout.addWidget(self.header_widget)
        
        # --- The Overlay Canvas Mapping Container ---
        canvas_container = QWidget()
        canvas_grid = QGridLayout(canvas_container)
        canvas_grid.setContentsMargins(0, 0, 0, 0)
        
        self.chat_history = QTextBrowser()
        self.chat_history.setOpenLinks(False)
        self.chat_history.setOpenExternalLinks(False)
        self.chat_history.setLineWrapMode(QTextBrowser.LineWrapMode.WidgetWidth)
        self.chat_history.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse | Qt.TextInteractionFlag.LinksAccessibleByMouse
        )
        self.chat_history.document().setDocumentMargin(0)
        canvas_grid.addWidget(self.chat_history, 0, 0)
        
        # The Floating Overlay Stop Button Layout
        self.stop_overlay_btn = QPushButton("🛑 Stop Generation")
        self.stop_overlay_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.stop_overlay_btn.setVisible(False)
        
        canvas_grid.addWidget(self.stop_overlay_btn, 0, 0, Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter)
        main_layout.addWidget(canvas_container)
        
        # --- Bottom Message Input Bar Row ---
        self.footer_widget = QWidget()
        footer_layout = QHBoxLayout(self.footer_widget)
        footer_layout.setContentsMargins(24, 12, 24, 24)
        
        self.input_container = QWidget()
        input_container_layout = QHBoxLayout(self.input_container)
        input_container_layout.setContentsMargins(20, 2, 20, 2)
        
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Message your local model...")
        input_container_layout.addWidget(self.input_field)
        
        self.send_btn = QPushButton("Send")
        
        footer_layout.addWidget(self.input_container)
        footer_layout.addWidget(self.send_btn)
        main_layout.addWidget(self.footer_widget)
