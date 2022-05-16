import datetime
import streamlit as st
import pandas as pd
from aux_func import *
import time

# ----------------------- LAYOUT ---------------------------
st.set_page_config(page_title="Alquiler de Coches")


# ----------------------- BACKEND ---------------------------
oficinas_df = pd.read_csv('oficinas_db.csv', index_col=0)
car_df = pd.read_csv('car_db.csv')
reservas_df = pd.read_csv('reservas_db.csv')
descuentos_df = pd.read_csv('descuentos_db.csv')

# ----------------------- Navigation ---------------------------
# Comprobamos si el usuario es administrador
is_admin = is_admin(st.session_state.get('user_id'))
if is_admin:
    page_list = ("Alquilar Coche", "Modificar datos de usuario", "Gestionar oficinas")
else:
    page_list = ("Alquilar Coche", "Modificar datos de usuario")
page = navigation(st, page_list)


    
# ----------------------- Multipage ---------------------------

# INICIO DE SESIÓN
if page == "Inicio de Sesión":
    placeholder = st.empty()

    with placeholder.container():
        st.header("Iniciar sesión")

        # Introducir datos
        usuario = st.text_input('Email o usuario')
        contraseña = st.text_input('Contraseña', type='password')

        # Botón de inicio de sesión
        if st.button('Iniciar sesión'):
            user_id = check_user_and_password(usuario, contraseña)
            if user_id == -1:
                st.error("Usuario o contraseña incorrectos")
            else:
                st.session_state['page'] = "Alquilar Coche"
                st.session_state['user_id'] = user_id
                st.success("Sesión iniciada correctamente. Ya puedes comenzar a alquilar un coche.")
                st.experimental_rerun()
        
        st.write("\n")
        st.write("\n")
        st.write("\n")


        st.subheader("¿No tienes cuenta?")
        # Botón de registro
        if st.button('Ir a registro'):
            st.session_state['page'] = "Registro usuario"
            st.experimental_rerun()

# REGISTRO DE USUARIO
elif page == "Registro usuario":
    placeholder = st.empty()

    with placeholder.container():
        st.header("Registrar usuario")

        email = st.text_input('Introduce tu email')
        usuario = st.text_input('Introduce tu usuario')
        contraseña = st.text_input('Contraseña', type='password')
        contraseña2 = st.text_input('Repite la contraseña', type='password')
        admin = st.checkbox('Soy administrador')
        code = "0"
        if admin:
            code = st.text_input('Introduce el código de administrador')
            
              
        if st.button('Registrar usuario'):
            if check_register_data(st,email, usuario, contraseña, contraseña2,admin,code):
                # Añadir en la base de datos
                state = add_user(usuario, contraseña, email, admin)

                if state == 0:
                    st.success("Registro completado correctamente. Ya puedes comenzar a alquilar un coche.")
                    time.sleep(2)
                    st.session_state['page'] = "Alquilar Coche"
                    st.experimental_rerun()
                else:
                    st.error("Error al registrar usuario.")

# MODIFICAR DATOS DE USUARIO
elif page == "Modificar datos de usuario":
    placeholder = st.empty()

    with placeholder.container():
        st.header("Modificar mis datos")

        old_email, old_usuario, old_contraseña = get_user_data(st.session_state['user_id'])

        email = st.text_input('Nuevo Email', old_email)
        usuario = st.text_input('Nuevo Usuario', old_usuario)
        contraseña = st.text_input('Nueva Contraseña', type='password')
        contraseña2 = st.text_input('Contraseña antigua', type='password')
              
        if st.button('Realizar cambios'):
            # Comprobamos que la contraseña el válida
            user_id = check_user_and_password(old_usuario, contraseña=contraseña2)
            if user_id == -1:
                st.error("Contraseña incorrecta")

            # Comprobamos que la información es válida
            elif check_register_data(st,email, usuario, contraseña, contraseña,False,"",drop=st.session_state['user_id']):
                # Cambiar en la base de datos
                state = edit_user(st,usuario, contraseña, email, st.session_state['user_id'])

                if state == 0:
                    st.success("Cambios completados con éxito.")

                else:
                    st.error("Error al cambiar datos de usuario.")
        
        st.write("\n")
        
        if st.button('Eliminar cuenta'):
                state = delete_user(st.session_state['user_id'])
                if state == 0:
                    time.sleep(2)
                    st.success("Cuenta eliminada correctamente.")
                    st.session_state.clear()
                    st.experimental_rerun()
                else:
                    st.error("Error al eliminar cuenta.")

elif page == "Gestionar oficinas":
    placeholder = st.empty()

    with placeholder.container():
        st.title("Gestión de oficinas")

        # Mostrar oficinas
        st.subheader("Oficinas")
        st.write(oficinas_df)

        # Añadir oficinas
        st.subheader("Añadir oficina")
        nombre = st.text_input('Nombre de la oficina')

        # Botón de añadir oficina
        if st.button('Añadir oficina'):
            state = add_office(nombre)
            if state == 0:
                st.success("Oficina añadida correctamente.")
                st.experimental_rerun()
            else:
                st.error("Error al añadir oficina.")

        # Eliminar oficina
        st.subheader("Eliminar oficina")
        oficina = st.selectbox('Selecciona la oficina a eliminar', oficinas_df.index)

        # Botón de eliminar oficina
        if st.button('Eliminar oficina'):
            state = delete_office(oficina)
            if state == 0:
                st.success("Oficina eliminada correctamente.")
                st.experimental_rerun()
            else:
                st.error("Error al eliminar oficina.")

        # Modificar oficina
        st.subheader("Modificar oficina")
        oficina = st.selectbox('Selecciona la oficina a modificar', oficinas_df.index)
        nombre = st.text_input('Nuevo nombre de la oficina', oficinas_df.loc[oficina, 'Nombre'])
        
        # Botón de modificar oficina
        if st.button('Modificar oficina'):
            state = edit_office(oficina, nombre)
            if state == 0:
                st.success("Oficina modificada correctamente.")
                st.experimental_rerun()
            else:
                st.error("Error al modificar oficina.")


