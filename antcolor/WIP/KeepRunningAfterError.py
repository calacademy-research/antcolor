#!/usr/bin/python
from subprocess import Popen
import sys
import AntWebColorQuantifier3

filename = "AntWebColorQuantifier3.py"
while True:
    ##AntWebColorQuantifier3.lastAnalyzed = AntWebColorQuantifier3.lastAnalyzed + AntWebColorQuantifier3.sortingi;
    print("\nStarting " + filename)
    p = Popen("python " + filename, shell=True)
    p.wait()