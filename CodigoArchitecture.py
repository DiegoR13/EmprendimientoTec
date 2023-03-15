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
gate_numbers = [101, 102, 103, 104, 105, 106]

## Calibración de la báscula

print("Calibración de la báscula")
serialInst.open()
peso_arduino = serialInst.readline() # read Serial.print from arduino
peso_arduino = peso_arduino.decode()
peso_arduino = peso_arduino.rstrip()
print("Peso de calibración : ", peso_arduino, "\n")
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

                if (float(peso_arduino) > 40): 
                    #check if the Serial msg is still the gate number
                    if (peso_arduino in gate_numbers):
                        print("Redo weight measurement")
                        continue
                    else:
                        ## Submit values to DB 
                        with connection.cursor() as cursor:
                            print("Update a la base de datos del peso inicial")
                            cursor.execute(f"update virtual_queue set estatus = 'En Zona de Carga', peso_inicial = '{peso_arduino}' where numero_orden = '{orden}'")
                            cursor.execute(f"update ordenes set peso_inicial = '{peso_arduino}' where numero_orden = '{orden}'") 
                            # Commit de los datos a la Base de Dato
                            connection.commit()

                # Mandar número de puerta la Arduino
                # Display en la pantalla LCD
                lcd_msg = letras[zona_carga]
                serialInst.write(lcd_msg.encode())
                time.sleep(5)

            # Buscar si se tiene que pesar el camión
            # pesaje final del mismo  
            elif row[2] == 'A Pesaje Final':
                orden = row[0]
                placas = row[1]
                peso_pedido_db = row[4]
                peso_inicial = row[6] 
        
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

                peso_pedido = float(peso_arduino) - float(peso_inicial)
                print("El peso de la carga en el camión con num_orden: ", orden, " con placas: ", placas, " es: ", peso_pedido, "\n")    
                if (peso_pedido >= peso_pedido_db * 0.95 and peso_pedido <= peso_pedido_db * 1.05):
                    print("La entrega cargada es correcta")
                else:
                    print("Warning ! Peso incorrecto")

                if (peso_arduino in gate_numbers):
                        print("Redo weight measurement")
                        continue
                else:
                    with connection.cursor() as cursor:
                        print("Update de la base de datos para el peso final \n")
                        cursor.execute(f"update virtual_queue set estatus = 'Salida', peso_final = {peso_arduino} where numero_orden = '{orden}'")
                        cursor.execute(f"update ordenes set peso_final = '{peso_arduino}' where numero_orden = '{orden}'")
                        # Commit de los datos a la Base de Datos
                        connection.commit()
                time.sleep(5)