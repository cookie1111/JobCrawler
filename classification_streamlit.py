import warnings
warnings.simplefilter(action='ignore',category=FutureWarning)

import streamlit as st
import pandas as pd
import numpy as np
from st_aggrid import AgGrid
from page_classification import ClassifyPages




def save_and_open_next(df,save=True):
    if not save:
        print("skipping")
        st.session_state['cur_folder'] = next(st.session_state['iterator'])
        st.experimental_rerun()
    print("saving")
    index = [i['_selectedRowNodeInfo']['nodeRowIndex'] for i in df.selected_rows]
    df['data'].loc[index,'Job'] = [not x for x in df['data'].loc[index,'Job']]
    df['data'].to_csv(str(st.session_state['cur_folder']) + '/df_annotated.csv')
    st.session_state['cur_folder'] = next(st.session_state['iterator'])


def main():

    if 'classifier' not in st.session_state:
        st.session_state['classifier'] = ClassifyPages("./pages_ds", ["career", "we-are-recruiting", "we-are-hiring", "job", "positions", "welcomekit",
                                     "joinus", "join-us", "recruit", "work-with-us", "work-for-us"])
        st.session_state['classifier'].add_translations(['de'])
        st.session_state['classifier'].key_words = st.session_state['classifier'].key_words + ["karrier"]
        st.session_state['iterator'] = iter(st.session_state['classifier'])
        st.session_state['cur_folder'] = next(st.session_state['classifier'])

    if st.session_state['classifier'].check_annotated(st.session_state['cur_folder']):
        save_and_open_next(None,False)
    try:
        df = st.session_state['classifier'].prep_classification(st.session_state['cur_folder'])
    except IndexError as e:
        print(f"IndexError for {st.session_state['cur_folder']}")
        save_and_open_next(None,False)


    df = st.session_state['classifier'].using_agGrid(df)
    #print(df.selected_rows)
    with st.sidebar:
        st.text(st.session_state["cur_folder"])
        next_button = st.button(
            label='Next',
            on_click=save_and_open_next,
            args = [df]

        )
    #if next_button:
        #save_and_open_next(df)
        #next_button = False
        #print(st.session_state)

if __name__ == "__main__":
    st.set_page_config(layout='wide')
    main()
    print("we out")
