import streamlit as st

# INICIALITZACIO DELS ESTATS DE LES ETAPES DE CORRECCIÓ

if "fase_1_completa" not in st.session_state:
    st.session_state.fase_1_completa = False

if "fase_2_completa" not in st.session_state:
    st.session_state.fase_2_completa = False

if "fase_3_completa" not in st.session_state:
    st.session_state.fase_3_completa = False


print("FASE 1")
