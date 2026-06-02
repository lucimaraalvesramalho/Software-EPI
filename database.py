import mysql.connector

# configurações de conexão com o banco de dados
db_config = {
    'host': 'localhost',
    'database': 'controle_epi',
    'user': 'root',
    'password': '1513'
}


def get_db_connection():
    return mysql.connector.connect(**db_config)
