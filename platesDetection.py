import cv2
import imutils
import pytesseract
import openpyxl
import getpass
import oracledb

#Input credentials and wallet documents to access de db
connection = oracledb.connect(
    user='admin',
    password=')Distribucion4',
    dsn='isr4lxwoxgglenv2_low',
    config_dir='opt\OracleCloud\MYDB',
    wallet_location='opt\OracleCloud\MYDB',
    wallet_password=')Distribucion4'
)

pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\\tesseract'
Adelante = False
pasar = False
cap = cv2.VideoCapture(0)

while True:
    ret, img = cap.read()
    if ret == False:
        break
    else:
        cv2.imshow("Frame", img)
        if cv2.waitKey(1) & 0xFF == ord('s'):
            pic = img
            pic = imutils.resize(pic, width=300)
            gray_image = cv2.cvtColor(pic, cv2.COLOR_BGR2GRAY)
            smoothened = cv2.bilateralFilter(gray_image, 11, 17, 17)
            edged = cv2.Canny(smoothened, 30,200)
            cnts,new = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            image1=pic.copy()
            cv2.drawContours(image1,cnts,-1,(0,255,0),3)
            cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:30]
            screenCnt = None
            image2 = pic.copy()
            cv2.drawContours(image2,cnts,-1,(0,255,0),3)
            for c in cnts:
                perimeter = cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, 0.018 * perimeter, True)
                if len(approx) == 4:
                    screenCnt = approx
                    x,y,w,h = cv2.boundingRect(c)
                    new_img = pic[y:y+h,x:x+w]
                    h2,w2,c2 = new_img.shape
                    cropped_img = new_img[int(30*h2/100):int((70*h2/100)), int(8*w2/100):int((93*w2/100))]
                    break
            plate = pytesseract.image_to_string(cropped_img, config='--psm 7')
            platenw = plate.strip()
            print("Number plate is:", platenw)


            ### Revision en base de datos de placas ###
            clientNum = "No client with those plates"
            clientName = "No client with those plates"

            # Connect to the db and query our 3 client columns as an array called "row"
            with connection.cursor() as cursor:
                for row in cursor.execute('select numero_cliente, nombre_cliente, placas from clientes'):
                    if row[2] == platenw:
                        clientNum = row[0]
                        clientName = row[1]
            print("Client Number: ", clientNum)
            print("Client Name: ", clientName)
            

            ### Revision de Ordenes ###
            clientOrd = "No orders Registered to that client"
            if clientNum != 'No client with those plates':

                # Query orders and assign values to variable for costumer
                with connection.cursor() as cursor:
                    for row in cursor.execute('select numero_cliente, nombre_cliente, numero_orden, estatus_orden, zona_carga from ordenes'):
                        if (row[0] == clientNum) and (row[3] == 'Pendiente'):
                            clientOrd = row[2]
                            LDassigned = row[4]
                            with connection.cursor() as cursor:
                                cursor.execute(f"update ordenes set estatus_orden = 'En proceso' where numero_orden = '{row[2]}'")
                            Adelante = True

            ### Comentado para evitar sobreescribir. Si es necesario para el funcionamiento ###
            # print(Adelante, clientOrd)
            if (Adelante == True) and (clientOrd != "No orders Registered to that client"):
                # Add order data to virtual queue
                ## Check how to implement the first in first out functionality (it might already be implemented  tho)
                with connection.cursor() as cursor:
                        rows = [(clientOrd, platenw, 'A Zona de Espera', LDassigned)]
                        cursor.executemany('insert into virtual_queue (numero_orden, placas, estatus, zona_carga) values(:1, :2, :3, :4)', rows)
                connection.commit()
                print('commmited changes')
                Adelante = False

            print("Clients order Number: ", clientOrd)

        elif cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            break