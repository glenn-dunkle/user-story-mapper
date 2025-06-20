# main.py
import requests
import time

print("Hello from Docker!")

start_time = time.time()

while time.time() - start_time < 30:
    print("Hello from User Story Mapper!")
    time.sleep(5)

