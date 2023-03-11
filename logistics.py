import openpyxl

class Logistics:
    def __init__(self):
        self.Lleno = False
        self.cortar = False

    def run(self):
        wbordenes = openpyxl.load_workbook("DB_Clientes_NoOrden.xlsx")
        wsOrdenes = wbordenes['Ordenes']
        wbprocess = openpyxl.load_workbook("ProcessStatus.xlsx")
        wsLD1 = wbprocess['ZonaCarga1']
        wsLD2 = wbprocess['ZonaCarga2']
        wsLD3 = wbprocess['ZonaCarga3']
        wsLD4 = wbprocess['ZonaCarga4']
        wsLD5 = wbprocess['ZonaCarga5']
        wsLD6 = wbprocess['ZonaCarga6']
        LDwsList = [wsLD1, wsLD2, wsLD3, wsLD4, wsLD5, wsLD6]
        wsWZ = wbprocess['Espera']
        wsQueue = wbprocess['VirtualQueue']
        LD1status = wsLD1['B1'].value
        LD2status = wsLD2['B1'].value
        LD3status = wsLD3['B1'].value
        LD4status = wsLD4['B1'].value
        LD5status = wsLD5['B1'].value
        LD6status = wsLD6['B1'].value
        LDstatList = [LD1status, LD2status, LD3status, LD4status, LD5status, LD6status]
        WZ1status = wsWZ['B2'].value
        WZ2status = wsWZ['B3'].value
        WZ3status = wsWZ['B4'].value
        WZ4status = wsWZ['B5'].value
        WZ5status = wsWZ['B6'].value
        WZstatList = [WZ1status, WZ2status, WZ3status, WZ4status, WZ5status]
        for rowsQ in wsQueue.iter_rows(min_row=2, min_col=3, max_col=3, max_row=40):
            for cellQ in rowsQ:
                rwQ = cellQ.row
                if cellQ.value == "A Zona de Espera":
                    assgndLD = wsQueue.cell(row=rwQ, column=4).value
                    assgndLDl = assgndLD - 1
                    orden = wsQueue.cell(row=rwQ, column= 1).value
                    placas = wsQueue.cell(row=rwQ, column= 2).value
                    if LDstatList[assgndLDl] == "Libre":
                        cellQ.value = "En Zona de Carga"
                        LDwsList[assgndLDl]['B1'] = "Cargando"
                        LDwsList[assgndLDl]['B2'] = orden
                        LDwsList[assgndLDl]['B3'] = placas
                        wbprocess.save("ProcessStatus.xlsx")
                        self.cortar = True
                        break
                    else:
                        for i in WZstatList:
                            if i == "Vacio":
                                fila = WZstatList.index(i)+2
                                cellQ.value = "En Zona de Espera"
                                wsQueue.cell(row=rwQ, column=5, value=fila-1)
                                wsWZ["B"+str(fila)] = "En Espera"
                                wsWZ["C"+str(fila)] = orden
                                wsWZ["D"+str(fila)] = placas
                                wsWZ["E"+str(fila)] = assgndLD
                                wbprocess.save("ProcessStatus.xlsx")
                                self.cortar = True
                                break
                            # else:
                                #Este pedo esta lleno
                        if self.cortar == True:
                            break
                elif cellQ.value == "En Zona de Espera":
                    assgndLD = wsQueue.cell(row=rwQ, column=4).value
                    assgndLDl = assgndLD - 1
                    orden = wsQueue.cell(row=rwQ, column= 1).value
                    placas = wsQueue.cell(row=rwQ, column= 2).value
                    assdWZ = wsQueue.cell(row=rwQ, column= 5).value
                    if LDstatList[assgndLDl] == "Libre":
                        cellQ.value = "En Zona de Carga"
                        LDwsList[assgndLDl]['B1'] = "Cargando"
                        LDwsList[assgndLDl]['B2'] = orden
                        LDwsList[assgndLDl]['B3'] = placas
                        wsWZ.cell(row=assdWZ+1, column=2, value="Vacio")
                        wsWZ.cell(row=assdWZ+1, column=3, value="N/A")
                        wsWZ.cell(row=assdWZ+1, column=4, value="N/A")
                        wsWZ.cell(row=assdWZ+1, column=5, value="N/A")
                        wsWZ.cell(row=assdWZ+1, column=6, value="N/A")
                        wbprocess.save("ProcessStatus.xlsx")
                        self.cortar = True
                        break

            if self.cortar == True:
                self.cortar = False
                break

        wbordenes.close()
        wbprocess.close()