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
        self.doc_header = "> avaliable comands (type 'help _command_' for \
more info about specific command)"

    def default(self, line):
        print("> Command doesn't exists")

    def do_export(self, *args):
        """Export your file in graph"""
        file = input('> Enter your filename: ')
        print(f"> Exporting in {fig.form}")
        fig.export(file)
        return

    def do_serial_export(self, *args):
        """export all files, containing template in name"""
        direct = input('Enter your path with files: ')
        template = input('Enter template for search (\
if you want all files to convert - don\'t type anything): ')
        if not template:
            template = '.txt'
        for dirpath, _, filenames in os.walk(direct):
            for filename in filenames:
                if template in filename:
                    fig.export(os.path.join(dirpath, filename))

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
        fig.title = input('> Enter your graph title: ')

    def do_format(self, *args):
        fig.form = input(">\n> Enter your format: ")

    def do_exit(self, *args):
        """Exit command"""
        raise KeyboardInterrupt
        return -1


# Program run
if __name__ == '__main__':
    c = CLI()
    while True:
        try:
            c.cmdloop()
        # Exceptions
        except ValueError:
            print("\n> This format isn't supported")
        except FileNotFoundError:
            print("\n> Directory doesn't exist")
        # except Exception:
        #     print(Exception)
        except KeyboardInterrupt:
            print('\n> Thank you for using!')
            break
