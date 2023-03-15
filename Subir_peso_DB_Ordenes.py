# ## Llenar base de datos de Ordenes

# # Uzziel Mesillas
# # Adán Márquez

# ## DB libraries
# import keyboard
# import oracledb

# ## Conection to Oracle Database
# connection = oracledb.connect(
#     user='admin',
#     password=')Distribucion4',
#     dsn='isr4lxwoxgglenv2_low',
#     config_dir='opt\OracleCloud\MYDB',
#     wallet_location='opt\OracleCloud\MYDB',
#     wallet_password=')Distribucion4'
# )

# ## Buscar datos de peso en Virtual Queue

# while True:
#     with connection.cursor() as cursor:
#         for row in cursor.execute('select numero_orden, peso_pedido, peso_final, peso_inicial from virtual_queue'):
            

# ## Llenar BD de ordenes
 