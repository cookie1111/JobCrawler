from pathlib import Path
import pandas as pd


class ClassifyPages:

    def __init__(self, path):
        self.path = Path(path)
        self.page_folders = [fold for fold in self.path.iterdir()]

    def __iter__(self,start = 0):
        self.n = start
        return self

    def __next__(self):
        if self.n < len(self.page_folders):
            self.n = self.n + 1
            return self.page_folders[self.n-1]
        raise StopIteration

    def get_folder_df(self, folder_path):
        folder_path = Path(folder_path)
        return pd.read_csv(folder_path.glob('df.csv')[0])
