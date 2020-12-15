#######################################################
#       Welocome to source code for ChromoGraph!      #
#  Some of the features are creating and optimizing.  #
#                   So, stay tuned!                   #
#######################################################

import matplotlib.pyplot as plt
import matplotlib
from cmd import Cmd
import pandas as pd
import numpy as np
import unidecode
import argparse
import sys
import os

# plt.rcParams['pgf.texsystem'] = 'pdflatex'
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['font.family'] = 'Calibri'


# crutch for bad windows unicode interpritation
# (in Linux Ubuntu all is ok)
def changer(x):
    if x[1].isdigit() or x[1] == '.':
        return x
    else:
        return x.replace(x[1], '')


def time_for_graph():
    print("choose your start time")
    min_time = float(input())
    print("choose your end time")
    max_time = float(input())
    return min_time, max_time


# The main function that exports pictures
def print_fig(form, min_time, max_time):
    # Iteration of all files in "path"
    for dirpath, dirnames, filenames in os.walk("."):
        for filename in filenames:
            # finding specific files
            if 'UV_VIS_1.txt' in filename:

                filenamef = os.path.join(dirpath, filename)  # full filename
                # decoding and changing file for normal python executing
                with open(filenamef, 'r') as g:
                    f = str(g.read().replace(',', '.'))
                    t = f.encode("utf-8")
                    t = t.decode("utf-8")
                    t = unidecode.unidecode(f)

                # Writing new file into old
                with open(filenamef, 'w') as g:
                    g.write(t)
                # Variable for easy debug
                time = "Time (min)"
                value = "Value (mAU)"

                # Reading new file
                df_ref = pd.DataFrame(pd.read_csv(filenamef,
                                      sep='\t',
                                      skiprows=42))
                # print((df_ref[value] == 0).any())

                # Crutch (look above)
                if df_ref[value].dtype != 'float':
                    df_ref[value] = df_ref[value].apply(changer)

                # cutting off unnecessary time (slip and flushing)
                df = df_ref[df_ref[time] >= min_time][
                           [time, value]].astype('float')
                df = df[df[time] <= max_time]

                # Coordinates for graph
                x = df[time].tolist()
                y = df[value].tolist()

                # Variables for more readable code
                miny = min(y)
                maxy = max(y)
                rnd = round(maxy * 0.1, -1)

                # Initializing graph
                fig, ax = plt.subplots(1, 1,
                                       figsize=(15, 10),
                                       tight_layout=True)

                # Graph customization
                ax.set_title(filename[0:10],
                             fontsize=25,
                             color='black',
                             pad=10)

                ax.set_xlabel('Time (min)',
                              fontsize=25,
                              color='black',
                              labelpad=10)
                ax.set_ylabel('Absorbance (mAU)',
                              fontsize=25,
                              color='black',
                              labelpad=10)
                ax.yaxis.set_ticks(
                    np.arange(round(miny, -2),
                              round(maxy, -2) + 100,
                              rnd))
                ax.xaxis.set_ticks(
                    np.arange(min_time, max_time + 1, 3))

                ax.yaxis.set_tick_params(labelsize=22)
                ax.xaxis.set_tick_params(labelsize=22)
                ax.axis([min_time - 1,
                        max_time + 1,
                        miny - rnd / 2,
                        maxy + rnd / 2])

                # Plotting
                ax = plt.plot(x, y, '-',
                              color='black',
                              markersize=1,
                              label='VIS_1')

                # Exporting file
                filename = filename.replace('.txt', f'.{form}')
                fig.savefig(f"{filename}",
                            format=f'{form}',
                            quality=100)
                # Closing fig fore faster executing
                print(f"successfully exported {filename}")
                plt.close()


# Command line (Cmd) class
class YourCmdSubclass(Cmd):
    """Make your txt chromatogramm into beautiful graph"""

    def do_svg(*args):
        """export in SVG format"""
        print('Exporting in SVG')
        min_time, max_time = time_for_graph()
        form = 'svg'
        print_fig(form, min_time, max_time)  # , path, dest)
        return -1

    def do_png(*args):
        """Export in PNG format"""
        print('Exporting in PNG')
        min_time, max_time = time_for_graph()
        form = 'png'
        print_fig(form, min_time, max_time)  # , path, dest)
        return -1

    def do_diff_type(*args):
        """Export in different format"""
        print("enter your format")
        form = input()
        min_time, max_time = time_for_graph()
        print(f"Exporting in {form}")
        print_fig(form, min_time, max_time)  # , path, dest)
        return -1

    def do_exit(*args):
        return -1


if __name__ == '__main__':
    try:
        c = YourCmdSubclass()
        command = ' '.join(sys.argv[1:])
        if command:
            sys.exit(c.onecmd(command))
        c.cmdloop()
    except KeyboardInterrupt:
        print('Thank you for using!')
