import datetime
import streamlit as st
import pandas as pd
from aux_func import *

# ----------------------- LAYOUT ---------------------------
st.set_page_config(page_title="Alquiler de Coches")


# ----------------------- BACKEND ---------------------------
oficinas_df = pd.read_csv('oficinas_db.csv')
car_df = pd.read_csv('car_db.csv')
reservas_df = pd.read_csv('reservas_db.csv')
descuentos_df = pd.read_csv('descuentos_db.csv')

# ----------------------- Sidebar ---------------------------
if st.session_state.get('key') == "valid":
    page = "Alquilar Coche"
else:
    page = "Inicio de Sesión"

# ----------------------- Multipage ---------------------------


if page == "Inicio de Sesión":
    placeholder = st.empty()

    with placeholder.container():
        st.header("Iniciar sesión")

        usuario = st.text_input('Email o usuario')
        contraseña = st.text_input('Contraseña', type='password')

        if st.button('Iniciar sesión'):
            if not check_user_and_password(usuario, contraseña):
                st.error("Usuario o contraseña incorrectos")
            else:
                st.session_state['key'] = "valid"
                st.success("Sesión iniciada correctamente. Ya puedes comenzar a alquilar un coche.")
                st.experimental_rerun()

elif page == "Alquilar Coche":
    placeholder = st.empty()
    if st.session_state.get('key') == "valid":
        with placeholder.container():
            st.title("Alquiler de Coches")
            st.header("Reservar coche")
            st.subheader("Datos de recogida")
            # Seleccionar oficina recogida
            oficina_recogida = st.selectbox("Elegir oficina de recogida", oficinas_df['Nombre'].tolist())

            cols = st.columns(2)
            # Seleccionar fecha y hora recogida
            fecha_recogida = cols[0].date_input("Fecha de recogida", datetime.date.today(), min_value=datetime.date.today())
            hora_recogida = cols[1].time_input("Hora de recogida", datetime.time(hour=8, minute=0))

            st.subheader("Datos de entrega")
            # Seleccionar oficina entrega
            oficina_entrega = st.selectbox("Elegir oficina de entrega", oficinas_df['Nombre'].tolist())

            cols = st.columns(2)
            # Seleccionar fecha y hora entrega
            fecha_entrega = cols[0].date_input("Fecha de entrega", fecha_recogida, min_value=fecha_recogida)
            hora_entrega = cols[1].time_input("Hora de entrega", datetime.time(hour=8, minute=0))

            check_datetime_value = check_datetime(fecha_recogida, hora_recogida, fecha_entrega, hora_entrega)
            
            if check_datetime_value == 1:
                st.error("Hora de recogida no válida. El horario de apertura es de 8:00 a 22:00")
            elif check_datetime_value == 2:
                st.error("Hora de entrega no válida. El horario de apertura es de 8:00 a 22:00")
            elif check_datetime_value == 3:
                st.error("Hora de recogida mayor o igual a la hora de entrega. ")
            elif check_datetime_value == 4:
                st.error("Fecha de recogida posterior a fecha de entrega.")
            elif check_datetime_value == 5:
                st.error("Hora de recogida anterior a fecha actual.")
            else:
                st.subheader("Elegir vehículo")
                car_df = get_available_cars(oficina_recogida)

                # Reservar vehículo
                car_gamma_selected = st.selectbox("Seleccionar gama", car_df['Category'].unique())
                cols = st.columns(2)
                car_brand_selected = cols[0].selectbox("Seleccionar coche", car_df[car_df["Category"] == car_gamma_selected]['Marca'].unique())
                available_cars = car_df[(car_df["Marca"] == car_brand_selected) & (car_df["Category"] == car_gamma_selected)]['Modelo']
                car_model_selected = cols[1].selectbox("Seleccionar modelo", available_cars.unique())
                available_cars = car_df[(car_df["Category"] == car_gamma_selected) & (car_df['Marca'] == car_brand_selected) & (car_df['Modelo'] == car_model_selected)]
                conducción_selected = st.radio("Conducción", available_cars["Manual"].map({False:"Automático", True:"Manual"}).unique())
                conduccion_binary = 1 if conducción_selected == "Manual" else 0
                available_cars = car_df[(car_df["Category"] == car_gamma_selected) & (car_df['Marca'] == car_brand_selected) & (car_df['Modelo'] == car_model_selected) & (car_df['Manual'] == conduccion_binary)]
                num_puertas_selected = st.radio("Número de puertas", available_cars["Num_Puertas"].unique())
                available_cars = car_df[(car_df["Category"] == car_gamma_selected) & (car_df['Marca'] == car_brand_selected) & (car_df['Modelo'] == car_model_selected) & (car_df['Manual'] == conduccion_binary) & (car_df['Num_Puertas'] == num_puertas_selected)]
                solar_roof_selected = st.radio("Techo Solar", available_cars["Solar_Roof"].map({False:"No", True:"Si"}).unique())
                soalr_roof_binary = 1 if solar_roof_selected == "Si" else 0
                available_cars = car_df[(car_df["Category"] == car_gamma_selected) & (car_df['Marca'] == car_brand_selected) & (car_df['Modelo'] == car_model_selected) & (car_df['Manual'] == conduccion_binary) & (car_df['Num_Puertas'] == num_puertas_selected) & (car_df['Solar_Roof'] == soalr_roof_binary)]
                lista_coches_disponibles = available_cars["Name"].to_list()
                lista_coches_disponibles.insert(0,"Ninguno")
                car_selected = st.selectbox("Seleccionar coche", lista_coches_disponibles)
                
                if car_selected != "Ninguno":
                    st.subheader("Otros Datos")
                    client_type_selected = st.radio("Tipo de cliente", ["Cliente regular", "Cliente de negocio"])
                    
                    descuento_selected = st.text_input("Código de descuento", "000000")
                    if descuento_selected != "000000":
                        descuento_selected = descuento_selected.upper()
                        if descuento_selected in descuentos_df["descuento"].to_list():
                            descuento = 0
                            st.error("Código de descuento no válido.")
                        else:
                            descuento = descuentos_df[descuentos_df["descuento"] == descuento_selected]["porcentaje"].to_list()[0]
                            st.success("Código de descuento válido.")
                    else:
                        descuento = 0

                    st.subheader("Información de pago")

                    cols = st.columns(2)
                    # Seleccionar tarjeta
                    tarjeta_selected = cols[0].selectbox("Seleccionar tarjeta", ["VISA", "MasterCard", "American Express"])
                    # Seleccionar número de tarjeta
                    num_tarjeta_selected = cols[1].text_input("Número de tarjeta", "")
                    # Seleccionar código de seguridad
                    cod_seguridad_selected = cols[0].text_input("Código de seguridad", "")
                    # Seleccionar fecha de expiración
                    fecha_expiracion_selected = cols[1].date_input("Fecha de expiración", datetime.date.today())
                    # Seleccionar nombre del titular
                    nombre_titular_selected = st.text_input("Nombre del titular", "")

                    check_payment_value = check_payment(tarjeta_selected, num_tarjeta_selected, cod_seguridad_selected, fecha_expiracion_selected, nombre_titular_selected)

                    if check_payment_value == 1:
                        st.error("Tarjeta no válida. El número de tarjeta debe tener 16 dígitos para Visa o MasterCard y 15 dígitos para American Express.")
                    elif check_payment_value == 2:
                        st.error("Tarjeta no válida. El código de seguridad debe tener 3 dígitos.")
                    elif check_payment_value == 3:
                        st.error("Tarjeta no válida. La fecha de expiración debe ser posterior a la fecha actual.")
                    elif check_payment_value == 4:
                        st.error("Tarjeta no válida. El nombre del titular debe tener al menos 3 caracteres.")
                    else:
                        info_cols = st.columns(2)
                        info_cols[0].subheader("Información de reserva")
                        with info_cols[0]:
                            st.write("Oficina de recogida: ", oficina_recogida)
                            st.write("Fecha de recogida: ", fecha_recogida)
                            st.write("Hora de recogida: ", hora_recogida)
                            st.write("Oficina de entrega: ", oficina_entrega)
                            st.write("Fecha de entrega: ", fecha_entrega)
                            st.write("Hora de entrega: ", hora_entrega)
                        info_cols[1].subheader("Información de vehículo")
                        with info_cols[1]:
                            st.write("Gama: ", car_gamma_selected)
                            st.write("Marca: ", car_brand_selected)
                            st.write("Modelo: ", car_model_selected)
                            st.write("Conducción: ", conducción_selected)
                            st.write("Número de puertas: ", num_puertas_selected)
                            st.write("Techo solar: ", solar_roof_selected)
                            st.write("Nombre del vehículo: ", car_selected)
                        info_cols = st.columns(2)
                        with info_cols[0]:  
                            st.subheader("Información de pago")
                            st.write("Tarjeta seleccionada: ", tarjeta_selected)
                            st.write("Número de tarjeta: ", num_tarjeta_selected)
                            st.write("Fecha de expiración: ", fecha_expiracion_selected)
                        
                        with info_cols[1]: 
                            st.subheader("Confirmación de pedido")
                            st.write("¿Está seguro de que desea confirmar la reserva?")
                            confirmar_pedido = st.button("Confirmar reserva")

                        if confirmar_pedido:
                            if len(reservas_df) != 0:
                                new_id =  reservas_df.index[-1] + 1
                            else:
                                new_id = 0
                            reservas_df.loc[len(reservas_df)] = [new_id, fecha_recogida,hora_recogida,fecha_entrega,hora_entrega,oficina_recogida, oficina_entrega,car_selected, client_type_selected, "Tarifa Test", descuento, "Ninguno", num_tarjeta_selected, nombre_titular_selected, 9999]
                            reservas_df.to_csv("reservas_db.csv", index=False)
                            st.success("Se ha confirmado la reserva.")
    else:
        st.markdown("#")
        st.markdown("#")
        st.markdown("#")
        st.markdown("#")
        st.markdown("#")
        st.markdown("#")

        st.title("Inicia Sesión para acceder a la aplicación")   