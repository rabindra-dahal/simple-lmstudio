# history_logger.py
import os
import json
from datetime import datetime
from engine_logic import SystemBackend  # 🚀 Hook into our existing telemetry backend tool

class HistoryLogger:
    """
    Manages automated disk storage serialization for your local dialogue strings.
    Appends conversation pairs and hardware usage logs into a single structured JSON array.
    """
    FILE_NAME = "chat_history.json"

    @classmethod
    def log_exchange(cls, model_name: str, prompt: str, response: str, temperature: float):
        """
        Records an active prompt-response text exchange layout block, updates 
        the local tracking file, and records peak system RAM usage.
        """
        # 🚀 NEW: Grab bare-metal RAM status at the exact second the response completes [INDEX]
        live_ram_percentage = SystemBackend.get_ram_usage()

        # Structure the enhanced data log exchange element payload
        exchange_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "model_utilized": model_name,
            "configuration": {
                "temperature": temperature
            },
            # 🚀 NEW: Append live resource footprint info inside the log block
            "telemetry": {
                "system_ram_utilization_percent": live_ram_percentage
            },
            "conversation": {
                "user_prompt": prompt,
                "assistant_response": response
            }
        }

        history_data = []

        # Safely read previous conversation blocks from the file
        if os.path.exists(cls.FILE_NAME):
            try:
                with open(cls.FILE_NAME, "r", encoding="utf-8") as f:
                    file_content = f.read().strip()
                    if file_content:
                        history_data = json.loads(file_content)
                        if not isinstance(history_data, list):
                            history_data = []
            except Exception as e:
                print(f"[History Logger Read Warning: {str(e)} - Resetting JSON structural bounds]")
                history_data = []

        # Append the newest exchange entry to the collection array list
        history_data.append(exchange_entry)

        # Write the structural context block safely to disk
        try:
            with open(cls.FILE_NAME, "w", encoding="utf-8") as f:
                json.dump(history_data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"[History Logger Write Failure: Cannot record dialogue data block: {str(e)}]")
