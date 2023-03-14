import openpyxl
import getpass
import oracledb

connection = oracledb.connect(
    user='admin',
    password=')Distribucion4',
    dsn='isr4lxwoxgglenv2_low',
    config_dir='opt\OracleCloud\MYDB',
    wallet_location='opt\OracleCloud\MYDB',
    wallet_password=')Distribucion4'
)


class Logistics:
    def __init__(self):
        self.Lleno = False
        self.cortar = False

    def run(self):
        with connection.cursor() as cursor:
            for row in cursor.execute('select numero_orden, placas, estatus, zona_carga from virtual_queue'):
                if row[2] == 'A Zona de Espera':
                    orden = row[0]
                    placas = row[1]
                    assgnLD = row[3]
                    for row1 in cursor.execute('select estado from zona_de_carga'):
                        if row1[0] == 'Libre':
                            cursor.execute(f"update virtual_queue set estatus = 'En Zona De Carga' where numero_orden = '{orden}'")
                            connection.commit()
                            sql = "update zona_de_carga set estado=:1, orden_en_proceso=:2, placas=:3 where zona=:4"
                            row_carga = ('cargando', orden, placas, assgnLD)
                            cursor.execute(sql, row_carga)
                            connection.commit()
                            self.cortar = True 

                        else:
                            for row2 in cursor.execute('select zona_espera, estado from zona_de_espera'):
                                if row2[1] == 'Vacio':
                                    assgndWZ = row[0]
                                    cursor.execute(f"update virtual_queue set estatus = 'En Zona De Espera' where numero_orden = '{orden}'") 
                                    row_espera = ('En Espera', orden, placas, assgndWZ, assgnLD)
                                    cursor.execute('update zona_de_espera set estado=:1, orden=:2, placas=:3, zona_espera=:4 where zona_carga=:5', row_espera)
                                    connection.commit()
                                    self.cortar = True
                                    break
                            if self.cortar ==  True:
                                break
                elif row[2] == 'En Zona de Espera':
                    orden = row[0]
                    placas = row[1]
                    assgnLD = row[3]
                    for row in cursor.execute(f'select estado from zona_de_carga where zona={assgnLD}'):
                        if  row[0] == 'Libre':
                            cursor.execute(f"update virtual_queue set estatus = 'En Zona De Carga' where numero_orden = '{orden}'")
                            row_carga = ('cargando', orden, placas, assgnLD)
                            cursor.execute('update zona_de_carga set estado=:1, orden_en_proceso=:2, placas=:3,  where zona=:4', row_carga)
                            cursor.execute(f"update zona_de_espera set estado='Vacio', orden=NULL, placas=NULL, zona_carga=NULL where zona_espera={assgndWZ}")
                            connection.commit()
                            self.cortar = True
                            break
                if self.cortar ==  True:
                    self.cortar = False
                    break