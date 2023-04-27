import numpy as np
import json 

import streamlit as st
from streamlit_modal import Modal
import streamlit.components.v1 as components
import requests as rs


def do_upload():
    if "up_vid" in st.session_state:
        uv = st.session_state.up_vid
        vid = {'up_vid' : (uv.name, uv.getvalue())}
        resp = rs.request( 'POST'
                              ,'http://localhost:5000/process'
                              , files = vid
                              #, stream = True
                              )

        del st.session_state.up_vid
        st.session_state.processing = False
        st.session_state.cache_vid = resp.content

        
def clear_vid():
    if "cache_vid" in st.session_state:
        del st.session_state.cache_vid


# I feel i'm in javascript at this point
def i_hate_python(up_file):
    def do_thing():
        st.session_state.up_vid = up_file
        st.session_state.processing = True

    return do_thing


body = st.empty()

if "processing" not in st.session_state:
    st.session_state.processing = False

with body.container():
    if st.session_state.processing:
        st.info("Processando o arquivo")
        
        # não funciona por algum motivo
        # st.spinner("Processando arquivo")
        
        do_upload()
        
        st.session_state.processing = False
        st.experimental_rerun()
    
    elif 'cache_vid' not in st.session_state:
        st.title("Detecção de Objetos")
        up_file = st.file_uploader("Escolha o vídeo que deseja processar", key="abc")
        st.button("Processar arquivo", on_click=i_hate_python(up_file))

    else:
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


