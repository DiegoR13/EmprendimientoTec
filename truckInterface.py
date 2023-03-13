from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import time
import threading
import openpyxl
from PIL import ImageTk, Image
from datetime import datetime
from logistics import Logistics
from platesDetection import plateDetection

class MainWindow(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.start()
        self.OrdersDone = 0
        self.OrdersPending = 0
        
    def callback(self):
        self.window.quit()  

    def cargaCompleta (self, ZC):
        self.OrdersDone += 1
        cortar = False
        wbprocess = openpyxl.load_workbook("ProcessStatus.xlsx")
        wsQ = wbprocess["VirtualQueue"]
        name = "ZonaCarga"+str(ZC)
        wsprocess = wbprocess[name]
        wsprocess['B1'] = "Libre"
        wsprocess['B2'] = "N/A"
        wsprocess['B3'] = "N/A"
        wsprocess['B4'] = "N/A"
        for rows in wsQ.iter_rows(min_row=2, max_row=40, min_col=3, max_col=3):
            for cell in rows:
                rw = cell.row
                assgLD = wsQ.cell(row=rw, column=4).value
                if (cell.value == "En Zona de Carga") and (assgLD == ZC):
                    orden = wsQ.cell(row=rw, column=1).value
                    wsQ.delete_rows(rw,1)
                    cortar = True
                    break
            if cortar == True:
                break
        wbprocess.save("ProcessStatus.xlsx")
        wbprocess.close()
        wbordenes = openpyxl.load_workbook("DB_Clientes_NoOrden.xlsx")
        wsordenes = wbordenes["Ordenes"]
        for rowsOr in wsordenes.iter_rows(min_row=2, max_row=40, min_col=3, max_col=3):
            for cellOr in rowsOr:
                rwOr = cellOr.row
                if cellOr.value == orden:
                    wsordenes.cell(row=rwOr, column=4, value="Completada")
                    wsordenes.cell(row=rwOr, column=5, value=None)
        wbordenes.save("DB_Clientes_NoOrden.xlsx")
        wbordenes.close()




    def warning(self):
        warnWin = messagebox.askokcancel(title="Program Stopped", message="The STOP button was pressed. Do you want to quit the program?", icon='warning')
        if warnWin:
            self.window.quit()

    def run(self):
        self.window = Tk()
        self.window.protocol("WM_DELETE_WINDOW", self.callback)
        width = self.window.winfo_screenwidth()
        height = self.window.winfo_screenheight()
        self.window.geometry("%dx%d" % (width, height))
        self.window.title("Truck GUI")
        self.window.configure(bg='#242529')
        self.window.iconbitmap('TruckFront.ico')
        
        self.frame1 = Frame(self.window)
        self.frame1.config(bg='#242529')
        self.frame1.pack(fill=X)
        self.frame2 = Frame(self.window)
        self.frame2.config(bg='#242529')
        self.frame2.pack(fill=X, padx = 70, pady = 20)
        self.frame3 = Frame(self.window)
        self.frame3.config(bg='#242529')
        self.frame3.pack(fill=X, padx = 100)
        self.frame4 = Frame(self.window)
        self.frame4.config(bg='#242529')
        self.frame4.pack(fill=X)

        self.frame1.columnconfigure(0, weight=1)
        self.frame1.columnconfigure(1, weight=1)
        self.frame1.columnconfigure(2, weight=1)

        self.frame2.rowconfigure(0, weight = 1)
        self.frame2.rowconfigure(1, weight = 2)
        self.frame2.rowconfigure(2, weight = 1)
        self.frame2.rowconfigure(3, weight = 1)
        self.frame2.rowconfigure(4, weight = 1)
        self.frame2.rowconfigure(5, weight = 1)
        self.frame2.rowconfigure(6, weight = 1)
        self.frame2.columnconfigure(0, weight = 1)
        self.frame2.columnconfigure(1, weight = 1)
        self.frame2.columnconfigure(2, weight = 1)
        self.frame2.columnconfigure(3, weight = 1)
        self.frame2.columnconfigure(4, weight = 1)
        self.frame2.columnconfigure(5, weight = 1)

        self.frame3.rowconfigure(0, weight = 1)
        self.frame3.rowconfigure(1, weight = 2)
        self.frame3.rowconfigure(2, weight = 1)
        self.frame3.rowconfigure(3, weight = 1)
        self.frame3.rowconfigure(4, weight = 1)
        self.frame3.rowconfigure(5, weight = 1)
        self.frame3.rowconfigure(6, weight = 1)

        self.frame3.columnconfigure(0, weight = 1)
        self.frame3.columnconfigure(1, weight = 1)
        self.frame3.columnconfigure(2, weight = 1)
        self.frame3.columnconfigure(3, weight = 1)
        self.frame3.columnconfigure(4, weight = 1)

        self.frame4.columnconfigure(0, weight = 1)
        self.frame4.columnconfigure(1, weight = 1)
        self.frame4.columnconfigure(2, weight = 1)

        Titulo = Label(self.frame1,text="CONTROL DE CARGA DE TRANSPORTE", font=("Verdana", 25, 'bold'), bg='#242529', fg='white')
        Titulo.grid(row=0, column=1, pady=15)

        Extra = Label(self.frame1, text="                    ", font=("Verdana", 20, 'bold'), bg='#242529', fg='white')
        Extra.grid(row=0, column=0)

        self.TxtTime = StringVar()
        self.TxtTime.set(datetime.now().strftime("%d/%m/%Y %H:%M"))
        self.TimeLbl = Label(self.frame1, textvariable=self.TxtTime, font=("Verdana", 13), bg='#242529', fg='white')
        self.TimeLbl.grid(row=0, column=2, sticky=E, padx=20)

        STLD1 = Label(self.frame2, text="Zona de Carga 1", font=("Verdana",13, 'bold'), bg='#242529', fg='white')
        STLD2 = Label(self.frame2, text="Zona de Carga 2", font=("Verdana",13, 'bold'), bg='#242529', fg='white')
        STLD3 = Label(self.frame2, text="Zona de Carga 3", font=("Verdana",13, 'bold'), bg='#242529', fg='white')
        STLD4 = Label(self.frame2, text="Zona de Carga 4", font=("Verdana",13, 'bold'), bg='#242529', fg='white')
        STLD5 = Label(self.frame2, text="Zona de Carga 5", font=("Verdana",13, 'bold'), bg='#242529', fg='white')
        STLD6 = Label(self.frame2, text="Zona de Carga 6", font=("Verdana",13, 'bold'), bg='#242529', fg='white')
        STLD1.grid(row=0, column=0)
        STLD2.grid(row=0, column=1)
        STLD3.grid(row=0, column=2)
        STLD4.grid(row=0, column=3)
        STLD5.grid(row=0, column=4)
        STLD6.grid(row=0, column=5)
        sep1_1 = ttk.Separator(self.frame2, orient='horizontal')
        sep1_2 = ttk.Separator(self.frame2, orient='horizontal')
        sep1_3 = ttk.Separator(self.frame2, orient='vertical')
        sep1_4 = ttk.Separator(self.frame2, orient='vertical')
        sep1_5 = ttk.Separator(self.frame2, orient='vertical')
        sep1_6 = ttk.Separator(self.frame2, orient='vertical')
        sep1_7 = ttk.Separator(self.frame2, orient='vertical')
        sep1_8 = ttk.Separator(self.frame2, orient='vertical')
        sep1_9 = ttk.Separator(self.frame2, orient='vertical')
        sep1_1.grid(column=0, row=0, columnspan=6, sticky=N+E+W)
        sep1_2.grid(column=0, row=6, columnspan=6, sticky=N+E+W)
        sep1_3.grid(row = 0, column = 0, rowspan = 6, sticky=N+S+W)
        sep1_4.grid(row = 0, column = 1, rowspan = 6, sticky=N+S+W)
        sep1_5.grid(row = 0, column = 2, rowspan = 6, sticky=N+S+W)
        sep1_6.grid(row = 0, column = 3, rowspan = 6, sticky=N+S+W)
        sep1_7.grid(row = 0, column = 4, rowspan = 6, sticky=N+S+W)
        sep1_8.grid(row = 0, column = 5, rowspan = 6, sticky=N+S+W)
        sep1_9.grid(row = 0, column = 6, rowspan = 6, sticky=N+S+W)

        STWZ1 = Label(self.frame3, text="Zona de Espera 1", font=("Verdana",13, 'bold'), bg='#242529', fg='white')
        STWZ2 = Label(self.frame3, text="Zona de Espera 2", font=("Verdana",13, 'bold'), bg='#242529', fg='white')
        STWZ3 = Label(self.frame3, text="Zona de Espera 3", font=("Verdana",13, 'bold'), bg='#242529', fg='white')
        STWZ4 = Label(self.frame3, text="Zona de Espera 4", font=("Verdana",13, 'bold'), bg='#242529', fg='white')
        STWZ5 = Label(self.frame3, text="Zona de Espera 5", font=("Verdana",13, 'bold'), bg='#242529', fg='white')
        STWZ1.grid(row=0, column=0)
        STWZ2.grid(row=0, column=1)
        STWZ3.grid(row=0, column=2)
        STWZ4.grid(row=0, column=3)
        STWZ5.grid(row=0, column=4)
        sep2_1 = ttk.Separator(self.frame3, orient='horizontal')
        sep2_2 = ttk.Separator(self.frame3, orient='horizontal')
        sep2_3 = ttk.Separator(self.frame3, orient='vertical')
        sep2_4 = ttk.Separator(self.frame3, orient='vertical')
        sep2_5 = ttk.Separator(self.frame3, orient='vertical')
        sep2_6 = ttk.Separator(self.frame3, orient='vertical')
        sep2_7 = ttk.Separator(self.frame3, orient='vertical')
        sep2_8 = ttk.Separator(self.frame3, orient='vertical')
        sep2_1.grid(column=0, row=0, columnspan=6, sticky=N+E+W)
        sep2_2.grid(column=0, row=7, columnspan=6, sticky=N+E+W)
        sep2_3.grid(row = 0, column = 0, rowspan = 7, sticky=N+S+W)
        sep2_4.grid(row = 0, column = 1, rowspan = 7, sticky=N+S+W)
        sep2_5.grid(row = 0, column = 2, rowspan = 7, sticky=N+S+W)
        sep2_6.grid(row = 0, column = 3, rowspan = 7, sticky=N+S+W)
        sep2_7.grid(row = 0, column = 4, rowspan = 7, sticky=N+S+W)
        sep2_8.grid(row = 0, column = 5, rowspan = 7, sticky=N+S+W)

        self.LZ1Free = Button(self.frame2, text="Carga Completa", font=("Verdana",13, 'bold'), borderwidth=4, bg='#f9e000', state='disabled', command=lambda: self.cargaCompleta(1))
        self.LZ2Free = Button(self.frame2, text="Carga Completa", font=("Verdana",13, 'bold'), borderwidth=4, bg='#f9e000', state='disabled', command=lambda: self.cargaCompleta(2))
        self.LZ3Free = Button(self.frame2, text="Carga Completa", font=("Verdana",13, 'bold'), borderwidth=4, bg='#f9e000', state='disabled', command=lambda: self.cargaCompleta(3))
        self.LZ4Free = Button(self.frame2, text="Carga Completa", font=("Verdana",13, 'bold'), borderwidth=4, bg='#f9e000', state='disabled', command=lambda: self.cargaCompleta(4))
        self.LZ5Free = Button(self.frame2, text="Carga Completa", font=("Verdana",13, 'bold'), borderwidth=4, bg='#f9e000', state='disabled', command=lambda: self.cargaCompleta(5))
        self.LZ6Free = Button(self.frame2, text="Carga Completa", font=("Verdana",13, 'bold'), borderwidth=4, bg='#f9e000', state='disabled', command=lambda: self.cargaCompleta(6))
        self.LZ1Free.grid(column=0, row=6, pady=10)
        self.LZ2Free.grid(column=1, row=6, pady=10)
        self.LZ3Free.grid(column=2, row=6, pady=10)
        self.LZ4Free.grid(column=3, row=6, pady=10)
        self.LZ5Free.grid(column=4, row=6, pady=10)
        self.LZ6Free.grid(column=5, row=6, pady=10)

        self.imgtruck = ImageTk.PhotoImage(Image.open("truck.png").resize((148,68)))
        self.imgempty = ImageTk.PhotoImage(Image.open("point.png").resize((148,68)))
        self.truck1LD = Label(self.frame2, image=self.imgempty, bg='#242529')
        self.truck2LD = Label(self.frame2, image=self.imgempty, bg='#242529')
        self.truck3LD = Label(self.frame2, image=self.imgempty, bg='#242529')
        self.truck4LD = Label(self.frame2, image=self.imgempty, bg='#242529')
        self.truck5LD = Label(self.frame2, image=self.imgempty, bg='#242529')
        self.truck6LD = Label(self.frame2, image=self.imgempty, bg='#242529')
        self.truck1LD.image = self.imgempty
        self.truck2LD.image = self.imgempty
        self.truck3LD.image = self.imgempty
        self.truck4LD.image = self.imgempty
        self.truck5LD.image = self.imgempty
        self.truck6LD.image = self.imgempty
        self.truck1LD.grid(column=0, row=1)
        self.truck2LD.grid(column=1, row=1)
        self.truck3LD.grid(column=2, row=1)
        self.truck4LD.grid(column=3, row=1)
        self.truck5LD.grid(column=4, row=1)
        self.truck6LD.grid(column=5, row=1)

        self.TextEstadoLD1 = StringVar()
        self.TextEstadoLD2 = StringVar()
        self.TextEstadoLD3 = StringVar()
        self.TextEstadoLD4 = StringVar()
        self.TextEstadoLD5 = StringVar()
        self.TextEstadoLD6 = StringVar()
        self.TextEstadoLD1.set("Estado: En Espera")
        self.TextEstadoLD2.set("Estado: En Espera")
        self.TextEstadoLD3.set("Estado: En Espera")
        self.TextEstadoLD4.set("Estado: En Espera")
        self.TextEstadoLD5.set("Estado: En Espera")
        self.TextEstadoLD6.set("Estado: En Espera")
        self.estadoLD1 = Label(self.frame2, textvariable=self.TextEstadoLD1, font=("Verdana",13), bg='#242529', fg='white')
        self.estadoLD2 = Label(self.frame2, textvariable=self.TextEstadoLD2, font=("Verdana",13), bg='#242529', fg='white')
        self.estadoLD3 = Label(self.frame2, textvariable=self.TextEstadoLD3, font=("Verdana",13), bg='#242529', fg='white')
        self.estadoLD4 = Label(self.frame2, textvariable=self.TextEstadoLD4, font=("Verdana",13), bg='#242529', fg='white')
        self.estadoLD5 = Label(self.frame2, textvariable=self.TextEstadoLD5, font=("Verdana",13), bg='#242529', fg='white')
        self.estadoLD6 = Label(self.frame2, textvariable=self.TextEstadoLD6, font=("Verdana",13), bg='#242529', fg='white')
        self.estadoLD1.grid(column=0, row=2, sticky=W, padx=5)
        self.estadoLD2.grid(column=1, row=2, sticky=W, padx=5)
        self.estadoLD3.grid(column=2, row=2, sticky=W, padx=5)
        self.estadoLD4.grid(column=3, row=2, sticky=W, padx=5)
        self.estadoLD5.grid(column=4, row=2, sticky=W, padx=5)
        self.estadoLD6.grid(column=5, row=2, sticky=W, padx=5)

        self.TextOrdenLD1 = StringVar()
        self.TextOrdenLD2 = StringVar()
        self.TextOrdenLD3 = StringVar()
        self.TextOrdenLD4 = StringVar()
        self.TextOrdenLD5 = StringVar()
        self.TextOrdenLD6 = StringVar()
        self.TextOrdenLD1.set("Orden: N/A")
        self.TextOrdenLD2.set("Orden: N/A")
        self.TextOrdenLD3.set("Orden: N/A")
        self.TextOrdenLD4.set("Orden: N/A")
        self.TextOrdenLD5.set("Orden: N/A")
        self.TextOrdenLD6.set("Orden: N/A")
        self.ordenLD1 = Label(self.frame2, textvariable=self.TextOrdenLD1, font=("Verdana",13), bg='#242529', fg='white')
        self.ordenLD2 = Label(self.frame2, textvariable=self.TextOrdenLD2, font=("Verdana",13), bg='#242529', fg='white')
        self.ordenLD4 = Label(self.frame2, textvariable=self.TextOrdenLD4, font=("Verdana",13), bg='#242529', fg='white')
        self.ordenLD3 = Label(self.frame2, textvariable=self.TextOrdenLD3, font=("Verdana",13), bg='#242529', fg='white')
        self.ordenLD5 = Label(self.frame2, textvariable=self.TextOrdenLD5, font=("Verdana",13), bg='#242529', fg='white')
        self.ordenLD6 = Label(self.frame2, textvariable=self.TextOrdenLD6, font=("Verdana",13), bg='#242529', fg='white')
        self.ordenLD1.grid(column=0, row=3, sticky=W, padx=5)
        self.ordenLD2.grid(column=1, row=3, sticky=W, padx=5)
        self.ordenLD3.grid(column=2, row=3, sticky=W, padx=5)
        self.ordenLD4.grid(column=3, row=3, sticky=W, padx=5)
        self.ordenLD5.grid(column=4, row=3, sticky=W, padx=5)
        self.ordenLD6.grid(column=5, row=3, sticky=W, padx=5)

        self.botOrdenLD1 = Button(self.frame2, text='*', font=("Verdana", 10, 'bold'), state='disabled')
        self.botOrdenLD2 = Button(self.frame2, text='*', font=("Verdana", 10, 'bold'), state='disabled')
        self.botOrdenLD3 = Button(self.frame2, text='*', font=("Verdana", 10, 'bold'), state='disabled')
        self.botOrdenLD4 = Button(self.frame2, text='*', font=("Verdana", 10, 'bold'), state='disabled')
        self.botOrdenLD5 = Button(self.frame2, text='*', font=("Verdana", 10, 'bold'), state='disabled')
        self.botOrdenLD6 = Button(self.frame2, text='*', font=("Verdana", 10, 'bold'), state='disabled')
        self.botOrdenLD1.grid(column=0, row=3, sticky=E, padx=5, pady=5)
        self.botOrdenLD2.grid(column=1, row=3, sticky=E, padx=5, pady=5)
        self.botOrdenLD3.grid(column=2, row=3, sticky=E, padx=5, pady=5)
        self.botOrdenLD4.grid(column=3, row=3, sticky=E, padx=5, pady=5)
        self.botOrdenLD5.grid(column=4, row=3, sticky=E, padx=5, pady=5)
        self.botOrdenLD6.grid(column=5, row=3, sticky=E, padx=5, pady=5)

        self.TextPlacasLD1 = StringVar()
        self.TextPlacasLD2 = StringVar()
        self.TextPlacasLD3 = StringVar()
        self.TextPlacasLD4 = StringVar()
        self.TextPlacasLD5 = StringVar()
        self.TextPlacasLD6 = StringVar()
        self.TextPlacasLD1.set("Placas: N/A")
        self.TextPlacasLD2.set("Placas: N/A")
        self.TextPlacasLD3.set("Placas: N/A")
        self.TextPlacasLD4.set("Placas: N/A")
        self.TextPlacasLD5.set("Placas: N/A")
        self.TextPlacasLD6.set("Placas: N/A")
        self.placasLD1 = Label(self.frame2, textvariable=self.TextPlacasLD1, font=("Verdana",13), bg='#242529', fg='white')
        self.placasLD2 = Label(self.frame2, textvariable=self.TextPlacasLD2, font=("Verdana",13), bg='#242529', fg='white')
        self.placasLD3 = Label(self.frame2, textvariable=self.TextPlacasLD3, font=("Verdana",13), bg='#242529', fg='white')
        self.placasLD4 = Label(self.frame2, textvariable=self.TextPlacasLD4, font=("Verdana",13), bg='#242529', fg='white')
        self.placasLD5 = Label(self.frame2, textvariable=self.TextPlacasLD5, font=("Verdana",13), bg='#242529', fg='white')
        self.placasLD6 = Label(self.frame2, textvariable=self.TextPlacasLD6, font=("Verdana",13), bg='#242529', fg='white')
        self.placasLD1.grid(column=0, row=4, sticky=W, padx=5)
        self.placasLD2.grid(column=1, row=4, sticky=W, padx=5)
        self.placasLD3.grid(column=2, row=4, sticky=W, padx=5)
        self.placasLD4.grid(column=3, row=4, sticky=W, padx=5)
        self.placasLD5.grid(column=4, row=4, sticky=W, padx=5)
        self.placasLD6.grid(column=5, row=4, sticky=W, padx=5)

        self.TextTiempoLD1 = StringVar()
        self.TextTiempoLD2 = StringVar()
        self.TextTiempoLD3 = StringVar()
        self.TextTiempoLD4 = StringVar()
        self.TextTiempoLD5 = StringVar()
        self.TextTiempoLD6 = StringVar()
        self.TextTiempoLD1.set("Tiempo Restante: N/A")
        self.TextTiempoLD2.set("Tiempo Restante: N/A")
        self.TextTiempoLD3.set("Tiempo Restante: N/A")
        self.TextTiempoLD4.set("Tiempo Restante: N/A")
        self.TextTiempoLD5.set("Tiempo Restante: N/A")
        self.TextTiempoLD6.set("Tiempo Restante: N/A")
        self.tiempoLD1 = Label(self.frame2, textvariable=self.TextTiempoLD1, font=("Verdana",13), bg='#242529', fg='white')
        self.tiempoLD2 = Label(self.frame2, textvariable=self.TextTiempoLD2, font=("Verdana",13), bg='#242529', fg='white')
        self.tiempoLD3 = Label(self.frame2, textvariable=self.TextTiempoLD3, font=("Verdana",13), bg='#242529', fg='white')
        self.tiempoLD4 = Label(self.frame2, textvariable=self.TextTiempoLD4, font=("Verdana",13), bg='#242529', fg='white')
        self.tiempoLD5 = Label(self.frame2, textvariable=self.TextTiempoLD5, font=("Verdana",13), bg='#242529', fg='white')
        self.tiempoLD6 = Label(self.frame2, textvariable=self.TextTiempoLD6, font=("Verdana",13), bg='#242529', fg='white')
        self.tiempoLD1.grid(column=0, row=5, sticky=W, padx=5)
        self.tiempoLD2.grid(column=1, row=5, sticky=W, padx=5)
        self.tiempoLD3.grid(column=2, row=5, sticky=W, padx=5)
        self.tiempoLD4.grid(column=3, row=5, sticky=W, padx=5)
        self.tiempoLD5.grid(column=4, row=5, sticky=W, padx=5)
        self.tiempoLD6.grid(column=5, row=5, sticky=W, padx=5)

        self.truck1WZ = Label(self.frame3, image=self.imgempty, bg='#242529')
        self.truck2WZ = Label(self.frame3, image=self.imgempty, bg='#242529')
        self.truck3WZ = Label(self.frame3, image=self.imgempty, bg='#242529')
        self.truck4WZ = Label(self.frame3, image=self.imgempty, bg='#242529')
        self.truck5WZ = Label(self.frame3, image=self.imgempty, bg='#242529')
        self.truck1WZ.image = self.imgempty
        self.truck2WZ.image = self.imgempty
        self.truck3WZ.image = self.imgempty
        self.truck4WZ.image = self.imgempty
        self.truck5WZ.image = self.imgempty
        self.truck1WZ.grid(column=0, row=1)
        self.truck2WZ.grid(column=1, row=1)
        self.truck3WZ.grid(column=2, row=1)
        self.truck4WZ.grid(column=3, row=1)
        self.truck5WZ.grid(column=4, row=1)

        self.TextEstadoWZ1 = StringVar()
        self.TextEstadoWZ2 = StringVar()
        self.TextEstadoWZ3 = StringVar()
        self.TextEstadoWZ4 = StringVar()
        self.TextEstadoWZ5 = StringVar()
        self.TextEstadoWZ1.set("Estado: Vacio")
        self.TextEstadoWZ2.set("Estado: Vacio")
        self.TextEstadoWZ3.set("Estado: Vacio")
        self.TextEstadoWZ4.set("Estado: Vacio")
        self.TextEstadoWZ5.set("Estado: Vacio")
        self.estadoWZ1 = Label(self.frame3, textvariable=self.TextEstadoWZ1, font=("Verdana",13), bg='#242529', fg='white')
        self.estadoWZ2 = Label(self.frame3, textvariable=self.TextEstadoWZ2, font=("Verdana",13), bg='#242529', fg='white')
        self.estadoWZ3 = Label(self.frame3, textvariable=self.TextEstadoWZ3, font=("Verdana",13), bg='#242529', fg='white')
        self.estadoWZ4 = Label(self.frame3, textvariable=self.TextEstadoWZ4, font=("Verdana",13), bg='#242529', fg='white')
        self.estadoWZ5 = Label(self.frame3, textvariable=self.TextEstadoWZ5, font=("Verdana",13), bg='#242529', fg='white')
        self.estadoWZ1.grid(column=0, row=2, sticky=W, padx=5)
        self.estadoWZ2.grid(column=1, row=2, sticky=W, padx=5)
        self.estadoWZ3.grid(column=2, row=2, sticky=W, padx=5)
        self.estadoWZ4.grid(column=3, row=2, sticky=W, padx=5)
        self.estadoWZ5.grid(column=4, row=2, sticky=W, padx=5)

        self.TextOrdenWZ1 = StringVar()
        self.TextOrdenWZ2 = StringVar()
        self.TextOrdenWZ3 = StringVar()
        self.TextOrdenWZ4 = StringVar()
        self.TextOrdenWZ5 = StringVar()
        self.TextOrdenWZ1.set("Orden: N/A")
        self.TextOrdenWZ2.set("Orden: N/A")
        self.TextOrdenWZ3.set("Orden: N/A")
        self.TextOrdenWZ4.set("Orden: N/A")
        self.TextOrdenWZ5.set("Orden: N/A")
        self.ordenWZ1 = Label(self.frame3, textvariable=self.TextOrdenWZ1, font=("Verdana",13), bg='#242529', fg='white')
        self.ordenWZ2 = Label(self.frame3, textvariable=self.TextOrdenWZ2, font=("Verdana",13), bg='#242529', fg='white')
        self.ordenWZ3 = Label(self.frame3, textvariable=self.TextOrdenWZ3, font=("Verdana",13), bg='#242529', fg='white')
        self.ordenWZ4 = Label(self.frame3, textvariable=self.TextOrdenWZ4, font=("Verdana",13), bg='#242529', fg='white')
        self.ordenWZ5 = Label(self.frame3, textvariable=self.TextOrdenWZ5, font=("Verdana",13), bg='#242529', fg='white')
        self.ordenWZ1.grid(column=0, row=3, sticky=W, padx=5)
        self.ordenWZ2.grid(column=1, row=3, sticky=W, padx=5)
        self.ordenWZ3.grid(column=2, row=3, sticky=W, padx=5)
        self.ordenWZ4.grid(column=3, row=3, sticky=W, padx=5)
        self.ordenWZ5.grid(column=4, row=3, sticky=W, padx=5)

        self.TextPlacasWZ1 = StringVar()
        self.TextPlacasWZ2 = StringVar()
        self.TextPlacasWZ3 = StringVar()
        self.TextPlacasWZ4 = StringVar()
        self.TextPlacasWZ5 = StringVar()
        self.TextPlacasWZ1.set("Placas: N/A")
        self.TextPlacasWZ2.set("Placas: N/A")
        self.TextPlacasWZ3.set("Placas: N/A")
        self.TextPlacasWZ4.set("Placas: N/A")
        self.TextPlacasWZ5.set("Placas: N/A")
        self.placasWZ1 = Label(self.frame3, textvariable=self.TextPlacasWZ1, font=("Verdana",13), bg='#242529', fg='white')
        self.placasWZ2 = Label(self.frame3, textvariable=self.TextPlacasWZ2, font=("Verdana",13), bg='#242529', fg='white')
        self.placasWZ3 = Label(self.frame3, textvariable=self.TextPlacasWZ3, font=("Verdana",13), bg='#242529', fg='white')
        self.placasWZ4 = Label(self.frame3, textvariable=self.TextPlacasWZ4, font=("Verdana",13), bg='#242529', fg='white')
        self.placasWZ5 = Label(self.frame3, textvariable=self.TextPlacasWZ5, font=("Verdana",13), bg='#242529', fg='white')
        self.placasWZ1.grid(column=0, row=4, sticky=W, padx=5)
        self.placasWZ2.grid(column=1, row=4, sticky=W, padx=5)
        self.placasWZ3.grid(column=2, row=4, sticky=W, padx=5)
        self.placasWZ4.grid(column=3, row=4, sticky=W, padx=5)
        self.placasWZ5.grid(column=4, row=4, sticky=W, padx=5)

        self.TextSiguienteWZ1 = StringVar()
        self.TextSiguienteWZ2 = StringVar()
        self.TextSiguienteWZ3 = StringVar()
        self.TextSiguienteWZ4 = StringVar()
        self.TextSiguienteWZ5 = StringVar()
        self.TextSiguienteWZ1.set("A Zona de Carga: N/A")
        self.TextSiguienteWZ2.set("A Zona de Carga: N/A")
        self.TextSiguienteWZ3.set("A Zona de Carga: N/A")
        self.TextSiguienteWZ4.set("A Zona de Carga: N/A")
        self.TextSiguienteWZ5.set("A Zona de Carga: N/A")
        self.siguienteWZ1 = Label(self.frame3, textvariable=self.TextSiguienteWZ1, font=("Verdana",13), bg='#242529', fg='white')
        self.siguienteWZ2 = Label(self.frame3, textvariable=self.TextSiguienteWZ2, font=("Verdana",13), bg='#242529', fg='white')
        self.siguienteWZ3 = Label(self.frame3, textvariable=self.TextSiguienteWZ3, font=("Verdana",13), bg='#242529', fg='white')
        self.siguienteWZ4 = Label(self.frame3, textvariable=self.TextSiguienteWZ4, font=("Verdana",13), bg='#242529', fg='white')
        self.siguienteWZ5 = Label(self.frame3, textvariable=self.TextSiguienteWZ5, font=("Verdana",13), bg='#242529', fg='white')
        self.siguienteWZ1.grid(column=0, row=5, sticky=W, padx=5)
        self.siguienteWZ2.grid(column=1, row=5, sticky=W, padx=5)
        self.siguienteWZ3.grid(column=2, row=5, sticky=W, padx=5)
        self.siguienteWZ4.grid(column=3, row=5, sticky=W, padx=5)
        self.siguienteWZ5.grid(column=4, row=5, sticky=W, padx=5)
        
        self.TextTiempoWZ1 = StringVar()
        self.TextTiempoWZ2 = StringVar()
        self.TextTiempoWZ3 = StringVar()
        self.TextTiempoWZ4 = StringVar()
        self.TextTiempoWZ5 = StringVar()
        self.TextTiempoWZ1.set("Tiempo de espera: N/A")
        self.TextTiempoWZ2.set("Tiempo de espera: N/A")
        self.TextTiempoWZ3.set("Tiempo de espera: N/A")
        self.TextTiempoWZ4.set("Tiempo de espera: N/A")
        self.TextTiempoWZ5.set("Tiempo de espera: N/A")
        self.tiempoWZ1 = Label(self.frame3, textvariable=self.TextTiempoWZ1, font=("Verdana",13), bg='#242529', fg='white')
        self.tiempoWZ2 = Label(self.frame3, textvariable=self.TextTiempoWZ2, font=("Verdana",13), bg='#242529', fg='white')
        self.tiempoWZ3 = Label(self.frame3, textvariable=self.TextTiempoWZ3, font=("Verdana",13), bg='#242529', fg='white')
        self.tiempoWZ4 = Label(self.frame3, textvariable=self.TextTiempoWZ4, font=("Verdana",13), bg='#242529', fg='white')
        self.tiempoWZ5 = Label(self.frame3, textvariable=self.TextTiempoWZ5, font=("Verdana",13), bg='#242529', fg='white')
        self.tiempoWZ1.grid(column=0, row=6, sticky=W, padx=5)
        self.tiempoWZ2.grid(column=1, row=6, sticky=W, padx=5)
        self.tiempoWZ3.grid(column=2, row=6, sticky=W, padx=5)
        self.tiempoWZ4.grid(column=3, row=6, sticky=W, padx=5)
        self.tiempoWZ5.grid(column=4, row=6, sticky=W, padx=5)

        imgstop = ImageTk.PhotoImage(Image.open("StopImg.png").resize((130,130)))
        botonStop = Button(self.frame4, image=imgstop, bg='#242529', borderwidth=0, command=self.warning)
        botonStop.grid(column=0, pady=30, padx=80, sticky=W)

        self.TextOrdsPen = StringVar()
        self.TextOrdsPen.set("Ordenes Pendientes: 0")
        self.OrdsPen = Label(self.frame4, textvariable=self.TextOrdsPen, font=("Verdana",15), bg='#242529', fg='white')
        self.OrdsPen.grid(row=0, column=1)
        self.TextOrdsDesp = StringVar()
        self.TextOrdsDesp.set("Ordenes Despachadas: 0")
        self.OrdsDesp = Label(self.frame4, textvariable=self.TextOrdsDesp, font=("Verdana",15), bg='#242529', fg='white')
        self.OrdsDesp.grid(row=0, column=2)

        self.window.mainloop()


    def update(self):
        now = datetime.now()
        mytime = now.strftime("%d/%m/%Y %H:%M")
        self.TxtTime.set(mytime)

        wbprocess = openpyxl.load_workbook("ProcessStatus.xlsx")
        wsLD1 = wbprocess['ZonaCarga1']
        wsLD2 = wbprocess['ZonaCarga2']
        wsLD3 = wbprocess['ZonaCarga3']
        wsLD4 = wbprocess['ZonaCarga4']
        wsLD5 = wbprocess['ZonaCarga5']
        wsLD6 = wbprocess['ZonaCarga6']
        wsWZ = wbprocess['Espera']

        if wsLD1['B1'].value == "Cargando":
            self.truck1LD.configure(image=self.imgtruck)
            self.LZ1Free["state"] = 'normal'
        else:
            self.truck1LD.configure(image=self.imgempty)
            self.LZ1Free["state"] = 'disabled'
        if wsLD2['B1'].value == "Cargando":
            self.truck2LD.configure(image=self.imgtruck)
            self.LZ2Free["state"] = 'normal'
        else:
            self.truck2LD.configure(image=self.imgempty)
            self.LZ2Free["state"] = 'disabled'
        if wsLD3['B1'].value == "Cargando":
            self.truck3LD.configure(image=self.imgtruck)
            self.LZ3Free["state"] = 'normal'
        else:
            self.truck3LD.configure(image=self.imgempty)
            self.LZ3Free["state"] = 'disabled'
        if wsLD4['B1'].value == "Cargando":
            self.truck4LD.configure(image=self.imgtruck)
            self.LZ4Free["state"] = 'normal'
        else:
            self.truck4LD.configure(image=self.imgempty)
            self.LZ4Free["state"] = 'disabled'
        if wsLD5['B1'].value == "Cargando":
            self.truck5LD.configure(image=self.imgtruck)
            self.LZ5Free["state"] = 'normal'
        else:
            self.truck5LD.configure(image=self.imgempty)
            self.LZ5Free["state"] = 'disabled'
        if wsLD6['B1'].value == "Cargando":
            self.truck6LD.configure(image=self.imgtruck)
            self.LZ6Free["state"] = 'normal'
        else:
            self.truck6LD.configure(image=self.imgempty)
            self.LZ6Free["state"] = 'disabled'

        self.TextEstadoLD1.set("Estado: " + wsLD1['B1'].value)
        self.TextEstadoLD2.set("Estado: " + wsLD2['B1'].value)
        self.TextEstadoLD3.set("Estado: " + wsLD3['B1'].value)
        self.TextEstadoLD4.set("Estado: " + wsLD4['B1'].value)
        self.TextEstadoLD5.set("Estado: " + wsLD5['B1'].value)
        self.TextEstadoLD6.set("Estado: " + wsLD6['B1'].value)
        self.TextOrdenLD1.set("Orden: " + wsLD1['B2'].value)
        self.TextOrdenLD2.set("Orden: " + wsLD2['B2'].value)
        self.TextOrdenLD3.set("Orden: " + wsLD3['B2'].value)
        self.TextOrdenLD4.set("Orden: " + wsLD4['B2'].value)
        self.TextOrdenLD5.set("Orden: " + wsLD5['B2'].value)
        self.TextOrdenLD6.set("Orden: " + wsLD6['B2'].value)
        self.TextPlacasLD1.set("Placas: " + wsLD1['B3'].value)
        self.TextPlacasLD2.set("Placas: " + wsLD2['B3'].value)
        self.TextPlacasLD3.set("Placas: " + wsLD3['B3'].value)
        self.TextPlacasLD4.set("Placas: " + wsLD4['B3'].value)
        self.TextPlacasLD5.set("Placas: " + wsLD5['B3'].value)
        self.TextPlacasLD6.set("Placas: " + wsLD6['B3'].value)
        self.TextTiempoLD1.set("Tiempo Restante: "+ wsLD1['B4'].value)
        self.TextTiempoLD2.set("Tiempo Restante: "+ wsLD2['B4'].value)
        self.TextTiempoLD3.set("Tiempo Restante: "+ wsLD3['B4'].value)
        self.TextTiempoLD4.set("Tiempo Restante: "+ wsLD4['B4'].value)
        self.TextTiempoLD5.set("Tiempo Restante: "+ wsLD5['B4'].value)
        self.TextTiempoLD6.set("Tiempo Restante: "+ wsLD6['B4'].value)

        if wsLD1['B2'].value != "N/A":
            self.botOrdenLD1["state"] = 'normal'
        else:
            self.botOrdenLD1["state"] = 'disabled'
        if wsLD2['B2'].value != "N/A":
            self.botOrdenLD2["state"] = 'normal'
        else:
            self.botOrdenLD2["state"] = 'disabled'
        if wsLD3['B2'].value != "N/A":
            self.botOrdenLD3["state"] = 'normal'
        else:
            self.botOrdenLD3["state"] = 'disabled'
        if wsLD4['B2'].value != "N/A":
            self.botOrdenLD4["state"] = 'normal'
        else:
            self.botOrdenLD4["state"] = 'disabled'
        if wsLD5['B2'].value != "N/A":
            self.botOrdenLD5["state"] = 'normal'
        else:
            self.botOrdenLD5["state"] = 'disabled'
        if wsLD6['B2'].value != "N/A":
            self.botOrdenLD6["state"] = 'normal'
        else:
            self.botOrdenLD6["state"] = 'disabled'

        if wsWZ['B2'].value == "En Espera":
            self.truck1WZ.configure(image=self.imgtruck)
        else:
            self.truck1WZ.configure(image=self.imgempty)
        if wsWZ['B3'].value == "En Espera":
            self.truck2WZ.configure(image=self.imgtruck)
        else:
            self.truck2WZ.configure(image=self.imgempty)
        if wsWZ['B4'].value == "En Espera":
            self.truck3WZ.configure(image=self.imgtruck)
        else:
            self.truck3WZ.configure(image=self.imgempty)
        if wsWZ['B5'].value == "En Espera":
            self.truck4WZ.configure(image=self.imgtruck)
        else:
            self.truck4WZ.configure(image=self.imgempty)
        if wsWZ['B6'].value == "En Espera":
            self.truck5WZ.configure(image=self.imgtruck)
        else:
            self.truck5WZ.configure(image=self.imgempty)

        self.TextEstadoWZ1.set("Estado: " + wsWZ['B2'].value)
        self.TextEstadoWZ2.set("Estado: " + wsWZ['B3'].value)
        self.TextEstadoWZ3.set("Estado: " + wsWZ['B4'].value)
        self.TextEstadoWZ4.set("Estado: " + wsWZ['B5'].value)
        self.TextEstadoWZ5.set("Estado: " + wsWZ['B6'].value)
        self.TextOrdenWZ1.set("Orden: " + wsWZ['C2'].value)
        self.TextOrdenWZ2.set("Orden: " + wsWZ['C3'].value)
        self.TextOrdenWZ3.set("Orden: " + wsWZ['C4'].value)
        self.TextOrdenWZ4.set("Orden: " + wsWZ['C5'].value)
        self.TextOrdenWZ5.set("Orden: " + wsWZ['C6'].value)
        self.TextPlacasWZ1.set("Placas: " + wsWZ['D2'].value)
        self.TextPlacasWZ2.set("Placas: " + wsWZ['D3'].value)
        self.TextPlacasWZ3.set("Placas: " + wsWZ['D4'].value)
        self.TextPlacasWZ4.set("Placas: " + wsWZ['D5'].value)
        self.TextPlacasWZ5.set("Placas: " + wsWZ['D6'].value)
        self.TextSiguienteWZ1.set("A Zona de Carga: "+ str(wsWZ['E2'].value))
        self.TextSiguienteWZ2.set("A Zona de Carga: "+ str(wsWZ['E3'].value))
        self.TextSiguienteWZ3.set("A Zona de Carga: "+ str(wsWZ['E4'].value))
        self.TextSiguienteWZ4.set("A Zona de Carga: "+ str(wsWZ['E5'].value))
        self.TextSiguienteWZ5.set("A Zona de Carga: "+ str(wsWZ['E6'].value))
        self.TextTiempoWZ1.set("Tiempo Restante: "+ wsWZ['F2'].value)
        self.TextTiempoWZ2.set("Tiempo Restante: "+ wsWZ['F3'].value)
        self.TextTiempoWZ3.set("Tiempo Restante: "+ wsWZ['F4'].value)
        self.TextTiempoWZ4.set("Tiempo Restante: "+ wsWZ['F5'].value)
        self.TextTiempoWZ5.set("Tiempo Restante: "+ wsWZ['F6'].value)
        
        wbprocess.close()

        self.OrdersPending = 0
        wbordenes = openpyxl.load_workbook("DB_Clientes_NoOrden.xlsx")
        wsordenes = wbordenes["Ordenes"]
        for rows in wsordenes.iter_rows(min_row=2, max_row=40, min_col=4, max_col=4):
            for cell in rows:
                if (cell.value != "Completada") and (cell.value != None):
                    self.OrdersPending += 1

        self.TextOrdsPen.set("Ordenes Pendientes: "+str(self.OrdersPending))
        self.TextOrdsDesp.set("Ordenes Despachadas: "+str(self.OrdersDone))
        wbordenes.close()

MW = MainWindow()
time.sleep(1)
while True:
    try:
        if MW.window.winfo_exists():
            MW.update()
            Logistics().run()
            plateDetection().run()
    except: 
        MW.callback()
        exit()