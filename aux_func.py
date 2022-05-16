from datetime import time
import datetime
from traceback import print_tb
import pandas as pd


# Returns: 
# 0: Fecha y hora correctas
# 1: Hora de recogida no válida
# 2: Hora de entrega no válida
# 3: Fecha de recogida igual a fecha de entrega y hora de recogida mayor a hora de entrega
# 4: Fecha de recogida superior a fecha de entrega


def check_datetime(fecha_recogida, hora_recogida, fecha_entrega, hora_entrega):
    # Si fecha es hoy
    if fecha_recogida == datetime.date.today():
        if hora_recogida < datetime.datetime.now().time() :
            return 5


    if (fecha_recogida < fecha_entrega):
        return check_hora(hora_recogida, hora_entrega)
    elif fecha_recogida == fecha_entrega:
        if (hora_recogida < hora_entrega):
            return check_hora(hora_recogida, hora_entrega)

        else:
            # Fecha de recogida igual a fecha de entrega y hora de recogida mayor a hora de entrega
            return 3
    else:
        # Fecha incorrrecta: la fecha de recogida es superior a la fecha de entrega
        return 4


def check_hora(hora_recogida, hora_entrega):
    if (time(8,0,0) <= hora_recogida <= time(22,0,0)):
        if (time(8,0,0) <= hora_entrega <= time(22,0,0)):
            return 0
        else:
            # Hora de entrega no válida
            return 2
    else:
        # Hora de recogida no válida
        return 1




def get_available_cars(oficina):
    car_df = pd.read_csv('car_db.csv')
    available_cars_df = pd.DataFrame(columns=car_df.columns)
    for i, row in car_df.iterrows():
        if row['Oficina'] == oficina:
            available_cars_df.loc[len(available_cars_df)] = row

    return available_cars_df



def check_payment(tarjeta_selected, num_tarjeta_selected, cod_seguridad_selected, fecha_expiracion_selected, nombre_titular_selected):
                if tarjeta_selected == "VISA":
                    if len(num_tarjeta_selected) != 16:
                        return 1
                elif tarjeta_selected == "MasterCard":
                    if len(num_tarjeta_selected) != 16:
                        return 1
                elif tarjeta_selected == "American Express":
                    if len(num_tarjeta_selected) != 15:
                        return 1
                if len(cod_seguridad_selected) != 3:
                    return 2
                if fecha_expiracion_selected < datetime.date.today():
                    return 3
                if len(nombre_titular_selected) == 0:
                    return 4
                return 0


def check_user_and_password(usuario, contraseña="", password=True, email = "", drop=""):
    users_df = pd.read_csv('users_db.csv')

    if drop != "":
        users_df.drop(drop, inplace=True)
    # Buscamos correspondencias
    for i, row in users_df.iterrows():
        # Si no queremos comprobar la contraseña
        if not password:
            if (row['usuario'] == usuario or row["email"] == email):
                return row["ID"]

        elif (row['usuario'] == usuario or row["email"] == usuario) and row['contrasena'] == contraseña:
            return row["ID"]
    else:
        return -1

def add_user(usuario, contraseña, email, admin):
    users_df = pd.read_csv('users_db.csv', index_col=0)

    # add new row
    users_df.loc[len(users_df)] = [usuario,email,contraseña,admin]
    # save
    users_df.to_csv('users_db.csv')
    return 0

# NAVIGATION CONTROL
def navigation(st, page_list):
    if st.session_state.get('page') == "Alquilar Coche":
        page = "Alquilar Coche"
        page = sidebar(st, page_list)

    elif st.session_state.get('page') == "Modificar datos de usuario":
        page = "Modificar datos de usuario"
        page = sidebar(st, page_list)

    elif st.session_state.get('page') == "Gestionar oficinas":
        page = "Gestionar oficinas"
        page = sidebar(st, page_list)
    elif st.session_state.get('page') == "Registro usuario":
        page = "Registro usuario"

    else:
        page = "Inicio de Sesión"

    return page



# SIDEBAR
def sidebar(st, page_list):
    with st.sidebar:
        page = st.selectbox("Navegación", page_list)
        # st.sidebar.markdown("#")
        close_session = st.button("Cerrar sesión")
        if close_session:
            st.session_state.clear()
            st.experimental_rerun()
        return page



def check_register_data(st,email,usuario, contraseña,contraseña2,admin,code, drop=""):
    res = True
    
    if (admin == True) & (code != "admin"):
        st.error("Código de administrador incorrecto.")

    # check if email is empty
    if len(email) == 0:
        st.error("El email no puede estar vacío.")
        res = False
    # check if user is empty
    elif len(usuario) == 0:
        st.error("El usuario no puede estar vacío.")
        res = False

    # check if password is empty
    elif len(contraseña) == 0:
        st.error("La contraseña no puede estar vacía.")
        res = False

    # EMAIL VÁLIDO
    elif "@" not in email:
        st.error("El email no es válido.")
        res = False

    # USUARIO VÁLIDO
    user_id = check_user_and_password(usuario, email=email, password=False, drop=drop)
    if user_id != -1:
        st.error("Usuario o email ya existente.")
        res = False

    elif contraseña != contraseña2:
        st.error("Las contraseñas no coinciden.")
        res = False


    return res



def get_user_data(user_id):
    users_df = pd.read_csv('users_db.csv')
    old_email = users_df.loc[user_id]["email"]
    old_usuario = users_df.loc[user_id]["usuario"]
    old_contraseña = users_df.loc[user_id]["contrasena"]
    return old_email, old_usuario, old_contraseña

def edit_user(st,usuario, contraseña, email, user_id):
    users_df = pd.read_csv('users_db.csv', index_col=0)
    users_df.at[user_id,"usuario"] = usuario
    users_df.at[user_id,"email"] = email
    users_df.at[user_id,"contrasena"] = contraseña
    users_df.to_csv('users_db.csv')
    return 0

def delete_user(user_id):
    users_df = pd.read_csv('users_db.csv', index_col=0)
    users_df.drop(user_id, inplace=True)
    users_df.reset_index(drop=True, inplace=True)
    users_df.to_csv('users_db.csv',)
    return 0

def is_admin(user_id):
    if user_id == None:
        return False
    users_df = pd.read_csv('users_db.csv', index_col=0)
    return users_df.at[user_id,"administrador"]

def add_office(name):
    offices_df = pd.read_csv('oficinas_db.csv', index_col=0)
    # add new row
    offices_df.loc[len(offices_df)] = [name]
    offices_df.to_csv('oficinas_db.csv')
    return 0

def delete_office(name):
    offices_df = pd.read_csv('oficinas_db.csv', index_col=0)
    offices_df.drop(name, inplace=True)
    offices_df.reset_index(drop=True, inplace=True)
    offices_df.to_csv('oficinas_db.csv',)
    return 0

def edit_office(name, new_name):
    offices_df = pd.read_csv('oficinas_db.csv', index_col=0)
    offices_df.at[name,"Nombre"] = new_name
    offices_df.to_csv('oficinas_db.csv')
    return 0