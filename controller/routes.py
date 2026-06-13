from flask import Blueprint, render_template, request, jsonify
from models.tables import funcionario, epi, registros
from database import get_db_connection
from datetime import datetime, timedelta

# Blueprint para agrupar rotas da API
api_routes = Blueprint('api_routes', __name__)


# ============ CREATE ============
# Definição das rotas para cadastro de funcionários, EPIs e registros


@api_routes.route('/api/funcionario', methods=['POST'])
def cadastrar_funcionario():
    conn = None
    cursor = None
    try:
        dados = request.get_json(silent=True)
        if not dados:
            dados = request.form.to_dict()

        func = funcionario(
            dados['matricula_funcionario'],
            dados['nome_funcionario'],
            dados['cpf_funcionario'],
            dados['setor_funcionario'],
            dados['funcao_funcionario'],
            dados['data_admissao_funcionario'],
            dados['telefone'],
            dados['email'],
            dados['whatsapp']
        )

        conn = get_db_connection()
        cursor = conn.cursor()

        sql = "INSERT INTO funcionarios (matricula_funcionario, nome_funcionario, cpf_funcionario, setor_funcionario, funcao_funcionario, data_admissao_funcionario, telefone, email, whatsapp) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (func.matricula_funcionario, func.nome_funcionario, func.cpf_funcionario, func.setor_funcionario, func.funcao_funcionario, func.data_admissao_funcionario, func.telefone, func.email, func.whatsapp))

        conn.commit()

        return jsonify({'message': 'Funcionário cadastrado com sucesso'}), 201
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()

@api_routes.route('/api/epi', methods=['POST'])
def cadastrar_epi():
    conn = None
    cursor = None
    try:
        dados = request.get_json()
        novo_epi = epi(
            dados['nome_epi'],
            dados['tipo_epi'], 
            dados['certificado_aprovacao_epi'], 
            dados['validade_certificado_aprovacao'])

        conn = get_db_connection()
        cursor = conn.cursor()

        sql = "INSERT INTO epi (nome_epi, tipo_epi, certificado_aprovacao_epi, validade_certificado_aprovacao) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (novo_epi.nome_epi, novo_epi.tipo_epi, novo_epi.certificado_aprovacao_epi, novo_epi.validade_certificado_aprovacao))

        conn.commit()
        return jsonify({'message': 'EPI cadastrado com sucesso'}), 201
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@api_routes.route('/api/registro', methods=['POST'])
def cadastrar_registro():
    conn = None
    cursor = None
    try:
        dados = request.get_json()
        registro = registros(
            dados['matricula_funcionario'], 
            dados['ca_EPI'],
            None,
            dados['data_devolucao'], 
            dados.get('data_troca'),
            dados.get('motivo_devolucao')
        )

        conn = get_db_connection()
        cursor = conn.cursor()

        sql = "INSERT INTO registros (matricula_funcionario, ca_EPI, data_devolucao, data_troca, motivo_devolucao) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (registro.matricula_funcionario, registro.ca_EPI, registro.data_devolucao, registro.data_troca, registro.motivo_devolucao))

        conn.commit()
        return jsonify({'message': 'Registro cadastrado com sucesso'}), 201
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# ============ GET ============
# Rotas para obter informações de funcionários, EPIs e registros

