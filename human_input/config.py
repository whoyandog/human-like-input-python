import json 
import os 

def singleton(cls):
    instances = {}
    
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    
    return get_instance

@singleton
class Settings: 

    def __init__(self, path="config.json"):

        self.hardware = \
        {
            "baudrate": 115200, 
            "timeout": 1.0, 
            "target_devices": [ 
                {"vid": 9025, "pid": 32823 },
                {"vid": 7000, "pid": 37382 },
                {"vid": 9025, "pid": 55 }
            ]
        }
        
        self.typing_settings = \
        {
            "error_rate": 0.03,
            "speed": 100.0
        }

        if os.path.exists(path):
            with open(path, 'r') as f:
                data = json.load(f)
                self.hardware.update(data.get("hardware", {}))
                self.typing_settings.update(data.get("typing_settings", {}))

settings = Settings()
