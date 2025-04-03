import time
from datetime import datetime


class DummySensor:
    
    def __init__(self):
        self.sensor_types = {
            'mars_base_internal_temperature': (-10, 35),
            'mars_base_external_temperature': (-80, 0),
            'mars_base_internal_humidity': (30, 80),
            'mars_base_external_illuminance': (0, 100000),
            'mars_base_internal_co2': (300, 2000),
            'mars_base_internal_oxygen': (19, 24)
        }
        self.counter = 0
    
    def read(self, sensor_type):
        if sensor_type in self.sensor_types:
            min_val, max_val = self.sensor_types[sensor_type]
            self.counter += 1
            seed = (time.time() * 1000 + self.counter) % 10000
            pseudo_random = (seed * 7919) % 10000 / 10000.0
            
            value = min_val + pseudo_random * (max_val - min_val)
            
            if sensor_type in ['mars_base_internal_temperature', 
                              'mars_base_external_temperature', 
                              'mars_base_internal_humidity']:
                return round(value, 1)
            else:
                return int(value)
        return None


class MissionComputer:
    
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': 0.0,
            'mars_base_external_temperature': 0.0,
            'mars_base_internal_humidity': 0.0,
            'mars_base_external_illuminance': 0,
            'mars_base_internal_co2': 0,
            'mars_base_internal_oxygen': 0
        }
        self.ds = DummySensor()
        self.running = False
        self.history = {key: [] for key in self.env_values.keys()}
        self.last_average_time = time.time()
    
    def pretty_print_dict(self, data):
        result = "{\n"
        for key, value in data.items():
            result += f'  "{key}": {value},\n'
        result = result[:-2] + "\n}"
        return result
    
    def get_sensor_data(self):
        self.running = True
        
        try:
            while self.running:
                current_time = time.time()
                
                for sensor_type in self.env_values.keys():
                    value = self.ds.read(sensor_type)
                    self.env_values[sensor_type] = value
                    
                    self.history[sensor_type].append(value)
                
                print(f'시간: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
                print('현재 환경 데이터:')
                print(self.pretty_print_dict(self.env_values))
                print('-'*50)
                
                if current_time - self.last_average_time >= 300:
                    averages = {}
                    for key, values in self.history.items():
                        if values:
                            averages[key] = sum(values) / len(values)
                        else:
                            averages[key] = 0
                    
                    print('\n' + '='*50)
                    print(f'시간: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
                    print('최근 5분 평균 환경 데이터:')
                    print(self.pretty_print_dict(averages))
                    print('='*50 + '\n')
                    
                    self.history = {key: [] for key in self.env_values.keys()}
                    self.last_average_time = current_time
                
                time.sleep(5)
                
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
        self.running = False
        print('System stopped....')


if __name__ == '__main__':
    print('화성 기지 환경 모니터링 시스템을 시작합니다.')
    print('모니터링을 중지하려면 Ctrl+C를 누르세요.')
    print('-'*50)
    
    RunComputer = MissionComputer()

    RunComputer.get_sensor_data()