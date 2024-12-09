import os
import re
import time
import threading
from collections import defaultdict
from multiprocessing import Process, Manager

def generate_large_text_file(filename, num_lines=100000):
    with open(filename, "w") as f:
        for _ in range(num_lines):
            f.write(" ".join(["word" + str(i) for i in range(100)]) + "\n")

def count_words_sequential(filename):
    word_count = defaultdict(int)
    with open(filename, "r") as file:
        for line in file:
            words = re.findall(r'\b\w+\b', line.lower())
            for word in words:
                word_count[word] += 1
    return word_count

def count_words_thread_worker(chunk, word_count, lock):
    local_count = defaultdict(int)
    for line in chunk:
        words = re.findall(r'\b\w+\b', line.lower())
        for word in words:
            local_count[word] += 1
    with lock:
        for word, count in local_count.items():
            word_count[word] += count

def count_words_multithreading(filename, num_threads=4):
    word_count = defaultdict(int)
    lock = threading.Lock()
    threads = []

    with open(filename, "r") as file:
        lines = file.readlines()
    chunk_size = len(lines) // num_threads

    for i in range(num_threads):
        chunk = lines[i * chunk_size:(i + 1) * chunk_size] if i < num_threads - 1 else lines[i * chunk_size:]
        thread = threading.Thread(target=count_words_thread_worker, args=(chunk, word_count, lock))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    return word_count

def count_words_process_worker(chunk, return_dict):
    local_count = defaultdict(int)
    for line in chunk:
        words = re.findall(r'\b\w+\b', line.lower())
        for word in words:
            local_count[word] += 1
    return_dict.update(local_count)

def count_words_multiprocessing(filename, num_processes=4):
    with open(filename, "r") as file:
        lines = file.readlines()

    chunk_size = len(lines) // num_processes
    chunks = [lines[i * chunk_size:(i + 1) * chunk_size] if i < num_processes - 1 else lines[i * chunk_size:]
              for i in range(num_processes)]
    
    manager = Manager()
    return_dict = manager.dict()
    processes = []

    for chunk in chunks:
        process = Process(target=count_words_process_worker, args=(chunk, return_dict))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    word_count = defaultdict(int)
    for word, count in return_dict.items():
        word_count[word] += count
    return word_count

if __name__ == "__main__":
    filename = "large_text_file.txt"
    generate_large_text_file(filename, num_lines=500000)

    print("Starting word count comparison...")
    
    start_time = time.time()
    seq_word_count = count_words_sequential(filename)
    seq_time = time.time() - start_time
    print(f"Sequential Processing Time: {seq_time:.2f} seconds")

    start_time = time.time()
    mt_word_count = count_words_multithreading(filename)
    mt_time = time.time() - start_time
    print(f"Multithreading Processing Time: {mt_time:.2f} seconds")
    
    start_time = time.time()
    mp_word_count = count_words_multiprocessing(filename)
    mp_time = time.time() - start_time
    print(f"Multiprocessing Processing Time: {mp_time:.2f} seconds")
    
    print("\nSpeedup Comparison:")
    print(f"Speedup with Multithreading: {seq_time / mt_time:.2f}x")
    print(f"Speedup with Multiprocessing: {seq_time / mp_time:.2f}x")

    os.remove(filename)
