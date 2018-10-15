#!/usr/bin/python3
import sys

def switch_demo(argument):
    switcher = {
            "1": 1,
            "2": 2,
            "3": 3,
            "4": 4,
            "5": 5,
            "n": "n",
        }
    print(switcher.get(argument, "Invalid selection\nTry again"))

switch_demo(sys.argv[1])
