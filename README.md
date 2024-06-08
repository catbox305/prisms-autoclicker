## Installation (Mac)

Download the .zip from the assets section of the latest release.
> Make sure to download the .zip that matches your CPU architecture.

Next, unzip the application and place it in your applications folder.\
You will not be able to open it yet due to the file being quarantined. **The app is not damaged.**\
To fix this, run ```xattr -d com.apple.quarantine /Users/`whoami`/Applications/"prism's autoclicker.app"``` in your command line/terminal. Make sure the application is named "prism's autoclicker" and located in your applications folder - otherwise the command won't work.

Finally, go to settings, select "Privacy/Security", and give the app "Input Monitoring" and "Accessibility" permissions.

## Installation (Windows)

Download `prisms autoclicker.py` from the assets section of the latest release.
> If you do not already have python installed/you have python 3.10 or under (check it with `py --version`) download it here: [https://python.org/downloads](https://www.python.org/downloads/)\
> Presumably, your installation of python will come with pip. You can check if pip is already installed with the command: `py -m pip --version`\
> If you see a message starting with "SyntaxError", type `exit()` and retry. This applies for most of the steps.\
> "Download" pip with this command: `py -m ensurepip --default-pip`. If that does not work, please consult this page: [https://packaging.python.org](https://packaging.python.org/en/latest/tutorials/installing-packages/#requirements-for-installing-packages)

Run the command: `py -m pip install pynput`\
Run the command: `py -m pip install pyinstaller`\
Once pyinstaller is ready, run: `pyinstaller [path to prisms autoclicker.py goes here]`
You should now have a working exe! (please send me the file so i can simplify this process. also the exe should be located in a "dist" folder in the same place as prisms autoclicker.py)

## Usage

Hotkeys:
```
<alt>+<t> Toggle autoclicker
<alt>+<r> Toggle tasks recording
<alt>+<p> Toggle tasks playback
```
For Mac users: Tasks and/or other functionality may be extremely laggy when game mode is enabled. Exiting fullscreen or turning game mode off should fix this.

#### If you found prism's autoclicker useful, please consider starring the repository =)
