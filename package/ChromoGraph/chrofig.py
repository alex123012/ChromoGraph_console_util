import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import tempfile
import unidecode
import os


class ChromoFigure:
    """ Export RAW-file chromatoramm to picture graph"""

    format_list = ['png', 'svg', 'jpg', 'jpeg', 'pdf']

    def __init__(self):
        self.__min_time = 15
        self.__max_time = 45
        self.__title = ''
        self.__format = 'png'
        self.__temp_file = os.path.join(tempfile.gettempdir(),
                                        tempfile.NamedTemporaryFile().name)

    def __changer(self, x):

        """For bad unidecodeing in Windows"""

        y = ''
        for i in x:
            if i.isdigit() or i == '.':
                y += i
        return float(y)

    def settings(self):
        print(f'min_time = {self.min_time}')
        print(f'max_time = {self.max_time}')
        print(f'Title = {self.title}' if self.title else 'No title')
        print(f'format = {self.form}')
        print(f'Tempfile directory = {self.tmpfile}')

    def __file_normalize(self, file):

        '''decoding and changing file for normal python executing'''

        with open(file, 'r') as f:
            tmp = unidecode.unidecode(str(f.read().replace(',', '.')))

        # Writing new file into temp file
        with open(self.__temp_file, 'w') as f:
            f.write(tmp)

    def __file_read(self):
        # Variable for easy debug
        time = "Time (min)"
        value = "Value (mAU)"

        # Reading new file
        df_ref = pd.DataFrame(pd.read_csv(self.__temp_file,
                                          sep='\t',
                                          skiprows=42))
        # Crutch for bad unidecoding
        if df_ref[value].dtype != 'float':
            df_ref[value] = df_ref[value].apply(self.__changer)

        # cutting off unnecessary time (slip and flushing)
        df = df_ref[df_ref[time] >= self.__min_time][
            [time, value]].astype('float')
        df = df[df[time] <= self.__max_time]

        x = df[time].tolist()
        y = df[value].tolist()
        return x, y

    def export(self, file):

        """Exporting chromatogramm into picture with your settings"""

        self.__file_normalize(file)

        # Coordinates for graph)
        x, y = self.__file_read()

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
        if x not in format_list:
            raise TypeError
        self.__format = x

    @form.getter
    def form(self):
        return self.__format

    @tmpfile.setter
    def tmpfile(self, x):
        self.__temp_file = os.path.join(tempfile.gettempdir(), x)

    @tmpfile.getter
    def tmpfile(self):
        return self.__temp_file
