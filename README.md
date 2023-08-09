# Flomodoro
A simple Flowtime/Flowmodoro method timer.

Programmed in python, but I run it as an .exe using pyinstaller.

![image](https://github.com/KishiBayes/timerApp/assets/55947955/a5bd8d3b-76ab-456d-85be-c88b722768b3)

# How to use:
Click start, and start working. When you reach the end of flow, click break. You will then have a fifth of the flow time in which you can break.

There is also a "Track Work Time" button which shows how much time you've spent in flow, day by day.

# How to install:
Clone the repository.

There is a wav (bell.wav) which signals the end of the break. You can of course use any wav file you like (just name it "bell.wav").
The one I use is a Sound Effect from <a href="https://pixabay.com/sound-effects/?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=105159">Pixabay</a>

If you want to turn it into a .exe file, navigate to the directory where this is saved, run pip install pyinstaller.
Then run pyinstaller stopwatch.py --noconsole --onefile.
Wherever you put the .exe file, make sure you put the wav in the same directory.
