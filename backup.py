#backs up my vikunja server and rpi, pulls and updates the backup clones of my git repos (I have a main ver on my computer that i edit but i always forget to pull to the nas, which kinda defeats the purpose of the backup), checks pi temps, updates libraries on said pi, just the general housekeeping stuff that I always forget to do. once its all done itll make a new text file with the output of the backup if there were any errors
import board
import digitalio
import time
from adafruit_debouncer import Debouncer
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
import neopixel
import os
import subprocess
from datetime import datetime
import re

kbd = Keyboard(usb_hid.devices)
cc = ConsumerControl(usb_hid.devices)

def tap(keys):
    for key in keys:
        kbd.press(key)
        kbd.release(key)

kbd.press(Keycode.right_control)
kbd.press(Keycode.alt)
kbd.press(Keyboard.T)
kbd.release(Keycode.right_control)
kbd.release(Keycode.alt)
kbd.release(Keyboard.T)

def type(input):
    for letter in input:
        tap(letter)

type("docker exec -it vikunja-vikunja-1 /app/vikunja/viknuja dump > /mnt/nasmedia/Misc/ViknujaBackups/viknuja-$(date +%F-%H%M).vikunjabackup")
tap(enter)

backup_dir = '/mnt/nasmedia/Misc/ViknujaBackups'
expected_name = 'vikunja-{}.vikunjabackup'.format(datetime.now().strftime('%F-%H%M'))
expected_path = os.path.join(backup_dir, expected_name)

if os.path.isfile(expected_path):
    print("placeholder")
else:
    error_file = os.path.join(os.path.expanduser('~'), 'Downloads', 'vikunja_backup_error_{}.txt'.format(datetime.now().strftime('%F-%H%M%S')))
    try:
        with open(error_file, 'w') as f:
            f.write('ERROR: Expected backup not found: {}\n'.format(expected_path))
            try:
                f.write('\nContents of backup directory ({}):\n'.format(backup_dir)) #test if I can even see the rest of the backups
                for entry in os.listdir(backup_dir):
                    f.write(' - {}\n'.format(entry))
            except Exception as list_err:
                f.write('Could not list backup directory {}: {}\n'.format(backup_dir, list_err))
        print('Error file created:', error_file)
    except Exception as write_err:
        print('Failed to create error file:', write_err)

base = '/mnt/nasmedia/Code_Backups'

if os.path.isdir(base):
    for name in os.listdir(base):
        repo_path = os.path.join(base, name)
        if not os.path.isdir(repo_path):
            continue
        if os.path.isdir(os.path.join(repo_path, '.git')):
            try:
                print("Updating:", repo_path)
                subprocess.run(['git', '-C', repo_path, 'pull'], check=True)
            except subprocess.CalledProcessError as e:
                print("git pull failed for", repo_path, ":", e)
        else:
            print("Skipping (not a git repo):", repo_path)
else:
    print("Base folder not found:", base)

try:
    raw = os.popen("vcgencmd measure_temp").read().strip()
    if raw:
        num = re.search(r"([0-9]+(?:\.[0-9]+)?)", raw) #still cant read regex lmao
        if num:
            temp_c = float(num.group(1))
            if temp_c > 45.0:
                note_file = os.path.join(
                    os.path.expanduser('~'),
                    'Downloads',
                    'rpi_temp_note_{}.txt'.format(datetime.now().strftime('%F-%H%M%S'))
                )
                try:
                    with open(note_file, 'w') as f:
                        f.write("WARNING: RPi CPU temp is {:.1f}C (>45C)\n".format(temp_c))
                        f.write("Raw output: {}\n".format(raw))
                    print("Temperature note written:", note_file)
                except Exception as write_err:
                    print("Failed to write temp note:", write_err)
        else:
            print("Could not parse temperature from output:", raw)
    else:
        print("No output from vcgencmd measure_temp")
except Exception as e:
    print("Failed to check temperature:", e)
