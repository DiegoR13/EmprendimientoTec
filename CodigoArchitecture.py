import serial
import time
import serial.tools.list_ports

ports=serial.tools.list_ports.comports()


#arduino = serial.Serial("COM5", 9600)
clientName=""
clientNum=""
mensjeinicial=""
serialInst=serial.Serial()
serialInst.baudrate = 9600
serialInst.port="COM6"
serialInst.open()


switch=1
Puerta=""

while switch==1:
    
    time.sleep(1)
    #insertar codigo de diego que tiene procesamiento de foto con la tecla Esto nos debe dar placas y registro (1/0)
    if (clientName!="No client with those plates"):
        mensajeinicial="Adelante"
    else:
        mensajeinicial="Vehiculo no registrado"
    print (mensajeinicial)
    peso=""
    time.sleep(2)
    peso = serialInst.readline() #Esto nos va dar lo que este en el print del arduino, osea el peso
    peso=peso.decode()
    peso=peso.rstrip()
    print(peso)
    #serialInst.close()
    #decodedpeso=str(peso[0:len(peso)].decode("utf-8")) #Poner esta linea solo si no nos da un int bonito


    #Mandamos peso a base de datos

    #Tomamos el dato de la puerta de SQL

    #Mandamos la puerta al arduino
    
    #serialInst.open()
    Puerta="f"
    serialInst.write(Puerta.encode('utf-8'))
    print("Ya envie el mensaje")
    #serialInst.close()
    time.sleep(2)