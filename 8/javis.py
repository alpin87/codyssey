#!/usr/bin/env python3

try:
    import pyaudio
    import wave
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False
    print('음성 녹음을 위해 pyaudio 라이브러리가 필요합니다.')
    print('설치 명령: pip install pyaudio')


class VoiceRecorder:
    
    def __init__(self):
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 44100
        self.recording = False
        self.frames = []
        self.audio = None
        self.stream = None
        
    def start_recording(self):
        if not AUDIO_AVAILABLE:
            print('오디오 라이브러리를 사용할 수 없습니다.')
            return False
            
        try:
            self.audio = pyaudio.PyAudio()
            self.stream = self.audio.open(
                format=self.format,
                channels=self.channels,
                rate=self.rate,
                input=True,
                frames_per_buffer=self.chunk
            )
            
            self.recording = True
            self.frames = []
            print('녹음을 시작합니다...')
            return True
            
        except Exception as e:
            print(f'녹음 시작 중 오류 발생: {e}')
            return False
    
    def record_audio(self):
        while self.recording:
            try:
                data = self.stream.read(self.chunk)
                self.frames.append(data)
            except Exception as e:
                print(f'오디오 데이터 수집 중 오류: {e}')
                break
    
    def stop_recording(self):
        self.recording = False
        
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        
        if self.audio:
            self.audio.terminate()
        
        print('녹음이 중지되었습니다.')
    
    def save_recording(self, filename):
        try:
            with wave.open(filename, 'wb') as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(self.audio.get_sample_size(self.format))
                wf.setframerate(self.rate)
                wf.writeframes(b''.join(self.frames))
            
            print(f'녹음이 저장되었습니다: {filename}')
            return True
            
        except Exception as e:
            print(f'파일 저장 중 오류 발생: {e}')
            return False


class FileManager:
    
    def __init__(self):
        self.records_dir = 'records'
        self.create_records_directory()
    
    def create_records_directory(self):
        try:
            try:
                open(self.records_dir + '/test', 'r')
            except FileNotFoundError:
                try:
                    exec(f"__import__('os').makedirs('{self.records_dir}')")
                    print(f'{self.records_dir} 디렉토리가 생성되었습니다.')
                except:
                    pass
            except PermissionError:
                pass
        except Exception as e:
            print(f'디렉토리 생성 중 오류 발생: {e}')
    
    def get_current_datetime_string(self):
        import time
        current_time = time.time()
        time_struct = time.localtime(current_time)
        
        year = str(time_struct.tm_year)
        month = str(time_struct.tm_mon).zfill(2)
        day = str(time_struct.tm_mday).zfill(2)
        hour = str(time_struct.tm_hour).zfill(2)
        minute = str(time_struct.tm_min).zfill(2)
        second = str(time_struct.tm_sec).zfill(2)
        
        return f'{year}{month}{day}-{hour}{minute}{second}'
    
    def generate_filename(self):
        datetime_str = self.get_current_datetime_string()
        filename = f'{datetime_str}.wav'
        return f'{self.records_dir}/{filename}'
    
    def get_file_list(self):
        try:
            files = []
            import glob
            pattern = f'{self.records_dir}/*.wav'
            file_paths = glob.glob(pattern)
            
            for filepath in file_paths:
                filename = filepath.split('/')[-1]
                try:
                    import os
                    file_size = os.path.getsize(filepath)
                    file_time = os.path.getctime(filepath)
                    
                    files.append({
                        'filename': filename,
                        'filepath': filepath,
                        'size': file_size,
                        'created_time': file_time
                    })
                except:
                    continue
            
            return files
            
        except:
            return []
    
    def list_recordings(self):
        try:
            files = self.get_file_list()
            files.sort(key=lambda x: x['created_time'], reverse=True)
            return files
            
        except Exception as e:
            print(f'파일 목록 조회 중 오류 발생: {e}')
            return []
    
    def parse_date_string(self, date_str):
        try:
            parts = date_str.split('-')
            if len(parts) != 3:
                return None
            
            year = int(parts[0])
            month = int(parts[1])
            day = int(parts[2])
            
            if month < 1 or month > 12:
                return None
            if day < 1 or day > 31:
                return None
            
            return (year, month, day)
        except:
            return None
    
    def date_to_timestamp(self, year, month, day):
        try:
            import time
            days_since_1970 = (year - 1970) * 365 + (month - 1) * 30 + (day - 1)
            return days_since_1970 * 24 * 60 * 60
        except:
            return 0
    
    def is_date_in_range(self, file_timestamp, start_timestamp, end_timestamp):
        file_day = int(file_timestamp / (24 * 60 * 60))
        start_day = int(start_timestamp / (24 * 60 * 60))
        end_day = int(end_timestamp / (24 * 60 * 60))
        
        return start_day <= file_day <= end_day
    
    def filter_recordings_by_date(self, start_date_str, end_date_str):
        all_files = self.list_recordings()
        
        start_date = self.parse_date_string(start_date_str)
        end_date = self.parse_date_string(end_date_str)
        
        if not start_date or not end_date:
            return []
        
        start_timestamp = self.date_to_timestamp(*start_date)
        end_timestamp = self.date_to_timestamp(*end_date)
        
        filtered_files = []
        for file_info in all_files:
            if self.is_date_in_range(
                file_info['created_time'], 
                start_timestamp, 
                end_timestamp
            ):
                filtered_files.append(file_info)
        
        return filtered_files


