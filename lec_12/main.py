import random
import time

def create_file(filename):
    with open(filename, 'w') as file:
        for _ in range(100):
            line = ' '.join(str(random.randint(1, 100)) for _ in range(20))
            file.write(line + '\n')

def read_and_process_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    return [list(map(int, line.split())) for line in lines]

def filter_numbers(arrays):
    return [[num for num in array if num > 40] for array in arrays]

def write_file(filename, arrays):
    with open(filename, 'w') as file:
        for array in arrays:
            line = ' '.join(map(str, array))
            file.write(line + '\n')

def read_file_generator(filename):
    with open(filename, 'r') as file:
        for line in file:
            yield list(map(int, line.split()))

def execution_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Execution time for {func.__name__}: {end - start:.4f} seconds")
        return result
    return wrapper

@execution_time
def main():
    filename = 'random_numbers.txt'
    create_file(filename)
    arrays = read_and_process_file(filename)
    filtered_arrays = filter_numbers(arrays)
    write_file(filename, filtered_arrays)
    for line in read_file_generator(filename):
        print(line)

main()

