import pandas as pd

class Ranking:
    top = [] # top 10 scores

    def __init__(self):
        df = pd.read_csv('ranking.csv')
        df = df.sort_values(by=['score'], ascending=False)
        df = df.reset_index(drop=True)
        #df to array of dictionaries
        self.top = df.head(10).to_dict('records')

    def readRanking(self):
        df = pd.read_csv('ranking.csv')
        df = df.sort_values(by=['score'], ascending=False)
        df = df.reset_index(drop=True)
        self.top = df.head(10)
        return

    def insertScore(self, name, score):
        df = pd.read_csv('ranking.csv')
        df = df.append({'name': name, 'score': score}, ignore_index=True)
        df = df.sort_values(by=['score'], ascending=False)
        df = df.reset_index(drop=True)
        df.to_csv('ranking.csv', index=False)
        self.top = df.head(10)
        return df
    

