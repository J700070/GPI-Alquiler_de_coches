from datetime import time
import datetime
import pandas as pd


# Returns: 
# 0: Fecha y hora correctas
# 1: Hora de recogida no válida
# 2: Hora de entrega no válida
# 3: Fecha de recogida igual a fecha de entrega y hora de recogida mayor a hora de entrega
# 4: Fecha de recogida superior a fecha de entrega


def check_datetime(fecha_recogida, hora_recogida, fecha_entrega, hora_entrega):
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


def check_user_and_password(usuario, contraseña):
    users_df = pd.read_csv('users_db.csv')

    for i, row in users_df.iterrows():
        if (row['usuario'] == usuario or row["email"] == usuario) and row['contrasena'] == contraseña:
            return True
    else:
        return False