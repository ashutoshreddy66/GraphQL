import threading
import time

# A simple function that simulates a time-consuming task
def print_numbers():
    for i in range(5):
        print(f"Number: {i}")
        time.sleep(1)  # Simulate a delay

# Create a thread
thread = threading.Thread(target=print_numbers)

# Start the thread
thread.start()

# Main thread continues to run
for i in range(5):
    print("Main thread is running")
    time.sleep(0.5)

# Wait for the thread to complete
thread.join()

print("All threads have finished execution.")
