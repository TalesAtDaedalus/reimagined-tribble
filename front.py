import numpy as np
import json 

import streamlit as st
import requests as rs

up_file = None
warning = None

def send_file():
    if up_file is not None:
        vid = {'upvid' : (up_file.name, up_file.getvalue())}
        resp = rs.request( 'POST'
                              ,'http://localhost:5000/process'
                              , files = vid
                              #, stream = True
                              )
        
        st.video(resp.content)

        #st.session_state['modo'] = 'processando'


if 'modo' not in st.session_state:
    st.session_state['modo'] = 'upload'

modo = st.session_state['modo']

if modo == 'upload':
    "Escolha um vídeo para realizar a detecção de objetos"
    up_file = st.file_uploader("Escolha um arquivo")

    st.button("Processar arquivo", on_click=send_file)
    

elif modo == 'processando':
    "Estou Processando"

elif modo == 'pronto':
    "Estou pronto"

else:
    "Algo deu errado :/"



