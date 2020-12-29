#######################################################
#       Welocome to source code for ChromoGraph!      #
#  Some of the features are creating and optimizing.  #
#                   So, stay tuned!                   #
#######################################################

from cmd import Cmd
from package.ChromoGraph.chrofig import *

fig = ChromoFigure()
file = 'test_UV_VIS_1.txt'
# Command line (Cmd) class
class CLI(Cmd):
    """Make your txt chromatogramm into beautiful graph"""
    def __init__(self):
        print('''> Welcome to ChromoGraph version 0.1.2-beta
> For more info type "help"''')
        Cmd.__init__(self)
        self.prompt = "> "
        self.doc_header = "> avaliable comands (type 'help _command_' for more info about specific command)"

    def default(self, line):
        print("> Command doesn't exists")

    def do_export(self, *args):
        """Export your file in graph"""
        fig.form = input(">\n> Enter your format: ")
        print(f"> Exporting in {fig.form}")
        fig.export(file)
        return

    def do_time(self, *args):
        """Change start and end time for graph"""
        print("> \n> choose your start time in min or type \"back\" to exit")
        ct = input('> default start - 15 min, end - 45 min:\t')
        if ct == "back":
            return
        fig.min_time = float(ct)
        fig.max_time = float(input("> Choose your end time: "))
        return
    
    def do_title(self, *args):
        """Changing graph title"""
        fig.title = input('> Enter your graph title')

    def do_exit(self, *args):
        """Exit command"""
        global Tr
        Tr = False
        print('\n> Thank you for using!')
        return -1


# Program run
if __name__ == '__main__':
    try:
        Tr = True
        c = CLI()
        while Tr:
            try:
                c.cmdloop()
            # Exceptions
            except ValueError:
                print("\n> This format isn't supported")
            except FileNotFoundError:
                print("\n> Directory doesn't exist")
            except Exception:
                print(Exception)
    except KeyboardInterrupt:
        print('\n> Thank you for using!')
