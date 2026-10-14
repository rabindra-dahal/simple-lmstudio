# ui/html_templates.py
from ui.theme_manager import ThemeManager

class HTMLTemplates:
    """Isolates heavy CSS style definitions and JavaScript core snippets from execution loops."""
    
    @classmethod
    def get_header_css(cls, theme_mode: str) -> str:
        c = ThemeManager.get_styles(theme_mode)
        return f"""
        <style>
            * {{ box-sizing: border-box; }}
            body {{
                background-color: {c['window_bg']}; color: {c['text_main']};
                margin: 0px; padding: 24px; font-family: 'Segoe UI', system-ui, sans-serif;
                display: flex; flex-direction: column; gap: 20px;
            }}
            .chat-row {{ display: flex; width: 100%; }}
            .user-row {{ justify-content: flex-end; }}
            .ai-row {{ justify-content: flex-start; }}
            .user-bubble {{
                background-color: {c['bubble_user']}; color: {c['bubble_user_text']};
                padding: 11px 16px; border-radius: 18px 18px 4px 18px;
                max-width: 70%; font-size: 14px; line-height: 1.5; word-wrap: break-word;
            }}
            .ai-card {{
                background-color: {c['bubble_ai']}; border: 1px solid {c['border']};
                border-radius: 18px 18px 18px 4px; padding: 16px; width: 85%; max-width: 85%;
            }}
            .header-table {{ width: 100%; margin-bottom: 10px; border-collapse: collapse; }}
            .label-ai {{ color: {c['accent_cyan']}; font-size: 11px; font-weight: 700; letter-spacing: 0.5px; }}
            .copy-icon-btn, .copy-code-btn {{ cursor: pointer; display: inline-block; padding: 4px; border-radius: 4px; }}
            .copy-icon-btn svg, .copy-code-btn svg {{ fill: {c['text_muted']}; }}
            .copy-icon-btn:hover svg, .copy-code-btn:hover svg {{ fill: {c['accent_cyan']}; }}
            .code-container {{ margin: 14px 0px; border-radius: 8px; border: 1px solid {c['border']}; overflow: hidden; width: 100%; }}
            .code-header {{ background-color: {c['input_bg']}; padding: 6px 16px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid {c['border']}; }}
            .code-lang {{ color: {c['text_muted']}; font-size: 11px; font-weight: 700; text-transform: uppercase; }}
            .content {{ font-size: 14px; line-height: 1.5; color: {c['text_main']}; }}
            h1, h2, h3 {{ color: {c['accent_cyan']}; margin-top: 12px; margin-bottom: 6px; font-weight: 600; font-size: 16px; }}
            p {{ margin: 0px 0px 8px 0px; }}
            ul, ol {{ margin-top: 4px; margin-bottom: 8px; padding-left: 20px; }}
            code {{ background-color: {c['input_bg']}; color: #ff79c6; font-family: 'Consolas', monospace; padding: 2px 4px; border-radius: 4px; font-size: 13px; }}
            pre {{ background-color: {c['input_bg']}; padding: 14px; margin: 0px !important; border: none !important; font-family: 'Consolas', monospace; overflow-x: auto; }}
        </style>
        <script src="qrc:///qtwebchannel/qwebchannel.js"></script>
        <script>
            var backend = null;
            new QWebChannel(qt.webChannelTransport, function (channel) {{ backend = channel.objects.pyBackend; }});
            function triggerCopy(msgId) {{ if (backend) {{ backend.executeNativeCopy(msgId); }} }}
            function formatCodeBlocks() {{
                document.querySelectorAll('pre').forEach(function(pre) {{
                    if (pre.parentNode.classList.contains('code-container')) return;
                    if (pre.querySelector('code') === null || pre.innerHTML.includes('<p>')) return;
                    var container = document.createElement('div'); container.className = 'code-container';
                    var header = document.createElement('div'); header.className = 'code-header';
                    header.innerHTML = '<span class="code-lang">Source Code</span><div class="copy-code-btn" onclick="copyRawCode(this)"><svg xmlns="http://w3.org" height="16px" viewBox="0 -960 960 960" width="16px"><path d="M360-240q-33 0-56.5-23.5T280-320v-480q0-33 23.5-56.5T360-880h360q33 0 56.5 23.5T800-800v480q0 33-23.5 56.5T720-240H360Zm0-80h360v-480H360v480ZM200-80q-33 0-56.5-23.5T120-160v-560h80v560h440v80H200Zm160-240v-480 480Z"/></svg></div>';
                    pre.parentNode.insertBefore(container, pre); container.appendChild(header); container.appendChild(pre);
                }});
            }}
            document.addEventListener("DOMContentLoaded", function() {{ formatCodeBlocks(); }});
            function copyRawCode(btn) {{
                var preBlock = btn.parentNode.nextElementSibling;
                if (backend) {{ backend.executeDirectTextCopy(preBlock.innerText || preBlock.textContent); }}
            }}
        </script>
        """

    @staticmethod
    def get_copy_svg(message_id: int) -> str:
        return f"""
        <div class="copy-icon-btn" onclick="triggerCopy({message_id})" title="Copy Entire Response">
            <svg xmlns="http://w3.org" height="18px" viewBox="0 -960 960 960" width="18px">
                <path d="M360-240q-33 0-56.5-23.5T280-320v-480q0-33 23.5-56.5T360-880h360q33 0 56.5 23.5T800-800v480q0 33-23.5 56.5T720-240H360Zm0-80h360v-480H360v480ZM200-80q-33 0-56.5-23.5T120-160v-560h80v560h440v80H200Zm160-240v-480 480Z"/>
            </svg>
        </div>
        """
