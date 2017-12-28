# Northeastern Timesheet Bot

This bot is a tool that automatically enters a weeks worth of hours into the
Northeastern University Student Employment form. 

## Instructions
- This should be run at the end of the week, or else the form will yell at you
for attempting to enter hours in advance. 
- Navigate to the page where hours are entered
- Run `python3 submitter.py <configName>`
  - Note that there should be a file matchin the configName in the configs folder
- Quickly switch back to the sheet where the hours are entered in. The script 
should begin entering times in 5 seconds after running. 
- There are built in delays that allow the webpage to load for selction. Its 
possible to reduce the delays but that process requires some tuning.  

## Setup 
In most cases, simply installing from requirements.txt should work
`pip install requirements.txt`

Linux users may need to go through additional steps to install the pyautogui 
module as explained [here][1]

[1]: http://pyautogui.readthedocs.io/en/latest/install.html

