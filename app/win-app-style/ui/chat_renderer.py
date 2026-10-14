# chat_renderer.py
import markdown
from ui.theme_manager import ThemeManager
from ui.html_templates import HTMLTemplates  # 🚀 IMPORT NEW STATIC EXTENSION LAYER

class ChatRenderer:
    """Compiles modern chat viewport elements cleanly without code file block size bloat."""
    
    @classmethod
    def get_global_css_header(cls, theme_mode: str = "dark") -> str:
        return HTMLTemplates.get_header_css(theme_mode)

    @staticmethod
    def get_user_bubble_html(prompt: str, theme_mode: str = "dark") -> str:
        return f'<div class="chat-row user-row"><div class="user-bubble">{prompt}</div></div>'

    @staticmethod
    def get_copy_svg_markup(message_id: int) -> str:
        return HTMLTemplates.get_copy_svg(message_id)

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
