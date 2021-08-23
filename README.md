# PythonFunkin
Friday Night Funkin', but recreated in Python.
This serves as my first ever Python project, and mostly uses the Pygame 2.0 library.
## Features
- The original game recreated using our own scoring system!
- The ability to import your own OGG/CAF and JSON files to be able to play your own songs & charts!
- Cross-compatibility -- It should be able to run both on Visual Studio Code using Pygame and on the iOS app Pythonista. (To build the game on either of those, see the sections below.)

# Building the game on iOS using Pythonista
This is a guide to fetch the project files on iOS using StaSh.

1. Download Pythonista on the App Store, then open it
2. Access the console by swiping left from the right edge of the screen.
3. Type this into the command line:
```Python
import requests as r; exec(r.get('https://bit.ly/get-stash').content)
```
4. Restart Pythonista (Open the App Switcher and swipe the app up, then come back into Pythonista again).
5. Find the `launch_stash.py` file (usually located in the "This iPad" folder)
6. Before running it, add a new line at the very top of the script and type this:
```Python
#!python2
```
This is necessary because we need to run the script on Python 2.7 in order for it to properly work.

7. Run the script using the Play button in the top-right corner of the screen.
8. A new window next to the console should have appeared, titled StaSh. Type this into the command line:
```
rm -r PythonFunkin/
git clone https://github.com/CubixL/PythonFunkin
```

9. Before processing that last command, StaSh might say something about installing the `dulwich` module. Simply press `y` and click enter.
10. You have successfully imported the game! The PythonFunkin folder should be somewhere inside the "This iPad" folder.
If you wish to run the game, find the `PythonFunkin.py` script, and run it with the play button.

## Fetching the last version of the game
If you already have PythonFunkin installed, but wish to update it, simply re-open `launch_stash.py`, and type these commands:
```
cd PythonFunkin/
git pull
```
Before confirming the last command, the system might give you a warning. This means that your local changes to the project will be overwritten by the new version, so be careful!

# Running the game on Visual Studio Code
You can download Python [here.](https://www.python.org/downloads/)

You can download Visual Studio Code [here.](https://code.visualstudio.com/)

To install the required libraries and the project itself, you can type this into a command prompt:
```
pip install -U pygame --user
git clone https://github.com/SirNytram/gameapp
pip install -e gameapp
git clone https://github.com/CubixL/PythonFunkin
code PythonFunkin
```
