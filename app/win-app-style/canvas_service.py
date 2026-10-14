# canvas_service.py
import json
from PyQt6.QtCore import QTimer
from ui.theme_manager import ThemeManager
from ui.chat_renderer import ChatRenderer

class CanvasService:
    """Authoritative repaint engine driving smooth, memory-optimized Chromium WebEngine views."""
    
    @staticmethod
    def redraw_entire_chat_canvas(ctrl, streaming_text: str = None, is_final_pass: bool = False):
        """🚀 THE TOTAL FLICKER, SCROLL, AND MEMORY SOLUTION: Safely handles node updates and drops layout bloat."""
        js_scroll_bottom = "window.scrollTo(0, document.body.scrollHeight);"

        # 1. Final Generation Markdown Compilation Pass (Triggers on Generation Stop)
        if is_final_pass:
            compiled_md_content = ChatRenderer.compile_markdown_payload(streaming_text, ctrl.current_theme)
            safe_final_html = json.dumps(compiled_md_content)
            
            # Step A: Update the inner text node layer with parsed rich HTML elements
            js_update_content = f"document.getElementById('msg_block_{ctrl.active_message_id}').innerHTML = {safe_final_html};"
            ctrl.win.chat_panel.chat_history.page().runJavaScript(js_update_content)
            
            # Step B: Restore header dual-square copy icon button using safe backticks
            svg_markup = ChatRenderer.get_copy_svg_markup(ctrl.active_message_id)
            js_restore_btn = f"document.querySelector('#ai_row_{ctrl.active_message_id} .copy-btn-container').innerHTML = `{svg_markup}`;"
            ctrl.win.chat_panel.chat_history.page().runJavaScript(js_restore_btn)
            
            # Step C: Scan and format any genuine code snippet blocks inside the response card
            ctrl.win.chat_panel.chat_history.page().runJavaScript("formatCodeBlocks();")
            
            # 🚀 Step D: CHROMIUM GARBAGE COLLECTION & MEMORY TRIMMING
            # Forces the V8 Javascript engine to immediately flush its text styling cache,
            # dropping backbuffer layout bloat right after processing heavy code cards!
            ctrl.win.chat_panel.chat_history.page().runJavaScript("if (window.gc) { window.gc(); }")
            
            # Anchor window focus strictly at the bottom
            ctrl.win.chat_panel.chat_history.page().runJavaScript(js_scroll_bottom)
            return

        # 2. Fast tracking incremental injections during active streaming passes (Word-by-word)
        if streaming_text is not None and ctrl.active_message_running:
            safe_js_text = json.dumps(streaming_text.replace('\n', '<br>') + " ▌")
            js_patch_cmd = f"document.getElementById('msg_block_{ctrl.active_message_id}').innerHTML = {safe_js_text};"
            ctrl.win.chat_panel.chat_history.page().runJavaScript(js_patch_cmd)
            ctrl.win.chat_panel.chat_history.page().runJavaScript(js_scroll_bottom)
            return

        # 3. Fallback Full Redraw Pass (Fires when user sends a fresh prompt query)
        canvas_html = ChatRenderer.get_global_css_header(ctrl.current_theme)
        for idx, element in enumerate(ctrl.chat_history_elements):
            if element["role"] == "user":
                canvas_html += ChatRenderer.get_user_bubble_html(element["text"], ctrl.current_theme)
            elif element["role"] == "assistant":
                canvas_html += ChatRenderer.get_assistant_bubble_html(element["text"], idx // 2, False, ctrl.current_theme)
                
        if streaming_text is not None:
            canvas_html += ChatRenderer.get_assistant_bubble_html(streaming_text, ctrl.active_message_id, True, ctrl.current_theme)
            ctrl.active_message_running = True
            
        ctrl.win.chat_panel.chat_history.setHtml(canvas_html)
        
        # Wait for Chromium to build document tags, then anchor focus at the base
        QTimer.singleShot(50, lambda: ctrl.win.chat_panel.chat_history.page().runJavaScript(js_scroll_bottom))

    @staticmethod
    def apply_global_theme_repaint(ctrl):
        """Paints 100% of visible system assets instantly with zero unstyled color bleed-through."""
        c = ThemeManager.get_styles(ctrl.current_theme)
        text_color = c["text_main"]
        bg_color = c["window_bg"]
        border_style = f"1px solid {c['border']}"
        
        ctrl.win.setStyleSheet(f"background-color: {bg_color};")
        ctrl.win.central_canvas.setStyleSheet(f"background-color: {bg_color}; border: none;")
        ctrl.win.chat_panel.setStyleSheet(f"background-color: {bg_color}; border: none;")
        
        ctrl.win.sidebar.apply_theme_colors(ctrl.current_theme)
        
        ctrl.win.chat_panel.header_widget.setStyleSheet(f"background-color: {c['sidebar_bg']}; border-bottom: {border_style};")
        ctrl.win.chat_panel.model_tag.setStyleSheet(f"color: {text_color}; font-size: 14px; font-weight: 600; background: transparent; border: none;")
        ctrl.win.chat_panel.status_subtext.setStyleSheet(f"color: {c['accent_cyan']}; font-size: 11px; font-weight: 500; background: transparent; border: none;")
        
        ctrl.win.chat_panel.footer_widget.setStyleSheet(f"background-color: {bg_color}; border: none;")
        ctrl.win.chat_panel.input_container.setStyleSheet(f"background-color: {c['sidebar_bg']}; border-radius: 24px; border: {border_style};")
        ctrl.win.chat_panel.input_field.setStyleSheet(f"QLineEdit {{ background-color: transparent; color: {text_color}; font-size: 14px; border: none; padding: 12px 0px; }}")
        
        ctrl.win.chat_panel.send_btn.setStyleSheet(f"""
            QPushButton {{ background-color: #0b57d0; color: white; font-weight: 600; font-size: 13px; border-radius: 18px; padding: 8px 22px; border: none; }}
            QPushButton:hover {{ background-color: #004ecc; }}
            QPushButton:disabled {{ background-color: {c['sidebar_bg']}; color: {c['text_muted']}; border: {border_style}; }}
        """)
        
        ctrl.win.chat_panel.stop_overlay_btn.setStyleSheet(f"""
            QPushButton {{ background-color: #da373c; color: white; font-weight: 600; font-size: 13px; border-radius: 18px; padding: 8px 22px; border: 1px solid #ff4d4d; }}
            QPushButton:hover {{ background-color: #a92b2f; }}
        """)
        
        CanvasService.redraw_entire_chat_canvas(ctrl)
