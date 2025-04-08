import os
import psutil
import platform
import ast

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
            with open('./4/setting.txt', 'r') as f:
                content = f.read()
                settings = ast.literal_eval(content)
                
                for category in default_settings:
                    if category in settings:
                        default_settings[category].update(settings[category])
                return default_settings
        except (FileNotFoundError, SyntaxError, ValueError) as e:
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
            return {k: v for k, v in all_info.items() 
                   if self.settings['system_info'].get(k, False)}
        except Exception as e:
            return {'error': f'시스템 정보를 가져오는 중 오류 발생: {str(e)}'}

    def get_mission_computer_load(self):
        try:
            all_load = self._get_system_load()
            return {k: v for k, v in all_load.items() 
                   if self.settings['system_load'].get(k, False)}
        except Exception as e:
            return {'error': f'시스템 부하 정보를 가져오는 중 오류 발생: {str(e)}'}

    def format_dict_to_string(self, data):
        return '{' + ', '.join(f"'{k}': {v}" for k, v in data.items()) + '}'

if __name__ == '__main__':
    computer = MissionComputer()
    
    print('시스템 정보:')
    print(computer.format_dict_to_string(computer.get_mission_computer_info()))
    
    print('\n시스템 부하 정보:')
    print(computer.format_dict_to_string(computer.get_mission_computer_load()))