@api_routes.route('/api/funcionario/', methods=['GET'])
def buscar_funcionario():
    matricula = request.args.get("matricula")
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        if matricula:
            cursor.execute(
                "SELECT * FROM funcionarios WHERE matricula_funcionario = %s", (matricula,)
            )
            resultado = cursor.fetchone()

        else:
            cursor.execute(
                "SELECT * FROM funcionarios"
            )
            resultado = cursor.fetchall()
        
        conn.commit()
        for funcionario in resultado if isinstance(resultado, list) else [resultado]:
            funcionario['data_admissao_funcionario'] = funcionario['data_admissao_funcionario'].strftime('%Y-%m-%d') if funcionario['data_admissao_funcionario'] else None
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@api_routes.route('/api/epi/', methods=['GET'])
def buscar_epi():
    ca = request.args.get("ca")
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        if ca:
            cursor.execute(
                "SELECT * FROM epi WHERE certificado_aprovacao_epi = %s", (ca,)
            )
            resultado = cursor.fetchone()
        
        else:
            cursor.execute(
                "SELECT * FROM epi"
            )
            resultado = cursor.fetchall()

        conn.commit()

        for epi in resultado:
            epi['validade_certificado_aprovacao'] = epi['validade_certificado_aprovacao'].strftime('%Y-%m-%d') if epi['validade_certificado_aprovacao'] else None

        return jsonify(resultado)
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@api_routes.route('/api/registro/', methods=['GET'])
def buscar_registro():
    matricula = request.args.get("matricula")
    ca = request.args.get("ca")
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        if matricula:
            cursor.execute(
                "SELECT * FROM registros WHERE matricula_funcionario = %s", (matricula,)
            )
            resultado = cursor.fetchall()
        elif ca:
            cursor.execute(
                "SELECT * FROM registros WHERE ca_EPI = %s", (ca,)
            )
            resultado = cursor.fetchall()
        else:
            cursor.execute(
                "SELECT * FROM registros"
            )
            resultado = cursor.fetchall()

        conn.commit()
        for registro in resultado:
            registro['data_entrega'] = registro['data_entrega'].strftime('%Y-%m-%d') if registro['data_entrega'] else None
            registro['data_devolucao'] = registro['data_devolucao'].strftime('%Y-%m-%d') if registro['data_devolucao'] else None
            registro['data_troca'] = registro['data_troca'].strftime('%Y-%m-%d') if registro['data_troca'] else None 
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# ============ UPDATE ============
# Rotas para atualização de funcionários, EPIs e registros


