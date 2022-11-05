from pathlib import Path
import pandas as pd
from deep_translator import GoogleTranslator as Translator
import streamlit as st
from st_aggrid import AgGrid,ColumnsAutoSizeMode
import st_aggrid


class ClassifyPages:

    def __init__(self, path, key_words):
        self.path = Path(path)
        self.page_folders = [fold for fold in self.path.iterdir()]
        self.key_words = key_words

    def __iter__(self,start = 0):
        self.n = start
        return self

    def __next__(self):
        if self.n < len(self.page_folders):
            self.n = self.n + 1
            return self.page_folders[self.n-1]
        raise StopIteration

    def add_translations(self, language = []):
        words_en = self.key_words
        for lang in language:
            t = Translator(source='en', target=lang)
            self.key_words = self.key_words + t.translate_batch(words_en)
        return self.key_words

    def get_folder_df(self, folder_path):
        folder_path = Path(folder_path)
        return pd.read_csv(list(folder_path.glob('df.csv'))[0])

    def prep_classification(self, folder_path):
        df = self.get_folder_df(folder_path)
        if 'Job' in df.columns:
            return df
        else:
            jobs = pd.Series([False]*len(df))
            for w in self.key_words:
                jobs = df.URL.str.contains(w,case=False,regex=False) + jobs

            df['Job'] = jobs
            return df

    def using_agGrid(self, df,fit = True):
        grid_return = AgGrid(df, editable=True,columns_auto_size_mode=ColumnsAutoSizeMode(2))
        return grid_return

    # last resort
    def manual_annotation(self, df,per_page):
        for i in range(len(df)//per_page):
            print(df.iloc[i:i+per_page])
            vals = input()
            vals
        return df


