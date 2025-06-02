import zipfile
import itertools
import string
import time
import os
import multiprocessing
from datetime import datetime

def try_extract(zip_path, password):
    """Try to extract ZIP file with password"""
    try:
        with zipfile.ZipFile(zip_path) as zf:
            zf.extractall(pwd=password.encode())
            return True, password
    except:
        return False, None

def worker(zip_path, passwords_chunk, process_id, result_queue, status_queue):
    """Worker process function"""
    total = len(passwords_chunk)
    for idx, password in enumerate(passwords_chunk):
        # Report progress periodically
        if idx % 1000 == 0:
            status_queue.put((process_id, idx, total))
        
        success, pwd = try_extract(zip_path, password)
        if success:
            result_queue.put((True, pwd))
            return
    
    # Report completion
    status_queue.put((process_id, total, total))

def unlock_zip(zip_file_path="C:\\Users\\qortm\\Desktop\\codyssey\\codyssey\\emergency_storage_key.zip"):
    """
    Find ZIP file password using parallel processing
    Password is a 6-character combination of digits and lowercase letters
    Using hints from the story to optimize search
    """
    if not os.path.exists(zip_file_path):
        print(f"ERROR: File {zip_file_path} not found.")
        print("Please verify the file path is correct.")
        print("Current file path setting: " + zip_file_path)
        return False

    # Record start time
    start_time = time.time()
    
    # All possible characters (digits + lowercase alphabets)
    chars = string.digits + string.ascii_lowercase
    
    print("=" * 60)
    print(f"ZIP Password Cracking Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"File Path: {zip_file_path}")
    print("Password Criteria: 6-character combination of digits and lowercase letters")
    print("Using story hints to prioritize search patterns")
    print("=" * 60)
    
    # Determine number of processes to use
    available_cores = multiprocessing.cpu_count()
    n_processes = max(1, min(available_cores - 1, 4))
    print(f"Using {n_processes} CPU cores for parallel processing.")
    
    # Track attempts
    attempt_count = 0
    
    # Based on the story hints, create prioritized password lists
    print("\n[1/5] Trying passwords related to Caesar cipher and Roman themes...")
    
    # Caesar related passwords (high priority)
    caesar_related = [
        # Caesar related
        'caesar', 'julius', 'roman', 'empire', 'cipher', 'shift', 'codes', 
        # Numeric variations of caesar
        'caesar1', 'caesar2', 'caesar3', 'caesar4', 'caesar5',
        'rome01', 'rome02', 'rome03', 'rome12', 'rome23',
        # Position related (engineer's desk with figurines)
        'figure', 'desk01', 'desk02', 'key123', 
        # Simple shifts of common words (as per Caesar cipher)
        'bcdefg', 'cdefgh', 'defghi', 'efghij', 'fghijk',
        # Simple codes
        'code01', 'code02', 'code03', 'code12', 'code99',
        # Mars related (since it's a Mars base)
        'mars01', 'mars02', 'marsb1', 'marsc2', 'marsz9'
    ]
    
    # Filter to ensure 6 characters
    caesar_related = [pwd for pwd in caesar_related if len(pwd) == 6]
    
    print(f"Trying {len(caesar_related)} Caesar/Rome related passwords...")
    
    for password in caesar_related:
        attempt_count += 1
        print(f"Attempt {attempt_count}: {password}", end="\r")
        
        success, pwd = try_extract(zip_file_path, password)
        if success:
            elapsed_time = time.time() - start_time
            print(f"\nSUCCESS! Password found: {pwd}")
            print(f"Attempts: {attempt_count}")
            print(f"Time taken: {elapsed_time:.2f} seconds")
            
            # Save password to file
            with open("password.txt", "w") as pwd_file:
                pwd_file.write(pwd)
            print(f"Password saved to password.txt")
            return True
    
    print("\n[2/5] Trying 'oc' pattern passwords (continuing from previous run)...")
    
    # Continue with 'oc' pattern as in previous run
    remaining_chars = 4  # Need 4 more characters after "oc"
    char_set = string.ascii_lowercase + string.digits
    
    # Process in batches
    batch_size = 100000
    total_combinations = len(char_set) ** remaining_chars
    estimated_batches = (total_combinations + batch_size - 1) // batch_size
    
    generator = itertools.product(char_set, repeat=remaining_chars)
    batch_count = 0
    
    while True:
        # Generate a batch of passwords
        current_batch = []
        try:
            for _ in range(batch_size):
                suffix = ''.join(next(generator))
                password = "oc" + suffix
                current_batch.append(password)
        except StopIteration:
            if not current_batch:
                break
        
        if current_batch:
            batch_count += 1
            print(f"\nProcessing batch {batch_count}/{estimated_batches} of 'oc' patterns")
            
            # Create queues for communication
            result_queue = multiprocessing.Queue()
            status_queue = multiprocessing.Queue()
            
            # Split batch for parallel processing
            worker_chunks = []
            worker_chunk_size = len(current_batch) // n_processes
            for i in range(n_processes):
                start_idx = i * worker_chunk_size
                end_idx = start_idx + worker_chunk_size if i < n_processes - 1 else len(current_batch)
                worker_chunks.append(current_batch[start_idx:end_idx])
            
            # Start processes
            processes = []
            for i in range(n_processes):
                p = multiprocessing.Process(
                    target=worker, 
                    args=(zip_file_path, worker_chunks[i], i, result_queue, status_queue)
                )
                processes.append(p)
                p.start()
            
            # Monitor progress
            total_tried = 0
            process_status = {i: (0, len(worker_chunks[i])) for i in range(n_processes)}
            last_update = time.time()
            passwords_per_second = 0
            
            try:
                while any(p.is_alive() for p in processes):
                    # Check for successful result
                    if not result_queue.empty():
                        success, pwd = result_queue.get()
                        if success:
                            # Terminate all processes
                            for p in processes:
                                p.terminate()
                            
                            elapsed_time = time.time() - start_time
                            attempt_count += sum(process_status[pid][0] for pid in process_status)
                            print(f"\nSUCCESS! Password found: {pwd}")
                            print(f"Attempts: {attempt_count:,}")
                            print(f"Time taken: {elapsed_time:.2f} seconds")
                            
                            # Save password to file
                            with open("password.txt", "w") as pwd_file:
                                pwd_file.write(pwd)
                            print(f"Password saved to password.txt")
                            return True
                    
                    # Update status
                    updates = 0
                    while not status_queue.empty() and updates < 100:
                        pid, current, total = status_queue.get()
                        old_current = process_status[pid][0]
                        process_status[pid] = (current, total)
                        total_tried += (current - old_current)
                        updates += 1
                    
                    # Update display (once per second)
                    if time.time() - last_update >= 1.0:
                        # Calculate speed
                        current_speed = total_tried / (time.time() - last_update) if last_update != start_time else 0
                        passwords_per_second = current_speed if passwords_per_second == 0 else (passwords_per_second * 0.7 + current_speed * 0.3)
                        
                        # Calculate progress for this batch
                        total_passwords = sum(total for _, total in process_status.values())
                        processed_passwords = sum(current for current, _ in process_status.values())
                        progress = processed_passwords / total_passwords if total_passwords > 0 else 0
                        
                        # Calculate overall progress
                        overall_progress = (batch_count - 1 + progress) / estimated_batches
                        
                        # Estimate remaining time
                        remaining_passwords = total_combinations - (attempt_count + processed_passwords)
                        remaining_time = remaining_passwords / passwords_per_second if passwords_per_second > 0 else 0
                        
                        # Print progress
                        print(f"\rBatch: {batch_count}/{estimated_batches} | "
                              f"Progress: {overall_progress*100:.2f}% | "
                              f"Speed: {passwords_per_second:.2f} pwd/sec | "
                              f"ETA: {remaining_time/60:.1f} min | "
                              f"Testing: oc{current_batch[0][2:6]}-oc{current_batch[-1][2:6]}", end="")
                        
                        total_tried = 0
                        last_update = time.time()
                    
                    time.sleep(0.1)
            
            except KeyboardInterrupt:
                print("\n\nInterrupted by user.")
                for p in processes:
                    p.terminate()
                return False
            
            # Update attempt count
            attempt_count += sum(process_status[pid][0] for pid in process_status)
            
            # Wait for all processes to finish
            for p in processes:
                p.join()
    
    print("\n[3/5] Trying Roman number patterns and Caesar cipher related combinations...")
    
    # Try combinations based on Roman numerals and shifts
    roman_prefixes = ["ro", "rm", "cs", "ci", "ju", "sh", "en", "fi", "ma", "ce"]
    roman_nums = ["i", "ii", "iii", "iv", "v", "vi", "x", "xi", "xii"]
    
    # Generate combinations like "roiii", "rmvi", "csxii", etc.
    roman_combinations = []
    for prefix in roman_prefixes:
        for num in roman_nums:
            # Ensure total length is 6 by adding padding if needed
            remaining_len = 6 - len(prefix) - len(num)
            if remaining_len >= 0:
                padding = ''.join(['0'] * remaining_len)
                roman_combinations.append(prefix + num + padding)
                
                # Add some variations with digits
                for d in range(10):
                    if remaining_len - 1 >= 0:
                        padding = ''.join(['0'] * (remaining_len - 1))
                        roman_combinations.append(prefix + num + str(d) + padding)
    
    print(f"Trying {len(roman_combinations)} Roman numeral combinations...")
    
    # Process these combinations
    for password in roman_combinations:
        if len(password) == 6:  # Double-check length
            attempt_count += 1
            print(f"Attempt {attempt_count}: {password}", end="\r")
            
            success, pwd = try_extract(zip_file_path, password)
            if success:
                elapsed_time = time.time() - start_time
                print(f"\nSUCCESS! Password found: {pwd}")
                print(f"Attempts: {attempt_count}")
                print(f"Time taken: {elapsed_time:.2f} seconds")
                
                # Save password to file
                with open("password.txt", "w") as pwd_file:
                    pwd_file.write(pwd)
                print(f"Password saved to password.txt")
                return True
    
    print("\n[4/5] Trying alphabet shifts (Caesar cipher principle)...")
    
    # Generate patterns based on alphabet shifts
    alphabet = string.ascii_lowercase
    
    # Try all possible shifts of common patterns
    base_patterns = ["abcdef", "qwerty", "asdfgh", "zxcvbn", "aaaaaa", "bbbbbb"]
    shift_combinations = []
    
    for pattern in base_patterns:
        for shift in range(1, 26):  # All possible Caesar shifts
            shifted = ""
            for char in pattern:
                if char in alphabet:
                    idx = (alphabet.index(char) + shift) % 26
                    shifted += alphabet[idx]
                else:
                    shifted += char
            shift_combinations.append(shifted)
    
    # Add numeric variations
    extended_shift_combinations = []
    for pattern in shift_combinations:
        extended_shift_combinations.append(pattern)
        # Add numeric substitutions (e.g., replace 'a' with '4', 'e' with '3', etc.)
        for i, char in enumerate(pattern):
            if char == 'a' or char == 'e' or char == 'i' or char == 'o':
                # Common letter-to-number substitutions
                num_map = {'a': '4', 'e': '3', 'i': '1', 'o': '0'}
                if char in num_map:
                    new_pattern = pattern[:i] + num_map[char] + pattern[i+1:]
                    extended_shift_combinations.append(new_pattern)
    
    print(f"Trying {len(extended_shift_combinations)} shift-based combinations...")
    
    # Process these combinations
    for password in extended_shift_combinations:
        if len(password) == 6:  # Double-check length
            attempt_count += 1
            print(f"Attempt {attempt_count}: {password}", end="\r")
            
            success, pwd = try_extract(zip_file_path, password)  # 여기 수정됨 (zip_path → zip_file_path)
            if success:
                elapsed_time = time.time() - start_time
                print(f"\nSUCCESS! Password found: {pwd}")
                print(f"Attempts: {attempt_count}")
                print(f"Time taken: {elapsed_time:.2f} seconds")
                
                # Save password to file
                with open("password.txt", "w") as pwd_file:
                    pwd_file.write(pwd)
                print(f"Password saved to password.txt")
                return True
    
    print("\n[5/5] Continuing with systematic search of all combinations...")
    print("This will now try all remaining combinations starting with common patterns.")
    
    # Common starting letters based on frequency in English
    common_first_letters = "etaoinshrdlucmfwypvkbjgqxz0123456789"
    common_second_letters = "etaoinshrdlucmfwypvkbjgqxz0123456789"
    
    # Prioritize search order based on letter frequency
    for first in common_first_letters:
        for second in common_second_letters:
            # Skip "oc" as we've already tried it
            if first == 'o' and second == 'c':
                continue
                
            prefix = first + second
            print(f"\nTrying passwords starting with '{prefix}'...")
            
            # Generate and process all combinations with this prefix
            remaining_chars = 4  # Need 4 more characters after two-letter prefix
            
            # Process in batches
            batch_size = 100000
            total_combinations = len(char_set) ** remaining_chars
            estimated_batches = (total_combinations + batch_size - 1) // batch_size
            
            generator = itertools.product(char_set, repeat=remaining_chars)
            batch_count = 0
            
            while True:
                # Generate a batch of passwords
                current_batch = []
                try:
                    for _ in range(batch_size):
                        suffix = ''.join(next(generator))
                        password = prefix + suffix
                        current_batch.append(password)
                except StopIteration:
                    if not current_batch:
                        break
                
                if current_batch:
                    batch_count += 1
                    print(f"\nProcessing batch {batch_count}/{estimated_batches} of '{prefix}' patterns")
                    
                    # Create queues for communication
                    result_queue = multiprocessing.Queue()
                    status_queue = multiprocessing.Queue()
                    
                    # Split batch for parallel processing
                    worker_chunks = []
                    worker_chunk_size = len(current_batch) // n_processes
                    for i in range(n_processes):
                        start_idx = i * worker_chunk_size
                        end_idx = start_idx + worker_chunk_size if i < n_processes - 1 else len(current_batch)
                        worker_chunks.append(current_batch[start_idx:end_idx])
                    
                    # Start processes
                    processes = []
                    for i in range(n_processes):
                        p = multiprocessing.Process(
                            target=worker, 
                            args=(zip_file_path, worker_chunks[i], i, result_queue, status_queue)
                        )
                        processes.append(p)
                        p.start()
                    
                    # Monitor progress
                    total_tried = 0
                    process_status = {i: (0, len(worker_chunks[i])) for i in range(n_processes)}
                    last_update = time.time()
                    passwords_per_second = 0
                    
                    try:
                        while any(p.is_alive() for p in processes):
                            # Check for successful result
                            if not result_queue.empty():
                                success, pwd = result_queue.get()
                                if success:
                                    # Terminate all processes
                                    for p in processes:
                                        p.terminate()
                                    
                                    elapsed_time = time.time() - start_time
                                    attempt_count += sum(process_status[pid][0] for pid in process_status)
                                    print(f"\nSUCCESS! Password found: {pwd}")
                                    print(f"Attempts: {attempt_count:,}")
                                    print(f"Time taken: {elapsed_time:.2f} seconds")
                                    
                                    # Save password to file
                                    with open("password.txt", "w") as pwd_file:
                                        pwd_file.write(pwd)
                                    print(f"Password saved to password.txt")
                                    return True
                            
                            # Update status
                            updates = 0
                            while not status_queue.empty() and updates < 100:
                                pid, current, total = status_queue.get()
                                old_current = process_status[pid][0]
                                process_status[pid] = (current, total)
                                total_tried += (current - old_current)
                                updates += 1
                            
                            # Update display (once per second)
                            if time.time() - last_update >= 1.0:
                                # Calculate speed
                                current_speed = total_tried / (time.time() - last_update) if last_update != start_time else 0
                                passwords_per_second = current_speed if passwords_per_second == 0 else (passwords_per_second * 0.7 + current_speed * 0.3)
                                
                                # Calculate progress for this batch
                                total_passwords = sum(total for _, total in process_status.values())
                                processed_passwords = sum(current for current, _ in process_status.values())
                                progress = processed_passwords / total_passwords if total_passwords > 0 else 0
                                
                                # Print progress
                                print(f"\rBatch: {batch_count}/{estimated_batches} | "
                                      f"Progress: {progress*100:.2f}% | "
                                      f"Speed: {passwords_per_second:.2f} pwd/sec | "
                                      f"Testing: {prefix}{current_batch[0][2:6]}-{prefix}{current_batch[-1][2:6]}", end="")
                                
                                total_tried = 0
                                last_update = time.time()
                            
                            time.sleep(0.1)
                    
                    except KeyboardInterrupt:
                        print("\n\nInterrupted by user.")
                        for p in processes:
                            p.terminate()
                        return False
                    
                    # Update attempt count
                    attempt_count += sum(process_status[pid][0] for pid in process_status)
                    
                    # Wait for all processes to finish
                    for p in processes:
                        p.join()
            
            # Continue with next prefix if password not found
    
    # If password is still not found after trying everything
    elapsed_time = time.time() - start_time
    print(f"\nTotal time: {elapsed_time:.2f} seconds")
    print(f"Total attempts: {attempt_count:,}")
    print("Password not found after trying all specified combinations.")
    return False

if __name__ == "__main__":
    # Required for multiprocessing on Windows
    multiprocessing.freeze_support()
    
    try:
        unlock_zip()
    except Exception as e:
        print(f"\nERROR: {str(e)}")
    
    # Wait for user input before closing
    input("\nPress any key to exit...")