@api_routes.route('/api/funcionario/<matricula>', methods=['PUT'])
def atualizar_funcionario(matricula):
    conn = None
    cursor = None
    try:
        dados = request.get_json()

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM funcionarios WHERE matricula_funcionario = %s",
            (matricula,)
        )

        funcionario_atual = cursor.fetchone()

        sql = """UPDATE funcionarios 
                 SET nome_funcionario = %s, cpf_funcionario = %s, setor_funcionario = %s, 
                     funcao_funcionario = %s, data_admissao_funcionario = %s 
                 WHERE matricula_funcionario = %s"""
        cursor.execute(sql, (dados.get('nome_funcionario', funcionario_atual[1]), dados.get('cpf_funcionario', funcionario_atual[2]), dados.get('setor_funcionario', funcionario_atual[3]), dados.get('funcao_funcionario', funcionario_atual[4]), dados.get('data_admissao_funcionario', funcionario_atual[5]), matricula))

        conn.commit()
        return jsonify({'message': 'Funcionário atualizado com sucesso'}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@api_routes.route('/api/epi/<ca_epi>', methods=['PUT'])
def atualizar_epi(ca_epi):
    conn = None
    cursor = None
    try:
        dados = request.get_json()

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM epi WHERE certificado_aprovacao_epi = %s",
            (ca_epi,)
        )
        epi_atual = cursor.fetchone()

        sql = """UPDATE epi 
                 SET nome_epi = %s, tipo_epi = %s, validade_certificado_aprovacao = %s 
                 WHERE certificado_aprovacao_epi = %s"""
        cursor.execute(sql, (dados.get('nome_epi', epi_atual[0]), dados.get('tipo_epi', epi_atual[1]), dados.get('validade_certificado_aprovacao', epi_atual[3]), ca_epi))

        conn.commit()
        return jsonify({'message': 'EPI atualizado com sucesso'}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@api_routes.route('/api/registro/<matricula>/<ca_epi>', methods=['PUT'])
def atualizar_registro(matricula, ca_epi):
    conn = None
    cursor = None
    try:
        dados = request.get_json()

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM registros WHERE matricula_funcionario = %s AND ca_EPI = %s", (matricula, ca_epi)
        )
        registro_atual = cursor.fetchone()

        sql = """UPDATE registros 
                 SET data_entrega = %s, data_devolucao = %s, data_troca = %s, motivo_devolucao = %s 
                 WHERE matricula_funcionario = %s AND ca_epi = %s"""
        cursor.execute(sql, (dados.get('data_entrega', registro_atual[2]), dados.get('data_devolucao', registro_atual[3]), dados.get('data_troca', registro_atual[4]), dados.get('motivo_devolucao', registro_atual[5]), matricula, ca_epi))

        conn.commit()
        return jsonify({'message': 'Registro atualizado com sucesso'}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# ============ DELETE ============
# Rotas para deletar funcionários, epi's e registros


@api_routes.route('/api/funcionario/<matricula>', methods=['DELETE'])
def deletar_funcionario(matricula):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        sql = "DELETE FROM funcionarios WHERE matricula_funcionario = %s"
        cursor.execute(sql, (matricula,))

        conn.commit()
        return jsonify({'message': 'Funcionário deletado com sucesso'}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@api_routes.route('/api/epi/<ca_epi>', methods=['DELETE'])
def deletar_epi(ca_epi):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        sql = "DELETE FROM epi WHERE certificado_aprovacao_epi = %s"
        cursor.execute(sql, (ca_epi,))

        conn.commit()
        return jsonify({'message': 'EPI deletado com sucesso'}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@api_routes.route('/api/registro/<matricula>/<ca_epi>', methods=['DELETE'])
def deletar_registro(matricula, ca_epi):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        sql = "DELETE FROM registros WHERE matricula_funcionario = %s AND ca_epi = %s"
        cursor.execute(sql, (matricula, ca_epi))

        conn.commit()
        return jsonify({'message': 'Registro deletado com sucesso'}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# ============ NOTIFICAÇÕES DE VENCIMENTO ============
# Rotas para gerenciar notificações de vencimento de CA

@api_routes.route('/api/notificacoes/verificar-vencimentos', methods=['POST'])
def verificar_vencimentos():
    """
    Verifica todos os EPIs e calcula quantos dias faltam para o vencimento.
    Cria notificações para aqueles que vencem em até 30 dias.
    Espera JSON com: {"dias_alerta": 30} (opcional, padrão 30)
    """
    conn = None
    cursor = None
    try:
        dados = request.get_json(silent=True) or {}
        dias_alerta = dados.get('dias_alerta', 30)
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Buscar todos os EPIs com registros de funcionários
        cursor.execute("""
            SELECT DISTINCT r.ca_EPI, r.matricula_funcionario, e.validade_certificado_aprovacao
            FROM registros r
            JOIN epi e ON r.ca_EPI = e.certificado_aprovacao_epi
            WHERE e.validade_certificado_aprovacao IS NOT NULL
        """)
        
        registros_epi = cursor.fetchall()
        notificacoes_criadas = 0
        data_hoje = datetime.now()
        
        for reg in registros_epi:
            ca_epi = reg['ca_EPI']
            matricula = reg['matricula_funcionario']
            data_vencimento = reg['validade_certificado_aprovacao']
            
            # Calcular dias para vencimento
            dias_para_vencimento = (data_vencimento - data_hoje).days
            
            # Se vence em até dias_alerta dias e ainda não foi notificado
            if 0 <= dias_para_vencimento <= dias_alerta:
                # Verificar se já existe notificação não enviada
                cursor.execute("""
                    SELECT id FROM notificacoes_vencimento
                    WHERE ca_epi = %s AND matricula_funcionario = %s AND enviado = FALSE
                """, (ca_epi, matricula))
                
                if not cursor.fetchone():
                    # Criar nova notificação
                    cursor.execute("""
                        INSERT INTO notificacoes_vencimento 
                        (ca_epi, matricula_funcionario, dias_para_vencimento, data_verificacao, enviado)
                        VALUES (%s, %s, %s, NOW(), FALSE)
                    """, (ca_epi, matricula, dias_para_vencimento))
                    notificacoes_criadas += 1
        
        conn.commit()
        return jsonify({
            'message': f'{notificacoes_criadas} notificação(ões) de vencimento criada(s)',
            'notificacoes_criadas': notificacoes_criadas,
            'dias_alerta': dias_alerta
        }), 200
        
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@api_routes.route('/api/notificacoes/pendentes', methods=['GET'])
def obter_notificacoes_pendentes():
    """
    Retorna todas as notificações de vencimento que ainda não foram enviadas.
    Opcional: passar matricula como query param para filtrar por funcionário
    """
    conn = None
    cursor = None
    try:
        matricula = request.args.get("matricula")
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        if matricula:
            cursor.execute("""
                SELECT n.*, e.nome_epi, e.tipo_epi, 
                       CONCAT(f.nome_funcionario, ' (', f.matricula_funcionario, ')') as funcionario_info,
                       e.validade_certificado_aprovacao
                FROM notificacoes_vencimento n
                JOIN epi e ON n.ca_epi = e.certificado_aprovacao_epi
                JOIN funcionarios f ON n.matricula_funcionario = f.matricula_funcionario
                WHERE n.enviado = FALSE AND n.matricula_funcionario = %s
                ORDER BY n.dias_para_vencimento ASC
            """, (matricula,))
        else:
            cursor.execute("""
                SELECT n.*, e.nome_epi, e.tipo_epi,
                       CONCAT(f.nome_funcionario, ' (', f.matricula_funcionario, ')') as funcionario_info,
                       e.validade_certificado_aprovacao
                FROM notificacoes_vencimento n
                JOIN epi e ON n.ca_epi = e.certificado_aprovacao_epi
                JOIN funcionarios f ON n.matricula_funcionario = f.matricula_funcionario
                WHERE n.enviado = FALSE
                ORDER BY n.dias_para_vencimento ASC, n.data_verificacao DESC
            """)
        
        notificacoes = cursor.fetchall()
        
        # Formatar datas
        for notif in notificacoes:
            notif['data_verificacao'] = notif['data_verificacao'].strftime('%Y-%m-%d %H:%M:%S') if notif['data_verificacao'] else None
            notif['data_envio'] = notif['data_envio'].strftime('%Y-%m-%d %H:%M:%S') if notif['data_envio'] else None
            notif['validade_certificado_aprovacao'] = notif['validade_certificado_aprovacao'].strftime('%Y-%m-%d') if notif['validade_certificado_aprovacao'] else None
        
        return jsonify({
            'total': len(notificacoes),
            'notificacoes': notificacoes
        }), 200
        
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@api_routes.route('/api/notificacoes/marcar-enviado/<int:notificacao_id>', methods=['PUT'])
def marcar_notificacao_enviada(notificacao_id):
    """
    Marca uma notificação como enviada (útil após disparar a notificação para o usuário)
    """
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE notificacoes_vencimento
            SET enviado = TRUE, data_envio = NOW()
            WHERE id = %s
        """, (notificacao_id,))
        
        conn.commit()
        
        if cursor.rowcount == 0:
            return jsonify({"erro": "Notificação não encontrada"}), 404
        
        return jsonify({'message': 'Notificação marcada como enviada'}), 200
        
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@api_routes.route('/api/notificacoes/status', methods=['GET'])
def status_notificacoes():
    """
    Retorna um resumo do status das notificações de vencimento
    """
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Total de notificações pendentes
        cursor.execute("SELECT COUNT(*) as pendentes FROM notificacoes_vencimento WHERE enviado = FALSE")
        pendentes = cursor.fetchone()['pendentes']
        
        # Total de notificações enviadas
        cursor.execute("SELECT COUNT(*) as enviadas FROM notificacoes_vencimento WHERE enviado = TRUE")
        enviadas = cursor.fetchone()['enviadas']
        
        # EPIs com vencimento em até 7 dias
        cursor.execute("""
            SELECT COUNT(*) as criticos FROM notificacoes_vencimento
            WHERE enviado = FALSE AND dias_para_vencimento <= 7
        """)
        criticos = cursor.fetchone()['criticos']
        
        return jsonify({
            'pendentes': pendentes,
            'enviadas': enviadas,
            'criticos': criticos
        }), 200
        
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


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