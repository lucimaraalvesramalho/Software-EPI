from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

db_config = {
    'host': 'localhost',
    'database': 'controle_epi',
    'user': 'root',
    'password': '1513'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

class epi:
    def __init__(self, nome_epi, tipo_epi, CA_epi, validade_certificado_epi):
        self.nome_epi = nome_epi
        self.tipo_epi = tipo_epi
        self.CA_epi = CA_epi
        self.validade_certificado_epi = validade_certificado_epi

class funcionario:
    def __init__(self, nome_funcionario, cpf_funcionario, setor_funcionario, funcao_funcionario, data_admissao_funcionario):
        self.nome_funcionario = nome_funcionario
        self.cpf_funcionario = cpf_funcionario
        self.setor_funcionario = setor_funcionario
        self.funcao_funcionario = funcao_funcionario
        self.data_admissao_funcionario = data_admissao_funcionario
    
class registros:
    def __init__(self, matricula_funcionario, ca_epi, data_entrega, data_devolucao, data_troca, motivo_devolucao):
        self.matricula_funcionario = matricula_funcionario
        self.ca_epi = ca_epi
        self.data_entrega = data_entrega
        self.data_devolucao = data_devolucao
        self.data_troca = data_troca
        self.motivo_devolucao = motivo_devolucao

@app.route('/epi', methods=['POST'])

def registrar_epi():
    dados = request.get_json()
    func = epi(dados['nome_epi'], dados['tipo_epi'], dados['CA_epi'], dados['validade_certificado_epi'])
    conn = get_db_connection()
    cursor = conn.cursor()

