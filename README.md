# Local AI Development Studio

A premium, high-performance, and **100% offline desktop chat application** built with Python and PyQt6. This application is specifically optimized for resource-constrained hardware (such as laptops with 8GB RAM), utilizing an asynchronous thread pipeline, localized caching, and an automated Chromium WebEngine viewport to achieve a smooth, zero-flicker conversational experience.

The interface is inspired by the minimalist, open-canvas aesthetic of **Google AI Studio**, featuring floating message capsules, theme-adaptive bordered cards, and specialized code segment extraction tools.

---

## ✨ Key Feature Architecture

* **🎨 Responsive Google AI Studio Layout:** Built using modern CSS Flexbox parameters to enforce strict layout constraints. User queries clip into compact right-aligned capsules, while assistant responses render as beautifully padded cards.
* **🏎️ Zero-Flicker Streaming Core:** Bypasses full-page HTML browser re-renders by utilizing incremental JavaScript inline-node injections (`runJavaScript`) to append text tokens seamlessly word-by-word.
* **💻 Smart Code Snippet Isolation:** Automatically detects raw Markdown programming blocks (`<pre><code>`) and wraps them inside standalone container cards featuring discrete vector icon actions.
* **📋 Dual-Channel Silent Clipboards:** Implements a direct JavaScript-to-Python interaction channel bridge (`QWebChannel`). Clicking a copy icon triggers native clipboard operations instantly without launching external Windows URL schema popups or dialogue errors.
* **📝 Dynamic Session Exporter:** Compiles active conversation matrices, timestamps, and model metadata cleanly into standardized Markdown (`.md`) files via a native Windows OS save prompt.
* **🌓 100% Coordinated Theme Engine:** Swaps between Dark Obsidian and Brilliant White profiles with a single click—completely repainting sidebar menus, combo boxes, text fields, and progress monitors simultaneously.
* **🧠 Auto-Scrolling Viewport Pins:** Embedded JavaScript listeners keep the viewport scroll bars dynamically pinned to the bottom of the page body during active text generations.
* **💾 Memory Accumulator Optimization:** Implements a 5-token micro-buffer accumulator to decrease browser layout tree geometry re-calculation passes by **80%**, preserving hardware lanes during long outputs.

---

## 📂 System Project Structure

```text
simple-lmstudio/
├── app/
│   └── win-app-style/
│       ├── ui_main.py            # Primary application orchestrator & window frame
│       ├── canvas_service.py     # Authoritative UI repaint & JS injection engine
│       ├── app_controller.py     # Lean coordinator for streams & event signaling loops
│       ├── ui/
│       │   ├── ui_chat.py        # Chat panel UI view container (QWebEngineView core)
│       │   ├── ui_sidebar.py     # Left parameter panel layout dashboard
│       │   ├── theme_manager.py  # Global hex layout profile color sheets
│       │   └── html_templates.py # Base HTML, CSS Flexbox layouts, and script blocks
│       └── utils/
│           ├── model_service.py  # Directory scanner and path validation registry
│           ├── clipboard_manager.py # Array matrix textual cache manager
│           └── export_service.py # Session compiler and document layout saving tool
├── models/                       # Target directory for local GGUF models
└── requirements.txt              # System software library dependencies
```

---

## 🛠️ Installation & Workspace Setup

### 1. Clone the Workspace
Ensure you are inside your working directory branch:
```cmd
cd D:\ML\github-mine\simple-lmstudio
```

### 2. Activate Virtual Environment
```cmd
venv\Scripts\activate
```

### 3. Install Dependencies
Install the required compilation frameworks and libraries, including the high-performance Chromium core extension:
```cmd
pip install PyQt6 PyQt6-WebEngine markdown
```

---

## 🚀 Running the Studio Application

1. Ensure your local GGUF model files (e.g., `Llama-3.2-3B-Instruct-Q4_K_M.gguf`) are placed inside your target storage directory folder.
2. Launch the primary interface engine from your virtual environment terminal prompt:
```cmd
python app/win-app-style/ui_main.py
```

### 💡 Resource Tips for 8GB RAM Laptops
Because loading a 3B model consumes roughly 2.0GB of static memory on top of Windows 11 baseline structures, hovering around **93%–96% RAM utilization** during code inference is normal. To keep your hardware cool:
* Adjust the context allocation variable (`n_ctx`) inside your inference script framework to `512` or `1024` tokens.
* Consider utilizing ultra-lightweight models such as **Qwen2.5-1.5B-Instruct** or **Llama-3.2-1B-Instruct** to lower peak memory spikes down to a stable 78% profile!

---

## 📄 License
This architecture project is open-source and maintained under the MIT License.
