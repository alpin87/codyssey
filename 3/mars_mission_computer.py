import random
import time

class DummySensor:
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': 0.0,
            'mars_base_external_temperature': 0.0,
            'mars_base_internal_humidity': 0.0,
            'mars_base_external_illuminance': 0.0,
            'mars_base_internal_co2': 0.0,
            'mars_base_internal_oxygen': 0.0
        }
    
    def set_env(self):
        env_ranges = {
            'mars_base_internal_temperature': (18.0, 30.0),
            'mars_base_external_temperature': (0.0, 21.0),
            'mars_base_internal_humidity': (50.0, 60.0),
            'mars_base_external_illuminance': (500.0, 715.0),
            'mars_base_internal_co2': (0.02, 0.1),
            'mars_base_internal_oxygen': (4.0, 7.0)
        }
        
        for key, (min_val, max_val) in env_ranges.items():
            self.env_values[key] = round(random.uniform(min_val, max_val), 2)
    
    def get_env(self):
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')
        
        log_entry = (
            f"{current_time}, "
            f"Internal Temp: {self.env_values['mars_base_internal_temperature']}°C, "
            f"External Temp: {self.env_values['mars_base_external_temperature']}°C, "
            f"Internal Humidity: {self.env_values['mars_base_internal_humidity']}%, "
            f"External Illuminance: {self.env_values['mars_base_external_illuminance']} W/m2, "
            f"Internal CO2: {self.env_values['mars_base_internal_co2']}%, "
            f"Internal O2: {self.env_values['mars_base_internal_oxygen']}%"
        )
        
        with open('env_log.txt', 'a') as log_file:
            log_file.write(log_entry + '\n')
        
        return self.env_values

def main():
    ds = DummySensor()
    
    ds.set_env()
    env_data = ds.get_env()
    print(env_data)

if __name__ == '__main__':
    main()