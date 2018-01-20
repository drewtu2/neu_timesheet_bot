#! python3
import pyautogui
import logging
import mylogger
import datetime
import csv
import cv2
import os
import sys
from math import pow
from time import sleep




DAYS_OF_WEEK = ["Sunday", 
    "Monday", 
    "Tuesday", 
    "Wednesday", 
    "Thursday", 
    "Friday", 
    "Saturday"]

def generateEntries(config_file):
    """
    Converts a csv file to a list of dicitonaries. The format of the csv is as 
    follows: 

    Monday 9:00AM Monday 9:45AM
    Tuesday 9:00PM Tuesday 9:30PM
    Wednesday 10:00AM Wednesday 11:00AM
    
    Returned list is as follows:
    entry = {
        "Start": Day1,
        "End": Day2
    }   
    day1 = {
            "Day": "Monday",
            "Time": "9:00AM"
    }
    day2 = {
            "Day": "Tuesday",
            "Time": "9:00AM"
    }
    entries = [day1, day2, day3]
    """

    def _make_entry(start, end):
        return {"Start": start, "End": end}

    def _make_day(day, time):
        return {"Day": day, "Time": time}

    if config_file is None:
        config_file = "myconfig.csv"

    logging.info("Generating entries from %s", config_file)
    fieldNames = ["DayStart", "TimeStart", "DayEnd", "TimeEnd"]
    entries = []
    directory = "configs/"
    
    try:
        if not os.path.exists(directory):
                os.makedirs(directory)
        with open(directory + config_file, "r") as fp:
            myfilter=filter(lambda row: row[0]!='#', fp)
            
            configReader = csv.DictReader(myfilter, fieldnames=fieldNames, delimiter=" ")
            for row in configReader:
                row_dict = dict(row)
                entry = _make_entry(
                        _make_day(row_dict["DayStart"], row_dict["TimeStart"]),
                        _make_day(row_dict["DayEnd"], row_dict["TimeEnd"]))
                entries.append(entry)
    except FileNotFoundError as e:
        logging.error(e)
        quit()

    logging.debug("Entries generated")
    return entries

def generateTimeList():
    """
    Returns a containing two lists of 15 minute interval Times. 
    """
    
    dtfmt = '%Y-%m-%d %I:%M:%S%p'

    def perdelta(start, end, delta):
        curr = start
        while curr <= end:
            yield curr
            curr += delta

    def genDay(start_time, end_time):
        start = datetime.datetime.strptime(start_time, dtfmt)
        end = datetime.datetime.strptime(end_time, dtfmt)
        results = [result for result in perdelta(start, end, datetime.timedelta(minutes=15))]
        results = [result.time() for result in results]
        return results
    
    start_range_start = '2000-01-01 12:00:00AM'
    start_range_end = '2000-01-01 11:45:00PM'
    
    Start_Times = genDay(start_range_start, start_range_end)

    end_range_start = '2000-01-01 12:15:00AM'
    end_range_end = '2000-01-02 5:00:00AM'

    End_Times = genDay(end_range_start, end_range_end)

    return (Start_Times, End_Times)

# List of times from [12:00AM - 11:45PM] at 15 minute intervals
TIMES = generateTimeList()