elif page == "Reservas":
    placeholder = st.empty()

    with placeholder.container():
        st.title("Mis reservas")

        if st.button('Ir a alquiler de coches'):
                st.session_state['pageName'] = "Alquilar Coche"
                st.experimental_rerun()

        st.header("Gestionar reservas")

        client_ID = st.session_state.get('ID')
        reservas = reservas_df[reservas_df["Client_ID"] == client_ID]

        st.table(reservas.drop(['ID','Tipo Cliente','Tarifa','Num_Tarjeta','Titular','Client_ID','Descuento'], axis = 1))

elif page == "Reservas":
    placeholder = st.empty()

    with placeholder.container():
        st.title("Mis reservas")

        if st.button('Ir a alquiler de coches'):
                st.session_state['pageName'] = "Alquilar Coche"
                st.experimental_rerun()

        st.header("Gestionar reservas")

        client_ID = st.session_state.get('ID')
        reservas = reservas_df[reservas_df["Client_ID"] == client_ID]

        st.table(reservas.drop(['ID','Tipo Cliente','Tarifa','Num_Tarjeta','Titular','Client_ID','Descuento'], axis = 1))

        option = st.selectbox(
            'Selecciona la reserva que desees eliminar',
            (reservas["Coche"].to_list()))
        st.write('Confirma para eliminar:', option)

        if st.button('Confirmar'):
            reservas = reservas[reservas.Coche != option] 
            reservas.to_csv("reservas_db.csv", index=False)
            st.experimental_rerun()

elif page == "Alquilar Coche":
    placeholder = st.empty()
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
                #Seleccionar tarifa 
                st.subheader("Tarifas")
                tarifa = st.radio("Seleccione el tipo de tarifa que desea aplicar",('Por kilometraje', 'Por día', 'Semanal', 'De fin de semana','De larga duración'))

                st.subheader("Otros Datos")
                client_type_selected = st.radio("Tipo de cliente", ["Cliente regular", "Cliente de negocio"])
                descuento = 0
                if client_type_selected=='Cliente de negocio':
                    descuento_selected = st.text_input("Código de descuento", "000000")
                    #descuento_selected = descuento_selected.upper()
                    if descuento_selected != "000000":
                        if int(descuento_selected) in descuentos_df["descuento"].to_list():
                            descuento = descuentos_df[descuentos_df["descuento"] == int(descuento_selected)]["porcentaje"].to_list()[0]
                            st.success(f"Código de descuento válido. Dispone usted de un descuento del {descuento}%")
                        else:
                            st.error("El código de descuento introducido no es válido.")
                #Añadir extras (Wifi, GPS, silla de seguridad y cadenas de nieve).
                st.subheader("Extras")
                wifi = st.checkbox("Wifi (+ 30€)") 
                gps = st.checkbox("GPS (+ 15€)")
                silla = st.checkbox("Silla de seguridad (+ 20€)")
                cadenas = st.checkbox("Cadenas de nieve (+ 35€)")
                
                #Obtener el precio total
                coche_elegido = available_cars.loc[available_cars['Name'] == str(car_selected)]
                precio_base = coche_elegido['Precio_por_dia'].to_list()[0]
                precio = 0

                #Aplicar tarifa
                if tarifa == 'Por kilometraje':
                    st.markdown(f"El precio del vehículo seleccionado, con la tarifa de kilometraje es de {int(precio_base)*0.03}€ por kilometro.")
                    precio = int(precio_base)*0.03

                elif tarifa == 'Por día':
                    st.markdown(f"El precio del vehículo seleccionado, con la tarifa por día es de {int(precio_base)}€ por día.")
                    precio = int(precio_base)

                elif tarifa == 'Semanal':
                    st.markdown(f"El precio del vehículo seleccionado, con la tarifa semanal es de {int(precio_base)*6.3}€ por semana.")
                    precio = int(precio_base)*6.3

                elif tarifa == 'De fin de semana':
                    st.markdown(f"El precio del vehículo seleccionado, con la tarifa de fin de semana es de {int(precio_base)*1.8}€ por fin de semana.")
                    precio = int(precio_base)*1.8

                elif tarifa == 'De larga duración':
                    st.markdown(f"El precio del vehículo seleccionado, con la tarifa de larga duración es de {int(precio_base)*0.8}€ por día. Solo se puede aplicar esta tarifa para reservas superiores a 10 días")
                    precio = int(precio_base)*0.8

                st.subheader("Precio total teniendo en cuenta posibles extras")
                if(wifi):
                    precio+=30
                if(gps):
                    precio+=15
                if(silla):
                    precio+=20
                if(cadenas):
                    precio+=35
                
                st.header(f"{precio}€")
            
                # Info de pago
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