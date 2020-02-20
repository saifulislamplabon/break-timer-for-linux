#!/usr/bin/env python3
import subprocess
import time
import sys
import getopt


def show_usages():
    usages = """
    Usage:
        python3 break-timer.py [OPTION…]

    Options:
        -h, --help          Show Help Options
        -d, --desktop       Name of the desktop environment (e.g: "gnome", "cinnamon", default "gnome")
        -t, --active-time   Time in minutes before the app shows screen lock notification after unlock (default 20)
        -p, --grace-period  Time in seconds before the screen get locked after showing notification (default 10)
    """
    print(usages)


def is_locked(desktop="gnome"):
    screensaver_inactive_msg = "The screensaver is inactive"

    try:
        output = subprocess.check_output(
            ["{0}-screensaver-command".format(desktop),  "-q"]).decode("utf-8").strip()

        if screensaver_inactive_msg in output:
            return False
        else:
            return True

    except subprocess.CalledProcessError:
        print("Error running screensaver-command. Make sure you have screensaver-command\
             installed for your desktop environment.")
        sys.exit(2)


def show_notification(grace_period):
    title = "It's time to take a break! Screen will be locked in {0} sceconds.".format(
        grace_period)
    subprocess.Popen(["notify-send",  title])


def lock_screen(desktop):
    subprocess.Popen(["{0}-screensaver-command".format(desktop),  "-l"])


def main(argv):
    desktop = "gnome"
    unlocked_time = 0
    grace_period = 10
    max_active_time = 30

    options = {
        "help": ["-h", "help"],
        "desktop": ["-d", "--desktop"],
        "active_time": ["-t", "--active-time"],
        "grace_period": ["-p", "--grace-period"]
    }

    try:
        opts, args = getopt.getopt(
            argv, "hd:t:p:", ["help", "desktop=", "active-time=", "grace-period="])
    except getopt.GetoptError:
        show_usages()
        sys.exit(2)

    for opt, arg in opts:
        if opt in options["help"]:
            show_usages()
            sys.exit(2)
        elif opt in options["desktop"]:
            desktop = arg
        elif opt in options["active_time"]:
            max_active_time = int(arg)
        elif opt in options["grace_period"]:
            grace_period = int(arg)

    print("Timer started. Next break in {0} minutes.".format(max_active_time))

    while True:
        time.sleep(60)

        if is_locked(desktop):
            unlocked_time = 0
        else:
            unlocked_time += 1
            print("Timer is running for {0} minutes. Next break in {1} minutes.".format(
                unlocked_time, max_active_time - unlocked_time))

        if unlocked_time >= max_active_time:
            unlocked_time = 0

            show_notification(grace_period)
            time.sleep(grace_period)

            lock_screen(desktop)


if __name__ == "__main__":
    main(sys.argv[1:])