class neu_job_bot():
    # Images
    ADD_ENTRY = "form_items/AddEntry.png"
    START_TIME = "form_items/StartTime.png"
    END_TIME = "form_items/EndTime.png"
    DAY = "form_items/Day.png"
    ADD = "form_items/Add.png"
    SMALL_SCREEN = "form_items/SmallScreen.png"
    FULL_SCREEN = "form_items/FullScreen.png"

    # 
    LOAD_DELAY = 1
    IS_START = 0
    IS_END = 1
    
    def __init__(self):
        self.num_retries = 5
        pass

    def run(self, configFile=None):
        entries = generateEntries(configFile)
        # Give the user a chance to kill the script.
        print('>>> 5 SECOND PAUSE TO LET USER PRESS CTRL-C <<<')
        sleep(5)
        for entry in entries:
            sleep(self.LOAD_DELAY)
            self.add_entry()
            self.set_start(entry["Start"])
            self.set_end(entry)
            self.set_submit()
    
    
    def add_entry(self, retried=False):
        try:
            logging.debug("Trying \"Add Entry\"")
            location = self.click_image(self.ADD_ENTRY)
            logging.info("Clicked \"Add Entry\"")
            sleep(self.LOAD_DELAY)
        except ValueError as e:
            self.retry(self.add_entry, None, retried)
            print(e)
    
    def set_day(self, day, retried = False):
        index = DAYS_OF_WEEK.index(day)
        try:
            location = self.click_image(self.DAY)
            logging.info("Clicked \"Day\"")
            pyautogui.typewrite(["down" for i in range(index)])
            pyautogui.typewrite(["enter"])
            logging.info("Entered Day")
            sleep(self.LOAD_DELAY)
        except ValueError as e:
            logging.error(e)
            self.retry(self.set_day, day, retried)
    
    def set_start(self, start, retried = False):
        try:
            self.set_day(start["Day"])
            logging.debug("Trying \"set_start\"")
            self.click_image(self.START_TIME)
            logging.info("Clicked \"set_start\"")
            self.set_time(start["Time"], self.IS_START)
            logging.info("Set Start Time")
            sleep(self.LOAD_DELAY)
        except ValueError as e:
            logging.error(e)
            self.retry(self.set_start, start, retried)
    
    def set_end(self, entry):
        
        # If the start and end date are not equal, then we've gone into the next
        # day
        new_day = entry["Start"]["Day"] != entry["End"]["Day"]
        end_time = entry["End"]["Time"]
        try:
            logging.debug("Trying \"set_end\"")
            self.click_image(self.END_TIME)
            logging.info("Clicked \"set_end\"")
            self.set_time(end_time, self.IS_END, new_day) 
            logging.info("Set End Time")
            sleep(self.LOAD_DELAY)
        except ValueError as e:
            logging.error(e)
            self.retry(self.set_end, start_time, retried)
    
    def set_submit(self):
        try:
            self.click_image(self.ADD)
            sleep(self.LOAD_DELAY)
        except ValueError as e:
            logging.error(e)
            self.retry(self.set_submit, None, retried)
    
    def set_time(self, time, is_end, new_day=False):
        dtfmt = '%I:%M%p'
        start = "8:00AM"
        
        start = datetime.datetime.strptime(start, dtfmt).time()
        time = datetime.datetime.strptime(time, dtfmt).time()
    
        index_current = TIMES[is_end].index(start)

        if new_day:
            # If this is a new day, we need the last time the value occured. 
            indicies = [i for i,val in enumerate(TIMES[is_end]) if val==time]
            index_goal = indicies[-1]
        else:
            # Otherwise, this value only occured once. 
            index_goal = TIMES[is_end].index(time)
    
        print(index_goal)
        print(index_current)
        print(index_delta)
        index_delta = index_goal - index_current
    
        if index_delta > 0:
            pyautogui.typewrite(["down" for i in range(index_delta)])
        elif index_delta < 0:
            pyautogui.typewrite(["up" for i in range(index_delta)])
        
        pyautogui.typewrite(["enter"])
    
    def click_image(self, png_name):
        """
        
        """
        
        button = pyautogui.locateCenterOnScreen(png_name, confidence =.8)
        
        if button is None:
            error_message = "Couldn't find the button"
            raise ValueError(error_message)
    
        x = button[0]/2
        y = button[1]/2
        
        pyautogui.moveTo(x,y)
        pyautogui.click()
        logging.debug("Location returned: %s", button)
        return button
    
    def retry(self, fx, arg, retried):
        if retried < self.num_retries:
            retried += 1

            delay = retried
            logging.info("Retrying %s attempt %d after %d second delay...", 
                    fx.__name__, 
                    retried, 
                    delay)
            
            sleep(delay)

            if arg:
                fx(arg, retried=retried)
            else:
                fx(retried=retried)
        else:
            logging.info("Retry failed....")
            quit()

if __name__ == "__main__":
    mylogger.config_logs()
    #generateEntries()
    bot = neu_job_bot()
    
    if len(sys.argv) == 2:
        bot.run(sys.argv[1])
    else:
        bot.run()
