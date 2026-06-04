from flask import Blueprint, render_template, request, jsonify
from models.tables import funcionario, epis, registros
from database import get_db_connection

# Blueprint para agrupar rotas da API
api_routes = Blueprint('api_routes', __name__)


# ============ CREATE ============
# Definição das rotas para cadastro de funcionários, EPIs e registros


@api_routes.route('/api/funcionario', methods=['POST'])
def cadastrar_funcionario():
    dados = request.get_json(silent=True)
    if not dados:
        dados = request.form.to_dict()

    func = funcionario(
        dados['matricula_funcionario'],
        dados['nome_funcionario'],
        dados['cpf_funcionario'],
        dados['setor_funcionario'],
        dados['funcao_funcionario'],
        dados['data_admissao_funcionario']
    )

    conn = get_db_connection()
    cursor = conn.cursor()

    sql = "INSERT INTO funcionarios (matricula_funcionario, nome_funcionario, cpf_funcionario, setor_funcionario, funcao_funcionario, data_admissao_funcionario) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, (func.matricula_funcionario, func.nome_funcionario, func.cpf_funcionario, func.setor_funcionario, func.funcao_funcionario, func.data_admissao_funcionario))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'message': 'Funcionário cadastrado com sucesso'}), 201


@api_routes.route('/api/epi', methods=['POST'])
def cadastrar_epi():
    dados = request.get_json()
    epi = epis(dados['nome_epi'], dados['tipo_epi'], dados['CA_epi'], dados['validade_certificado_epi'])

    conn = get_db_connection()
    cursor = conn.cursor()

    sql = "INSERT INTO epis (nome_epi, tipo_epi, CA_epi, validade_certificado_epi) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (epi.nome_epi, epi.tipo_epi, epi.CA_epi, epi.validade_certificado_epi))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'message': 'EPI cadastrado com sucesso'}), 201


@api_routes.route('/api/registro', methods=['POST'])
def cadastrar_registro():
    dados = request.get_json()
    registro = registros(dados['matricula_funcionario'], dados['ca_epi'], dados['data_entrega'], dados['data_devolucao'], dados['data_troca'], dados['motivo_devolucao'])

    conn = get_db_connection()
    cursor = conn.cursor()

    sql = "INSERT INTO registros (matricula_funcionario, ca_epi, data_entrega, data_devolucao, data_troca, motivo_devolucao) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, (registro.matricula_funcionario, registro.ca_epi, registro.data_entrega, registro.data_devolucao, registro.data_troca, registro.motivo_devolucao))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'message': 'Registro cadastrado com sucesso'}), 201


# ============ UPDATE ============
# Rotas para atualização de funcionários, EPIs e registros


@api_routes.route('/api/funcionario/<matricula>', methods=['PUT'])
def atualizar_funcionario(matricula):
    dados = request.get_json()

    conn = get_db_connection()
    cursor = conn.cursor()

    sql = """UPDATE funcionarios 
             SET nome_funcionario = %s, cpf_funcionario = %s, setor_funcionario = %s, 
                 funcao_funcionario = %s, data_admissao_funcionario = %s 
             WHERE matricula_funcionario = %s"""
    cursor.execute(sql, (dados['nome_funcionario'], dados['cpf_funcionario'], dados['setor_funcionario'], dados['funcao_funcionario'], dados['data_admissao_funcionario'], matricula))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'message': 'Funcionário atualizado com sucesso'}), 200


@api_routes.route('/api/epi/<ca_epi>', methods=['PUT'])
def atualizar_epi(ca_epi):
    dados = request.get_json()

    conn = get_db_connection()
    cursor = conn.cursor()

    sql = """UPDATE epis 
             SET nome_epi = %s, tipo_epi = %s, validade_certificado_epi = %s 
             WHERE CA_epi = %s"""
    cursor.execute(sql, (dados['nome_epi'], dados['tipo_epi'], dados['validade_certificado_epi'], ca_epi))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'message': 'EPI atualizado com sucesso'}), 200


@api_routes.route('/api/registro/<matricula>/<ca_epi>', methods=['PUT'])
def atualizar_registro(matricula, ca_epi):
    dados = request.get_json()

    conn = get_db_connection()
    cursor = conn.cursor()

    sql = """UPDATE registros 
             SET data_entrega = %s, data_devolucao = %s, data_troca = %s, motivo_devolucao = %s 
             WHERE matricula_funcionario = %s AND ca_epi = %s"""
    cursor.execute(sql, (dados['data_entrega'], dados['data_devolucao'], dados['data_troca'], dados['motivo_devolucao'], matricula, ca_epi))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'message': 'Registro atualizado com sucesso'}), 200


# ============ DELETE ============
# Rotas para deletar funcionários, epi's e registros


@api_routes.route('/api/funcionario/<matricula>', methods=['DELETE'])
def deletar_funcionario(matricula):
    conn = get_db_connection()
    cursor = conn.cursor()

    sql = "DELETE FROM funcionarios WHERE matricula_funcionario = %s"
    cursor.execute(sql, (matricula,))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'message': 'Funcionário deletado com sucesso'}), 200


@api_routes.route('/api/epi/<ca_epi>', methods=['DELETE'])
def deletar_epi(ca_epi):
    conn = get_db_connection()
    cursor = conn.cursor()

    sql = "DELETE FROM epis WHERE CA_epi = %s"
    cursor.execute(sql, (ca_epi,))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'message': 'EPI deletado com sucesso'}), 200


@api_routes.route('/api/registro/<matricula>/<ca_epi>', methods=['DELETE'])
def deletar_registro(matricula, ca_epi):
    conn = get_db_connection()
    cursor = conn.cursor()

    sql = "DELETE FROM registros WHERE matricula_funcionario = %s AND ca_epi = %s"
    cursor.execute(sql, (matricula, ca_epi))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'message': 'Registro deletado com sucesso'}), 200


# HTML ROUTES - Rotas para renderizar as páginas HTML
@api_routes.route('/index')
def index():
    return render_template('index.html')

@api_routes.route('/cadastro-funcionario')
def cadastro_funcionario():
    return render_template('cadastrar-funcionario.html')

@api_routes.route('/cadastro-epi')
def cadastro_epi():
    return render_template('cadastrar-epi.html')

@api_routes.route('/criar-registro')
def criar_registro():
    return render_template('criar-registro.html')   

@api_routes.route('/atualizar-registro')
def atualizar_registros():
    return render_template('atualizar-registros.html')

@api_routes.route('/atualizar-cadastros')
def atualizar_cadastros():
    return render_template('atualizar-cadastros.html')