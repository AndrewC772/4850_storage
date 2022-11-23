import mysql.connector

db_conn = mysql.connector.connect(host="lab6a-andrew.switzerlandnorth.cloudapp.azure.com", user="network_api",
                                  password="network_api_password", database="network_api")

db_cursor = db_conn.cursor()

db_cursor.execute('''
        CREATE TABLE devices
        (id INTEGER NOT NULL AUTO_INCREMENT,
        device_id INTEGER, 
        device_name VARCHAR(250) NOT NULL,
        mac VARCHAR(50) NOT NULL,
        ip VARCHAR(50) NOT NULL,
        latency DOUBLE NOT NULL,
        network_id INTEGER,
        date_created VARCHAR(100) NOT NULL,
        last_update VARCHAR(100) NOT NULL,
        trace_id VARCHAR(50) NOT NULL,
        CONSTRAINT device_id_pk PRIMARY KEY (id))
    ''')

db_cursor.execute('''
        CREATE TABLE networks
        (id INTEGER NOT NULL AUTO_INCREMENT,
        network_id INTEGER NOT NULL,
        network_name VARCHAR(250) NOT NULL,
        network VARCHAR(50) NOT NULL,
        subnet_mask VARCHAR(50) NOT NULL,
        gateway VARCHAR(50),
        dns VARCHAR(50),
        device_count INTEGER,
        date_created VARCHAR(100) NOT NULL,
        trace_id VARCHAR(50) NOT NULL,
        CONSTRAINT device_id_pk PRIMARY KEY (id))
    ''')

db_conn.commit()
db_conn.close()
