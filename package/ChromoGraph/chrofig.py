import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import tempfile
import unidecode
import os

class ChromoFigure:
    """ Export RAW-file chromatoramm to picture graph"""
    
    def __init__(self):
        self.__min_time = 15
        self.__max_time = 45
        self.__title = ''
        self.__format = 'png'
        self.__temp_file = os.path.join(tempfile.gettempdir(), f'tmp_{self.__title}')
    
    @staticmethod
    def changer(x):
        """For bad unidecodeing in Windows"""
        if x[1].isdigit() or x[1] == '.':
            return x
        else:
            while x[1].isdigit() != True:
                x = x.replace(x[1], '')
            return x

    min_time = property(doc="Start time for graph")
    max_time = property(doc="End time for graph")
    title = property(doc='Title on the top of the graph')
    form = property(doc='Format to export')
    tmpfile = property(doc='Temp file to write temporary result file')

    @min_time.setter
    def min_time(self, x):
        
        self.__min_time = x
    @min_time.getter
    def min_time(self):
        return self.__min_time


    @max_time.setter
    def max_time(self, x):
        self.__max_time = x
    @max_time.getter
    def max_time(self):
        return self.__max_time


    @title.setter
    def title(self, x):
        self.__title = x
    @title.getter
    def title(self):
        return self.__title

    @form.setter
    def form(self, x):
        self.__format = x
    @form.getter
    def form(self):
        return self.__format

    @tmpfile.setter
    def tmpfile(self, x):
        self.__temp_file = x
    @tmpfile.getter
    def tmpfile(self):
        return self.__temp_file


    def export(self, file):
        """Exporting chromatogramm into picture with your settings"""
        # decoding and changing file for normal python executing
        with open(file, 'r') as f:
            tmp = unidecode.unidecode(str(f.read().replace(',', '.')))
        # Writing new file into old
        with open(self.__temp_file, 'w') as f:
            f.write(tmp)
        # Variable for easy debug
        time = "Time (min)"
        value = "Value (mAU)"

        # Reading new file
        df_ref = pd.DataFrame(pd.read_csv(self.__temp_file,
                                sep='\t',
                                skiprows=42))
        # Crutch for bad unidecoding
        if df_ref[value].dtype != 'float':
                    df_ref[value] = df_ref[value].apply(ChromoFigure.changer)

        # cutting off unnecessary time (slip and flushing)
        df = df_ref[df_ref[time] >= self.__min_time][
                    [time, value]].astype('float')
        df = df[df[time] <= self.__max_time]

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
        ax.set_title(self.__title,
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
            np.arange(self.__min_time, self.__max_time + 1, 3))

        ax.yaxis.set_tick_params(labelsize=22)
        ax.xaxis.set_tick_params(labelsize=22)
        ax.axis([self.__min_time - 1,
                self.__max_time + 1,
                miny - rnd / 2,
                maxy + rnd / 2])

        # Plotting
        ax = plt.plot(x, y, '-',
                        color='black',
                        markersize=1,
                        label='VIS_1')

        # Exporting file
        filename = f"{file.replace('.txt', f'.{self.__format}')}"

        fig.savefig(f"{filename}",
                    format=f'{self.__format}',)
        # Closing fig fore faster executing
        print(f"> successfully exported {file}")
        plt.close()
