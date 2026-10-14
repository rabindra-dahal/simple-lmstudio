# ui_canvas.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from ..utils.system_telemetry import SystemTelemetry
import gc # Python Garbage Collector module

class SystemMonitorCanvas(QWidget):
    """A highly optimized, memory-safe hardware monitoring dashboard component."""
    def __init__(self, parent=None, width=3, height=2, dpi=100):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Native labels use virtually 0 RAM compared to graphic charts
        self.stats_label = QLabel("Initializing Telemetry Dashboard...")
        self.stats_label.setStyleSheet("""
            color: #00ffcc; 
            font-family: 'Segoe UI', Arial; 
            font-size: 13px; 
            font-weight: 500;
            line-height: 1.6;
        """)
        layout.addWidget(self.stats_label)

    def refresh_graph(self):
        """Pulls bare-metal stats from system telemetry without causing memory leaks."""
        try:
            # 1. Fetch live hardware values
            metrics = SystemTelemetry.get_ram_metrics()
            
            # 2. Update layout text labels instantly
            status_text = (
                f"📊 RAM Status: {metrics['percent']}% Used\n\n"
                f"🔹 System Used: {metrics['used']} GB\n"
                f"🔹 Free Available: {metrics['available']} GB\n"
                f"🔹 Total Hardware: {metrics['total']} GB"
            )
            self.stats_label.setText(status_text)
            
            # 3. THE FORCE RESET: Manually trigger Python to clean up uncollected background array references
            gc.collect()
            
        except Exception as e:
            self.stats_label.setText(f"Telemetry Status: Offline ({str(e)})")
