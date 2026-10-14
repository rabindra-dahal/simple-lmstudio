# chat_renderer.py
import markdown
from .theme_manager import ThemeManager

class ChatRenderer:
    """Compiles a spacious, clean card bubble layout with full light/dark responsiveness."""
    
    @staticmethod
    def get_global_css_header(theme_mode: str = "dark") -> str:
        c = ThemeManager.get_styles(theme_mode)
        return f"""
        <style>
            body {{
                background-color: {c['window_bg']};
                color: {c['text_main']};
                margin: 0px;
                padding: 16px;
                font-family: 'Segoe UI', system-ui, sans-serif;
            }}
            a {{ color: {c['accent_cyan']}; text-decoration: none; font-weight: 600; }}
        </style>
        """

    @staticmethod
    def get_user_bubble_html(prompt: str, theme_mode: str = "dark") -> str:
        c = ThemeManager.get_styles(theme_mode)
        return f"""
        <div style="margin-bottom: 20px; width: 100%; text-align: right; clear: both;">
            <div style="display: inline-block; background-color: {c['bubble_user']}; color: {c['bubble_user_text']}; 
                        padding: 10px 16px; border-radius: 16px 16px 2px 16px; text-align: left; 
                        max-width: 70%; font-size: 14px; line-height: 1.5;">
                {prompt}
            </div>
        </div>
        <div style="clear: both;"></div>
        """

    @staticmethod
    def get_assistant_bubble_html(response_text: str, message_id: int, is_streaming: bool, theme_mode: str = "dark") -> str:
        c = ThemeManager.get_styles(theme_mode)
        
        if is_streaming:
            formatted_text = response_text.replace('\n', '<br>') + " ▌"
        else:
            formatted_text = markdown.markdown(response_text, extensions=['fenced_code', 'tables'])
            
            # Format compiled text variables to look beautiful inside the message panels
            formatted_text = formatted_text.replace('<h1>', f'<h1 style="color: {c["accent_cyan"]}; font-size: 18px; font-weight: 600; margin-top: 0;">')
            formatted_text = formatted_text.replace('<h2>', f'<h2 style="color: {c["accent_cyan"]}; font-size: 16px; font-weight: 600; margin-top: 12px;">')
            formatted_text = formatted_text.replace('<p>', f'<p style="margin: 0px 0px 8px 0px; color: {c["text_main"]}; line-height: 1.5;">')
            formatted_text = formatted_text.replace('<ul>', f'<ul style="margin-top: 4px; margin-bottom: 8px; padding-left: 20px; color: {c["text_main"]};">')
            formatted_text = formatted_text.replace('<li>', f'<li style="margin-bottom: 4px;">')
            formatted_text = formatted_text.replace('<code>', f'<code style="background-color: {c["input_bg"]}; color: #ff79c6; font-family: Consolas, monospace; padding: 2px 4px; border-radius: 4px; font-size: 13px;">')
            formatted_text = formatted_text.replace('<pre>', f'<pre style="background-color: {c["input_bg"]}; padding: 12px; border-radius: 6px; border: 1px solid {c["border"]}; font-family: Consolas, monospace; overflow-x: auto; margin: 10px 0;">')

        # 🚀 THE FIXED ANCHOR ROUTINE: Passing a clean integer ID prevents QTextBrowser from blocking the link
        return f"""
        <div style="margin-bottom: 20px; text-align: left; width: 100%; clear: both;">
            <div style="background-color: {c['bubble_ai']}; border: 1px solid {c['border']};
                        border-radius: 16px 16px 16px 2px; padding: 16px; width: 85%; display: block;">
                <table width="100%" cellspacing="0" cellpadding="0" border="0" style="margin-bottom: 12px;">
                    <tr>
                        <td align="left" style="color: {c['accent_cyan']}; font-size: 11px; font-weight: 700; letter-spacing: 0.5px;">
                            ✨ LOCAL ASSISTANT
                        </td>
                        <td align="right">
                            {" " if is_streaming else f'<a href="copy://{message_id}">📋 COPY TEXT</a>'}
                        </td>
                    </tr>
                </table>
                <div style="color: {c['text_main']}; font-size: 14px; line-height: 1.5;">
                    {formatted_text}
                </div>
            </div>
        </div>
        <div style="clear: both;"></div>
        """
