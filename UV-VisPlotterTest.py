import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
import datetime
from io import StringIO

timestamp = datetime.datetime.now()

if len(sys.argv) > 1:
    note = sys.argv[1]
else:
    note = "NoteNotProvided"

path = "10-19-23 - 1mm full and vapor and 10um bubble"
save = "Plots/" + timestamp.strftime("%Y-%b-%d") + "/" + timestamp.strftime("%X") + ": " + note + "/"
if not os.path.exists(save):
    os.makedirs(save)

files = [
    f"{path}/1mmfull.csv",
    "10-10-23 - 10um CS2/10um CS2-2 - 500nm cutoff.csv",
    f"{path}/10umbubble.csv"
]  # Add paths to all files you want to read

data_frames = {}
data_info = {}
for file_path in files:

    # Read the first two lines of the file to determine the number of datasets
    lines = []
    with open(file_path, 'r') as file:
        for line in file:
            stripped_line = line.strip()
            if not stripped_line:  # check for the blank line indicating start of log
                break
            lines.append(stripped_line)

    # Extract headers
    header1 = lines[0].strip().split(',')
    header2 = lines[1].strip().split(',')

    # Exclude headers from the lines list
    lines = lines[2:]

    # Convert the lines (excluding headers) to a single string
    # and then use StringIO to convert it into a file-like object
    data = StringIO("\n".join(lines))

    num_datasets = header2.count("Wavelength (nm)")

    unique_headers = []
    name_counts = {}
    for i, name in enumerate(header2):
        if name in name_counts:
            name_counts[name] += 1
            unique_name = f"{name}.{name_counts[name]}"
            unique_headers.append(unique_name)
        else:
            name_counts[name] = 0  # Initialize count to 0 for first occurrence
            unique_headers.append(name)

    df = pd.read_csv(data, header=None, names=unique_headers)
    data_frames[file_path] = df

    # Store the DataFrame and its unique headers in the dictionary
    data_info[file_path] = {
        'data': df,
        'headers': unique_headers,
        'header1': header1
}

# Start plotting
plt.figure(dpi=600)
plt.title(f"UV-Vis: CS₂")  # You can modify this if needed
plt.xlabel("nm")
plt.ylabel("Abs")
plt.minorticks_on()
plt.tick_params(which='both', direction='in', pad=5)

color_dict = {
    'teal': "#099e7d",
    'light_red': "#e57373",
    'light_blue': "#64B5F6",
    'purple': "#b366ff"
}
colors = list(color_dict.values())

datasets_to_plot = {
    f"{path}/1mmfull.csv": ["1mm full", "1mm vapor"],
    f"{path}/10umbubble.csv": ["10um bubble"],
    "10-10-23 - 10um CS2/10um CS2-2 - 500nm cutoff.csv": ["10um full"]
}
color_index = 0
for file_path, info in data_info.items():
    df = info['data']
    unique_headers = info['headers']
    num_datasets = len(unique_headers) // 2  # Adjusted to use unique headers

    for i in range(num_datasets):
        dataset_name = info['header1'][i*2]

        # Check if this dataset should be plotted for this file
        if file_path in datasets_to_plot and dataset_name not in datasets_to_plot[file_path]:
            continue

        w_col_name = unique_headers[i*2]
        a_col_name = unique_headers[i*2 + 1]

        plt.plot(df[w_col_name], df[a_col_name], color=colors[color_index % len(colors)], label=f"{dataset_name}")
        color_index += 1

plt.legend()
plt.savefig(f"{save} UV-Vis Spectra.png", format="png")
plt.savefig(f"{save} UV-Vis Spectra.pdf", format="pdf")
plt.savefig(f"{save} UV-Vis Spectra.svg", format="svg", transparent=True)
