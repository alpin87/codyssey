import os
import csv
import speech_recognition as sr


def get_audio_files():
    files = []
    for file in os.listdir('.'):
        if file.endswith(('.wav', '.mp3', '.m4a')):
            files.append(file)
    return files


def audio_to_text(files):
    r = sr.Recognizer()
    
    try:
        with sr.AudioFile(files) as source:
            audio = r.record(source)
            text = r.recognize_google(audio, language='ko-KR')
            return text
    except:
        return '인식 실패'


def save_csv(filename, text):
    csv_name = filename.replace('.wav', '.csv').replace('.mp3', '.csv').replace('.m4a', '.csv')
    
    with open(csv_name, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['시간', '텍스트'])
        writer.writerow(['0-전체', text])
    
    print(f'{csv_name} 저장 완료')


def search_keyword(keyword):
    for file in os.listdir('.'):
        if file.endswith('.csv'):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if keyword in content:
                        print(f'{file}에서 발견: {keyword}')
            except:
                pass


def main():
    print('1. STT 변환  2. 키워드 검색')
    choice = input('선택: ')
    
    if choice == '1':
        files = get_audio_files()
        print(f'파일 {len(files)}개 발견')
        
        for file in files:
            print(f'처리중: {file}')
            text = audio_to_text(file)
            save_csv(file, text)
            
    elif choice == '2':
        keyword = input('키워드: ')
        search_keyword(keyword)


if __name__ == '__main__':
    main()