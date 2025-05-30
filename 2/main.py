try:
    with open('Mars_Base_Inventory_List.csv', 'r') as f:
        content = f.read().strip()
        lines = content.split('\n')
        data = [line.split(',') for line in lines]
    
    print("Mars_Base_Inventory_List.csv 원본 내용:")
    for row in data:
        print(row)
    
    header = data[0]
    inventory_data = data[1:]
    
    flammability_index = 0
    for i, col_name in enumerate(header):
        if col_name == 'Flammability':
            flammability_index = i
            break
    
    sorted_data = sorted(inventory_data, key=lambda x: float(x[flammability_index]), reverse=True)
    
    print("\n인화성이 높은 순으로 정렬된 목록:")
    for row in sorted_data:
        print(row)
    
    dangerous_items = []
    for row in sorted_data:
        if float(row[flammability_index]) >= 0.7:
            dangerous_items.append(row)
    
    print("\n인화성 지수가 0.7 이상인 목록:")
    for row in dangerous_items:
        print(row)
    
    try:
        with open('Mars_Base_Inventory_danger.csv', 'w') as f:
            header_line = ','.join(header) + '\n'
            f.write(header_line)
            
            for row in dangerous_items:
                line = ','.join(row) + '\n'
                f.write(line)
        print("\n위험 항목이 Mars_Base_Inventory_danger.csv 파일에 저장되었습니다.")
    except Exception as e:
        print(f"CSV 파일 저장 중 오류 발생: {e}")

    try:
        with open('Mars_Base_Inventory_List.bin', 'wb') as f:
            full_data = [header] + sorted_data
            for row in full_data:
                line = ','.join(row) + '\n'
                f.write(line.encode('utf-8'))
        
        print("\n정렬된 데이터가 Mars_Base_Inventory_List.bin 파일에 저장되었습니다.")
    except Exception as e:
        print(f"이진 파일 저장 중 오류 발생: {e}")
    
    try:
        print("\nMars_Base_Inventory_List.bin 파일에서 읽은 내용:")
        with open('Mars_Base_Inventory_List.bin', 'rb') as f:
            content = f.read().decode('utf-8')
            print(content)
    except Exception as e:
        print(f"이진 파일 읽기 중 오류 발생: {e}")

except FileNotFoundError:
    print("Mars_Base_Inventory_List.csv 파일을 찾을 수 없습니다.")
except Exception as e:
    print(f"프로그램 실행 중 오류 발생: {e}")