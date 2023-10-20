#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit as curveFit
import datetime
import os
import sys
from io import StringIO

timestamp = datetime.datetime.now()

if len(sys.argv) > 0:
    note = sys.argv[1]

path = "10-19-23 - 1mm full and vapor and 10um bubble"
save = "Plots/" + timestamp.strftime("%Y-%b-%d") + "/" + timestamp.strftime("%X") + ": " + note + "/"
if not os.path.exists(save):
  os.makedirs(save)

# import data
run = "2"
df = {}

with open(f"{path}/1mmfull.csv", 'r') as file:
    lines = []
    for line in file:
        if line.strip() == "":  # check for the blank line indicating start of log
            break
        lines.append(line)

# Convert the lines to a single string and then use StringIO to convert it into a file-like object
data = StringIO("\n".join(lines))

# Now read it using pandas
df = pd.read_csv(data, delimiter=',')
df = pd.read_csv(f"{path}/1mmfull.csv", skiprows=1)

#plot
plt.figure(dpi=600)
plt.title(f"UV-Vis: 1mm CS₂ liquid") #10μm
plt.xlabel("nm")
plt.ylabel("Abs")
#plt.xlim()
#plt.ylim()
plt.minorticks_on()
plt.tick_params(which='both', direction='in', pad=5)

plt.plot(df["Wavelength (nm)"], df["Abs"], color="#099e7d")
plt.savefig(f"{save} UV-Vis Spectra.png", format="png")
plt.savefig(f"{save} UV-Vis Spectra.pdf", format="pdf")
plt.savefig(f"{save} UV-Vis Spectra.svg", format="svg", transparent=True)
