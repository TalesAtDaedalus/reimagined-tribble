import numpy as np
import json 

import streamlit as st
from streamlit_modal import Modal
import streamlit.components.v1 as components
import requests as rs

body = st.empty()

def wrapper_send_file(up_vid):
    def send_file():
        if up_vid is not None:
            
            with body:
                st.spinner("Processando arquivo")
            
            vid = {'upvid' : (up_vid.name, up_vid.getvalue())}
            resp = rs.request( 'POST'
                                  ,'http://localhost:5000/process'
                                  , files = vid
                                  #, stream = True
                                  )
            st.session_state.cache_vid = resp.content

    return send_file
        
def clear_vid():
    if "cache_vid" in st.session_state:
        del st.session_state.cache_vid


if 'cache_vid' not in st.session_state:
    with body.container():
        st.title("Detetcção de Objetos")
        up_file = st.file_uploader("Escolha o vídeo que deseja processar")

        st.button("Processar arquivo", on_click=wrapper_send_file(up_file))
else:
    with body.container():
        st.title("Resultado")
        st.video(st.session_state.cache_vid)

        modal = Modal(key="mod_id", title="Atenção")
        st.button("Voltar", on_click=modal.open)

        if modal.is_open():
            with modal.container():
                st.warning("Se voltar perderá o vídeo atual, você tem certeza?")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.button("Cancelar", on_click=modal.close)
                with col2:
                    st.button("Voltar", type="primary", on_click=lambda:(clear_vid(), modal.close()))


