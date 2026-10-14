# canvas_service.py
from PyQt6.QtGui import QPalette, QColor
from ui.theme_manager import ThemeManager
from ui.chat_renderer import ChatRenderer

class CanvasService:
    """Authoritative repaint engine that injects colors into 100% of visible system assets instantly."""
    
    @staticmethod
    def redraw_entire_chat_canvas(ctrl, streaming_text: str = None):
        ctrl.win.chat_panel.chat_history.document().clear()
        c = ThemeManager.get_styles(ctrl.current_theme)
        
        palette = ctrl.win.chat_panel.chat_history.palette()
        palette.setColor(QPalette.ColorRole.Base, QColor(c['window_bg']))
        palette.setColor(QPalette.ColorRole.Text, QColor(c['text_main']))
        ctrl.win.chat_panel.chat_history.setPalette(palette)
        
        canvas_html = ChatRenderer.get_global_css_header(ctrl.current_theme)
        for idx, element in enumerate(ctrl.chat_history_elements):
            if element["role"] == "user":
                canvas_html += ChatRenderer.get_user_bubble_html(element["text"], ctrl.current_theme)
            elif element["role"] == "assistant":
                canvas_html += ChatRenderer.get_assistant_bubble_html(element["text"], idx // 2, False, ctrl.current_theme)
                
        if streaming_text is not None:
            canvas_html += ChatRenderer.get_assistant_bubble_html(streaming_text, ctrl.active_message_id, True, ctrl.current_theme)
            
        ctrl.win.chat_panel.chat_history.setHtml(canvas_html)
        ctrl.win.chat_panel.chat_history.ensureCursorVisible()

    @staticmethod
    def apply_global_theme_repaint(ctrl):
        """🚀 THE CONVERSION CORE: Overwrites every widget layer to match the active theme hex parameters perfectly."""
        c = ThemeManager.get_styles(ctrl.current_theme)
        text_color = c["text_main"]
        bg_color = c["window_bg"]
        border_style = f"1px solid {c['border']}"
        
        # 1. Paint core window layouts
        ctrl.win.setStyleSheet(f"background-color: {bg_color};")
        ctrl.win.central_canvas.setStyleSheet(f"background-color: {bg_color}; border: none;")
        ctrl.win.chat_panel.setStyleSheet(f"background-color: {bg_color}; border: none;")
        
        # 2. Invoke the deep recolor matrix routines inside the sidebar panels
        ctrl.win.sidebar.apply_theme_colors(ctrl.current_theme)
        
        # 3. Paint top navigation dashboard headers
        ctrl.win.chat_panel.header_widget.setStyleSheet(f"background-color: {c['sidebar_bg']}; border-bottom: {border_style};")
        ctrl.win.chat_panel.model_tag.setStyleSheet(f"color: {text_color}; font-size: 14px; font-weight: 600; background: transparent;")
        ctrl.win.chat_panel.status_subtext.setStyleSheet(f"color: {c['accent_cyan']}; font-size: 11px; font-weight: 500; background: transparent;")
        
        # 4. Paint chat canvas view sheets
        ctrl.win.chat_panel.chat_history.setStyleSheet(f"QTextBrowser {{ background-color: {bg_color}; border: none; padding: 24px; }}")
        
        # 5. 🚀 FIXED: Paint bottom input line capsule box tray and solve invisible typing text layers
        ctrl.win.chat_panel.footer_widget.setStyleSheet(f"background-color: {bg_color}; border: none;")
        ctrl.win.chat_panel.input_container.setStyleSheet(f"background-color: {c['sidebar_bg']}; border-radius: 24px; border: {border_style};")
        ctrl.win.chat_panel.input_field.setStyleSheet(f"QLineEdit {{ background-color: transparent; color: {text_color}; font-size: 14px; border: none; padding: 12px 0px; }}")
        
        # 6. Paint footer interaction buttons
        ctrl.win.chat_panel.send_btn.setStyleSheet(f"""
            QPushButton {{ background-color: #0b57d0; color: white; font-weight: 600; font-size: 13px; border-radius: 18px; padding: 8px 20px; border: none; }}
            QPushButton:hover {{ background-color: #004ecc; }}
            QPushButton:disabled {{ background-color: {c['sidebar_bg']}; color: {c['text_muted']}; border: {border_style}; }}
        """)
        
        # 7. Paint floating overlay stop badges
        ctrl.win.chat_panel.stop_overlay_btn.setStyleSheet(f"""
            QPushButton {{ background-color: {c['sidebar_bg']}; color: {text_color}; font-weight: 600; font-size: 13px; border-radius: 16px; padding: 8px 22px; border: {border_style}; margin-bottom: 20px; }}
            QPushButton:hover {{ background-color: {c['input_bg']}; }}
        """)
        
        # Force fresh canvas redraw loop
        CanvasService.redraw_entire_chat_canvas(ctrl)
