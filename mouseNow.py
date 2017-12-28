#! python3

import pyautogui
print('Press Ctrl-C to quit.')

while True:
    try:
        # Get and print the mouse coordinates.
        x, y = pyautogui.position()
        
        positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
        positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
        pixelColor = pyautogui.screenshot().getpixel((x, y))
        positionStr += ' RGB: (' + str(pixelColor[0]).rjust(3)
        positionStr += ', ' + str(pixelColor[1]).rjust(3)
        positionStr += ', ' + str(pixelColor[2]).rjust(3) + ')'
        print(positionStr, end='')
        print()
    except KeyboardInterrupt:
        print('\nDone.')
        break;

