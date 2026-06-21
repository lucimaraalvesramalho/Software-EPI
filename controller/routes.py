# Importação das bibliotecas utilizadas no backend
from flask import Blueprint, render_template, request, jsonify, send_file
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
from models.tables import funcionario, epi, Registros
from database import get_db_connection
from datetime import datetime, timedelta
import json
import os
import re
from dotenv import load_dotenv
from twilio.rest import Client

# Carrega variáveis do ambiente
load_dotenv()

# Blueprint para agrupar rotas da API
api_routes = Blueprint('api_routes', __name__)

def formatar_para_twilio(telefone_raw):
    if not telefone_raw:
        return ""
    # Remove qualquer caractere que não seja número
    numeros = re.sub(r'\D', '', str(telefone_raw))

    # Formata número brasileiro
    if len(numeros) == 11:
        return f"+55{numeros}"
    # Formata número já com código do país
    elif len(numeros) == 13:
        return f"+{numeros}"

    # Retorna como está caso não tenha padrão
    return numeros

def buscarPanel():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
    SELECT COUNT(*) AS total
    FROM epi
    WHERE DATE(validade_certificado_aprovacao) = CURDATE()
""")
    vencendoHoje = cursor.fetchone()["total"]

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM registros
        WHERE data_entrega = CURDATE()
    """)
    entregasHoje = cursor.fetchone()["total"]

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM epi
        WHERE validade_certificado_aprovacao < CURDATE()
    """)

    vencidos = cursor.fetchone()["total"]

    cursor.close()
    conn.close()

    return {
        "vencimentos_hoje" : vencendoHoje,
        "entregas_hoje" : entregasHoje,
        "vencidos" : vencidos
    }

def buscarDashboard():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Total de EPIs
    cursor.execute("SELECT COUNT(*) AS total FROM epi")
    total_epi = cursor.fetchone()["total"]

    #registros criados hoje
    cursor.execute("SELECT COUNT(*) AS total FROM registros WHERE data_entrega = CURDATE()")
    registros_hoje = cursor.fetchone()['total']

    # Total de funcionários
    cursor.execute("SELECT COUNT(*) AS total FROM funcionarios")
    total_funcionarios = cursor.fetchone()["total"]

    # EPIs vencendo em 7 dias
    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM epi
        WHERE validade_certificado_aprovacao
        BETWEEN CURDATE()
        AND DATE_ADD(CURDATE(), INTERVAL 7 DAY)
    """)
    vencendo7 = cursor.fetchone()["total"]

    # EPIs vencendo em 7 dias
    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM epi
        WHERE validade_certificado_aprovacao
        BETWEEN CURDATE()
        AND DATE_ADD(CURDATE(), INTERVAL 30 DAY)
    """)
    vencendo30 = cursor.fetchone()["total"]

    # Últimos registros
    cursor.execute("""
        SELECT
            f.nome_funcionario,
            e.nome_epi,
            r.data_entrega,
            r.data_troca
        FROM registros r
        INNER JOIN funcionarios f
            ON r.matricula_funcionario = f.matricula_funcionario
        INNER JOIN epi e
            ON r.ca_EPI = e.certificado_aprovacao_epi
        ORDER BY r.data_entrega DESC,
         r.matricula_funcionario DESC,
         r.ca_EPI DESC
        LIMIT 10
    """)

    ultimos_registros = cursor.fetchall()

    cursor.close()
    conn.close()

    return {
        "total_epi": total_epi,
        "total_funcionarios": total_funcionarios,
        "vencendo_30_dias": vencendo30,
        "vencendo_7_dias": vencendo7,
        "ultimos_registros": ultimos_registros
    }

@api_routes.route('/teste-dashboard')
def teste_dashboard():
    return jsonify(buscarDashboard())


# ============ CREATE ============
# Definição das rotas para cadastro de funcionários, EPIs e registros

@api_routes.route('/api/funcionario', methods=['POST'])
def cadastrar_funcionario():
    # Cadastra um novo funcionário
    conn = None
    cursor = None
    try:
        # Pega os dados enviados
        dados = request.get_json(silent=True)
        if not dados:
            # Fallback para formulário
            dados = request.form.to_dict()

        # Cria objeto do funcionário
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

        # Conecta ao banco
        conn = get_db_connection()
        cursor = conn.cursor()

        # Insere os dados do funcionário
        sql = "INSERT INTO funcionarios (matricula_funcionario, nome_funcionario, cpf_funcionario, setor_funcionario, funcao_funcionario, data_admissao_funcionario, telefone, email, whatsapp) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (func.matricula_funcionario, func.nome_funcionario, func.cpf_funcionario, func.setor_funcionario, func.funcao_funcionario, func.data_admissao_funcionario, func.telefone, func.email, func.whatsapp))

        # Confirma a operação
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
    # Cadastra um novo EPI
    conn = None
    cursor = None
    try:
        # Pega os dados do EPI
        dados = request.get_json()

        # Cria objeto do EPI
        novo_epi = epi(
            dados['nome_epi'],
            dados['tipo_epi'], 
            dados['certificado_aprovacao_epi'], 
            dados['validade_certificado_aprovacao'])

        # Conecta ao banco
        conn = get_db_connection()
        cursor = conn.cursor()

        # Insere o EPI
        sql = "INSERT INTO epi (nome_epi, tipo_epi, certificado_aprovacao_epi, validade_certificado_aprovacao) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (novo_epi.nome_epi, novo_epi.tipo_epi, novo_epi.certificado_aprovacao_epi, novo_epi.validade_certificado_aprovacao))

        # Confirma a operação
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
    # Cadastra um novo registro
    conn = None
    cursor = None
    try:
        # Pega os dados do registro
        dados = request.get_json()

        # Cria objeto do registro
        registro = Registros(
            dados['matricula_funcionario'], 
            dados['ca_EPI'],
            None,   
            dados['data_devolucao']
        )

        # Conecta ao banco
        conn = get_db_connection()
        cursor = conn.cursor()

        # Insere o registro
        sql = "INSERT INTO registros (matricula_funcionario, ca_EPI, data_devolucao, data_troca, motivo_devolucao) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (registro.matricula_funcionario, registro.ca_EPI, registro.data_devolucao, registro.data_troca, registro.motivo_devolucao))

        # Confirma a operação
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
    # Busca funcionários
    matricula = request.args.get("matricula")
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Busca por matrícula ou lista tudo
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

        # Confirma a conexão
        conn.commit()

        # Formata datas para JSON
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
    # Busca EPIs
    ca = request.args.get("ca")
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Busca por CA ou lista tudo
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

        # Confirma a conexão
        conn.commit()

        # Formata datas para JSON
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
    # Busca registros
    matricula = request.args.get("matricula")
    ca = request.args.get("ca")
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Busca por matrícula, CA ou lista tudo
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

        # Confirma a conexão
        conn.commit()

        # Formata datas para JSON
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
    # Atualiza funcionário
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
                     funcao_funcionario = %s, data_admissao_funcionario = %s, telefone = %s, email = %s, whatsapp = %s 
                 WHERE matricula_funcionario = %s"""
        cursor.execute(sql, (dados.get('nome_funcionario', funcionario_atual[1]), dados.get('cpf_funcionario', funcionario_atual[2]), dados.get('setor_funcionario', funcionario_atual[3]), dados.get('funcao_funcionario', funcionario_atual[4]), dados.get('data_admissao_funcionario', funcionario_atual[5]), dados.get('telefone', funcionario_atual[6]),dados.get('email', funcionario_atual[7]),dados.get('whatsapp', funcionario_atual[8]), matricula))

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
    # Atualiza EPI
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
    # Atualiza registro
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
    # Remove funcionário
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
    # Remove EPI
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
    # Remove registro
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

