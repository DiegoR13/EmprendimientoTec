
import oracledb


## Conection to Oracle Database
connection = oracledb.connect(
    user='admin',
    password=')Distribucion4',
    dsn='isr4lxwoxgglenv2_low',
    config_dir='opt\OracleCloud\MYDB',
    wallet_location='opt\OracleCloud\MYDB',
    wallet_password=')Distribucion4'
)

with connection.cursor() as cursor:
    for row in cursor.execute('select numero_orden, placas, estatus, zona_carga, zona_espera, peso_pedido, peso_final, peso_inicial from virtual_queue'):
                #print("Estado actual :", row[2])
                # Buscar si se tiene que pesar el camión 
                # pesaje inicial del mismo
                if row[2] == 'A Pesaje Inicial':
                    # leer serial del Arduino para el valor del Peso 
                    # inicial del camión
                    print(row[0])
                    orden = row[0]
                    placas = row[1]
                    print("Pesaje inicial del camión con placas :", placas, " y número de orden: ", orden, "\n")

                    # Conexión al puerto Serial del Arduino
                        
                    cursor.execute(f"update virtual_queue set estatus = 'En Zona de Carga', peso_inicial = '44.44' where numero_orden = '{orden}'") 
                    # Commit de los datos a la Base de Dato
                    connection.commit()
                    print('after commit')
                else:
                    break
                    