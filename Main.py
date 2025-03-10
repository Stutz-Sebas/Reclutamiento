import time
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import streamlit_authenticator as stauth
import yaml

from yaml.loader import SafeLoader

# Cargar la configuración desde un archivo YAML
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

stauth.Hasher.hash_passwords(config['credentials'])

with open('config.yaml', 'w') as file:
    yaml.dump(config, file, default_flow_style=False)

# Autenticación
authenticator = stauth.Authenticate(
    config['credentials'], 
    config['cookie']['name'], 
    config['cookie']['key'], 
    config['cookie']['expiry_days']
)

# ----- Páginas -----

# -----END Páginas -----

if "authentication_status" not in st.session_state:
    st.session_state["authentication_status"] = None

try:
    authenticator.login(single_session=True)
except Exception as e:
    st.error(e)

if st.session_state['authentication_status'] is None:
    st.warning("Por favor, ingresa tu usuario y contraseña.")

if st.session_state['authentication_status'] is False:
    st.error("❌ Usuario o contraseña incorrectos")

if st.session_state['authentication_status']:
    
    # ----- SIDEBAR -----

    st.sidebar.title(f"Hola {st.session_state['name']}! 😃")
    pages = {
        "Paginas": [
            st.Page("Inicio.py", title="Inicio"),
            st.Page("Candidatos.py", title="Candidatos"),
            st.Page("Modelo.py", title="Modelo"),
        ]
    }

    authenticator.logout(location="sidebar", button_name="Cerrar sesión ☕")
    st.sidebar.button("Cambiar contraseña", key="change_password")

    # ----- END SIDEBAR -----

    # ----- Cambiar contraseña -----
    if st.session_state.get("change_password", False):
        try:
            if authenticator.reset_password(st.session_state['username']):
                # Actualiza las credenciales en el diccionario config
                config['credentials'] = authenticator.credentials
                stauth.Hasher.hash_passwords(config['credentials'])
                
                # Guarda los cambios en el archivo YAML
                with open('config.yaml', 'w') as file:
                    yaml.dump(config, file, default_flow_style=False)

                st.toast('✅ Contraseña modificada exitosamente')
                time.sleep(3)
                st.session_state["change_password"] = False
        except Exception as e:
            st.error(f"Error al cambiar la contraseña: {e}")
    # ----- END Cambiar contraseña -----

    pg = st.navigation(pages)
    pg.run()




        

