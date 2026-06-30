# Demonstrates running multiple tasks in parallel instead of sequentially, improving performance for CPU- and I/O-bound workloads.
from multiprocessing import Process
import time

def compute_square(number):
    print(f"Computing square of {number}")
    # Simulates a time-consuming operation
    time.sleep(2)
    result = number * number
    print(f"Result: {result}")

if __name__ == "__main__":
    processes = []
    # Create and start 4 parallel processes
    for i in range(4):
        # target specifies the function executed by the process; equivalent to compute_square(i) in a separate process
        process = Process(target=compute_square, args=(i,))
        processes.append(process)
        process.start()

    # Wait for all processes to finish (must be outside the start loop)
    for process in processes:
        process.join()

    print("All processes finished")