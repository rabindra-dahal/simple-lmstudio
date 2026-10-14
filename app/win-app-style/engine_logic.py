# engine_logic.py
import os
import psutil
import logging
from PyQt6.QtCore import QThread, pyqtSignal
from llama_cpp import Llama

# Suppress core C++ internal log trace warnings out of the terminal view
logging.getLogger("llama-cpp-python").setLevel(logging.ERROR)

class InferenceWorker(QThread):
    """
    Asynchronous background computing loop mapped strictly to CPU execution lanes.
    Safely unpacks index-nested text deltas and intercepts interruptions instantly.
    """
    token_received = pyqtSignal(str)  # Emitted word-by-word as text chunks arrive
    finished = pyqtSignal()          # Emitted when the engine completes generation

    def __init__(self, model_path, prompt, temperature):
        super().__init__()
        self.model_path = model_path
        self.prompt = prompt
        self.temperature = temperature

    def run(self):
        try:
            # Re-route low-level stream output descriptors to keep the terminal output silent
            old_stdout = os.dup(1)
            old_stderr = os.dup(2)
            to_devnull = os.open(os.devnull, os.O_WRONLY)
            os.dup2(to_devnull, 1)
            os.dup2(to_devnull, 2)

            try:
                # 🚀 ULTRA-LIGHT CPU EXECUTION BUFFER PROFILE
                # Running Vulkan-free keeps memory allocations isolated strictly to CPU lanes
                llm = Llama(
                    model_path=self.model_path, 
                    verbose=False,
                    n_gpu_layers=0,      # Zero out GPU offloading to stop Iris Xe RAM mirroring
                    n_ctx=2048,          # Bounded dialogue memory ceiling to prevent cache spikes
                    n_threads=4,         # Perfectly matches the physical core count of your i5 CPU
                    n_batch=32,          # Drops token parsing sizes down to protect memory registers
                    n_ubatch=32,        
                    use_mmap=False,      # Direct RAM sequential reading instead of virtual page files
                    use_mlock=False      # Allows instant OS memory recycling
                )
            finally:
                os.dup2(old_stdout, 1)
                os.dup2(old_stderr, 2)
                os.close(old_stdout)
                os.close(old_stderr)
                os.close(to_devnull)

            # Map user inputs cleanly into standard ChatML structural templates
            messages = [
                {"role": "system", "content": "You are a precise, helpful local AI assistant."},
                {"role": "user", "content": self.prompt}
            ]
            
            response_stream = llm.create_chat_completion(
                messages=messages,
                temperature=self.temperature,
                stream=True
            )
            
            # 🔄 RECURRENT TOKEN LOOP: Extract incoming chunks safely
            for chunk in response_stream:
                # 🛑 THE USER BUTTON SIGNAL INTERLOCK CHECK
                # Instantly breaks execution loop if the stop generation button is clicked
                if self.isInterruptionRequested():
                    break
                    
                choices = chunk.get('choices', [])
                if choices and len(choices) > 0:
                    # 🚀 THE CRITICAL ARRAY DEREFERENCE FIX:
                    # Extract index 0 immediately if the server returns a list container array
                    first_choice = choices[0] if isinstance(choices, list) else choices
                    
                    if isinstance(first_choice, dict):
                        delta = first_choice.get('delta', {})
                        content = delta.get('content', '')
                        
                        # Pass the clean, extracted text fragment string straight to the UI thread
                        if content:
                            self.token_received.emit(content)
                    
        except Exception as e:
            self.token_received.emit(f"\n[Engine Processing Failure: {str(e)}]")
        finally:
            self.finished.emit()


class SystemBackend:
    """Manages system metrics extraction and file checks completely decoupled from presentation logic."""
    
    @staticmethod
    def get_ram_usage() -> float:
        """Extracts the system's current live physical RAM utilization percentage metric."""
        return psutil.virtual_memory().percent

    @staticmethod
    def discover_gguf_models(directory_path: str) -> list:
        """Scans the local directory and filters down output files exclusively to .gguf formats."""
        if not os.path.exists(directory_path):
            try:
                os.makedirs(directory_path)
            except Exception:
                return []
        return [f for f in os.listdir(directory_path) if f.endswith('.gguf')]
