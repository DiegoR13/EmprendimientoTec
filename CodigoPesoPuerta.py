import serial
import time
import serial.tools.list_ports

ports=serial.tools.list_ports.comports()

peso=0
#estado=""

numo=""
puerta=0

#arduino = serial.Serial("COM5", 9600)
while True:
    estado=input("Ingrese estado: ")
    serialInst=serial.Serial()
    serialInst.baudrate = 9600
    serialInst.port="COM6"
    serialInst.open()
    if estado=="a pesaje inicial":
        peso=""
        time.sleep(3)
        peso = serialInst.readline() #Esto nos va dar lo que este en el print del arduino, osea el peso
        peso=peso.decode()
        pesoinicial=peso.rstrip()
        print(pesoinicial)
        #serialInst.close()
        #serialInst.open()

    puerta = "1" #Conectar el codigo de diego aqui para que nos de la puerta
    puertadisp="e"
    #poner el codigo que haga adan aqui con la variable puertadisp
    serialInst.write(puertadisp.encode('utf-8'))
    print("Ya envie el mensaje")
    #serialInst.close()
    time.sleep(2)
    estado=""




