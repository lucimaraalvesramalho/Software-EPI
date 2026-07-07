"""
Modelos de dados usados pela aplicação Software-EPI.

Cada classe representa uma entidade principal do sistema:
- epi: informações sobre Equipamentos de Proteção Individual
- funcionario: dados dos funcionários cadastrados
- Registros: movimentações de entrega/retorno/troca de EPIs
- notificacao: avisos de validade de certificado de aprovação
- usuarios: credenciais de acesso ao sistema
"""

class epi:
    """Representa um Equipamento de Proteção Individual (EPI)."""

    def __init__(self, nome_epi, tipo_epi, certificado_aprovacao_epi, validade_certificado_aprovacao):
        # Nome do EPI, por exemplo "Capacete" ou "Luva".
        self.nome_epi = nome_epi
        # Tipo ou categoria do EPI, como "Cabeça", "Mãos", "Respiração".
        self.tipo_epi = tipo_epi
        # Número do Certificado de Aprovação (CA) do EPI.
        self.certificado_aprovacao_epi = certificado_aprovacao_epi
        # Data de validade do certificado de aprovação do EPI.
        self.validade_certificado_aprovacao = validade_certificado_aprovacao


class funcionario:
    """Representa um funcionário cadastrado no sistema."""

    def __init__(self, matricula_funcionario, nome_funcionario, cpf_funcionario, setor_funcionario, funcao_funcionario, data_admissao_funcionario, telefone, email, whatsapp):
        # Matrícula ou identificador do funcionário.
        self.matricula_funcionario = matricula_funcionario
        # Nome completo do funcionário.
        self.nome_funcionario = nome_funcionario
        # CPF do funcionário, usado para identificação legal.
        self.cpf_funcionario = cpf_funcionario
        # Setor onde o funcionário trabalha.
        self.setor_funcionario = setor_funcionario
        # Função ou cargo do funcionário.
        self.funcao_funcionario = funcao_funcionario
        # Data de admissão do funcionário na empresa.
        self.data_admissao_funcionario = data_admissao_funcionario
        # Número de telefone do funcionário.
        self.telefone = telefone
        # Endereço de e-mail do funcionário.
        self.email = email
        # Número de WhatsApp do funcionário, se houver.
        self.whatsapp = whatsapp


class Registros:
    """Registra a entrega e devolução de um EPI a um funcionário."""

    def __init__(self, matricula_funcionario, ca_EPI, data_entrega=None, data_devolucao=None, data_troca=None, motivo_devolucao=None):
        # Matrícula do funcionário que recebeu o EPI.
        self.matricula_funcionario = matricula_funcionario
        # Código do certificado de aprovação do EPI entregue.
        self.ca_EPI = ca_EPI
        # Data em que o EPI foi entregue ao funcionário.
        self.data_entrega = data_entrega
        # Data em que o EPI foi devolvido, se aplicável.
        self.data_devolucao = data_devolucao
        # Data de troca do EPI, quando houver substituição.
        self.data_troca = data_troca
        # Motivo da devolução ou troca, como desgaste ou fim de uso.
        self.motivo_devolucao = motivo_devolucao


class notificacao:
    """Representa um aviso sobre a validade do CA de um EPI para um funcionário."""

    def __init__(self, ca_epi, matricula_funcionario, dias_para_vencimento, data_verificacao=None, enviado=False, data_envio=None):
        # Certificado de aprovação do EPI que está próximo do vencimento.
        self.ca_epi = ca_epi
        # Matrícula do funcionário associado à notificação.
        self.matricula_funcionario = matricula_funcionario
        # Quantos dias faltam para o vencimento do certificado.
        self.dias_para_vencimento = dias_para_vencimento
        # Data em que a validade foi verificada.
        self.data_verificacao = data_verificacao
        # Se a notificação já foi enviada ao usuário.
        self.enviado = enviado
        # Data em que a notificação foi enviada.
        self.data_envio = data_envio


class usuarios:
    """Representa um usuário que pode acessar o sistema."""

    def __init__(self, nome, usuario, senha):
        # Nome completo do usuário do sistema.
        self.nome = nome
        # Nome de login utilizado para autenticação.
        self.usuario = usuario
        # Senha criptografada ou em texto do usuário.
        self.senha = senha
  