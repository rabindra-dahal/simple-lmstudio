# chat_renderer.py
import markdown
from ui.theme_manager import ThemeManager

class ChatRenderer:
    """Compiles modern, responsive chat components utilizing native CSS Flexbox layers and JS bridges."""
    
    @classmethod
    def get_global_css_header(cls, theme_mode: str = "dark") -> str:
        c = ThemeManager.get_styles(theme_mode)
        # 🚀 Double curly braces {{ }} allow JavaScript to reside safely inside an f-string!
        return f"""
        <style>
            * {{ box-sizing: border-box; }}
            body {{
                background-color: {c['window_bg']};
                color: {c['text_main']};
                margin: 0px;
                padding: 24px;
                font-family: 'Segoe UI', system-ui, sans-serif;
                display: flex;
                flex-direction: column;
                gap: 20px;
            }}
            .chat-row {{ display: flex; width: 100%; }}
            .user-row {{ justify-content: flex-end; }}
            .ai-row {{ justify-content: flex-start; }}
            
            .user-bubble {{
                background-color: {c['bubble_user']};
                color: {c['bubble_user_text']};
                padding: 11px 16px;
                border-radius: 18px 18px 4px 18px;
                max-width: 70%;
                font-size: 14px;
                line-height: 1.5;
                word-wrap: break-word;
            }}
            .ai-card {{
                background-color: {c['bubble_ai']};
                border: 1px solid {c['border']};
                border-radius: 18px 18px 18px 4px;
                padding: 16px;
                width: 85%;
                max-width: 85%;
            }}
            .header-table {{ width: 100%; margin-bottom: 10px; border-collapse: collapse; }}
            .label-ai {{ color: {c['accent_cyan']}; font-size: 11px; font-weight: 700; letter-spacing: 0.5px; }}
            .copy-btn {{ color: {c['text_muted']}; text-decoration: none; font-size: 11px; font-weight: 600; cursor: pointer; }}
            .copy-btn:hover {{ color: {c['accent_cyan']}; }}
            
            .content {{ font-size: 14px; line-height: 1.5; color: {c['text_main']}; }}
            h1, h2, h3 {{ color: {c['accent_cyan']}; margin-top: 12px; margin-bottom: 6px; font-weight: 600; }}
            h1 {{ font-size: 18px; }} h2 {{ font-size: 16px; }}
            p {{ margin: 0px 0px 8px 0px; }}
            ul, ol {{ margin-top: 4px; margin-bottom: 8px; padding-left: 20px; }}
            li {{ margin-bottom: 4px; }}
            code {{ background-color: {c['input_bg']}; color: #ff79c6; font-family: 'Consolas', monospace; padding: 2px 4px; border-radius: 4px; font-size: 13px; }}
            pre {{ background-color: {c['input_bg']}; padding: 12px; border-radius: 6px; border: 1px solid {c['border']}; font-family: 'Consolas', monospace; overflow-x: auto; margin: 10px 0; }}
        </style>
        
        <!-- THE NATIVE JAVA INTERCEPTOR CORE: Securely binds bridge events -->
        <script src="qrc:///qtwebchannel/qwebchannel.js"></script>
        <script>
            var backend = null;
            new QWebChannel(qt.webChannelTransport, function (channel) {{
                backend = channel.objects.pyBackend;
            }});
            function triggerCopy(msgId) {{
                if (backend) {{ backend.executeNativeCopy(msgId); }}
            }}
        </script>
        """

    @staticmethod
    def get_user_bubble_html(prompt: str, theme_mode: str = "dark") -> str:
        return f"""
        <div class="chat-row user-row">
            <div class="user-bubble">{prompt}</div>
        </div>
        """

    @staticmethod
    def get_assistant_bubble_html(response_text: str, message_id: int, is_streaming: bool, theme_mode: str = "dark") -> str:
        c = ThemeManager.get_styles(theme_mode)
        if is_streaming:
            formatted_text = response_text.replace('\n', '<br>') + " ▌"
        else:
            formatted_text = markdown.markdown(response_text, extensions=['fenced_code', 'tables'])

        action_button = " " if is_streaming else f'<span class="copy-btn" onclick="triggerCopy({message_id})">📋 COPY TEXT</span>'
        
        return f"""
        <div class="chat-row ai-row" id="ai_row_{message_id}">
            <div class="ai-card">
                <table class="header-table">
                    <tr>
                        <td align="left" class="label-ai">✨ LOCAL ASSISTANT</td>
                        <!-- 🚀 CONTAINER ANCHOR HOOK: Target cell for finalize pass -->
                        <td align="right" class="copy-btn-container">{action_button}</td>
                    </tr>
                </table>
                <div class="content" id="msg_block_{message_id}">{formatted_text}</div>
            </div>
        </div>
        """

    @staticmethod
    def compile_markdown_payload(raw_text: str, theme_mode: str = "dark") -> str:
        """Exposes clean standalone markdown transformations directly to the canvas service [INDEX]."""
        c = ThemeManager.get_styles(theme_mode)
        html = markdown.markdown(raw_text, extensions=['fenced_code', 'tables'])
        html = html.replace('<h1>', f'<h1 style="color: {c["accent_cyan"]}; font-size: 18px; font-weight: 600; margin-top: 0;">')
        html = html.replace('<h2>', f'<h2 style="color: {c["accent_cyan"]}; font-size: 16px; font-weight: 600; margin-top: 12px;">')
        html = html.replace('<p>', f'<p style="margin: 0px 0px 8px 0px; color: {c["text_main"]}; line-height: 1.5;">')
        html = html.replace('<ul>', f'<ul style="margin-top: 4px; margin-bottom: 8px; padding-left: 20px; color: {c["text_main"]};">')
        html = html.replace('<li>', f'<li style="margin-bottom: 4px;">')
        html = html.replace('<code>', f'<code style="background-color: {c["input_bg"]}; color: #ff79c6; font-family: Consolas, monospace; padding: 2px 4px; border-radius: 4px; font-size: 13px;">')
        html = html.replace('<pre>', f'<pre style="background-color: {c["input_bg"]}; padding: 12px; border-radius: 6px; border: 1px solid {c["border"]}; font-family: Consolas, monospace; overflow-x: auto; margin: 10px 0;">')
        return html
