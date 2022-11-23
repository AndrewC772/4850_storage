import sqlite3

conn = sqlite3.connect('network_device_api.sqlite')

c = conn.cursor()
c.execute('''
          CREATE TABLE devices
          (id INTEGER PRIMARY KEY ASC,
           device_id INTEGER, 
           device_name VARCHAR(250) NOT NULL,
           mac VARCHAR(50) NOT NULL,
           ip VARCHAR(50) NOT NULL,
           latency REAL NOT NULL,
           network_id INTEGER,
           date_created VARCHAR(100) NOT NULL,
           last_update VARCHAR(100) NOT NULL,
           trace_id VARCHAR(50) NOT NULL)
          ''')

c.execute('''
          CREATE TABLE networks
          (id INTEGER PRIMARY KEY ASC,
           network_id INTEGER, 
           network_name VARCHAR(250) NOT NULL,
           network VARCHAR(50) NOT NULL,
           subnet_mask VARCHAR(50) NOT NULL,
           gateway VARCHAR(50),
           dns VARCHAR(50),
           device_count INTEGER,
           date_created VARCHAR(100) NOT NULL,
           trace_id VARCHAR(50) NOT NULL)
          ''')

conn.commit()
conn.close()
