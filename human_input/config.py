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
            "handshake_timeout": 0.05,
            "handshake_attempts": 5,
            "command_timeout": 1,
            "target_devices": [ 
                {"vid": 9025, "pid": 32823 },
                {"vid": 7000, "pid": 37382 },
                {"vid": 9025, "pid": 55 }
            ]
        }
        
        self.typing_settings = \
        {
            "error_rate": 0.03,
            "speed": 85.0,
            "layout": "en",
            "timing": {
                "interval_std_ratio": 0.30,
                "min_interval": 0.015,
                "space_pause_min": 0.08,
                "space_pause_max": 0.24,
                "typo_reaction_min": 0.12,
                "typo_reaction_max": 0.38,
                "shift_down_multiplier": 0.45,
                "key_hold_multiplier": 0.70,
                "shift_up_multiplier": 0.30,
                "post_key_multiplier": 1.00,
                "backspace_hold_multiplier": 0.55,
                "post_backspace_multiplier": 0.85,
                "shift_lead_min_multiplier": 0.35,
                "shift_lead_max_multiplier": 1.40,
                "shift_release_lag_min_multiplier": 0.10,
                "shift_release_lag_max_multiplier": 1.05,
                "shift_sticky_probability": 0.035,
                "shift_sticky_correction_probability": 0.85
            }
        }

        if os.path.exists(path):
            with open(path, 'r') as f:
                data = json.load(f)
                self.hardware.update(data.get("hardware", {}))
                input_typing = data.get("typing_settings", {})
                input_timing = input_typing.get("timing")

                self.typing_settings.update(input_typing)
                if isinstance(input_timing, dict):
                    self.typing_settings["timing"].update(input_timing)

settings = Settings()
