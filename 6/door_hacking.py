import zipfile
import itertools
import string
import time
import multiprocessing
import os


def try_extract_with_validation(zip_path, password):
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            file_list = zip_ref.namelist()
            if not file_list:
                return False
            test_content = zip_ref.read(file_list[0], pwd=password.encode('utf-8'))
            return True
    except Exception as e:
        return False


def worker_optimized(zip_path, password_range_info, process_id, result_queue, status_queue):
    chars, start_idx, end_idx = password_range_info
    count = 0
    for idx in range(start_idx, end_idx):
        password = ''
        temp_idx = idx
        for _ in range(8):
            password = chars[temp_idx % len(chars)] + password
            temp_idx //= len(chars)
        count += 1
        if count % 1000 == 0:
            status_queue.put((process_id, count, end_idx - start_idx))
        if try_extract_with_validation(zip_path, password):
            result_queue.put((True, password))
            return
    status_queue.put((process_id, count, end_idx - start_idx))


def unlock_zip(zip_file_path='C:\\Users\\qortm\\Desktop\\emergency_storage_key.zip'):
    if not os.path.exists(zip_file_path):
        print(f'ERROR: File {zip_file_path} not found.')
        return False
    
    print('=' * 60)
    print('ZIP Password Cracking')
    print(f'File Path: {zip_file_path}')
    print('=' * 60)
    
    try:
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            file_list = zip_ref.namelist()
            print(f'ZIP file contains {len(file_list)} files')
    except Exception as e:
        print(f'Error reading ZIP file: {e}')
        return False
    
    chars = string.digits + string.ascii_lowercase
    total_combinations = len(chars) ** 8
    print(f'Character set: {chars}')
    print(f'Total combinations to check: {total_combinations:,}')
    
    num_physical_cores = multiprocessing.cpu_count()
    n_processes = num_physical_cores
    print(f'Using {n_processes} processes')
    
    start_time = time.time()
    
    common_patterns = [
        'qwerty12', 'password', '12345678', '11111111', '12312312',
        'abc12345', '123abc45', '00000000', '65432112', '12332112',
        'a1234567', '12345abc', 'admin123', '1admin23', '1q2w3e4r',
        'caesar12', 'julius12', 'roman123', 'cipher12', 'shift123'
    ]
    
    print(f'Testing {len(common_patterns)} common patterns...')
    for i, pattern in enumerate(common_patterns):
        if len(pattern) == 8:
            print(f'Testing: {pattern}', end='\r')
            if try_extract_with_validation(zip_file_path, pattern):
                elapsed_time = time.time() - start_time
                print(f'\nSUCCESS! Password found: {pattern}')
                print(f'Time taken: {elapsed_time:.2f} seconds')
                with open('C:\\Users\\qortm\\Desktop\\password.txt', 'w') as pwd_file:
                    pwd_file.write(pattern)
                print('Password saved to password.txt')
                return True
    
    print('Starting brute force attack...')
    chunk_size = total_combinations // n_processes
    password_ranges = []
    
    for i in range(n_processes):
        start_idx = i * chunk_size
        end_idx = start_idx + chunk_size if i < n_processes - 1 else total_combinations
        password_ranges.append((chars, start_idx, end_idx))
    
    result_queue = multiprocessing.Queue()
    status_queue = multiprocessing.Queue()
    
    processes = []
    for i in range(n_processes):
        p = multiprocessing.Process(
            target=worker_optimized,
            args=(zip_file_path, password_ranges[i], i, result_queue, status_queue)
        )
        p.start()
        processes.append(p)
    
    print(f'Started {n_processes} parallel processes')
    
    total_checked = 0
    process_status = {i: (0, password_ranges[i][2] - password_ranges[i][1]) for i in range(n_processes)}
    last_update = time.time()
    
    try:
        while any(p.is_alive() for p in processes):
            if not result_queue.empty():
                success, pwd = result_queue.get()
                if success:
                    for p in processes:
                        p.terminate()
                        p.join(timeout=0.5)
                    elapsed_time = time.time() - start_time
                    total_checked += sum(process_status[pid][0] for pid in process_status)
                    print(f'\nSUCCESS! Password found: {pwd}')
                    print(f'Total passwords checked: {total_checked:,}')
                    print(f'Total time: {elapsed_time:.2f} seconds')
                    with open('C:\\Users\\qortm\\Desktop\\password.txt', 'w') as pwd_file:
                        pwd_file.write(pwd)
                    print('Password saved to password.txt')
                    return True
            
            updates = 0
            while not status_queue.empty() and updates < 100:
                pid, current, total = status_queue.get()
                old_current = process_status[pid][0]
                process_status[pid] = (current, total)
                total_checked += (current - old_current)
                updates += 1
            
            if time.time() - last_update >= 1.0:
                current_checked = sum(process_status[pid][0] for pid in process_status)
                total_to_check = sum(process_status[pid][1] for pid in process_status)
                progress = current_checked / total_to_check if total_to_check > 0 else 0
                print(f'\rProgress: {progress*100:.4f}% | Checked: {current_checked:,}/{total_to_check:,}', end='')
                total_checked = 0
                last_update = time.time()
            time.sleep(0.1)
    
    except KeyboardInterrupt:
        print('\nInterrupted by user.')
        for p in processes:
            p.terminate()
            p.join(timeout=1)
        return False
    
    for p in processes:
        p.join()
    
    elapsed_time = time.time() - start_time
    total_checked = sum(process_status[pid][0] for pid in process_status)
    print(f'\nPassword not found after checking {total_checked:,} combinations')
    print(f'Total time: {elapsed_time:.2f} seconds')
    return False


if __name__ == '__main__':
    multiprocessing.set_start_method('spawn', force=True)
    try:
        unlock_zip()
    except Exception as e:
        print(f'Error: {e}')
    input('\nPress any key to exit...')