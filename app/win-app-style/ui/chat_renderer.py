# chat_renderer.py
import markdown
from ui.theme_manager import ThemeManager

class ChatRenderer:
    """Compiles modern, responsive chat components utilizing native CSS Flexbox layers, clean vector icon buttons, and JS bridges."""
    
    @classmethod
    def get_global_css_header(cls, theme_mode: str = "dark") -> str:
        c = ThemeManager.get_styles(theme_mode)
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
            
            /* MINIMALIST VECTOR ICON BUTTON STYLING */
            .copy-icon-btn {{
                cursor: pointer;
                display: inline-block;
                padding: 4px;
                border-radius: 4px;
                transition: background-color 0.2s;
            }}
            .copy-icon-btn:hover {{ background-color: {c['input_bg']}; }}
            .copy-icon-btn svg {{ fill: {c['text_muted']}; transition: fill 0.2s; }}
            .copy-icon-btn:hover svg {{ fill: {c['accent_cyan']}; }}
            
            /* NEW INDIVIDUAL CODE BLOCK WRAPPER STYLES */
            .code-container {{
                margin: 14px 0px;
                border-radius: 8px;
                border: 1px solid {c['border']};
                overflow: hidden;
                width: 100%;
            }}
            .code-header {{
                background-color: {c['input_bg']};
                padding: 6px 16px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                border-bottom: 1px solid {c['border']};
                user-select: none;
            }}
            .code-lang {{
                color: {c['text_muted']};
                font-size: 11px;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }}
            
            /* INTERACTIVE SUBTLE HOVER EFFECT FOR THE INLINE SNIPPET SVG ICON */
            .copy-code-btn {{
                cursor: pointer;
                display: inline-block;
                padding: 4px;
                border-radius: 4px;
                transition: background-color 0.2s;
            }}
            .copy-code-btn:hover {{ background-color: {c['border']}; }}
            .copy-code-btn svg {{ fill: {c['text_muted']}; transition: fill 0.2s; }}
            .copy-code-btn:hover svg {{ fill: {c['accent_cyan']}; }}
            
            .content {{ font-size: 14px; line-height: 1.5; color: {c['text_main']}; }}
            h1, h2, h3 {{ color: {c['accent_cyan']}; margin-top: 12px; margin-bottom: 6px; font-weight: 600; }}
            h1 {{ font-size: 18px; }} h2 {{ font-size: 16px; }}
            p {{ margin: 0px 0px 8px 0px; }}
            ul, ol {{ margin-top: 4px; margin-bottom: 8px; padding-left: 20px; color: {c['text_main']}; }}
            li {{ margin-bottom: 4px; }}
            code {{ background-color: {c['input_bg']}; color: #ff79c6; font-family: 'Consolas', monospace; padding: 2px 4px; border-radius: 4px; font-size: 13px; }}
            
            pre {{ 
                background-color: {c['input_bg']}; 
                padding: 14px; 
                margin: 0px !important; 
                border: none !important; 
                font-family: 'Consolas', monospace; 
                overflow-x: auto; 
            }}
        </style>
        
        <script src="qrc:///qtwebchannel/qwebchannel.js"></script>
        <script>
            var backend = null;
            new QWebChannel(qt.webChannelTransport, function (channel) {{
                backend = channel.objects.pyBackend;
            }});
            
            function triggerCopy(msgId) {{
                if (backend) {{ backend.executeNativeCopy(msgId); }}
            }}
            
            /* 🚀 AUTOMATED INJECTION ENGINE WITH RE-CONFIGURED SVG ICON BUTTON ELEMENT */
            function formatCodeBlocks() {{
                document.querySelectorAll('pre').forEach(function(pre) {{
                    if (pre.parentNode.classList.contains('code-container')) return;
                    
                    var container = document.createElement('div');
                    container.className = 'code-container';
                    
                    var header = document.createElement('div');
                    header.className = 'code-header';
                    
                    // 🚀 FIXED: Replaces the text link with an identical minimalist SVG dual-square vector graphic
                    header.innerHTML = '<span class="code-lang">Source Code</span>' +
                                       '<div class="copy-code-btn" onclick="copyRawCode(this)" title="Copy Code Block">' +
                                       '<svg xmlns="http://w3.org" height="16px" viewBox="0 -960 960 960" width="16px">' +
                                       '<path d="M360-240q-33 0-56.5-23.5T280-320v-480q0-33 23.5-56.5T360-880h360q33 0 56.5 23.5T800-800v480q0 33-23.5 56.5T720-240H360Zm0-80h360v-480H360v480ZM200-80q-33 0-56.5-23.5T120-160v-560h80v560h440v80H200Zm160-240v-480 480Z"/>' +
                                       '</svg></div>';
                    
                    pre.parentNode.insertBefore(container, pre);
                    container.appendChild(header);
                    container.appendChild(pre);
                }});
            }}
            
            function copyRawCode(btn) {{
                var preBlock = btn.parentNode.nextElementSibling;
                var rawCodeText = preBlock.innerText || preBlock.textContent;
                if (backend) {{ backend.executeDirectTextCopy(rawCodeText); }}
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
    def get_copy_svg_markup(message_id: int) -> str:
        """Compiles a clean, pure SVG dual-square copy button matching Google AI Studio."""
        return f"""
        <div class="copy-icon-btn" onclick="triggerCopy({message_id})" title="Copy Entire Response Text">
            <svg xmlns="http://w3.org" height="18px" viewBox="0 -960 960 960" width="18px">
                <path d="M360-240q-33 0-56.5-23.5T280-320v-480q0-33 23.5-56.5T360-880h360q33 0 56.5 23.5T800-800v480q0 33-23.5 56.5T720-240H360Zm0-80h360v-480H360v480ZM200-80q-33 0-56.5-23.5T120-160v-560h80v560h440v80H200Zm160-240v-480 480Z"/>
            </svg>
        </div>
        """

    @staticmethod
    def get_assistant_bubble_html(response_text: str, message_id: int, is_streaming: bool, theme_mode: str = "dark") -> str:
        c = ThemeManager.get_styles(theme_mode)
        if is_streaming:
            formatted_text = response_text.replace('\n', '<br>') + " ▌"
        else:
            formatted_text = markdown.markdown(response_text, extensions=['fenced_code', 'tables'])

        action_button = " " if is_streaming else ChatRenderer.get_copy_svg_markup(message_id)
        return f"""
        <div class="chat-row ai-row" id="ai_row_{message_id}">
            <div class="ai-card">
                <table class="header-table">
                    <tr>
                        <td align="left" class="label-ai">✨ LOCAL ASSISTANT</td>
                        <td align="right" class="copy-btn-container">{action_button}</td>
                    </tr>
                </table>
                <div class="content" id="msg_block_{message_id}">{formatted_text}</div>
            </div>
        </div>
        """

    @staticmethod
    def compile_markdown_payload(raw_text: str, theme_mode: str = "dark") -> str:
        c = ThemeManager.get_styles(theme_mode)
        html = markdown.markdown(raw_text, extensions=['fenced_code', 'tables'])
        html = html.replace('<h1>', f'<h1 style="color: {c["accent_cyan"]}; font-size: 18px; font-weight: 600; margin-top: 0;">')
        html = html.replace('<h2>', f'<h2 style="color: {c["accent_cyan"]}; font-size: 16px; font-weight: 600; margin-top: 12px;">')
        html = html.replace('<p>', f'<p style="margin: 0px 0px 8px 0px; color: {c["text_main"]}; line-height: 1.5;">')
        html = html.replace('<ul>', f'<ul style="margin-top: 4px; margin-bottom: 8px; padding-left: 20px; color: {c["text_main"]};">')
        html = html.replace('<li>', f'<li style="margin-bottom: 4px;">')
        html = html.replace('<code>', f'<code style="background-color: {c["input_bg"]}; color: #ff79c6; font-family: Consolas, monospace; padding: 2px 4px; border-radius: 4px; font-size: 13px;">')
        return html
