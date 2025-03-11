print('Hello Mars')

try:
    with open('./mission_computer_main.log', 'r') as file:
        log_content = file.read()
        print(log_content)

        # 로그 라인 분리
        log_lines = log_content.strip().split('\n')

        # 보너스 1: 시간 역순으로 정렬
        sorted_lines = sorted(log_lines, reverse=True)

        print('\n=== 시간 역순 정렬 ===')
        for line in sorted_lines:
            print(line)

        # 보너스 2: 문제 부분 저장
        error_keywords = ['error', 'failure', 'failed', 'critical', 'warning', 'exception', 'explosion', 'unstable']
        problem_lines = []

        for line in log_lines:
            if any(keyword in line.lower() for keyword in error_keywords):
                problem_lines.append(line)

        # 문제 로그 파일에 저장
        if problem_lines:
            with open('problem_logs.txt', 'w') as problem_file:
                for line in problem_lines:
                    problem_file.write(line + '\n')
            print('문제가 발생한 로그를 problem_logs.txt 파일에 저장했습니다.')

        # 분석 보고서 작성
        with open('log_analysis.md', 'w', encoding='utf-8') as report_file:
            report_file.write('# 미션 컴퓨터 로그 분석 보고서\n\n')
            report_file.write('## 개요\n\n')
            report_file.write('mission_computer_main.log 파일 분석을 통해 사고의 원인을 파악했습니다.\n\n')

            report_file.write('## 로그 요약\n\n')
            report_file.write(f'- 총 로그 항목 수: {len(log_lines)}개\n')
            report_file.write(f'- 문제가 발생한 항목 수: {len(problem_lines)}개\n')
            report_file.write(f'- 로그 기록 시간 범위: {log_lines[0].split(",")[0]} ~ {sorted_lines[0].split(",")[0]}\n\n')

            report_file.write('## 문제 원인\n\n')
            report_file.write('로그 분석 결과, 다음과 같은 주요 문제점이 발견되었습니다:\n\n')
            report_file.write('1. 산소 탱크 불안정 상태 발생 (2023-08-27 11:35:00)\n')
            report_file.write('2. 산소 탱크 폭발 사고 발생 (2023-08-27 11:40:00)\n\n')

            report_file.write('## 사고 분석\n\n')
            report_file.write('- 로켓이 성공적으로 착륙한 후에도 시스템 모니터링이 부족했던 것으로 보입니다.\n')
            report_file.write('- 착륙 후 약 7분 후에 산소 탱크의 불안정 상태가 감지되었으나, 즉각적인 대응이 이루어지지 않았습니다.\n')
            report_file.write('- 불안정 상태 감지 후 5분 만에 산소 탱크 폭발이 발생했습니다.\n')
            report_file.write('- 폭발 후 20분 후에 미션 센터와 제어 시스템이 종료되었습니다.\n\n')

            report_file.write('## 결론 및 권장사항\n\n')
            report_file.write('1. 착륙 후에도 모든 시스템에 대한 지속적인 모니터링이 필요합니다.\n')
            report_file.write('2. 산소 탱크와 같은 중요 장비에 대한 이상 징후가 발견될 경우, 즉각적인 대응 절차가 마련되어야 합니다.\n')
            report_file.write('3. 비상 상황 발생 시 자동 대응 시스템 구축이 필요합니다.\n')
            report_file.write('4. 장비 안전성에 대한 정기적인 점검 및 유지보수 일정을 강화해야 합니다.\n')

        print('로그 분석 보고서가 log_analysis.md 파일로 저장되었습니다.')

except FileNotFoundError:
    print('파일을 찾을 수 없습니다.')
except Exception as e:
    print(f'오류가 발생했습니다: {e}')