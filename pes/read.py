import pandas as pd

class Read():
    def readCol(self, adress="names", col="name"):
        df = pd.read_csv((adress+".csv"), usecols=[col])
        df.reset_index(inplace=True)
        return df
    '''
    def readRow(self, adress="names", col="name", row = "row"):
        df = pd.read_csv((adress+".csv"))
        return df[df.col == row]'''

#print(df.head())