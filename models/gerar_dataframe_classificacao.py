import pandas as pd

class GerarDataframe():
    def __init__(self,dataframe:pd.DataFrame):
        self.df = dataframe
        self.criar_classes()

    def criar_classes(self):
        self.df['normal'] = ['nao' if 0 == x else 'sim' for x in self.df['normal']]
        self.df['desbalanceamento'] = ['baixo' if 06.0 == x or 10.0 == x else ('medio' if 15.0 == x or 20.0 == x else ('alto' if 25.0 == x or 30.0 == x or 35.0 == x else '-')) for x in self.df['desbalanceamento']]
        self.df['desalinhamento_horizontal'] = ['baixo' if 0.50 == x else ('medio' if 1.00 == x or 1.50 == x else ('alto' if 2.00 == x else '-')) for x in self.df['desalinhamento_horizontal']]
        self.df['desalinhamento_vertical'] = ['baixo' if 0.51 == x or 0.63 == x else ('medio' if 1.27 == x or 1.40 == x else ('alto' if 1.78 == x or 1.90 == x else '-')) for x in self.df['desalinhamento_vertical']]
        self.df['ball_fault'] = ['baixo' if 06.0 == x else ('medio' if 20.0 == x else ('alto' if 35.0 == x else '-')) for x in self.df['ball_fault']]
        self.df['outer_race'] = ['baixo' if 06.0 == x else ('medio' if 20.0 == x else ('alto' if 35.0 == x else '-')) for x in self.df['outer_race']]
        
    def Get(self):
        return self.df