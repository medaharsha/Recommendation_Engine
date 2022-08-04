# -*- coding: utf-8 -*-
"""
Created on Sat Feb 19 09:29:55 2022

@author: medah
"""
import streamlit as st
st.set_page_config(page_title="Song Recommendation", layout="wide")

import pandas as pd
import base64



rasa_dict = {'love/beauty':'Shringara','heroism/courage':'Veera','surprise/wonder':'Adhbhutha','peace/tranquility':'Shantha','sorrow':'Karuna','laughter':'Haasya'}
rasa_names = list(rasa_dict.keys())

@st.cache(allow_output_mutation=True)
def load_data():
    df = pd.read_excel("Songs_with_MFCC_Features_2_segments_Final_Result_Reco_engine.xlsx")
    track_df = df.iloc[:,42:]
    return track_df

track_df = load_data()




def Get_Songs(rasa):
    col_name = rasa_dict[rasa]
    songs_df = track_df.sort_values(col_name, ascending=False)[:30]
    songs_path = songs_df["file_path"].to_list()
    return songs_path
    




title = "Mood Based Recommendation Engine"
st.title(title)

st.write("Adios ! If you wish to change you mood, listen to the songs recommended by our recommendation engine.")
st.markdown("##")



with st.container():
    col1, col2,col3 = st.columns((1.5,1,2))
    with col2:
        file_ = open("listening-to-music-spongebob.gif", "rb")
        contents = file_.read()
        data_url = base64.b64encode(contents).decode("utf-8")
        file_.close()

        st.markdown(
            f'<img src="data:image/gif;base64,{data_url}" alt="cat gif">',
            unsafe_allow_html=True,
            )




with st.container():
    col1, col2,col3 = st.columns((2,0.5,0.5))
    with col1:
        st.markdown(""" ## Choose your genre: """,True)
        rasa = st.radio(
            "",
            rasa_names, index=rasa_names.index("heroism/courage"))
        
        
        
tracks_per_page = 6 
songs_path = Get_Songs(rasa)

if 'previous_inputs' not in st.session_state:
    st.session_state['previous_inputs'] = [rasa]

current_inputs = [rasa] 
if current_inputs != st.session_state['previous_inputs']:
    if 'start_track_i' in st.session_state:
        st.session_state['start_track_i'] = 0
    st.session_state['previous_inputs'] = current_inputs

if 'start_track_i' not in st.session_state:
    st.session_state['start_track_i'] = 0

with st.container():
    col1, col2, col3 = st.columns([2,1,2])
    if st.button("Recommend More Songs"):
        if st.session_state['start_track_i'] < len(songs_path):
            st.session_state['start_track_i'] += tracks_per_page
            
    current_tracks = songs_path[st.session_state['start_track_i']: st.session_state['start_track_i'] + tracks_per_page]
    if st.session_state['start_track_i'] < len(songs_path): 
        count = 0
        for path in current_tracks:
            if count%2 == 0:
                with col1:
                    audio_file = open(path, 'rb')
                    audio_bytes = audio_file.read()
                    st.audio(audio_bytes)
                count+=1
            else:
                with col3:
                    audio_file = open(path, 'rb')
                    audio_bytes = audio_file.read()
                    st.audio(audio_bytes)
                count+=1
    else:
        st.write("No songs left to recommends")
            
    
                

