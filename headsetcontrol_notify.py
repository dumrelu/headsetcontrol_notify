#!/usr/bin/env python

import subprocess
from sys import stderr

# The battery percentage after which the script sends notifications
LOW_BATTERY_THRESHOLD = 20

def run_process(command):
    '''
    Runs the given command and returns (exit_code, stdout, stderr)
    '''
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout,stderr = process.communicate()
    exit_code = process.wait()

    return exit_code, stdout.decode(), stderr.decode()

if __name__ == "__main__":
    # Run the headsetcontrol utility
    exit_code, stdout, stderr = run_process(["headsetcontrol", "-b"])
    stdout_lines = stdout.split('\n')

    if exit_code != 0:
        print("Error while running headsetcontrol. Headset is probably disconnected.")
        print(stderr)
        exit(1)
    
    # Parse the name of the headset. First line of the out should be "Found Logitech G533!"
    headset_name = " ".join(stdout_lines[0].split(' ')[1:])[:-1]
    print(f"Headset name: {headset_name}")

    # Parse the battery status. Second line is either "Battery: X%" or "Battery: Charging"
    percentage_string = stdout_lines[1].split(' ')[1] # Either "X%"" or "Charging"
    battery_charging = False
    battery_percentage = 0

    if percentage_string == "Charging":
        battery_charging = True
    else:
        battery_percentage = int(percentage_string[:-1])
    
    print(f"Battery status: {percentage_string}. Parsed values: battery_charging={battery_charging}, battery_percentage={battery_percentage}")

    # If the headset is not charging and the battery percentage is lower than the threshold, we send a notification
    if not battery_charging and battery_percentage < LOW_BATTERY_THRESHOLD:
        message = f"{headset_name}: {battery_percentage} remaining!"

        run_process(["notify-send", "-t", "10000", "-i", "emblem-warning", message])
    
