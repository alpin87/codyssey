import os
import psutil
import platform

class MissionComputer:
    def __init__(self):
        self.settings = self._load_settings()

    def _load_settings(self):
        default_settings = {
            'system_info': {
                'os': True,
                'os_version': True,
                'cpu_type': True,
                'cpu_cores': True,
                'memory_size': True
            },
            'system_load': {
                'cpu_usage': True,
                'ram_usage': True
            }
        }
        
        try:
            with open('./setting.txt', 'r') as f:
                settings = {}
                lines = f.readlines()
                current_section = None
                
                for line in lines:
                    line = line.strip()
                    if line.startswith('[') and line.endswith(']'):
                        current_section = line[1:-1]
                        settings[current_section] = {}
                    elif '=' in line and current_section:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip().lower() == 'true'
                        settings[current_section][key] = value
                
                for category in default_settings:
                    if category in settings:
                        default_settings[category].update(settings[category])
                        
                return default_settings
        except FileNotFoundError as e:
            print(f'설정 파일을 읽는 중 오류가 발생했습니다. 기본 설정을 사용합니다: {str(e)}')
            return default_settings

    def _get_system_info(self):
        return {
            'os': platform.system(),
            'os_version': platform.version(),
            'cpu_type': platform.processor(),
            'cpu_cores': psutil.cpu_count(),
            'memory_size': f'{round(psutil.virtual_memory().total / (1024**3), 2)}GB'
        }

    def _get_system_load(self):
        return {
            'cpu_usage': psutil.cpu_percent(),
            'ram_usage': psutil.virtual_memory().percent
        }

    def get_mission_computer_info(self):
        try:
            all_info = self._get_system_info()
            result = {k: v for k, v in all_info.items() 
                   if self.settings['system_info'].get(k, False)}
            print(self.pretty_print_dict(result))
            return result
        except Exception as e:
            error_result = {'error': f'시스템 정보를 가져오는 중 오류 발생: {str(e)}'}
            print(self.pretty_print_dict(error_result))
            return error_result

    def get_mission_computer_load(self):
        try:
            all_load = self._get_system_load()
            result = {k: v for k, v in all_load.items() 
                   if self.settings['system_load'].get(k, False)}
            print(self.pretty_print_dict(result))
            return result
        except Exception as e:
            error_result = {'error': f'시스템 부하 정보를 가져오는 중 오류 발생: {str(e)}'}
            print(self.pretty_print_dict(error_result))
            return error_result

    def pretty_print_dict(self, data):
        result = "{\n"
        for key, value in data.items():
            if isinstance(value, str):
                value_str = f'"{value}"'
            else:
                value_str = str(value)
            result += f'  "{key}": {value_str},\n'
        result = result[:-2] + "\n}"
        return result

if __name__ == '__main__':
    runComputer = MissionComputer()
    
    print('시스템 정보:')
    runComputer.get_mission_computer_info()
    
    print('\n시스템 부하 정보:')
    runComputer.get_mission_computer_load()