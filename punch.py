#!/usr/local/bin/python3

from datetime import datetime, timedelta
import pickle
import os
import sys

save_file = os.environ.get("HOME") + "/Documents/Projects/neu_timesheet_bot/.punch_card.pickle"
config_file = os.environ.get("HOME") + "/Documents/Projects/neu_timesheet_bot/1-22.csv"

def punch_in():
    """
    Clocks in to the system. A save file is created marking the start time. 
    
    """

    now = datetime.now()
    print("Punched in at " + str(now))
    # The file exists.... check to make sure we want to overwrite it
    if os.path.isfile(save_file):
        if confirm_overwrite():
            pass
        else:
            # Abort...
            print("Not overwriting... Exiting...")
            sys.exit(0)
    
    with open(save_file, 'wb+') as f:
        pickle.dump(now, f)

def confirm_overwrite():
    """
    If the pickle save file already exists, we haven't clocked out since the
    last time we clocked in. Therefore, confirm the user wants to overwrite 
    the old file...

    Returns true if we want to overwrite the previous file. 
    """

    confirm = input("It appears a previous clockin time still exists. Are you sure you want to overwrite your previous start time?[y/n]")

    if str(confirm).lower() == "y":
        return True 
    elif str(confirm).lower() == "n":
        return False 
    else:
        return confirm_overwrite()

def punch_out():
    """
    Logs the start and end time to the end config file. 
    
    Removes the temp save file 
    """
    if not os.path.isfile(save_file):
        print("Error: You are not currently punched in")
        exit(0)

    # Round the start time down to the nearest 15 minute mark
    start = pickle.load(open(save_file, 'rb'))
    start = start - timedelta(minutes=start.minute % 15,
            seconds=start.second,
            microseconds=start.microsecond)
    
    # Round the end time up to the nearest 15 minute mark
    end = datetime.now()
    end = end - timedelta(seconds=end.second, microseconds= end.microsecond)
    end = end + timedelta(minutes=15 - (end.minute % 15))
    
    print("Punched out at " + str(end))

    os.remove(save_file)

    with open(config_file, 'a+') as f:
        myfmt = "%A %I:%M%p"
        output_string = start.strftime(myfmt) + " " + end.strftime(myfmt) + "\n"
        f.write(output_string)

def punch_print():
    """
    Prints the current config file times
    """
    with open(config_file, 'r') as f:
        for line in f:
            print(line)

def print_time_in():
    """
    Prints the time you clocked in 
    """

    if not os.path.isfile(save_file):
        print("ERROR: You are not currently punched in...")
    else:
        print("Time in: " + str(pickle.load(open(save_file, 'rb'))))

def print_usage():
    print("Usage:")
    print("Clock in:\t punch in")
    print("Clock out:\t punch out")
    print("Time in:\t punch time_in")
    print("View Timecard:\t punch print")
    sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print_usage()
    else:
        if sys.argv[1] == "in":
            punch_in()
        elif sys.argv[1] == "out":
            punch_out()
        elif sys.argv[1] == "print":
            punch_print()
        elif sys.argv[1] == "time_in":
            print_time_in()
        else:
            print_usage()



