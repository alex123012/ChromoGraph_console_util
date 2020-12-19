#! /home/alexmakh/anaconda3/bin/python3

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

# Default values of variables to change in program
min_time = 15
max_time = 45
dest = os.getcwd()


# crutch for bad windows unicode interpritation
# (in Linux Ubuntu all is ok)
def changer(x):
    if x[1].isdigit() or x[1] == '.':
        return x
    else:
        return x.replace(x[1], '')


# The main function that exports pictures
def print_fig(form, min_time, max_time, dest):
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
                filename = f"{dest}/{filename.replace('.txt', f'.{form}')}"

                fig.savefig(f"{filename}",
                            format=f'{form}',
                            quality=100)
                # Closing fig fore faster executing
                print(f"successfully exported {filename}")
                plt.close()


# Command line (Cmd) class
class CLI(Cmd):
    """Make your txt chromatogramm into beautiful graph"""
    def __init__(self):
        Cmd.__init__(self)
        self.prompt = "> "
        self.intro = '''\n\n\n\n\n> Welcome to ChromoGraph version 0.1.2-beta
> For more info type "help"'''
        self.doc_header ="> avaliable comands (type 'help _command_' for more info about specific command)"

    def default(self, line):
        print("> Command doesn't exists")

    def do_export(self, args):
        """Export your file in graph"""
        print("> Enter your format")
        form = input("> Format: ")
        print(f"> Exporting in {form}")
        print_fig(form, min_time, max_time, dest)  # , path, dest)
        return -1

    def do_path(self, args):
        """Change path to convert"""
        print(f"> Enter new path (current path: {os.getcwd()}) or type \"back\" to exit")
        cd = input("> New path: ")
        if cd == "back":
            return 0
        os.chdir(cd)
        print(f"> successfully changed path to {os.getcwd()}")
        return 0

    def do_time(self, args):
        """Change start and end time for graph"""
        print("> choose your start time in min or type \"back\" to exit")
        ct = input('> default start - 15 min, end - 45 min:\t')
        if ct == "back":
            return 0

        global min_time, max_time
        min_time = float(ct)
        print("> Choose your end time")
        max_time = float(input("End: "))
        return 0

    def do_dest(self, args):
        """Change export destination"""
        global dest
        print(f"> Enter new export destination or type \"back\", default {dest}")
        nd = input("> New destination: ")

        if nd == "back":
            return 0

        if os.path.exists(nd):
            dest = nd
            print(f"> successfully changed destination to {dest}")
            return 0

        yn = input("> This directory doesn't exists, make new? [Y/n]? ")
        listy = ['y', 'yes', 'ye']

        if yn.lower() in listy:
            os.mkdir(nd)
            dest = nd
            print(f"> successfully changed destination to {dest}")
            return 0
        else:
            print("> destination hasn't changed")
            return 0

    def do_exit(self, args):
        """Exit command"""
        global Tr
        Tr = False
        print('\n> Thank you for using!')
        return -1


if __name__ == '__main__':
    Tr = True
    c = CLI()
    # c.onecmd("startup")
    while Tr:
        try:
            c.cmdloop()
        except ValueError:
            print("\n> This format isn't supported")
        except FileNotFoundError:
            print("\n> Directory doesn't exist")
        except KeyboardInterrupt:
            Tr = False
            print('\n> Thank you for using!')
