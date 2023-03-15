## Arduino Serial Communication
# Send and receive data via Serial Port

# Orlando Barajas
# Adán Márquez

## Arduino libraries
import serial
import time
import serial.tools.list_ports

## DB libraries
import keyboard
import oracledb

ports = serial.tools.list_ports.comports()

## Conection to Oracle Database
connection = oracledb.connect(
    user='admin',
    password=')Distribucion4',
    dsn='isr4lxwoxgglenv2_low',
    config_dir='opt\OracleCloud\MYDB',
    wallet_location='opt\OracleCloud\MYDB',
    wallet_password=')Distribucion4'
)

## Preparación para la conexión al Arduino

serialInst = serial.Serial()
serialInst.baudrate = 9600
serialInst.port = "COM4"

## Preparación de mensaje a LCD

letras = ["0", "e", "f", "g", "h", "i", "j"]

## Calibración de la báscula

print("Calibración de la báscula")
serialInst.open()
peso_arduino = serialInst.readline() # read Serial.print from arduino
peso_arduino = peso_arduino.decode()
peso_arduino = peso_arduino.rstrip()
print("El peso inicial es : ", peso_arduino, "\n")
# Cerrar conexión con el Arduino
# serialInst.close()
time.sleep(2)

## General while True 
while True:
    with connection.cursor() as cursor:
        for row in cursor.execute('select numero_orden, placas, estatus, zona_carga, peso_pedido, peso_final, peso_inicial from virtual_queue'):
            # Buscar si se tiene que pesar el camión 
            # pesaje inicial del mismo
            if row[2] == 'A Pesaje Inicial':
                # leer serial del Arduino para el valor del Peso 
                # inicial del camión
                print(row[0])
                orden = row[0]
                placas = row[1]
                zona_carga = row[3]
                print("Pesaje inicial del camión con placas :", placas, " y número de orden: ", orden, "\n")

                # Conexión al puerto Serial del Arduino
                # serialInst.open()
                print("Conexión al Arduino minus t-5 s")
                time.sleep(5)
                peso_arduino = serialInst.readline() # read Serial.print from arduino
                peso_arduino = peso_arduino.decode()
                peso_arduino = peso_arduino.rstrip()
                peso_arduino = str(peso_arduino)
                print("El peso inicial es : ", peso_arduino, "\n")
                time.sleep(2)
                # Cerrar conexión con el Arduino
                # serialInst.close()

                # Registrar en DB el peso_inicial
                # Cambiar Status a -> "A Zona De Espera"

                update_values = ('En Zona de Carga', peso_arduino, orden)

                print("Update a la base de datos del peso inicial")
                if (float(peso_arduino) > 40): 
                    with connection.cursor() as cursor:
                        cursor.execute(f"update virtual_queue set estatus = 'En Zona de Carga', peso_inicial = '{peso_arduino}' where numero_orden = '{orden}'") 
                # Commit de los datos a la Base de Dato
                        connection.commit()
                lcd_msg = letras[zona_carga]
                serialInst.write(lcd_msg.encode())
                time.sleep(5)

            # Buscar si se tiene que pesar el camión
            # pesaje final del mismo  
            elif row[2] == 'A Pesaje Final':
                orden = row[0]
                placas = row[1]
                peso_inicial = row[7] 
                print("Pesaje final del camión con placas :", placas, " y número de orden: ", orden, "\n")
                # Conexión al puerto Serial del Arduino
                # serialInst.open()
                print("Conexión al Arduino")
                time.sleep(5)
                peso_arduino = serialInst.readline() # read Serial.print from arduino
                peso_arduino = peso_arduino.decode()
                peso_arduino = peso_arduino.rstrip()
                peso_arduino = float(peso_arduino)
                print("El peso final es : ", peso_arduino, "\n")
                time.sleep(2)
                # Cerrar conexión con el Arduino
                # serialInst.close()

                # Registrar en DB el peso_inicial
                # Cambiar Status a -> "A Zona De Espera"

                print("Update de la base de datos para el peso final")
                with connection.cursor() as cursor:
                    cursor.execute(f"update virtual_queue set estatus = 'Salida', peso_final = {peso_arduino} where numero_orden = '{orden}'")
                # Commit de los datos a la Base de Datos
                    connection.commit()
                time.sleep(5)

                diff_peso = peso_arduino - peso_inicial
                print("El peso de la carga en el camión con num_orden: ", orden, " con placas: ", placas, " es: ", diff_peso)    

# #arduino = serial.Serial("COM5", 9600)
# clientName=""
# clientNum=""
# mensjeinicial=""
# serialInst=serial.Serial()
# serialInst.baudrate = 9600
# serialInst.port="COM4"
# serialInst.open()

# switch = 1
# Puerta = ""

# while switch == 1:
    
#     time.sleep(1)
#     #insertar codigo de diego que tiene procesamiento de foto con la tecla Esto nos debe dar placas y registro (1/0)
#     if (clientName!="No client with those plates"):
#         mensajeinicial="Adelante"
#     else:
#         mensajeinicial="Vehiculo no registrado"
#     print (mensajeinicial)
#     peso=""
#     time.sleep(2)
#     peso = serialInst.readline() #Esto nos va dar lo que este en el print del arduino, osea el peso
#     peso=peso.decode()
#     peso=peso.rstrip()
#     print(peso)
#     #serialInst.close()
#     #decodedpeso=str(peso[0:len(peso)].decode("utf-8")) #Poner esta linea solo si no nos da un int bonito


#     #Mandamos peso a base de datos

#     #Tomamos el dato de la puerta de SQL

#     #Mandamos la puerta al arduino
    
#     #serialInst.open()
#     Puerta = "f"
#     serialInst.write(str(Puerta).encode())
#     print("Ya envie el mensaje")
#     #serialInst.close()
#     time.sleep(5)