import cv2
import imutils
import pytesseract
import openpyxl
pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\\tesseract'

class plateDetection:
    def __init__(self):
        self.Adeltante = False
        self.pasar = False
        self.cap = cv2.VideoCapture(0)
        self.myimg = cv2.imread("Biblioteca\Empty.png")
    
    def run(self):
        ret, img = self.cap.read()
        cv2.imshow("Frame", img)
        # cv2.imshow("Frame", self.myimg)
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
            wb = openpyxl.load_workbook("DB_Clientes_Transportistas.xlsx")
            ws = wb["Placas"]
            clientNum = "No client with those plates"
            clientName = "No client with those plates"
            for rows in ws.iter_rows(min_row=1, min_col=3, max_col=3, max_row=40):
                for cell in rows:
                    if cell.value == platenw:
                        rw = cell.row
                        clientNum = ws.cell(row=rw, column = 1).value
                        clientName = ws.cell(row=rw, column = 2).value
            print("Client Number: ", clientNum)
            print("Client Name: ", clientName)
            

            # ### Revision de Ordenes ###
            clientOrd = "No orders Registered to that client"
            if clientNum != "No client with those plates":
                wborden = openpyxl.load_workbook("DB_Clientes_NoOrden.xlsx")
                wsorden = wborden["Ordenes"]
                for rowsOrd in wsorden.iter_rows(min_row=1, min_col=1, max_col=1, max_row=40):
                    for cellOrd in rowsOrd:
                        rw = cellOrd.row
                        ordStat = wsorden.cell(row=rw, column=4).value
                        if (cellOrd.value == clientNum) and (ordStat == "Pendiente"):
                            clientOrd = wsorden.cell(row=rw, column=3)
                            clientOrd = clientOrd.value
                            LDassigned = wsorden.cell(row=rw, column=5).value
                            wsorden.cell(row=rw, column=4, value="En proceso")
                            wborden.save("DB_Clientes_NoOrden.xlsx")
                            wborden.close()
                            self.Adeltante = True

            if (self.Adeltante == True) and (clientOrd != "No orders Registered to that client"):
                wbprocess = openpyxl.load_workbook("ProcessStatus.xlsx")
                wsprocess = wbprocess["VirtualQueue"]
                for rowsProc in wsprocess.iter_rows(min_row=2, min_col=1, max_col=1, max_row=40):
                    for cellProc in rowsProc:
                        rwProc = cellProc.row
                        if cellProc.value == None :
                            wsprocess.cell(row=rwProc, column=1, value=clientOrd)
                            wsprocess.cell(row=rwProc, column=2, value=platenw)
                            wsprocess.cell(row=rwProc, column=3, value="A Zona de Espera")
                            wsprocess.cell(row=rwProc, column=4, value=LDassigned)
                            wbprocess.save("ProcessStatus.xlsx")
                            wbprocess.close()
                            self.Adelante = False
                            self.pasar = True
                            break
                    if self.pasar == True:
                        self.pasar = False
                        break

            print("Clients order Number: ", clientOrd)