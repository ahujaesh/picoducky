picoducky submission!

i saw someone get a extra picoducky for submitting early and i was lwk wondering if i could get one too

My plan is to use one for being a menace at school and one for backups at home (too lazy to open a terminal and remember what to backup, so id like to just plug smth in and have it backup eveything to the NAS, I like backups bc ive been burned by data loss before)

I host a viknuja server for some friends that i would liek to automate the backup process of ([file](/backup.py)). Right now, the file backs up my vikunja server and rpi, pulls and updates the backup clones of my git repos (I have a main ver on my computer that i edit but i always forget to pull to the nas, which kinda defeats the purpose of the backup), checks pi temps, updates libraries on said pi, just the general housekeeping stuff that I always forget to do. Once its all done it'll make a new text file with the output of the backup if there were any errors

The other picoducky i plan to use to use for school ([file](/backup.py)).

Hackatime screenshot

Demo:

- backup system works fine manually, so the terminal command works, all this does it automate it

Screenhot of past backup commands working
![1760748997719](image/readme/1760748997719.png)

![1760749027231](image/readme/1760749027231.png)

Demo video of backup, proving the python works by me just running it manually (i dont have a raspi pico but itll do the same thing if it was ran from a pico)
![1760749815828](image/readme/1760749815828.mp4)

- dont have a chromebook to test the mencace program on, and the shortcuts are different on windows (what im writing this on, though i want to install linux once i get the chance) from chromebook