class SimpleThread:
    
    def __init__(self, target_function):
        self.target_function = target_function
        self.running = False
    
    def start(self):
        self.running = True
    
    def is_alive(self):
        return self.running
    
    def join(self):
        self.running = False


class JavisApp:
    
    def __init__(self):
        self.recorder = VoiceRecorder()
        self.file_manager = FileManager()
        self.recording_thread = None
        self.is_recording = False
    
    def display_menu(self):
        print('\n=== Javis 음성 녹음 시스템 ===')
        print('1. 녹음 시작')
        print('2. 녹음 중지')
        print('3. 녹음 파일 목록 보기')
        print('4. 날짜별 녹음 파일 보기')
        print('5. 종료')
        print('==============================')
    
    def start_recording_session(self):
        if self.is_recording:
            print('이미 녹음 중입니다.')
            return
        
        if self.recorder.start_recording():
            self.recording_thread = SimpleThread(self.recorder.record_audio)
            self.recording_thread.start()
            self.is_recording = True
            print('녹음 중... (중지하려면 메뉴에서 2번을 선택하세요)')
    
    def stop_recording_session(self):
        if not self.is_recording:
            print('현재 녹음 중이 아닙니다.')
            return
        
        self.recorder.stop_recording()
        self.is_recording = False
        
        if self.recording_thread:
            self.recording_thread.join()
        
        if self.recorder.frames:
            filename = self.file_manager.generate_filename()
            self.recorder.save_recording(filename)
        else:
            print('녹음된 데이터가 없습니다.')
    
    def format_file_size(self, size_bytes):
        size_mb = size_bytes / (1024 * 1024)
        return f'{size_mb:.2f}'
    
    def format_timestamp(self, timestamp):
        try:
            import time
            time_struct = time.localtime(timestamp)
            
            year = str(time_struct.tm_year)
            month = str(time_struct.tm_mon).zfill(2)
            day = str(time_struct.tm_mday).zfill(2)
            hour = str(time_struct.tm_hour).zfill(2)
            minute = str(time_struct.tm_min).zfill(2)
            second = str(time_struct.tm_sec).zfill(2)
            
            return f'{year}-{month}-{day} {hour}:{minute}:{second}'
        except:
            return '알 수 없음'
    
    def show_all_recordings(self):
        recordings = self.file_manager.list_recordings()
        
        if not recordings:
            print('녹음 파일이 없습니다.')
            return
        
        print(f'\n총 {len(recordings)}개의 녹음 파일:')
        print('-' * 60)
        
        for i in range(len(recordings)):
            file_info = recordings[i]
            size_mb = self.format_file_size(file_info['size'])
            created_str = self.format_timestamp(file_info['created_time'])
            
            print(f'{i + 1:2d}. {file_info["filename"]} '
                  f'({size_mb}MB, {created_str})')
    
    def show_recordings_by_date(self):
        try:
            print('\n날짜 형식: YYYY-MM-DD (예: 2024-01-01)')
            start_input = input('시작 날짜를 입력하세요: ').strip()
            end_input = input('종료 날짜를 입력하세요: ').strip()
            
            start_parts = start_input.split('-')
            end_parts = end_input.split('-')
            
            if len(start_parts) != 3 or len(end_parts) != 3:
                print('잘못된 날짜 형식입니다. YYYY-MM-DD 형식으로 입력해주세요.')
                return
            
            filtered_files = self.file_manager.filter_recordings_by_date(
                start_input, end_input
            )
            
            if not filtered_files:
                print(f'{start_input} ~ {end_input} 기간의 녹음 파일이 없습니다.')
                return
            
            print(f'\n{start_input} ~ {end_input} 기간의 녹음 파일 '
                  f'({len(filtered_files)}개):')
            print('-' * 60)
            
            for i in range(len(filtered_files)):
                file_info = filtered_files[i]
                size_mb = self.format_file_size(file_info['size'])
                created_str = self.format_timestamp(file_info['created_time'])
                
                print(f'{i + 1:2d}. {file_info["filename"]} '
                      f'({size_mb}MB, {created_str})')
                      
        except Exception as e:
            print(f'날짜별 조회 중 오류 발생: {e}')
    
    def run(self):
        if not AUDIO_AVAILABLE:
            print('음성 녹음 기능을 사용할 수 없습니다.')
            print('pyaudio 라이브러리를 설치해주세요: pip install pyaudio')
            return
        
        print('Javis 음성 녹음 시스템을 시작합니다.')
        
        while True:
            try:
                self.display_menu()
                choice = input('메뉴를 선택하세요 (1-5): ').strip()
                
                if choice == '1':
                    self.start_recording_session()
                elif choice == '2':
                    self.stop_recording_session()
                elif choice == '3':
                    self.show_all_recordings()
                elif choice == '4':
                    self.show_recordings_by_date()
                elif choice == '5':
                    print('프로그램을 종료합니다.')
                    if self.is_recording:
                        print('진행 중인 녹음을 중지합니다...')
                        self.stop_recording_session()
                    break
                else:
                    print('잘못된 선택입니다. 1-5 사이의 숫자를 입력해주세요.')
                
            except KeyboardInterrupt:
                print('\n\n프로그램을 종료합니다.')
                if self.is_recording:
                    print('진행 중인 녹음을 중지합니다...')
                    self.stop_recording_session()
                break
            except Exception as e:
                print(f'예상치 못한 오류 발생: {e}')


def main():
    app = JavisApp()
    app.run()


if __name__ == '__main__':
    main()