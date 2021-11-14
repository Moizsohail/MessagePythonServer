import os
from time import sleep
import subprocess
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-w", "--watch", nargs="+", required=True)
parser.add_argument("-c", "--command", nargs="+", required=True)
args = parser.parse_args()


def re_execute(command):
    global proc
    if proc:
        proc.terminate()
    proc = subprocess.Popen(command)


command = args.command


last_change = [os.stat(filename).st_mtime for filename in args.watch]

proc = None
print("Watching", args.watch)

while True:
    sleep(3)
    if any([last_change[i] != os.stat(args.watch[i]).st_mtime for i in range(len(args.watch))]):
        print("Update", args.command)
        last_change = [os.stat(filename).st_mtime for filename in args.watch]
        re_execute(command)