@api_routes.route('/api/notificacoes/verificar', methods=['POST'])
def verificar_vencimentos():
    """
    Verifica os EPIs que vencem nos próximos dias e grava as notificações
    pendentes na tabela notificacoes_vencimento.
    Espera JSON com: {"dias_alerta": 30} (opcional, padrão 30)
    """
    conn = None
    cursor = None
    try:
        dados = request.get_json(silent=True) or {}
        dias_alerta = int(dados.get('dias_alerta', 30))

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                r.matricula_funcionario,
                r.ca_EPI,
                e.nome_epi,
                e.tipo_epi,
                e.validade_certificado_aprovacao
            FROM registros r
            JOIN epi e ON r.ca_EPI = e.certificado_aprovacao_epi
            WHERE e.validade_certificado_aprovacao IS NOT NULL
        """)

        registros_epi = cursor.fetchall()
        notificacoes_criadas = 0
        # Data atual para cálculo
        data_hoje = datetime.now().date()

        # Percorre os registros para montar alertas
        for reg in registros_epi:
            data_vencimento = reg['validade_certificado_aprovacao']
            if not data_vencimento:
                continue

            # Calcula quantos dias faltam
            dias_para_vencimento = (data_vencimento - data_hoje).days

            # Ignora vencidos ou fora do limite
            if dias_para_vencimento < 0 or dias_para_vencimento > dias_alerta:
                continue

            # Verifica se já existe alerta pendente
            cursor.execute(
                """
                SELECT id
                FROM notificacoes_vencimento
                WHERE ca_epi = %s
                  AND matricula_funcionario = %s
                  AND enviado = FALSE
                """,
                (reg['ca_EPI'], reg['matricula_funcionario'])
            )

            if cursor.fetchone():
                continue

            # Cria nova notificação pendente
            cursor.execute(
                """
                INSERT INTO notificacoes_vencimento
                (ca_epi, matricula_funcionario, dias_para_vencimento, data_verificacao, enviado)
                VALUES (%s, %s, %s, NOW(), FALSE)
                """,
                (reg['ca_EPI'], reg['matricula_funcionario'], dias_para_vencimento)
            )
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
    Opcional: passar matricula como query param para filtrar por funcionário.
    """
    conn = None
    cursor = None
    try:
        matricula = request.args.get('matricula')

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        if matricula:
            cursor.execute(
                """
                SELECT
                    n.id,
                    n.ca_epi,
                    n.matricula_funcionario,
                    n.dias_para_vencimento,
                    n.data_verificacao,
                    n.enviado,
                    n.data_envio,
                    e.nome_epi,
                    e.tipo_epi,
                    e.validade_certificado_aprovacao,
                    f.nome_funcionario,
                    f.telefone,
                    f.whatsapp
                FROM notificacoes_vencimento n
                JOIN epi e ON n.ca_epi = e.certificado_aprovacao_epi
                JOIN funcionarios f ON n.matricula_funcionario = f.matricula_funcionario
                WHERE n.enviado = FALSE
                  AND n.matricula_funcionario = %s
                ORDER BY n.dias_para_vencimento ASC, n.data_verificacao DESC
                """,
                (matricula,)
            )
        else:
            cursor.execute(
                """
                SELECT
                    n.id,
                    n.ca_epi,
                    n.matricula_funcionario,
                    n.dias_para_vencimento,
                    n.data_verificacao,
                    n.enviado,
                    n.data_envio,
                    e.nome_epi,
                    e.tipo_epi,
                    e.validade_certificado_aprovacao,
                    f.nome_funcionario,
                    f.telefone,
                    f.whatsapp
                FROM notificacoes_vencimento n
                JOIN epi e ON n.ca_epi = e.certificado_aprovacao_epi
                JOIN funcionarios f ON n.matricula_funcionario = f.matricula_funcionario
                WHERE n.enviado = FALSE
                ORDER BY n.dias_para_vencimento ASC, n.data_verificacao DESC
                """
            )

        # Pega as notificações pendentes
        notificacoes = cursor.fetchall()

        # Formata datas para resposta
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
    Marca uma notificação como enviada após o disparo.
    """
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE notificacoes_vencimento
            SET enviado = TRUE, data_envio = NOW()
            WHERE id = %s
            """,
            (notificacao_id,)
        )

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
    Retorna um resumo do status das notificações de vencimento.
    """
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT COUNT(*) as pendentes FROM notificacoes_vencimento WHERE enviado = FALSE")
        pendentes = cursor.fetchone()['pendentes']

        cursor.execute("SELECT COUNT(*) as enviadas FROM notificacoes_vencimento WHERE enviado = TRUE")
        enviadas = cursor.fetchone()['enviadas']

        cursor.execute(
            """
            SELECT COUNT(*) as criticos FROM notificacoes_vencimento
            WHERE enviado = FALSE AND dias_para_vencimento <= 7
            """
        )
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


@api_routes.route('/api/notificacoes/enviar', methods=['POST'])
def enviar_notificacoes():
    """
    Envia as notificações pendentes.
    Body opcional:
      - tipo: 'sms' ou 'whatsapp'
      - destinatario: número específico para sobrescrever o destino
      - matricula: filtra uma matrícula específica
      - content_sid: SID do template do WhatsApp (se existir)
    """
    dados = request.get_json(silent=True) or {}
    tipo_envio = dados.get('tipo', 'sms').lower()

    if tipo_envio not in ('sms', 'whatsapp'):
        return jsonify({"erro": "tipo deve ser 'sms' ou 'whatsapp'"}), 400

    return _enviar_notificacoes_por_tipo(tipo_envio, dados)


def _enviar_notificacoes_por_tipo(tipo_envio, dados=None):
    conn = None
    cursor = None
    try:
        if dados is None:
            dados = request.get_json(silent=True) or {}

        matricula = dados.get('matricula')
        destinatario = dados.get('destinatario')
        content_sid = dados.get('content_sid') or os.getenv('TWILIO_CONTENT_SID')

        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        sms_from = os.getenv('TWILIO_PHONE_NUMBER')
        whatsapp_from = os.getenv('TWILIO_WHATSAPP_NUMBER')

        if not account_sid or not auth_token:
            return jsonify({"erro": "Credenciais do Twilio não configuradas"}), 500

        if tipo_envio == 'whatsapp' and not whatsapp_from:
            return jsonify({"erro": "Número do WhatsApp não configurado"}), 500

        if tipo_envio == 'sms' and not sms_from:
            return jsonify({"erro": "Número do SMS não configurado"}), 500

        client = Client(account_sid, auth_token)

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        if matricula:
            cursor.execute(
                """
                SELECT
                    n.id,
                    n.ca_epi,
                    n.matricula_funcionario,
                    n.dias_para_vencimento,
                    e.nome_epi,
                    e.validade_certificado_aprovacao,
                    f.nome_funcionario,
                    f.telefone,
                    f.whatsapp
                FROM notificacoes_vencimento n
                JOIN epi e ON n.ca_epi = e.certificado_aprovacao_epi
                JOIN funcionarios f ON n.matricula_funcionario = f.matricula_funcionario
                WHERE n.enviado = FALSE
                  AND n.matricula_funcionario = %s
                ORDER BY n.dias_para_vencimento ASC
                """,
                (matricula,)
            )
        else:
            cursor.execute(
                """
                SELECT
                    n.id,
                    n.ca_epi,
                    n.matricula_funcionario,
                    n.dias_para_vencimento,
                    e.nome_epi,
                    e.validade_certificado_aprovacao,
                    f.nome_funcionario,
                    f.telefone,
                    f.whatsapp
                FROM notificacoes_vencimento n
                JOIN epi e ON n.ca_epi = e.certificado_aprovacao_epi
                JOIN funcionarios f ON n.matricula_funcionario = f.matricula_funcionario
                WHERE n.enviado = FALSE
                ORDER BY n.dias_para_vencimento ASC
                """
            )

        # Busca notificações pendentes
        notificacoes = cursor.fetchall()
        contador_sucesso = 0

        # Envia cada notificação
        for notif in notificacoes:
            # Define para onde mandar
            telefone_destino = formatar_para_twilio(
                destinatario or notif.get('whatsapp') or notif.get('telefone')
            )

            if not telefone_destino:
                continue

            # Monta a mensagem
            mensagem = (
                f"Olá {notif['nome_funcionario']}, o EPI {notif['nome_epi']} "
                f"({notif['ca_epi']}) vence em {notif['dias_para_vencimento']} dias. "
                f"Validade: {notif['validade_certificado_aprovacao']}"
            )

            # Envia por SMS ou WhatsApp
            if tipo_envio == 'whatsapp':
                payload = {
                    'from_': f"whatsapp:{whatsapp_from}",
                    'to': f"whatsapp:{telefone_destino}"
                }

                # Se houver template do Twilio, usa o formato recomendado
                if content_sid:
                    payload['content_sid'] = content_sid
                    payload['content_variables'] = json.dumps({
                        '1': notif['validade_certificado_aprovacao'],
                        '2': str(notif['dias_para_vencimento'])
                    })
                else:
                    payload['body'] = mensagem

                client.messages.create(**payload)
            else:
                client.messages.create(
                    body=mensagem,
                    from_=sms_from,
                    to=telefone_destino
                )

            # Marca como enviada
            cursor.execute(
                """
                UPDATE notificacoes_vencimento
                SET enviado = TRUE, data_envio = NOW()
                WHERE id = %s
                """,
                (notif['id'],)
            )
            contador_sucesso += 1

        # Confirma as mudanças
        conn.commit()
        return jsonify({
            'message': f'Processamento concluído. {contador_sucesso} notificação(ões) enviada(s) por {tipo_envio}',
            'enviadas': contador_sucesso,
            'tipo': tipo_envio,
            'destinatario': destinatario
        }), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# ============ ROTAS DE HTML ============

# HTML ROUTES - Rotas para renderizar as páginas HTML
@api_routes.route('/')
def index():
    dashboard = buscarDashboard()
    panel = buscarPanel()
    return render_template('index.html', dashboard=dashboard, panel=panel)

@api_routes.route('/cadastro-funcionario')
def cadastro_funcionario():
    return render_template('cadastrar-funcionario.html')

@api_routes.route('/funcionarios')
def funcionarios():
    return render_template('funcionarios.html')

@api_routes.route('/epis')
def epis():
    return render_template('epis.html')

@api_routes.route('/cadastro-epi')
def cadastro_epi():
    return render_template('cadastrar-epi.html')

@api_routes.route('/criar-registro')
def criar_registro():
    return render_template('criar-registro.html')   

@api_routes.route('/registros')
def registros():
    return render_template('registros.html')

@api_routes.route('/atualizar-cadastros')
def atualizar_cadastros():
    return render_template('atualizar-cadastros.html')

# ============ GERAÇÃO DE GRÁFICOS ============
# Gera gráficos para serem usados nno frontend

@api_routes.route('/api/graficos/light')
def gerarGrafico():
    conn = None
    cursor = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM registros WHERE data_troca IS NOT NULL")
        devolvidos = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM registros WHERE data_troca IS NULL")
        nao_devolvidos = cursor.fetchone()[0]

        fig, ax = plt.subplots(figsize=(6, 4), facecolor='#f8f7ff')
        ax.set_facecolor('#f8f7ff')

        ax.pie(
            [devolvidos, nao_devolvidos],
            labels=['Devolvidos', 'Não devolvidos'],
            autopct='%1.1f%%',
            startangle=90,
            colors=['#7d6cfd', '#f59e0b'],
            wedgeprops={'edgecolor': '#f8f7ff', 'linewidth': 1.5},
            textprops={'color': '#042016', 'fontsize': 10}
        )

        ax.set_title('Situação dos EPIs', color='#042016', fontsize=12, pad=12)
        ax.axis('equal')

        buffer = BytesIO()
        fig.savefig(buffer, format='png', bbox_inches='tight', dpi=150)
        buffer.seek(0)
        plt.close(fig)

        return send_file(
            buffer,
            mimetype='image/png'
        )
    except Exception as e:
        return jsonify({'erro': str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



# @api_routes.route('/api/graficos/')