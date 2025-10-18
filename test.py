#i usually code in java so python pmo (dont expect good)
#these are all up to date from previous tests, but this is proof the python backup program works
import os
import subprocess

base = 'Z:\Code_Backups'

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

#I dont have anything to test this on lmao so imma js run it manually 
#imagine this was running on a raspi pico or smth
