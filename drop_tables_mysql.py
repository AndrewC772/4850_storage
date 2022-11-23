import mysql.connector

db_conn = mysql.connector.connect(host="lab6a-andrew.switzerlandnorth.cloudapp.azure.com", user="network_api",
                                  password="network_api_password", database="network_api")

db_cursor = db_conn.cursor()

db_cursor.execute('''
        DROP TABLE devices
    ''')

db_cursor.execute('''
        DROP TABLE networks
    ''')

db_conn.commit()
db_conn.close()
