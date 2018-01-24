# Northeastern Timesheet Bot

This bot is a tool that automatically enters a weeks worth of hours into the
Northeastern University Student Employment form. 

This set of scripts uses pyautogui in order to find and click the appropriate elements.
Because of the way pyautogui searches (comparing screenshots of images), this method
may be unreliable across different platforms. 

## Submitter Instructions
- This should be run at the end of the week, or else the form will yell at you
for attempting to enter hours in advance. 
- Navigate to the page where hours are entered
- Run `python3 submitter.py <configName>`
  - Note that there should be a file matchin the configName in the configs folder
- Quickly switch back to the sheet where the hours are entered in. The script 
should begin entering times in 5 seconds after running. 
- There are built in delays that allow the webpage to load for selction. Its 
possible to reduce the delays but that process requires some tuning.  

## Punch Instructions
The punch script helps autogenerate the configs needed for submission. It has the following commands
- `punch in`: signs you in (i.e. start time)
- `punch out`: signs you out (i.e. end time)
- `punch print`: prints your current week config
- `punch time_in`: prints what time you signed in for your current session

## Setup 
In most cases, simply installing from requirements.txt should work
`pip install requirements.txt`

Linux users may need to go through additional steps to install the pyautogui 
module as explained [here][1]

## Future Work
- Have punching in and out autoselect the appropriate config file. 
- Implement browser based method using Selenium for faster and more robust support. 
- Selenium implementation should also be able to be a "set and go", navigating to the 
correct page, and submitting times without you needing to even log in...

[1]: http://pyautogui.readthedocs.io/en/latest/install.html

