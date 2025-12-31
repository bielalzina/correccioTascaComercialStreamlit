# Botones para continuar o controlar etapas de un proceso
# Otra alternativa a anidar contenido dentro de un botón es usar un valor
# st.session_state que designe el paso o la etapa de un proceso. En este
# ejemplo, tenemos cuatro etapas en nuestro script:

# 0 Antes de que el usuario comience.
# 1 El usuario ingresa su nombre.
# 2 El usuario elige un color.
# 3 El usuario recibe un mensaje de agradecimiento.

# Un botón al principio avanza la etapa de 0 a 1. Un botón al final la
# reinicia de 3 a 0. Los demás widgets utilizados en las etapas 1 y 2
# tienen devoluciones de llamada para configurar la etapa. Si tiene un
# proceso con pasos dependientes y desea mantener visibles las etapas
# anteriores, dicha devolución de llamada obliga al usuario a volver a
# las etapas posteriores si modifica un widget anterior.

import streamlit as st

if "stage" not in st.session_state:
    st.session_state.stage = 0


def set_state(i):
    st.session_state.stage = i


if st.session_state.stage == 0:
    st.button("Begin", on_click=set_state, args=[1])

if st.session_state.stage >= 1:
    name = st.text_input("Name", on_change=set_state, args=[2])

if st.session_state.stage >= 2:
    st.write(f"Hello {name}!")
    color = st.selectbox(
        "Pick a Color",
        [None, "red", "orange", "green", "blue", "violet"],
        on_change=set_state,
        args=[3],
    )
    if color is None:
        set_state(2)

if st.session_state.stage >= 3:
    st.write(f":{color}[Thank you!]")
    st.button("Start Over", on_click=set_state, args=[0])
