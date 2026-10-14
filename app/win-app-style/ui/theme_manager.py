# theme_manager.py

class ThemeManager:
    """
    Central style definitions provider for the Local AI Studio workspace.
    Ensures 100% visual translation across all layouts on light/dark mode toggles.
    """
    THEMES = {
        "dark": {
            "window_bg": "#131314",        # Deep velvet backdrop canvas
            "sidebar_bg": "#1e1f20",       # Dark satin sidebar panels
            "border": "#2e3035",           # High-visibility crisp border lines
            "text_main": "#e3e3e3",        # Off-white clean typography
            "text_muted": "#949ba4",       # Muted slate secondary labels
            "bubble_user": "#0b57d0",      # Classic Google royal blue user bubble
            "bubble_user_text": "#ffffff", # Pure white text for user messages
            "bubble_ai": "#1e1f20",        # Distinct card fill to isolate AI responses
            "accent_green": "#23a55a",     # High-visibility metric bar green
            "accent_cyan": "#a8c7fa",      # Soft blue title highlights
            "input_bg": "#2a2b2d"
        },
        "light": {
            "window_bg": "#ffffff",        # Open bright clean canvas
            "sidebar_bg": "#f0f4f9",       # Soft light gray-blue trays
            "border": "#dee2e6",           # Subtle hairline divider line
            "text_main": "#1f1f1f",        # Deep charcoal text font
            "text_muted": "#5f6368",       # Graphite secondary labels
            "bubble_user": "#0b57d0",      # Clear royal blue user bubble
            "bubble_user_text": "#ffffff", # Pure white text for user messages
            "bubble_ai": "#f8f9fa",        # Off-white card fill to contrast canvas
            "accent_green": "#248046",     # Solid forest green metrics
            "accent_cyan": "#0b57d0",      # Deep blue title highlights
            "input_bg": "#e9eef6"
        }
    }

    @classmethod
    def get_styles(cls, mode: str = "dark") -> dict:
        return cls.THEMES.get(mode, cls.THEMES["dark"])

    @classmethod
    def get_sidebar_stylesheet(cls, mode: str) -> str:
        """Generates comprehensive stylesheet overrides forcing full panel color conversions."""
        c = cls.get_styles(mode)
        t = c["text_main"]
        b = c["sidebar_bg"]
        input_bg = c["input_bg"]
        border_color = c["border"]
        
        return f"""
            QWidget {{
                background-color: {b};
                color: {t};
                font-family: 'Segoe UI', Arial, sans-serif;
            }}
            QLabel {{
                background-color: transparent;
                border: none;
            }}
            QComboBox {{
                background-color: {input_bg};
                color: {t};
                border: 1px solid {border_color};
                border-radius: 6px;
                padding: 6px 12px;
            }}
            QComboBox::drop-down {{ border: none; }}
            QComboBox QAbstractItemView {{
                background-color: {input_bg};
                color: {t};
                selection-background-color: #0b57d0;
                selection-color: white;
                border: 1px solid {border_color};
            }}
            QSlider::groove:horizontal {{
                height: 6px;
                background: {input_bg};
                border-radius: 3px;
            }}
            QSlider::sub-page:horizontal {{
                background: #0b57d0;
                border-radius: 3px;
            }}
            QSlider::handle:horizontal {{
                background: {t};
                width: 14px;
                margin-top: -4px;
                margin-bottom: -4px;
                border-radius: 7px;
            }}
            QProgressBar {{
                background-color: {input_bg};
                border-radius: 4px;
                border: none;
            }}
            QProgressBar::chunk {{
                background-color: {c['accent_green']};
                border-radius: 4px;
            }}
            QPushButton {{
                background-color: {input_bg};
                color: {t};
                border-radius: 6px;
                padding: 8px 12px;
                border: 1px solid {border_color};
                font-weight: 500;
            }}
            QPushButton:hover {{
                background-color: #383a40;
                color: white;
            }}
        """
