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

    Monday 9:00AM 9:45AM
    Tuesday 9:00PM 9:30PM
    Wednesday 10:00AM 11:00AM
    
    Returned list is as follows:
    day1 = {
            "Day": "Monday",
            "Start": "9:00AM",
            "End":"9:45AM"}
    day1 = {
            "Day": "Tuesday",
            "Start": "9:00PM",
            "End":"9:30PM"}
    day2 = {
            "Day": "Wednesday",
            "Start": "10:00AM",
            "End":"11:00AM"}
    entries = [day1, day2, day3]
    """
    if config_file is None:
        config_file = "myconfig.csv"

    logging.info("Generating entries from %s", config_file)
    fieldNames = ["Day", "Start", "End"]
    entries = []
    directory = "configs/"
    
    try:
        if not os.path.exists(directory):
                os.makedirs(directory)
        with open(directory + config_file, "r") as fp:
            myfilter=filter(lambda row: row[0]!='#', fp)
            
            configReader = csv.DictReader(myfilter, fieldnames=fieldNames, delimiter=" ")
            for row in configReader:
                entries.append(dict(row))
    except FileNotFoundError as e:
        logging.error(e)
        quit()

    logging.debug("Entries generated")
    return entries

def generateTimeList():
    def perdelta(start, end, delta):
        curr = start
        while curr <= end:
            yield curr
            curr += delta
    dtfmt = '%I:%M:%S%p'
    a = '12:00:00AM'
    b = '11:45:00PM'
    start = datetime.datetime.strptime(a,dtfmt)
    end = datetime.datetime.strptime(b,dtfmt)
    results = [result for result in perdelta(start, end, datetime.timedelta(minutes=15))]
    return results

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
        self.num_retries = 3
        pass

    def run(self, configFile=None):
        entries = generateEntries(configFile)
        for entry in entries:
            # Give the user a chance to kill the script.
            print('>>> 5 SECOND PAUSE TO LET USER PRESS CTRL-C <<<')
            sleep(5)
            
            self.add_entry()
            self.set_day(entry["Day"])
            self.set_start(entry["Start"])
            self.set_end(entry["End"])
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
    
    def set_start(self, start_time, retried = False):
        try:
            logging.debug("Trying \"set_start\"")
            self.click_image(self.START_TIME)
            logging.info("Clicked \"set_start\"")
            self.set_time(start_time, self.IS_START)
            logging.info("Set Start Time")
            sleep(self.LOAD_DELAY)
        except ValueError as e:
            logging.error(e)
            self.retry(self.set_start, start_time, retried)
    
    def set_end(self, end_time):
        try:
            logging.debug("Trying \"set_end\"")
            self.click_image(self.END_TIME)
            logging.info("Clicked \"set_end\"")
            self.set_time(end_time, self.IS_END) 
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
    
    def set_time(self, time, is_end):
        dtfmt = '%I:%M%p'
        start = "8:00AM"
        
        start = datetime.datetime.strptime(start, dtfmt)
        time = datetime.datetime.strptime(time, dtfmt)
    
        index_current = TIMES.index(start) + is_end
        index_goal = TIMES.index(time)
    
        index_delta = index_goal - index_current
    
        if index_delta > 0:
            pyautogui.typewrite(["down" for i in range(index_delta)])
        elif index_delta < 0:
            pyautogui.typewrite(["up" for i in range(index_delta)])
        
        pyautogui.typewrite(["enter"])
    
        pass
    
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
