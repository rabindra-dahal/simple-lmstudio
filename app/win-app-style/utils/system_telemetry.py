# system_telemetry.py
import psutil

class SystemTelemetry:
    """Queries bare-metal machine stats to monitor performance changes."""
    
    @staticmethod
    def get_ram_metrics() -> dict:
        """
        Fetches detailed, real-time memory telemetry metrics.
        Converts baseline raw bytes to readable Gigabytes (GB).
        """
        vm = psutil.virtual_memory()
        
        # 1024^3 converts bytes directly into Gigabytes (GB)
        gb_factor = 1024 ** 3 
        
        return {
            "percent": vm.percent,
            "used": round(vm.used / gb_factor, 2),
            "available": round(vm.available / gb_factor, 2),
            "total": round(vm.total / gb_factor, 2)
        }
