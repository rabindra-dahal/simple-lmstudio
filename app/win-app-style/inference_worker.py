# inference_worker.py
import os
import sys
import logging
from PyQt6.QtCore import QThread, pyqtSignal
from llama_cpp import Llama

# Mute deep C++ console log dumps
logging.getLogger("llama-cpp-python").setLevel(logging.ERROR)

class InferenceWorker(QThread):
    """
    Background worker thread running exclusively on the CPU.
    Leverages clean native threads without any Vulkan memory mapping overhead.
    """
    token_received = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, model_path, prompt, temperature):
        super().__init__()
        self.model_path = model_path
        self.prompt = prompt
        self.temperature = temperature

    def run(self):
        llm = None
        try:
            # Silence internal C++ stderr output to keep Python stable
            old_stdout = os.dup(1)
            old_stderr = os.dup(2)
            to_devnull = os.open(os.devnull, os.O_WRONLY)
            os.dup2(to_devnull, 1)
            os.dup2(to_devnull, 2)

            try:
                # 🚀 LIGHTWEIGHT PURE CPU COMPUTE ENGINE
                llm = Llama(
                    model_path=self.model_path,
                    verbose=False,
                    n_gpu_layers=0,      # Hard-disabled GPU operations
                    n_ctx=2048,          # Tight context ceiling
                    n_threads=4,         # Matches the physical cores of i5-1135G7
                    n_batch=512,         # Fast token processing block size
                    use_mmap=False,      # Stops Windows from virtual caching
                    use_mlock=False      # Allows system to recycle RAM instantly
                )
            finally:
                os.dup2(old_stdout, 1)
                os.dup2(old_stderr, 2)
                os.close(old_stdout)
                os.close(old_stderr)
                os.close(to_devnull)

            # Chat structuring for Llama 3 models
            messages = [
                {"role": "system", "content": "You are a precise, helpful local AI assistant."},
                {"role": "user", "content": self.prompt}
            ]
            
            response_stream = llm.create_chat_completion(
                messages=messages,
                temperature=self.temperature,
                stream=True
            )
            
            for chunk in response_stream:
                if self.isInterruptionRequested():
                    break
                choices = chunk.get('choices', [])
                if choices and len(choices) > 0:
                    delta = choices[0].get('delta', {})
                    content = delta.get('content', '')
                    if content:
                        self.token_received.emit(content)
                        
        except Exception as e:
            self.token_received.emit(f"\n[Execution Error: {str(e)}]")
        finally:
            self.finished.emit()
