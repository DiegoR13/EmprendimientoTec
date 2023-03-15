import sys
import keyboard
import oracledb

connection = oracledb.connect(
    user='admin',
    password=')Distribucion4',
    dsn='isr4lxwoxgglenv2_low',
    config_dir='opt\OracleCloud\MYDB',
    wallet_location='opt\OracleCloud\MYDB',
    wallet_password=')Distribucion4'
)

cortar = False

while True:
    try:
        if keyboard.is_pressed('q'):
            break
        with connection.cursor() as cursor:
            for row in cursor.execute('select numero_orden, placas, estatus, zona_carga, zona_espera from virtual_queue'):
                if row[2] == 'A Zona de Espera':
                    orden = row[0]
                    placas = row[1]
                    assgnLD = str(row[3])
                    with connection.cursor() as cursor:
                        estado_carga = cursor.execute(f'select estado from zona_de_carga where zona = {assgnLD}')
                    # for row1 in cursor.execute('select estado from zona_de_carga'):
                    if estado_carga == 'Libre':
                        with connection.cursor() as cursor:
                            cursor.execute(f"update virtual_queue set estatus = 'En Zona De Carga' where numero_orden = '{orden}'")
                            connection.commit()
                            sql = "update zona_de_carga set estado=:1, orden_en_proceso=:2, placas=:3 where zona=:4"
                            row_carga = ('Cargando', orden, placas, assgnLD)
                            cursor.execute(sql, row_carga)
                            connection.commit()
                        cortar = True 

                    else:
                        print('to waiting zone')
                        with connection.cursor() as cursor:
                            for row2 in cursor.execute('select zona_espera, estado from zona_de_espera'):
                                if row2[1] == 'Vacio':
                                    assgndWZ = row2[0]
                                    cursor.execute(f"update virtual_queue set estatus = 'En Zona De Espera', zona_espera = {row2[0]} where numero_orden = '{orden}'") 
                                    row_espera = ('En Espera', orden, placas, assgnLD, assgndWZ)
                                    cursor.execute('update zona_de_espera set estado=:1, orden=:2, placas=:3, zona_carga=:4 where zona_espera=:5', row_espera)
                                    connection.commit()
                                    cortar = True
                                    break
                            if cortar ==  True:
                                break
                elif row[2] == 'En Zona De Espera':
                    orden = row[0]
                    placas = row[1]
                    assgnLD = row[3]
                    assgndWZ = row[4]
                    with connection.cursor() as cursor:
                        for row in cursor.execute(f'select estado from zona_de_carga where zona={assgnLD}'):
                            if  row[0] == 'Libre':
                                cursor.execute(f"update virtual_queue set estatus = 'En Zona De Carga' where numero_orden = '{orden}'")
                                row_carga = ('Cargando', orden, placas, assgnLD)
                                cursor.execute('update zona_de_carga set estado=:1, orden_en_proceso=:2, placas=:3 where zona=:4', row_carga)
                                cursor.execute(f"update zona_de_espera set estado='Vacio', orden=NULL, placas=NULL, zona_carga=NULL where zona_espera={assgndWZ}")
                                connection.commit()
                                cortar = True
                                break
                        if cortar ==  True:
                            cortar = False
                            break
    except:
        pass   