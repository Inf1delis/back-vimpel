import pymongo
from sshtunnel import SSHTunnelForwarder

import variables

HOST = "151.248.115.245"
MONGO_DB = "vimpel38"
USER = "root"

server = 0
if variables.LOCAL:
    server = SSHTunnelForwarder(
        HOST,
        ssh_pkey="~/.ssh/id_rsa",
        ssh_private_key_password="secret",
        ssh_username=USER,
        remote_bind_address=('127.0.0.1', 27017)
    )

    server.start()
    client = pymongo.MongoClient('127.0.0.1', server.local_bind_port)  # server.local_bind_port is assigned local port
else:
    client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')

db = client[MONGO_DB]
