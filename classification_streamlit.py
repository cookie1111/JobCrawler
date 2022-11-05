import warnings
warnings.simplefilter(action='ignore',category=FutureWarning)

import streamlit as st
import pandas as pd
import numpy as np
from st_aggrid import AgGrid
from page_classification import ClassifyPages




def save_and_open_next(df):
    print(st.session_state['cur_folder'])
    df.to_csv(str(st.session_state['cur_folder']) + '/df_annotated.csv')
    st.session_state['cur_folder'] = next(st.session_state['iterator'])


def main():

    if 'classifier' not in st.session_state:
        st.session_state['classifier'] = ClassifyPages("./pages_ds", ["career", "we-are-recruiting", "we-are-hiring", "job", "positions", "welcomekit",
                                     "joinus", "join-us", "recruit", "work-with-us", "work-for-us"])
        st.session_state['iterator'] = iter(st.session_state['classifier'])
        st.session_state['cur_folder'] = next(st.session_state['classifier'])

    df = st.session_state['classifier'].using_agGrid(st.session_state['classifier'].prep_classification(st.session_state['cur_folder']))
    #print(df)
    with st.sidebar:
        st.text(st.session_state["cur_folder"])
        next_button = st.button(
            label='Next',
            #on_click=save_and_open_next,
            #args=df['data']
        )
    if next_button:
        save_and_open_next(df['data'])
        #print(st.session_state)

if __name__ == "__main__":
    st.set_page_config(layout='wide')
    main()
    print("we out")
